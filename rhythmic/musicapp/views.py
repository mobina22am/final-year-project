from django.http import HttpResponse
# *************
from django.contrib.auth import login, authenticate
from django.http import JsonResponse
from django.contrib.auth import get_user_model
from django.views.decorators.csrf import csrf_exempt
from .models import User
import json


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

        user = authenticate(username=username, password=password)

        if user:
            login(request, user)
            response = JsonResponse({"message": "User created successfully!"}, status=201)
            response.set_cookie('token', username, httponly=True)
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
            response = JsonResponse({"message": "Logged in successfully!"}, status=200)
            response.set_cookie('token', username, httponly=True)
            return response
        
        else:
            return JsonResponse({"error": "Invalid credentials"}, status=400)

    return JsonResponse({"error": "Invalid method"}, status=405)




@csrf_exempt
def logout_view(request):
    response = JsonResponse({"message": "Logged out successfully!"})
    response.delete_cookie('token')
    return response


def home(request):
    return HttpResponse("Hello, this is the music app home page.")