import os
import sys
import imageio_ffmpeg
import whisper

# Ensure ffmpeg binary is accessible to Whisper
ffmpeg_exe = imageio_ffmpeg.get_ffmpeg_exe()
ffmpeg_dir = os.path.dirname(ffmpeg_exe)
os.environ["PATH"] = ffmpeg_dir + os.pathsep + os.environ.get("PATH", "")

def transcribe_audio(audio_path="audio_sample.mp3", model_name="base"):
    if not os.path.exists(audio_path):
        print(f"? Audio file not found: {audio_path}")
        print("Please place an audio file (e.g. .mp3, .wav, .m4a) in the directory or specify a valid file path.")
        return None

    print(f"??? Loading Whisper model (\"{model_name}\")...")
    model = whisper.load_model(model_name)

    print(f"?? Transcribing \"{audio_path}\"...")
    result = model.transcribe(audio_path)

    print("\n" + "="*50)
    print("?? Transcribed Text:")
    print("="*50)
    print(result["text"])
    print("="*50)

    return result

if __name__ == "__main__":
    audio_file = sys.argv[1] if len(sys.argv) > 1 else "audio_sample.mp3"
    model_size = sys.argv[2] if len(sys.argv) > 2 else "base"
    transcribe_audio(audio_file, model_size)

