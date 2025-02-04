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
            return JsonResponse({"error": "Email already exists"}, status=400)

        if User.objects.filter(username=username).exists():
            return JsonResponse({"error": "Username already exists"}, status=400)


        user = User.objects.create(
            first_name=name,
            email=email,
            birthday=birthday,
            username=username
        )

        user.set_password(password)

        user.save()

        return JsonResponse({"message": "User created successfully!"}, status=201)
    
    return JsonResponse({"message": "User not created!"}, status=400)


def home(request):
    return HttpResponse("Hello, this is the music app home page.")