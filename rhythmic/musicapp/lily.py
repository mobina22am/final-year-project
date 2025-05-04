import os
from music21 import environment

# Set the temporary directory for music21 to a specific folder so the data from music21 is accessible and its place is known
temp_dir = '/Users/mobinaaghaeimaleki/Documents/GitHub/final-year-project/rhythmic/analysedInstruments/music21_temp'

# Create the directory of the music21 if it doesn't already exist
if not os.path.exists(temp_dir):
    os.makedirs(temp_dir)

# Set the environment variable for music21 to use this directory
os.environ['M21_TEMP'] = temp_dir

# Verifying the path
print(f"Temporary directory for music21: {os.environ['M21_TEMP']}")