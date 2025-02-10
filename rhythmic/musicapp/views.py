from urllib import request
from django.http import HttpResponse
# *************
from django.contrib.auth import login, logout, authenticate
from django.http import JsonResponse
from django.contrib.auth import get_user_model
from django.views.decorators.csrf import csrf_exempt
from .models import User
import json
import librosa
import numpy as np
import requests
from io import BytesIO
import soundfile as sf



User = get_user_model()

@csrf_exempt
def UserSignUp(request):

    if request.method == "POST":

        data = json.loads(request.body)
        name = data["name"]
        email = data["email"]
        birthday = data["birthday"]
        password = data["password"]
        username = data["username"]


        if User.objects.filter(email=email).exists():
            return JsonResponse({"error": "Email already exists"}, status=400)

        if User.objects.filter(username=username).exists():
            return JsonResponse({"error": "Username already exists"}, status=400)


        user = User.objects.create(
            first_name=name,
            email=email,
            birthday=birthday,
            username=username,
        )

        user.set_password(password)
        user.save()

        user = authenticate(username=username, password=password)

        if user:
            login(request, user)

            request.session.create()

            response = JsonResponse({"message": "User created successfully!", "token": request.session.session_key, "name": user.first_name}, status=201)
            response.set_cookie(key="token", value=request.session.session_key, httponly=True, secure=True, samesite='None') 


            return response
    
    return JsonResponse({"message": "User not created!"}, status=400)


@csrf_exempt
def userLogin(request):

    if request.method == "POST":

        data = json.loads(request.body)
        username = data["username"]
        password = data["password"]

        user = authenticate(username=username, password=password)

        if user:
            login(request, user)

            request.session.create()


            response = JsonResponse({"message": "Logged in successfully!", "token": request.session.session_key, "name": user.first_name}, status=200)
            response.set_cookie(key="token", value=request.session.session_key, httponly=True, secure=True, samesite='None')


            return response
        
        else:
            return JsonResponse({"error": "Invalid credentials"}, status=400)

    return JsonResponse({"error": "Invalid method"}, status=405)



@csrf_exempt
def updateProfile(request):

    if request.method == "PUT":

        if not request.user.is_authenticated:
            return JsonResponse({"error": "You are not logged in"}, status=401)

        data = json.loads(request.body)
        user = request.user

        user.first_name = data["name"]
        user.email = data["email"]  
        user.birthday = data["birthday"]
        user.username = data["username"]


        if user.check_password(data["oldPassword"]):
            pass

        else:
            return JsonResponse({"error": "Invalid password"}, status=400)

        if "password" in data:
            user.set_password(data["password"])

        user.save()

        request.session.create()

        response = JsonResponse({"message": "Profile updated successfully!", "token": request.session.session_key, "name":user.first_name}, status=200)
        response.set_cookie(key="token", value=request.session.session_key , httponly=True, secure=True, samesite='None')

        return response
    

    if request.method == "GET":
        if not request.user.is_authenticated:
            return JsonResponse({"error": "You are not logged in"}, status=401)
        
        user = request.user
        return JsonResponse({"name": user.first_name, "email": user.email, "birthday": user.birthday, "username": user.username}, status=200)


    return JsonResponse({"error": "Invalid method"}, status=405)


@csrf_exempt
def findInstruments(request):

    if request.method == "POST":

        try:
            data = json.loads(request.body)
            audioUrl = data.get("audio_url")

            if not audioUrl:
                return JsonResponse({"error": "No audio file found"}, status=400)
            
            response = requests.get(audioUrl)

            if response.status_code != 200:
                return JsonResponse({"error": "Failed to download audio"}, status=400)
            
            audioFile = BytesIO(response.content)

            y, sr = librosa.load(audioFile, sr=None)

            spectral = librosa.feature.spectral_centroid(y=y, sr=sr)[0]
            rolloff = librosa.feature.spectral_rolloff(y=y, sr=sr)[0]
            
            foundInstruments = []
            if np.mean(spectral) > 5000:
                foundInstruments.append("Electric Guitar")
            if np.mean(rolloff) < 3000:
                foundInstruments.append("Acoustic Guitar")
            if np.mean(spectral) < 2000:
                foundInstruments.append("Piano")

            return JsonResponse({"instruments": foundInstruments})
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)



@csrf_exempt
def logoutView(request):
    response = JsonResponse({"message": "Logged out successfully!"})
    response.delete_cookie('token')
    logout(request)
    return response


def home(request):
    return HttpResponse("Hello, this is the music app home page.")