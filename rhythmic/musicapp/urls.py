from django.urls import path
from django.contrib import admin
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('signup/', views.UserSignUp, name='signUp'),
    path('login/', views.userLogin, name='logIn'),
    path('logout/', views.logout, name='logOut'),
    path('profile/', views.updateProfile, name='profile'),
    path('findinstruments', views.findInstruments, name='findInstruments'),
    path('generatednotes', views.generatedNotes, name='generatedNotes'),
]