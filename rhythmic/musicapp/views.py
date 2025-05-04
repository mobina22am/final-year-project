# Necessary libraries for the application (backend) to function
from django.contrib.auth import login, logout, authenticate
from django.http import JsonResponse, HttpResponse
from django.contrib.auth import get_user_model
from django.views.decorators.csrf import csrf_exempt
from .models import User, StoredSongs
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
import magic 
from music21 import environment
from django.views.decorators.clickjacking import xframe_options_exempt
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required
from django.core.files.storage import default_storage
from django.contrib.auth.hashers import make_password
from music21 import stream, note, meter

# restoring the temporary directory for music 21 and setting the environment
tempM21Dir = '/Users/mobinaaghaeimaleki/Documents/GitHub/final-year-project/rhythmic/analysedInstruments/music21_temp'

# Creating the path if it doesn't exist
if not os.path.exists(tempM21Dir):
    os.makedirs(tempM21Dir)

os.environ['M21_TEMP'] = tempM21Dir

us = environment.UserSettings()

# Set the LilyPond path for music21
us['lilypondPath'] = '/opt/homebrew/bin/lilypond'

# Initiating the youtube url base
ytUrl = "https://www.youtube.com/results?search_query="

User = get_user_model()
songData = {}

# The function that will handle the sign up functionality of the application
@csrf_exempt
def UserSignUp(request):

    if request.method == "POST":

        data = json.loads(request.body)
        name = data["name"]
        email = data["email"]
        birthday = data["birthday"]
        password = data["password"]
        username = data["username"]

        # Checking if the email already exists
        if User.objects.filter(email=email).exists():
            return JsonResponse({"error": "Email already exists"}, status=400)

        # Checking if the username already exists
        if User.objects.filter(username=username).exists():
            return JsonResponse({"error": "Username already exists"}, status=400)

        # If all of the conditions has been passed, the user is created
        user = User.objects.create(
            first_name=name,
            email=email,
            birthday=birthday,
            username=username,
        )

        # Setting (hashing) the user's password
        user.set_password(password)

        # Saving the user
        user.save()

        # Allows the user to login straight away after signing up by checking the username and password
        user = authenticate(username=username, password=password)

        if user:

            login(request, user)

            request.session.create()

            response = JsonResponse({"message": "User created successfully!", "token": request.session.session_key, "name": user.first_name}, status=201)
            response.set_cookie(key="token", value=request.session.session_key, httponly=True, secure=True, samesite='None') 

            return response
    
    return JsonResponse({"message": "User not created!"}, status=400)


# The function handles the login functionality of the application
@csrf_exempt
def userLogin(request):

    if request.method == "POST":

        # Loading the username and the password input by hte user
        data = json.loads(request.body)
        username = data["username"]
        password = data["password"]

        # Validating the input data with the data from database 
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


# The functions handles the forgot credential functionality of the application
@csrf_exempt
def forgotCredentials(request):

    if request.method == 'POST':

        data = json.loads(request.body)

        # Gets data from the request sent from the frontend input by the user
        name = data.get('name')
        email = data.get('email')
        birthday = data.get('birthday')

        # Searches for a user that matches the condition
        user = User.objects.filter(first_name=name, email=email, birthday=birthday).first()

        # If there is any user, returning the username of the user
        if user:
            return JsonResponse({"message": f"Your username is {user.username}. If you forgot your password, please reset it."}, status=200)
        else:
            return JsonResponse({"error": "No user found with the provided details"}, status=400)


# Handling the reset password functionality of the application
@csrf_exempt
def resetPassword(request):

    if request.method == 'POST':

        data = json.loads(request.body)

        # Getting the users data input
        name = data.get('name')
        email = data.get('email')
        birthday = data.get('birthday')
        newPassword = data.get('newPassword')

        # Checking if the user exists
        user = User.objects.filter(first_name=name, email=email, birthday=birthday).first()

        # If the user exists, the password is reset
        if user:
            # Hashing the new password
            user.password = make_password(newPassword)  

            # Saving the user
            user.save()

            return JsonResponse({"message": "Your password has been successfully reset."}, status=200)
        
        else:
            return JsonResponse({"error": "No user found with the provided details"}, status=400)


