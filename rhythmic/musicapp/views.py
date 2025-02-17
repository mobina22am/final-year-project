from django.http import HttpResponse
# *************
from django.contrib.auth import login, logout, authenticate
from django.http import JsonResponse
from django.contrib.auth import get_user_model
from django.views.decorators.csrf import csrf_exempt
from .models import User
import json
import librosa
import pretty_midi
import numpy as np
import requests
from io import BytesIO
import yt_dlp
import subprocess
import os
from spleeter.separator import Separator
import soundfile as sf
import tempfile
from pydub import AudioSegment



ytUrl = "https://www.youtube.com/results?search_query="
User = get_user_model()
songData = {}

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


def searchSongLink(songName, artistName):

    query = f"{songName} {artistName} official audio"
    songUrl = ytUrl + "+".join(query.split())

    response = requests.get(songUrl)

    if "watch?v=" in response.text:
        video_id = response.text.split("watch?v=")[1].split('"')[0]
        return f"https://www.youtube.com/watch?v={video_id}"
    return None


def downloadSongAudio(youtubeLink):
    """Downloads the YouTube audio and saves it as an MP3."""
    outputPath = "songs/%(title)s.%(ext)s"

    ydlOpts = {
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
        'outtmpl': outputPath,
    }

    with yt_dlp.YoutubeDL(ydlOpts) as ydl:
        info = ydl.extract_info(youtubeLink, download=True)

    return ydl.prepare_filename(info)



@csrf_exempt
def getSongAudio(request, songName, artistName):
    """API endpoint to find and download a song based on name and artist."""

    if request.method == "POST":
        if not songName or not artistName:
            return JsonResponse({"error": "Missing song name or artist name"}, status=400)

        youtubeLink = searchSongLink(songName, artistName)

        if not youtubeLink:
            return JsonResponse({"error": "Song not found on YouTube"}, status=404)

        audioPath = downloadSongAudio(youtubeLink)

        return JsonResponse({"audio_path": audioPath})

    return JsonResponse({"error": "Invalid request"}, status=400)



@csrf_exempt
def findInstruments(request):

    import glob
    separator = Separator('spleeter:5stems')
    global foundInstruments
    global songData

    if request.method == "POST":
        foundInstruments = []
        
        try:
            data = json.loads(request.body.decode("utf-8"))
            songName = data.get("name")
            artistName = data.get("artist")

            
            response = getSongAudio(request, songName, artistName)
            songData = json.loads(response.content) 


            if "audio_path" not in songData:
                return JsonResponse({"error": "Failed to download song audio"}, status=500)
            
            songPathString = songData["audio_path"]
            songPathString = songPathString.replace(".webm", ".mp3")
            

            try:
                separator.separate_to_file(songPathString, "separatedAudio")

            except subprocess.CalledProcessError:
                return JsonResponse({"error": "Failed to separate instruments"}, status=500)
            

            separatedDirection = f"separatedAudio/{os.path.basename(songPathString).split('.')[0]}/*"

            for file in glob.glob(separatedDirection):

                y, sr = librosa.load(file, sr=None)

                spectralCentroids = librosa.feature.spectral_centroid(y=y, sr=sr).mean()
                zeroCrossingRate = librosa.feature.zero_crossing_rate(y).mean()
                spectralBandwidth = librosa.feature.spectral_bandwidth(y=y, sr=sr).mean()


                if "bass.wav" in file and spectralCentroids < 900 and zeroCrossingRate < 0.05:
                    foundInstruments.append("Bass")

                if "drums.wav" in file and spectralBandwidth > 2000 and zeroCrossingRate > 0.1:
                    foundInstruments.append("Drums")

                if "other.wav" in file and 900 < spectralCentroids < 3500 and 1000 < spectralBandwidth < 4500:
                    foundInstruments.append("Guitar")


                if "other.wav" in file or "other.wav" in file and 1500 < spectralCentroids < 4000 and 2000 < spectralBandwidth < 5000:
                        foundInstruments.append("Violin")

                if "piano.wav" in file and spectralCentroids > 3000 and spectralBandwidth > 4000:
                    foundInstruments.append("Piano")


            foundInstruments = list(set(foundInstruments))


            songData = { "name": songName, "artist": artistName, "audio_path": songPathString, "instruments": foundInstruments }

            return JsonResponse({"message": "instruments detected", "instruments": foundInstruments, "song": songData}, status=200)
        
        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON"}, status=400)


    if request.method == "GET":
        if songData:
            return JsonResponse({"instruments": foundInstruments, "song": songData}, status=200)
        
        return JsonResponse({"error": "No song data detected"}, status=404)

    return JsonResponse({"error": "Invalid request"}, status=405)



@csrf_exempt
def getNotes(instrumentAudio):

    if not os.path.exists(instrumentAudio):
        return JsonResponse({"error": "File not found"}, status=404)

    y,s = librosa.load(instrumentAudio, sr=None)
    pitches, magnitudes = librosa.piptrack(y=y, sr=s)


    pitchesValues = []

    for t in range(pitches.shape[1]):
        index = magnitudes[:, t].argmax()
        pitch = pitches[index, t]
        if pitch > 0:
            pitchesValues.append(pitch)


    midi = pretty_midi.PrettyMIDI()
    instrument = pretty_midi.Instrument(program=0)

    for pitch in pitchesValues:

        note = pretty_midi.Note(velocity=100, pitch=int(librosa.hz_to_midi(pitch)), start=0, end=1)

        # print("")
        # print("")
        # print("")
        # print(note)
        # print("")
        # print("")   
        # print("")

        instrument.notes.append(note)


    midi.instruments.append(instrument)
    midiPath = "generated_notes/midi_output.mid"
    midi.write(midiPath)

    return midiPath


@csrf_exempt
def logoutView(request):
    response = JsonResponse({"message": "Logged out successfully!"})
    response.delete_cookie('token')
    logout(request)
    return response


def home(request):
    return HttpResponse("Hello, this is the music app home page.")