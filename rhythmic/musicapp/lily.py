import os
from music21 import environment

# Set the temp directory to a specific folder
temp_dir = '/Users/mobinaaghaeimaleki/Documents/GitHub/final-year-project/rhythmic/analysedInstruments/music21_temp'

# Create the directory if it doesn't exist
if not os.path.exists(temp_dir):
    os.makedirs(temp_dir)

# Set the environment variable for music21 to use this directory
os.environ['M21_TEMP'] = temp_dir

# Verify the path
print(f"Temporary directory for music21: {os.environ['M21_TEMP']}")