from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from whisper_model import transcribe_audio
from summarizer_model import summarize_text
from fastapi.staticfiles import StaticFiles
from fastapi import Request
from fastapi.responses import FileResponse
from gtts import gTTS
import pyttsx3
import shutil
import os

app = FastAPI()

# Allow frontend requests
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.post("/transcribe")
async def transcribe(file: UploadFile = File(...)):
    temp_audio_path = f"temp_{file.filename}"
    with open(temp_audio_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    text = transcribe_audio(temp_audio_path)
    summary = summarize_text(text)

    os.remove(temp_audio_path)

    # Debug prints (optional)
    print("Transcript:", text)
    print("Summary:", summary)
    return {
    "transcript": str(text),
    "summary": str(summary)
}
@app.post("/text-to-speech")
async def text_to_speech(request: Request):
    data = await request.json()
    text = data.get("text")
    if not text:
        return {"error": "No text provided"}

    output_path = "tts_output.mp3"
    tts = gTTS(text)
    tts.save(output_path)

    return FileResponse(output_path, media_type="audio/mpeg", filename="tts_output.mp3")



app.mount("/", StaticFiles(directory="../frontend", html=True), name="static")

