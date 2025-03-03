# *************
from django.contrib.auth import login, logout, authenticate
from django.http import JsonResponse, HttpResponse
from django.contrib.auth import get_user_model
from django.views.decorators.csrf import csrf_exempt
from .models import User
import matplotlib.pyplot as plt
from music21 import stream, note, meter
from music21 import environment
import json
import librosa
import pretty_midi
import requests
import yt_dlp
import subprocess
import os
import glob
import shutil
import matplotlib
matplotlib.use('Agg')
import re
import base64
# from spleeter.separator import Separator
# import soundfile as sf
# import tempfile
# from pydub import AudioSegment
# from io import BytesIO
# import numpy as np



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
            
            # 6-stem demucs model
            try:
                subprocess.run(["demucs", "-n", "htdemucs_ft", songPathString], check=True)

            except subprocess.CalledProcessError:
                return JsonResponse({"error": "Failed to separate instruments"}, status=500)
            

            separatedInstrumentFolder = f"separatedInstruments/{artistName} - {songName}"
            
            os.makedirs(separatedInstrumentFolder, exist_ok=True)

            separatedDirection = f"separated/htdemucs_ft/{os.path.basename(songPathString).split('.')[0]}/*"

            for file in glob.glob(separatedDirection):

                if "vocals.wav" in file:
                    continue

                if "bass.wav" in file:
                    foundInstruments.append("Bass")
                    targetPath = os.path.join(separatedInstrumentFolder, "bass.wav")
                    shutil.move(file, targetPath)
                    continue

                if "drums.wav" in file:
                    foundInstruments.append("Drums")
                    targetPath = os.path.join(separatedInstrumentFolder, "drums.wav")
                    shutil.move(file, targetPath)
                    continue

                if "piano.wav" in file:
                    foundInstruments.append("Piano")
                    targetPath = os.path.join(separatedInstrumentFolder, "piano.wav")
                    shutil.move(file, targetPath)
                    continue

                if "guitar.wav" in file:
                    foundInstruments.append("Guitar")
                    targetPath = os.path.join(separatedInstrumentFolder, "guitar.wav")
                    shutil.move(file, targetPath)
                    continue


                if "other.wav" in file:

                    y, sr = librosa.load(file, sr=None)

                    spectralCentroids = librosa.feature.spectral_centroid(y=y, sr=sr).mean()
                    # zeroCrossingRate = librosa.feature.zero_crossing_rate(y).mean()
                    spectralBandwidth = librosa.feature.spectral_bandwidth(y=y, sr=sr).mean()
                    spectralRolloff = librosa.feature.spectral_rolloff(y=y, sr=sr, roll_percent=0.85).mean()

                    if 900 < spectralCentroids < 2500 and 1000 < spectralBandwidth < 4500:
                        foundInstruments.append("Guitar")
                        targetPath = os.path.join(separatedInstrumentFolder, "guitar.wav")
                        shutil.move(file, targetPath)
                        continue

                    if 3000 < spectralCentroids < 6000 and 4000 < spectralBandwidth < 7000 and spectralRolloff > 6000:
                        foundInstruments.append("Violin")
                        targetPath = os.path.join(separatedInstrumentFolder, "violin.wav")
                        shutil.move(file, targetPath)
                        
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



def generateMusicSheet(notesData,artistName, songName, instrumentName):
    # Create a music21 stream for visualization
    score = stream.Score()
    part = stream.Part()
    
    # Add time signature (4/4 time)
    part.append(meter.TimeSignature('4/4'))
    
    
    for noteData in notesData:
        midiNote = noteData['pitch']
        m21Note = note.Note(midiNote, quarterLength=1.0)  # Set the quarter length to 1 (can be adjusted)
        part.append(m21Note)

    score.append(part)

    musicSheetPath = f"generatedMusicSheets/{artistName}_{songName}_{instrumentName}_sheet.png"
    os.makedirs("generatedMusicSheets", exist_ok=True)

    # Plot the music sheet
    fig = plt.figure(figsize=(10, 2))
    ax = fig.add_subplot(111)
    ax.axis('off')
    score.show('lily', file=fig)

    # Save the image of the sheet music
    
    plt.savefig(musicSheetPath, format="png")
    plt.close(fig)

    return musicSheetPath

@csrf_exempt
def generatedNotes(request):

    if request.method == "POST":
        try:
            data = json.loads(request.body.decode("utf-8"))
            instrumentName = data.get("instrument")
            songName = data.get("song")
            artistName = data.get("artist")

            if not instrumentName or not songName:
                return JsonResponse({"error": "Missing instrument or song name"}, status=400)   

            instrumentAudioFile = f"separatedInstruments/{artistName} - {songName}/{instrumentName.lower()}.wav"

            if not os.path.exists(instrumentAudioFile):
                return JsonResponse({"error": "Instrument audio file not found"}, status=404)

            y, sr = librosa.load(instrumentAudioFile, sr=None)
            pitches, magnitudes = librosa.piptrack(y=y, sr=sr)

            pitchesValues = [pitches[magnitudes[:, i].argmax(), i] for i in range(pitches.shape[1]) if pitches[magnitudes[:, i].argmax(), i] > 0]

            midi = pretty_midi.PrettyMIDI()
            instrument = pretty_midi.Instrument(program=0)

            notesData = []

            if not pitchesValues:
                return JsonResponse({"error": "No pitch values detected, check audio quality"}, status=500)

            for pitch in pitchesValues:
                midiNote = int(librosa.hz_to_midi(pitch))
                note = pretty_midi.Note(velocity=100, pitch=midiNote, start=0, end=1)
                instrument.notes.append(note)
                notesData.append({"pitch": midiNote, "note": pretty_midi.note_number_to_name(midiNote)})


            midi.instruments.append(instrument)
            midiPath = f"generatedNotes/{songName}_{instrumentName}.mid"
            os.makedirs("generatedNotes", exist_ok=True)
            midi.write(midiPath)

            musicSheetPath = generateMusicSheet(notesData, artistName, songName, instrumentName)

            return JsonResponse({"message": "Notes generated", "midi_path": midiPath, "sheet_path": musicSheetPath}, status=200)

        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON"}, status=400)

        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)
        

    if request.method == "GET":
        try:
            songName = request.GET.get("song")
            instrument = request.GET.get("instrument")
            artistName = request.GET.get("artist")

            if not songName or not instrument:
                return JsonResponse({"error": "Missing song or instrument name"}, status=400)

            midiPath = f"generatedNotes/{songName}_{instrument}.mid"

            if not os.path.exists(midiPath):
                return JsonResponse({"error": "MIDI file not found"}, status=404)
        

            midiData = pretty_midi.PrettyMIDI(midiPath)
            generatedNotes = []

            for instrument in midiData.instruments:
                for note in instrument.notes:
                    generatedNotes.append({"pitch": note.pitch, "note": pretty_midi.note_number_to_name(note.pitch), "start_time": note.start, "end_time": note.end})

            musicSheetPath = f"generatedMusicSheets/{artistName}_{songName}_{instrument}_sheet.png"
            
            return JsonResponse({"message": "Notes retrieved", "notes": generatedNotes, "musicSheet": musicSheetPath}, status=200)
        
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)

    return JsonResponse({"error": "Invalid request"}, status=405)



@csrf_exempt
def logoutView(request):
    response = JsonResponse({"message": "Logged out successfully!"})
    response.delete_cookie('token')
    logout(request)
    return response


def home(request):
    return HttpResponse("Hello, this is the music app home page.")