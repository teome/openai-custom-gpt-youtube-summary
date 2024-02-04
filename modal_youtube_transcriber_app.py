import os
import openai
from fastapi.responses import JSONResponse
from modal import Image, Secret, Stub, web_endpoint
from pydantic import BaseModel
from pytube import YouTube

# Define the Docker image and stub for Modal
image = Image.debian_slim().pip_install(["fastapi", "uvicorn", "pytube", "openai"])
stub = Stub(image=image)

class VideoRequest(BaseModel):
    url: str

class TranscriptionResponse(BaseModel):
    transcription: str

@stub.function(secret=Secret.from_name("agents_modal00"))
@web_endpoint(method="POST")
def transcribe_video(request: VideoRequest):
    """Download audio from the YouTube video and transcribe it using OpenAI's Whisper model"""
    try:
        yt = YouTube(request.url)
        audio_stream = yt.streams.filter(only_audio=True).first()
        if not audio_stream:
            raise Exception("No audio stream available")
        # Determine the file extension from the mime type
        file_extension = audio_stream.mime_type.split('/')[-1]
        audio_file = audio_stream.download(filename=f"temp_audio.{file_extension}")
    except Exception as e:
        return JSONResponse(status_code=400, content={"detail": f"Error downloading video: {e}"})

    # Transcribe the audio using OpenAI's Whisper
    try:
        client = openai.Client()
        response = client.audio.transcriptions.create(
            file=open(audio_file, "rb"),
            model="whisper-1",
            language="en",
        )
        transcription = response.text
    except Exception as e:
        return JSONResponse(status_code=500, content={"detail": f"Error transcribing audio: {e}"})
    finally:
        os.remove(audio_file)

    return JSONResponse(content={"transcription": transcription})

if __name__ == "__main__":
    stub.serve_forever()
