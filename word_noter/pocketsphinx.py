import io
import pocketsphinx
from .audio import save_record


def recognize(data):
    content = io.BytesIO()
    save_record(data, content)
    content.seek(0)
    return recognize_from_wav_content(content)


def recognize_from_wav_content(wav_content):
    audio = pocketsphinx.AudioFile()
    audio.f = wav_content
    return [phrase.hypothesis() for phrase in audio]