# The function is responsible to update the user data
@csrf_exempt
def updateProfile(request):

    if request.method == "PUT":

        # This action is not available unless the user is logged in
        if not request.user.is_authenticated:
            return JsonResponse({"error": "You are not logged in"}, status=401)

        # Getting user's data to be changed or updated
        data = json.loads(request.body)
        user = request.user

        user.first_name = data["name"]
        user.email = data["email"]  
        user.birthday = data["birthday"]
        user.username = data["username"]

        # Check if the user's password is right. If not, updating action will not take place
        if user.check_password(data["oldPassword"]):
            pass

        else:
            return JsonResponse({"error": "Invalid password"}, status=400)

        # Check if the user wanted to change the password
        if "password" in data:
            user.set_password(data["password"])

        # Saving the user
        user.save()

        request.session.create()

        response = JsonResponse({"message": "Profile updated successfully!", "token": request.session.session_key, "name":user.first_name}, status=200)
        response.set_cookie(key="token", value=request.session.session_key , httponly=True, secure=True, samesite='None')

        return response
    

    if request.method == "GET":

        # The user must be logged in to be able to update the profile
        if not request.user.is_authenticated:
            return JsonResponse({"error": "You are not logged in"}, status=401)
        
        # Sending some of the users data (not the password) to the frontend to be displayed to the user
        user = request.user
        return JsonResponse({"name": user.first_name, "email": user.email, "birthday": user.birthday, "username": user.username}, status=200)

    return JsonResponse({"error": "Invalid method"}, status=405)


# The function searches for any video on YouTube that matches the data given
def searchSongLink(songName, artistName):

    # Merging the YouTube URL base and the input data from the user to find the matching video
    query = f"{songName} {artistName} official audio"
    songUrl = ytUrl + "+".join(query.split())

    response = requests.get(songUrl)

    # If a video exist, the link will be returned
    if "watch?v=" in response.text:
        video_id = response.text.split("watch?v=")[1].split('"')[0]
        return f"https://www.youtube.com/watch?v={video_id}"
    return None


# This function downloads the song based on the link given to it
def downloadSongAudio(youtubeLink):

    # Setting the directory that will hold the downloaded songs' file
    outputPath = "songs/%(title)s.%(ext)s"

    # Setting for the song file to be downloaded
    ydlOpts = {
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
        'outtmpl': outputPath,
    }

    # Finally downloading the song file
    with yt_dlp.YoutubeDL(ydlOpts) as ydl:
        info = ydl.extract_info(youtubeLink, download=True)

    return ydl.prepare_filename(info)


# This function will get the name of the song and the artist and will call two previous functions to download the song's file
@csrf_exempt
def getSongAudio(request, songName, artistName):

    if request.method == "POST":

        # Checking if all of the song data is available
        if not songName or not artistName:
            return JsonResponse({"error": "Missing song name or artist name"}, status=400)

        # Searching for a matching video on YouTube
        youtubeLink = searchSongLink(songName, artistName)

        # If the song doesn't exist on YouTube, let the user know
        if not youtubeLink:
            return JsonResponse({"error": "Song not found on YouTube"}, status=404)

        # Downloading the song and getting the exact location or directory of the song 
        audioPath = downloadSongAudio(youtubeLink)

        return JsonResponse({"audio_path": audioPath})

    return JsonResponse({"error": "Invalid request"}, status=400)


