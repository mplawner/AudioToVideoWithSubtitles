import argparse
import subprocess
from PIL import Image

def process_file(infile, outfile, bg_image, srt_file, dry_run=False):
    """
    Process an audio file to generate a video with a waveform overlay on an image with subtitles.
    
    Parameters:
    - infile: Path to the input audio file.
    - outfile: Path to the output video file.
    - bg_image: Path to the background image file.
    - srt_file: Path to the subtitle file in SRT format.
    - dry_run: If True, runs ffplay for testing instead of ffmpeg for file generation.
    """
    # Get the dimensions of the background image
    with Image.open(bg_image) as img:
        width, height = img.size

    # Calculate the position of the waveform overlay dynamically
    wave_y_position = int(height * (2100 / 3000))
    wave_height = int(height * (500 / 3000))

    filter1 = (f"showwaves=mode=cline:s={width}x{wave_height}:colors=#687A6E:r=15, "
               f"scale={width}:-1, colorkey=0x000000:0.1:0.1[waves];"
               f"movie={bg_image}[bg];"
               f"[bg][waves]overlay=x=0:y={wave_y_position},"
               f"subtitles={srt_file}:force_style='PrimaryColour=&H00FFFFFF,BorderStyle=4,BackColour=&H80000000,Outline=0'[tmp]")

    if dry_run:
        command = [
            "ffmpeg", "-i", infile, "-filter_complex", filter1, 
            "-map", "[tmp]", "-map", "0:a?", "-f", "matroska", "-"
        ]
        ffplay_command = ["ffplay", "-"]
        print("Command to run:", ' '.join(command + ["|"] + ffplay_command))
        ffmpeg = subprocess.Popen(command, stdout=subprocess.PIPE)
        subprocess.run(ffplay_command, stdin=ffmpeg.stdout)
        ffmpeg.stdout.close()
    else:
        vcodec = "libx264"
        vcodec_options = "-pix_fmt yuv420p -tune stillimage -crf 28 -preset veryslow -bf 2 -flags +cgop -r 15"
        acodec = "aac"
        acodec_options = "-b:a 192k -ar 44100"
        extraflags = "-movflags +faststart"

        command = [
            "ffmpeg", "-i", infile, "-filter_complex", filter1, 
            "-map", "[tmp]", "-map", "0:a?", "-c:v", vcodec, 
            *vcodec_options.split(), "-c:a", acodec, 
            *acodec_options.split(), *extraflags.split(), outfile
        ]
        print("Command to run:", ' '.join(command))
        subprocess.run(command)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Process audio file to generate a video with waveform overlay on an image with subtitles.')
    parser.add_argument('-i', '--infile', required=True, help='Input audio file')
    parser.add_argument('-o', '--outfile', required=True, help='Output video file')
    parser.add_argument('-b', '--bg_image', required=True, help='Background image file')
    parser.add_argument('-s', '--srt_file', required=True, help='Subtitle file in SRT format')
    parser.add_argument('--dry-run', action='store_true', help='If provided, runs ffplay for testing instead of ffmpeg for file generation')
    
    args = parser.parse_args()
    process_file(args.infile, args.outfile, args.bg_image, args.srt_file, dry_run=args.dry_run)

