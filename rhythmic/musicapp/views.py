from django.shortcuts import render

from django.http import HttpResponse

# *************
from django.contrib.auth.hashers import make_password
from django.http import JsonResponse
from django.contrib.auth import get_user_model
import json


User = get_user_model()

def UserSignUp(request):

    if request.method == "POST":

        data = json.loads(request.body)
        name = data["name"]
        email = data["email"]
        birthday = data["birthday"]
        password = data["password"]
        username = data["username"]

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