# This function will detect the instruments used in the song passed
@csrf_exempt
def findInstruments(request):

    global foundInstruments
    global songData

    if request.method == "POST":

        foundInstruments = []
        
        try:
            # Getting the name of the artist and the name of the song from the frontend
            data = json.loads(request.body.decode("utf-8"))
            songName = data.get("name")
            artistName = data.get("artist")

            # Searching for a match from the song files that their instruments have been seperated and detcted
            separatedInstrumentFolder = f"separatedInstruments/{artistName} - {songName}"

            # Checking to see if the songs instrument has already been detected and available to save time and energy
            if os.path.exists(separatedInstrumentFolder):
                for file in glob.glob(os.path.join(separatedInstrumentFolder, '*')):

                    if "bass.wav" in file:
                        foundInstruments.append("Bass")
                        continue

                    if "drums.wav" in file:
                        foundInstruments.append("Drums")
                        continue

                    if "piano.wav" in file:
                        foundInstruments.append("Piano")
                        continue

                    if "guitar.wav" in file:
                        foundInstruments.append("Guitar")
                        continue
                
                # Making a list of all of the instruments detected
                foundInstruments = list(set(foundInstruments))

                # If there are instruments detected, pass the information to the frontend to be displayed
                if foundInstruments:
                    songData = {"name": songName, "artist": artistName, "instruments": foundInstruments}
                    return JsonResponse({"message": "instruments detected", "instruments": foundInstruments, "song": songData}, status=200)


            # If the song's instruments have not been detected before:

            # Getting the actual song audio file
            response = getSongAudio(request, songName, artistName)
            songData = json.loads(response.content) 

            # Check to see if there is any song downloaded
            if "audio_path" not in songData:
                return JsonResponse({"error": "Failed to download song audio"}, status=500)
            
            # Storing the audio file path and converting it to MP3
            songPathString = songData["audio_path"]
            songPathString = songPathString.replace(".webm", ".mp3")
            
            # following is the 6-stem demucs model that will detect the instruments in the song
            try:
                subprocess.run(["demucs", "-n", "htdemucs_ft", songPathString], check=True)

            except subprocess.CalledProcessError:
                return JsonResponse({"error": "Failed to separate instruments"}, status=500)
            
            # The final folder to store the instruments audio file
            separatedInstrumentFolder = f"separatedInstruments/{artistName} - {songName}"
            
            # Creating the folder if it doesn't already exist
            os.makedirs(separatedInstrumentFolder, exist_ok=True)

            # Storing the file that will get the initial data from Demucs
            separatedDirection = f"separated/htdemucs_ft/{os.path.basename(songPathString).split('.')[0]}/*"

            # If the seperated instrumens audio files exist, move them to a new directory, 
            # separatedInstrumentFolder in this case (vocals not included as it is not necessary for the purpose of this project)
            # This action is to make sure only the necessary instruments are displayed to the user
            for file in glob.glob(separatedDirection):

                # Don't need the vocals
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

                # This file may have more than one instrument audio inside, therefore, further detection is necessary
                if "other.wav" in file:
                    
                    # Librosa is used to do further maths calculation based different frequencies to find specific instrument
                    y, sr = librosa.load(file, sr=None)

                    # Necessary calculation bases
                    spectralCentroids = librosa.feature.spectral_centroid(y=y, sr=sr).mean()
                    spectralBandwidth = librosa.feature.spectral_bandwidth(y=y, sr=sr).mean()
                    spectralRolloff = librosa.feature.spectral_rolloff(y=y, sr=sr, roll_percent=0.85).mean()

                    # Detecting the specific instrument by comparing to the base values
                    if 900 < spectralCentroids < 2500 and 1000 < spectralBandwidth < 4500:
                        foundInstruments.append("Guitar")
                        targetPath = os.path.join(separatedInstrumentFolder, "guitar.wav")
                        shutil.move(file, targetPath)
                        continue

                    if 3000 < spectralCentroids < 6000 and 4000 < spectralBandwidth < 7000 and spectralRolloff > 6000:
                        foundInstruments.append("Violin")
                        targetPath = os.path.join(separatedInstrumentFolder, "violin.wav")
                        shutil.move(file, targetPath)
                        
            # Adding the found instrument to the list to be returrned
            foundInstruments = list(set(foundInstruments))

            # Storing the song data to be returned
            songData = { "name": songName, "artist": artistName, "audio_path": songPathString, "instruments": foundInstruments }

            return JsonResponse({"message": "instruments detected", "instruments": foundInstruments, "song": songData}, status=200)
        
        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON"}, status=400)


    if request.method == "GET":

        # Returning the song data
        if songData:
            return JsonResponse({"instruments": foundInstruments, "song": songData}, status=200)
        
        return JsonResponse({"error": "No song data detected"}, status=404)

    return JsonResponse({"error": "Invalid request"}, status=405)


