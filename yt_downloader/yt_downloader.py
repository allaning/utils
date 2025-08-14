# YT video downloader
#
# Usage:
#
#   To avoid requiring FFmpeg (need to use 720p or lower):
#   python your_script_name.py "https://www.youtube.com/watch?v=VIDEO_ID" --max-res 720
#
#   Using default settings:
#   python your_script_name.py "https://www.youtube.com/watch?v=VIDEO_ID"
#
#   With English subtitles:
#   python your_script_name.py "https://www.youtube.com/watch?v=VIDEO_ID" --subs
#
#   With Spanish and French subs:
#   python your_script_name.py "https://www.youtube.com/watch?v=VIDEO_ID" --subs --sub-lang es fr
#
#   With English subtitles embedded:
#   python your_script_name.py "https://www.youtube.com/watch?v=VIDEO_ID" --subs --embed-subs
#
# Notes:
#   - FFmpeg: As mentioned in the code, embedding subtitles requires ffmpeg to be installed on your system and accessible in your system's PATH.
#   - Subtitle Availability: yt-dlp can only download subtitles that are available on the YouTube video. Some videos may not have any, or only have auto-generated ones.

import yt_dlp
import ffmpeg
import argparse

def download_youtube_video(url, download_subtitles=False, subtitle_langs=['en'], embed_subtitles=False, max_resolution=None):
    ydl_opts = {
        'outtmpl': '%(title)s.%(ext)s',
    }

    # Format selection logic
    if max_resolution:
        # Request a progressive stream up to the specified resolution
        # 'best[height<=?RES][ext=mp4]' tries to find a single MP4 file with video and audio
        # 'bestvideo[height<=?RES][ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best'
        # This is more complex, but `best[height<=?RES]` is simpler if you want to avoid ffmpeg
        ydl_opts['format'] = f'best[height<=?{max_resolution}][ext=mp4]'
        print(f"Attempting to download video in progressive MP4 format up to {max_resolution}p.")
        print("Note: Higher resolutions (e.g., 1080p, 1440p) are usually separate video/audio streams and will still require FFmpeg for merging.")
    else:
        # Default to best video and audio, which will require FFmpeg for merging
        ydl_opts['format'] = 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best'
        ydl_opts['merge_output_format'] = 'mp4' # This explicitly tells yt-dlp to merge into MP4

    if download_subtitles:
        ydl_opts.update({
            'writesubs': True,
            'subtitleslangs': subtitle_langs,
            'allsubs': False,
        })
        if embed_subtitles:
            ydl_opts['embedsubs'] = True
            print("Embedding subtitles into video (requires FFmpeg).")
        else:
            print("Downloading subtitles as separate files.")

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info_dict = ydl.extract_info(url, download=True)
            video_title = info_dict.get('title', url)
            print(f"Successfully downloaded: {video_title}")
            if download_subtitles:
                print(f"Subtitles handled for: {video_title}")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Download YouTube videos with optional subtitles and resolution control.")
    parser.add_argument("url", help="The YouTube video URL to download.")

    parser.add_argument(
        "--subs",
        action="store_true",
        help="Download subtitles for the video."
    )

    parser.add_argument(
        "--sub-lang",
        nargs="*",
        default=['en'],
        help="Specify subtitle languages (e.g., 'en fr es'). Defaults to 'en'."
    )

    parser.add_argument(
        "--embed-subs",
        action="store_true",
        help="Embed subtitles into the video file (requires ffmpeg)."
    )

    # New optional argument for max resolution
    parser.add_argument(
        "--max-res",
        type=int,
        help="Maximum resolution for progressive download (e.g., 720). May avoid FFmpeg if progressive stream is available."
    )

    args = parser.parse_args()

    download_youtube_video(
        args.url,
        download_subtitles=args.subs,
        subtitle_langs=args.sub_lang,
        embed_subtitles=args.embed_subs,
        max_resolution=args.max_res
    )

