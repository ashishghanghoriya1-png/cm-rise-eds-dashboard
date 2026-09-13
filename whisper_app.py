import os
import shutil
import imageio_ffmpeg
import whisper

# 1. Automatic FFmpeg PATH Setup (Ensures Whisper can decode .mp3, .wav, .m4a on Windows)
ffmpeg_bin = imageio_ffmpeg.get_ffmpeg_exe()
ffmpeg_dir = os.path.dirname(ffmpeg_bin)
target_ffmpeg = os.path.join(ffmpeg_dir, "ffmpeg.exe")
if not os.path.exists(target_ffmpeg):
    shutil.copy(ffmpeg_bin, target_ffmpeg)
os.environ["PATH"] = ffmpeg_dir + os.pathsep + os.environ.get("PATH", "")

# 2. Load Whisper Model ("tiny", "base", "small", "medium", "large")
print("Loading Whisper model...")
model = whisper.load_model("base")

# 3. Transcribe Audio File
audio_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "audio_sample.wav")
if os.path.exists(audio_path):
    print(f"Transcribing {audio_path}...")
    result = model.transcribe(audio_path)
    print("\nTranscribed Text:")
    print(result["text"])
else:
    print(f"?? Audio file \"{audio_path}\" not found in current directory.")
    print("Please place your .mp3, .wav, or .m4a file in this folder and rerun.")