# The function will generate the music sheet of the song requested
def generateMusicSheet(notesData, artistName, songName, instrumentName):

    # Storing the necessary libraries to generate the music sheet
    score = stream.Score()
    part = stream.Part()
    
    # Adding a time signature to Part
    part.append(meter.TimeSignature('4/4'))

    # Starting the first measurement
    currentMeasure = stream.Measure(number=1)
    # Setting the time signature logic (every 4 beats)
    beatsPerMeasure = 4
    # Tracking variables
    currentBeats = 0  
    measureCount = 0  

    # Going over all of the notes getting the pitch value and duration to create music21 object
    for noteData in notesData:
        midiNote = noteData['pitch']
        duration = noteData.get('duration', 1.0)
        m21Note = note.Note(midiNote, quarterLength=duration)

        # Adding the notes and tracking duration
        currentMeasure.append(m21Note)
        currentBeats += m21Note.quarterLength

        # Checking if the measure is full to be added to the part and start a new measure for the next note in the loop
        if currentBeats >= beatsPerMeasure:
            part.append(currentMeasure)
            currentMeasure = stream.Measure(number=currentMeasure.number + 1)
            currentBeats = 0
            measureCount += 1  

    # Adding the last measure to the part variable
    if len(currentMeasure.notes) > 0:
        part.append(currentMeasure)

    # Finally adding the completed part to the score
    score.append(part)

    # Getting the path to the music sheets and making sur eit exists
    outputDir = os.path.abspath("generatedMusicSheets")
    os.makedirs(outputDir, exist_ok=True)

    # Naming the file and creating a LilyPond and PDF file for each
    fileName = f"{artistName}_{songName}_{instrumentName}"
    lilypondFilePath = os.path.join(outputDir, f"{fileName}.ly")
    pdfFilePath = os.path.join(outputDir, f"{fileName}.pdf")

    # Setting for theLilyPond file to make sure a proper line break is done for the music sheet
    lilypondContent = r"""
\version "2.24.2"
\paper {
    indent = 0\mm
    line-width = 180\mm
    ragged-right = ##t
    ragged-bottom = ##t
}
\layout {
    \context {
        \Score
        \override SpacingSpanner.base-shortest-duration = #(ly:make-moment 1/8)
    }
}
\new Staff {
"""

    # 4/4 time signature and measures to force a line break when necessary
    notes_per_measure = 4  
    measures_per_line = 4  
    note_counter = 0
    measure_counter = 0


    for noteData in notesData:
        # Necessary conversion of the data notation for LilyPond file 
        pitch = noteData['note'].lower().replace("#", "is") 
        duration = noteData.get("duration", "4")

        # To make sure the valid data with correct durations are passed
        if duration not in ["1", "2", "4", "8", "16"]:
            duration = "4"  

        # Adding the content to LilyPond
        lilypondContent += f" {pitch}{duration}"
        note_counter += 1

        # Further setting to make sure proper line breaks
        if note_counter % notes_per_measure == 0:
            measure_counter += 1
            if measure_counter % measures_per_line == 0:
                lilypondContent += " \n\\break\n"

    lilypondContent += "\n}"

    # Write the lilyPond file
    with open(lilypondFilePath, "w") as f:
        f.write(lilypondContent)

    # Generate the music sheet as a PDF file
    try:
        subprocess.run(["lilypond", "--pdf", "-o", outputDir, lilypondFilePath], check=True)

        if os.path.exists(pdfFilePath):
            print(f"Music sheet generated at: {pdfFilePath}")
            return pdfFilePath
        else:
            print("Error: PDF not generated.")
            return "Error: PDF not generated."

    except subprocess.CalledProcessError as e:
        print(f"Error running LilyPond: {str(e)}")
        return f"Error generating sheet: {str(e)}"
    

# The function will call the previous function to generate the music sheet and return the actual PDF file
@xframe_options_exempt
@csrf_exempt
def generatedNotes(request):

    if request.method == "POST":
        try:
            # Loading the data chosen from the user
            data = json.loads(request.body.decode("utf-8"))
            instrumentName = str(data.get("instrument"))
            songName = data.get("song")
            artistName = data.get("artist")

            # Checking if the data is available
            if not instrumentName or not songName or not artistName:
                return JsonResponse({"error": "Missing instrument, song or artist name"}, status=400)   

            # Seraching for the requested instrument audio file
            instrumentAudioFile = f"separatedInstruments/{artistName} - {songName}/{instrumentName.lower()}.wav"

            # Check if the file exists
            if not os.path.exists(instrumentAudioFile):
                return JsonResponse({"error": "Instrument audio file not found"}, status=404)

            # Loading the audio file and doing the necessary calculations to be passed to the generateMusicSheet function
            y, sr = librosa.load(instrumentAudioFile, sr=None)
            pitches, magnitudes = librosa.piptrack(y=y, sr=sr)

            pitchesValues = [pitches[magnitudes[:, i].argmax(), i] for i in range(pitches.shape[1]) if pitches[magnitudes[:, i].argmax(), i] > 0]

            midi = pretty_midi.PrettyMIDI()
            instrument = pretty_midi.Instrument(program=0)

            notesData = []

            # Checking if the pitches value exists
            if not pitchesValues:
                return JsonResponse({"error": "No pitch values detected, check audio quality"}, status=500)

            # Loading the audio file data to the variable notesData
            for pitch in pitchesValues:
                midiNote = int(librosa.hz_to_midi(pitch))
                note = pretty_midi.Note(velocity=100, pitch=midiNote, start=0, end=1)
                instrument.notes.append(note)
                notesData.append({"pitch": midiNote, "note": pretty_midi.note_number_to_name(midiNote)})

            # Creating a midi file, later to be processed for the music sheet generation purpose
            midi.instruments.append(instrument)

            midiPath = f"generatedNotes/{artistName}_{songName}_{instrumentName}.mid"
            os.makedirs("generatedNotes", exist_ok=True)
            midi.write(midiPath)

            # Getting the path  of the generated music sheet
            musicSheetPath = generateMusicSheet(notesData, artistName, songName, instrumentName)

            # Printing the music sheet
            print(musicSheetPath)

            return JsonResponse({"message": "Notes generated", "sheetPath": musicSheetPath}, status=200)
        
        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON"}, status=400)

        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)
        
    if request.method == "GET":
        try:
            # Loading the data passed from the frontend
            songName = request.GET.get("song")
            instrument = str(request.GET.get("instrument"))
            artistName = request.GET.get("artist")

            # Check if all of the data needed is available
            if not songName or not instrument:
                return JsonResponse({"error": "Missing song or instrument name"}, status=400)

            # Getting the path of the requested music sheet
            musicSheetPath = f"generatedMusicSheets/{artistName}_{songName}_{instrument}.pdf"

            # Check to see if the sheet exists
            if not os.path.exists(musicSheetPath):
                return JsonResponse({"error": "Music sheet not found"}, status=404)
            
            return JsonResponse({"message": "Notes retrieved", "musicSheet": f"/generatedMusicSheets/{artistName}_{songName}_{instrument}.pdf"}, status=200)
        
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)

    return JsonResponse({"error": "Invalid request"}, status=405)


