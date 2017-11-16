from django.shortcuts import render, redirect
from .models import User
import bcrypt
from django.contrib.messages import error

# Create your views here.
def index(request):
    return render(request, 'ud_app/index.html')

def signinPage(request):
    return render(request, 'ud_app/signin.html')

def signin(request):
    errors = User.objects.validate_signin(request.POST)
    if type(errors) == list:
        for err in errors:
            error(request, err)
        return redirect('/signin')
    context = {
        'user': User.objects.get(email=request.POST['email'])
    }
    try: 
        request.session['user']
    except KeyError:
        request.session['words'] = ['']
    request.session['user'] = User.objects.get(email=request.POST['email'])
    return redirect('/')