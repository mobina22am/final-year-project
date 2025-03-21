from django.urls import path
from django.contrib import admin
from . import views
from django.conf import settings
from django.conf.urls.static import static

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
]


if settings.DEBUG:
    # Serve user-uploaded files
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    
    # Serve generated music sheets separately
    urlpatterns += static("generatedMusicSheets/", document_root=settings.GENERATED_SHEETS_DIR)