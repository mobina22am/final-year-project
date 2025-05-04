from django.urls import path
from django.contrib import admin
from . import views
from django.conf import settings
from django.conf.urls.static import static

# All the possible paths in the application and their related views.py function to handle the request
urlpatterns = [
    path('', views.home, name='home'),
    path('signup/', views.UserSignUp, name='signUp'),
    path('login/', views.userLogin, name='logIn'),
    path('logout/', views.logout, name='logOut'),
    path('profile/', views.updateProfile, name='profile'),
    path('findinstruments', views.findInstruments, name='findInstruments'),
    path('generatednotes', views.generatedNotes, name='generatedNotes'),
    path("savemusicsheet", views.saveMusicSheet, name="saveMusicSheet"),
    path('getsavedsongs/', views.getSavedSongs, name='get-saved-songs'),
    path('getmusicsheet/<int:songId>/', views.getMusicSheet, name='getMusicSheet'),
    path('forgotcredentials/', views.forgotCredentials, name='forgotCredentials'),
    path('resetpassword/', views.resetPassword, name='ResetPassword'),
    path('deletesong/<int:songId>/', views.deleteSong, name='deleteSong'),
]

if settings.DEBUG:
    # Handles the files that has been uploaded by the user
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    
    # Handles generated music sheets separately and independently
    urlpatterns += static("generatedMusicSheets/", document_root=settings.GENERATED_SHEETS_DIR)