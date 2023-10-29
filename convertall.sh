#!/bin/bash

# Check if the user has provided enough arguments
if [ "$#" -ne 2 ]; then
    echo "Usage: $0 <folder_path> <background_image>"
    exit 1
fi

# Get the folder path and background image from the arguments
FOLDER="$1"
BG_IMAGE="$2"

# Check if the provided folder exists
if [ ! -d "$FOLDER" ]; then
    echo "Error: Provided folder does not exist."
    exit 1
fi

# Check if the provided background image exists
if [ ! -f "$BG_IMAGE" ]; then
    echo "Error: Provided background image does not exist."
    exit 1
fi

# Iterate over all wav files in the folder
for WAV_FILE in "$FOLDER"/*.wav; do
    # Check if the wav file exists
    if [[ -f "$WAV_FILE" ]]; then
        # Extract the filename without extension
        FILENAME=$(basename -- "$WAV_FILE")
        BASENAME="${FILENAME%.*}"
        
        # Construct the srt filename
        SRT_FILE="$FOLDER/$BASENAME.srt"
        
        # Construct the output filename
        OUT_FILE="$FOLDER/$BASENAME.mov"
        
        # Check if the corresponding srt file exists
        if [[ -f "$SRT_FILE" ]]; then
            echo "Processing $WAV_FILE with $SRT_FILE..."
            
            # Call the Python script with the appropriate arguments
            python3 makewave.py -i "$WAV_FILE" -o "$OUT_FILE" -b "$BG_IMAGE" -s "$SRT_FILE"
        else
            echo "Warning: Corresponding srt file for $WAV_FILE does not exist. Skipping..."
        fi
    fi
done

