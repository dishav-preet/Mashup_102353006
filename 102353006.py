import sys
import subprocess
import os
from pydub import AudioSegment


def create_folders():
    for folder in ["videos", "audios", "trimmed"]:
        if not os.path.exists(folder):
            os.makedirs(folder)


def convert_videos_to_audio():
    print("Converting videos to audio...")

    for file in os.listdir("videos"):
        if file.endswith(".mp4"):
            video_path = os.path.join("videos", file)
            try:
                audio = AudioSegment.from_file(video_path)
                audio_name = file.replace(".mp4", ".mp3")
                audio.export(os.path.join("audios", audio_name), format="mp3")
            except Exception as e:
                print(f"Skipping {file}: {e}")


def download_videos(singer, count):
    print("Downloading videos from YouTube...")

    query = f"ytsearch{count}:{singer} songs"

    command = [
    sys.executable, "-m", "yt_dlp",
    "--js-runtimes", "node",
    "-f", "mp4",
    "--no-playlist",
    "-o", "videos/%(title)s.%(ext)s",
    query
    ]



    subprocess.run(command, check=True)


def trim_audio_files(seconds):
    print(f"Trimming first {seconds} seconds from audio files...")

    for file in os.listdir("audios"):
        if file.endswith(".mp3"):
            audio_path = os.path.join("audios", file)

            try:
                audio = AudioSegment.from_mp3(audio_path)
                trimmed_audio = audio[:seconds * 1000]

                trimmed_audio.export(
                    os.path.join("trimmed", file),
                    format="mp3"
                )
            except Exception as e:
                print(f"Skipping {file}: {e}")


def merge_audios(output_file):
    print("Merging all audio files into one...")

    final_audio = AudioSegment.empty()

    for file in os.listdir("trimmed"):
        if file.endswith(".mp3"):
            audio_path = os.path.join("trimmed", file)
            audio = AudioSegment.from_mp3(audio_path)
            final_audio += audio

    final_audio.export(output_file, format="mp3")


def main():
    if len(sys.argv) != 5:
        print("Usage: python <program.py> <SingerName> <NumberOfVideos> <AudioDuration> <OutputFileName>")
        sys.exit(1)

    singer = sys.argv[1]

    try:
        num_videos = int(sys.argv[2])
        duration = int(sys.argv[3])
    except ValueError:
        print("Error: NumberOfVideos and AudioDuration must be integers")
        sys.exit(1)

    output_file = sys.argv[4]

    if num_videos <= 10:
        print("Error: NumberOfVideos must be greater than 10")
        sys.exit(1)

    if duration <= 20:
        print("Error: AudioDuration must be greater than 20 seconds")
        sys.exit(1)

    print("Inputs validated successfully ✅")
    print("Singer:", singer)
    print("Videos:", num_videos)
    print("Duration:", duration)
    print("Output:", output_file)

    create_folders()
    download_videos(singer, num_videos)
    convert_videos_to_audio()
    trim_audio_files(duration)
    merge_audios(output_file)

    print("Mashup created successfully 🎉")


if __name__ == "__main__":
    main()
