# Audio to Video with Waveform and Subtitles

This script processes an audio file to generate a video with a waveform overlay on a provided image and includes subtitles from an SRT file.

## Dependencies

- FFmpeg: This script uses FFmpeg for audio and video processing. Ensure you have FFmpeg installed and available in your system's PATH.
- Python libraries: The script requires the following Python libraries:
  - `PIL` (or `Pillow`)
  - `subprocess`

You can install the required Python libraries using pip:

```bash
pip install Pillow
```

## Usage

```bash
python3 makewave.py -i INPUT_AUDIO -o OUTPUT_VIDEO -b BACKGROUND_IMAGE -s SUBTITLE_FILE [--dry-run]
```

- `-i, --infile`: Path to the input audio file.
- `-o, --outfile`: Path to the output video file.
- `-b, --bg_image`: Path to the background image file.
- `-s, --srt_file`: Path to the subtitle file in SRT format.
- `--dry-run`: If provided, runs ffplay for testing instead of ffmpeg for file generation.

## Example

```bash
python3 makewave.py -i sample_audio.wav -o output_video.mov -b background.png -s subtitles.srt
```

## License

[MIT License](LICENSE)

## Why

I was looking for a audiogram creator so that I could convert my wife's podcasts to video format. I knew ffmpeg had the capabilities, but couldn't find anything free out there that would do the job.

