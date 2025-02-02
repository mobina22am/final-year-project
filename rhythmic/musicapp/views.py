from django.shortcuts import render

from django.http import HttpResponse

# *************
from django.contrib.auth.hashers import make_password
from django.http import JsonResponse
from django.contrib.auth import get_user_model
from django.views.decorators.csrf import csrf_exempt
import json
from .models import User


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
            return JsonResponse({"error": "Email already exists"})

        if User.objects.filter(username=username).exists():
            return JsonResponse({"error": "Username already exists"})


        user = User.objects.create(
            name=name,
            email=email,
            birthday=birthday,
            password=make_password(password),
            username=username
        )

        user.save()

        return JsonResponse({"message": "User created successfully!"})
    
    return JsonResponse({"message": "User not created!"})


def home(request):
    return HttpResponse("Hello, this is the music app home page.")