# The function will save the music sheet to the database
@csrf_exempt
@login_required
def saveMusicSheet(request):

    if request.method == "POST":
        try:
            # Getting the necessary data from the frontend
            songName = request.POST.get("song")
            artistName = request.POST.get("artist")
            instrument = request.POST.get("instrument")
            pdfFile = request.FILES.get("pdfFile")

            # Check to see if they exist
            if not songName or not artistName or not pdfFile:
                return JsonResponse({"error": "Missing required fields"}, status=400)

            # Make sure it is a valid PDF file
            mime = magic.Magic(mime=True)
            # Read the first 2KB of the file to make sure of the type
            file_type = mime.from_buffer(pdfFile.read(2048)) 
            # Reset the file pointer after reading the file
            pdfFile.seek(0)  

            # Make sure the type of the file is PDF
            if file_type != "application/pdf":
                return JsonResponse({"error": "Invalid file type. Please upload a PDF."}, status=400)

            # Read the entire PDF file as binary data (this is the best way to be stored in the database)
            pdf_data = pdfFile.read()

            # Store the song data abd the PDF file in the database
            storedSong = StoredSongs.objects.create(
                user=request.user,
                name=songName,
                artist=artistName,
                instrument=instrument,
                details=f"Music sheet for {songName} by {artistName}",
                pdfFile=pdf_data, 
            )

            return JsonResponse({"message": "Music sheet stored successfully", "storedSongId": storedSong.id}, status=201)

        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)

    return JsonResponse({"error": "Invalid request method"}, status=405)


# The function gets the lists of the songs that their music sheet have stored
@login_required
def getSavedSongs(request):

    if request.method == "GET":
        try:
            # Getting the name of the song and the artist and the instrument of the song stored
            songs = StoredSongs.objects.filter(user=request.user).values("id", "name", "artist", "instrument")
            return JsonResponse({"songs": list(songs)}, status=200)
        
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)
        
    return JsonResponse({"error": "Invalid request method"}, status=405)


# Getting the PDF file of the music sheet from the database
@login_required
def getMusicSheet(request, songId):

    # Retrieve the stored song and make sure it is owned by the user
    storedSong = get_object_or_404(StoredSongs, id=songId, user=request.user)

    # Searching for a matching music sheet
    if not storedSong.pdfFile:
        return JsonResponse({"error": "No PDF found for this song"}, status=404)

    response = HttpResponse(storedSong.pdfFile, content_type="application/pdf")
    response["Content-Disposition"] = f'inline; filename="{storedSong.name}.pdf"'
    return response


# The function will delete the requested music sheet from the database
@csrf_exempt
@login_required
def deleteSong(request, songId):

    if request.method == "DELETE":
        try:
            # Retrieve the stored song and make sure it is owned by the user
            storedSong = get_object_or_404(StoredSongs, id=songId, user=request.user)
            
            # Delete the song and the music sheet
            storedSong.delete()

            return JsonResponse({"message": "Music sheet deleted successfully."}, status=200)
        
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)
    
    return JsonResponse({"error": "Invalid request method"}, status=405)


# Logout the user from the application
@csrf_exempt
def logoutView(request):
    response = JsonResponse({"message": "Logged out successfully!"})
    response.delete_cookie('token')
    logout(request)
    return response


# A simple message for the main backend of the applicatino to make sure it is running
def home(request):
    return HttpResponse("Hello, this is the music app home page.")