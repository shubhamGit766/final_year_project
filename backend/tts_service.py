import base64
import tempfile
import os
from gtts import gTTS

async def text_to_speech_base64(text: str) -> str:
    print(f"[TTS] Converting text to speech: {text[:60]}...")
    tts = gTTS(text=text, lang='en', tld='com', slow=False)
    
    with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as tmp:
        tmp_path = tmp.name

    try:
        tts.save(tmp_path)
        with open(tmp_path, "rb") as f:
            audio_bytes = f.read()
        print("[TTS] Done!")
        return base64.b64encode(audio_bytes).decode("utf-8")
    finally:
        os.unlink(tmp_path)