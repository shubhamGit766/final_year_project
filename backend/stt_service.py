import os
from groq import Groq

def get_groq_client():
    return Groq(api_key=os.getenv("GROQ_API_KEY"))

async def transcribe_audio(file_path: str) -> str:
    client = get_groq_client()
    print(f"[STT] Transcribing via Groq Whisper: {file_path}")
    with open(file_path, "rb") as f:
        transcription = client.audio.transcriptions.create(
            model="whisper-large-v3",
            file=f,
            language="en"
        )
    print(f"[STT] Transcript: {transcription.text}")
    return transcription.text.strip()

# from faster_whisper import WhisperModel

# _model = None

# def get_model():
#     global _model
#     if _model is None:
#         print("[STT] Loading Whisper model...")
#         _model = WhisperModel("base", device="cpu", compute_type="int8")
#         # _model = WhisperModel("small", device="cpu", compute_type="int8")
#         print("[STT] Whisper model loaded!")
#     return _model

# async def transcribe_audio(file_path: str) -> str:
#     model = get_model()
#     print(f"[STT] Transcribing audio: {file_path}")
#     segments, info = model.transcribe(
#         file_path,
#         beam_size=5,
#         language="en",
#         vad_filter=True,
#         vad_parameters=dict(min_silence_duration_ms=500),
#     )
#     transcript = " ".join(segment.text.strip() for segment in segments)
#     print(f"[STT] Transcript: {transcript}")
#     return transcript.strip()