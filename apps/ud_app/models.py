from __future__ import unicode_literals
import re
from django.db import models
import bcrypt

# Create your models here.
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9\.\+_-]+@[a-zA-Z0-9\._-]+\.[a-zA-Z]*$')

class userManager(models.Manager):

    def validate_signin(self, post_data):
        errors = []
        if len(self.filter(email=post_data['email'])) > 0:
            user = self.filter(email=post_data['email'])[0]
            print "got the user", user
            if not bcrypt.checkpw(post_data['password'].encode(), user.password.encode()):
                errors.append("Incorrect password")
        else:
            errors.append("Could not find User")
        if errors:
            return errors
        else:
            return user

    def validate_registration(self, post_data):
        errors = []
        # Empty fields
        for field, value in post_data.iteritems():
            if len(value) < 1:
                errors.append("{} field is required".format(
                    field.replace('_', ' ')))

        # Name length and alpha
        if len(post_data['fname']) < 2:
            errors.append("First name must be at least 2 characters long")
        elif not post_data['fname'].isalpha():
            errors.append("Name can only contain characters")
        if len(post_data['lname']) < 2:
            errors.append("Last name must be at least 2 characters long")
        elif not post_data['lname'].isalpha():
            errors.append("Name can only contain characters")

        # Email format and exist
        if not re.match(EMAIL_REGEX, post_data['email']):
            errors.append("Invalid email")
        if len(self.filter(email=post_data['email'])) > 1:
            errors.append("Email already registered")

        # Password length and match
        if len(post_data['password']) < 8:
            errors.append("Password must be at least 8 characters long")
        if post_data['password'] != post_data['pw_confirm']:
            errors.append("Passwords do not match")

        if not errors:
            pw_hash = bcrypt.hashpw(
                (post_data['password'].encode()), bcrypt.gensalt(5))
            new_user = User.objects.create(
                first_name=post_data['fname'],
                last_name=post_data['lname'],
                email=post_data['email'],
                password=pw_hash,
                user_level = False,
            )
            return new_user

        return errors


class User(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    user_level = models.BooleanField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = userManager()

    def __repr__(self):
        return "<User: {} {} {}>".format(self.email, self.first_name, self.password)
