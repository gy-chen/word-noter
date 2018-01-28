import io
from google.cloud import speech
from google.cloud.speech import enums
from google.cloud.speech import types
from .audio import save_record


def recognize(data):
    content = io.BytesIO()
    save_record(data, content, channels=1)
    return recognize_from_wav_content(content.getvalue()).results


def recognize_from_wav_content(wav_content):
    client = speech.SpeechClient()
    audio = types.RecognitionAudio(content=wav_content)
    config = types.RecognitionConfig(
        encoding=enums.RecognitionConfig.AudioEncoding.LINEAR16,
        sample_rate_hertz=44100,
        language_code='en-US')
    response = client.recognize(config, audio)
    return response.results
