import subprocess
import os
from pydub import AudioSegment


def create_mashup(singer, num_videos, duration, output_file):

    if num_videos <= 10:
        raise ValueError("Number of videos must be greater than 10")

    if duration <= 20:
        raise ValueError("Duration must be greater than 20 seconds")

    # Create folders
    for folder in ["videos", "audios", "trimmed"]:
        if not os.path.exists(folder):
            os.makedirs(folder)

    print("Downloading videos...")

    query = f"ytsearch{num_videos}:{singer} songs"

    command = [
        "yt-dlp",
        "--js-runtimes", "node",
        "--no-playlist",
        "-f", "mp4",
        "-o", "videos/%(title)s.%(ext)s",
        query
    ]

    result = subprocess.run(command)

    if result.returncode != 0:
        print("Download failed. Skipping download step.")


    print("Converting videos to mp3...")

    for file in os.listdir("videos"):
        if file.endswith(".mp4"):
            video_path = os.path.join("videos", file)
            audio = AudioSegment.from_file(video_path)
            audio_name = file.replace(".mp4", ".mp3")
            audio.export(os.path.join("audios", audio_name), format="mp3")

    print("Trimming audio...")

    for file in os.listdir("audios"):
        if file.endswith(".mp3"):
            audio_path = os.path.join("audios", file)
            audio = AudioSegment.from_mp3(audio_path)
            trimmed_audio = audio[:duration * 1000]
            trimmed_audio.export(
                os.path.join("trimmed", file),
                format="mp3"
            )

    print("Merging audio...")

    final_audio = AudioSegment.empty()

    for file in os.listdir("trimmed"):
        if file.endswith(".mp3"):
            audio_path = os.path.join("trimmed", file)
            audio = AudioSegment.from_mp3(audio_path)
            final_audio += audio

    final_audio.export(output_file, format="mp3")

    print("Mashup created successfully!")
