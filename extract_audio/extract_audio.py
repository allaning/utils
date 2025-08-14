import subprocess
import os
import argparse

def extract_audio_with_ffmpeg(input_file, output_file=None):
    """
    Extracts audio from a video file and saves it as an MP3.

    Args:
        input_file (str): The path to the input video file.
        output_file (str, optional): The path to save the extracted audio.
    """
    if not os.path.exists(input_file):
        print(f"❌ Error: Input file '{input_file}' not found.")
        return

    # If no output file is provided, create a default name with an .mp3 extension
    if output_file is None:
        filename_without_ext, _ = os.path.splitext(input_file)
        output_file = f"{filename_without_ext}.mp3"
        print(f"No output file specified. Using default: '{output_file}'")

    # Construct the FFmpeg command
    command = [
        'ffmpeg',
        '-i', input_file,
        '-vn',
        '-c:a', 'libmp3lame',
        '-q:a', '2',
        output_file
    ]

    try:
        subprocess.run(command, check=True)
        print(f"✅ Audio extracted successfully to '{output_file}'")
    except subprocess.CalledProcessError as e:
        print(f"❌ FFmpeg command failed with error: {e}")
    except FileNotFoundError:
        print("❌ Error: FFmpeg not found. Make sure it's installed and in your system PATH.")

def main():
    parser = argparse.ArgumentParser(description="Extracts audio from a video file using FFmpeg.")
    parser.add_argument("input_file", help="The path to the input video file (e.g., 'my_video.mp4').")
    parser.add_argument("--output-file", "-o", help="The path for the output audio file (e.g., 'my_audio.mp3'). If not provided, a default name will be used.")

    args = parser.parse_args()

    extract_audio_with_ffmpeg(args.input_file, args.output_file)

if __name__ == "__main__":
    main()

