from django.conf.urls import url
from . import views
urlpatterns = [
    url(r'^$', views.index),
    url(r'^signinPage$', views.signinPage),
    url(r'^signin$', views.signin),
    url(r'^registerPage$', views.registerPage),
    url(r'^register$', views.register),

]
