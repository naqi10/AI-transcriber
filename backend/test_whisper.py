import whisper

# Load the model (downloads it first time only)
model = whisper.load_model("base")  # You can also try "small", "medium"

# Transcribe an audio file
result = model.transcribe("voice.mp3")  # Put your actual file here
print("🔊 Transcript:")
print(result["text"])
