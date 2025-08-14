# Had to install moviepy via: pip install moviepy==1.0.3

import sys
from moviepy.editor import VideoFileClip, concatenate_videoclips

# Check if at least two video files were provided
if len(sys.argv) < 3:
    print("Usage: python join_videos.py video1.mp4 video2.mp4 [video3.mp4 ...]")
    sys.exit(1)

# Get the list of filenames from arguments
video_files = sys.argv[1:]

# Load each video clip
clips = []
for file in video_files:
    try:
        clip = VideoFileClip(file)
        clips.append(clip)
    except Exception as e:
        print(f"Error loading {file}: {e}")
        sys.exit(1)

# Concatenate and export
final_clip = concatenate_videoclips(clips, method="compose")  # 'compose' handles different resolutions
output_filename = "joined_output.mp4"
final_clip.write_videofile(output_filename, codec="libx264")

print(f"Exported joined video to: {output_filename}")

