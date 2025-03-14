from django.urls import path
from django.contrib import admin
from . import views
from django.conf import settings
from django.conf.urls.static import static
from .views import generatedNotes

urlpatterns = [
    path('', views.home, name='home'),
    path('signup/', views.UserSignUp, name='signUp'),
    path('login/', views.userLogin, name='logIn'),
    path('logout/', views.logout, name='logOut'),
    path('profile/', views.updateProfile, name='profile'),
    path('findinstruments', views.findInstruments, name='findInstruments'),
    path('generatednotes', views.generatedNotes, name='generatedNotes'),
    path("generatednotes", generatedNotes, name="generated_notes"),
    path("savemusicsheet", views.saveMusicSheet, name="saveMusicSheet"),
]


if settings.DEBUG:
    urlpatterns += static("/generatedMusicSheets/", document_root=settings.GENERATED_SHEETS_DIR)