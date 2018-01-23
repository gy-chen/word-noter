import collections
import io
import logging
from google.cloud import speech
from google.cloud.speech import enums
from google.cloud.speech import types
from .audio import save_record


def recognize(data):
    client = speech.SpeechClient()
    content = io.BytesIO()
    save_record(data, content, channels=1)
    audio = types.RecognitionAudio(content=content.getvalue())
    config = types.RecognitionConfig(
        encoding=enums.RecognitionConfig.AudioEncoding.LINEAR16,
        sample_rate_hertz=44100,
        language_code='en-US')
    response = client.recognize(config, audio)
    return response.results


if __name__ == '__main__':
    import asyncio
    from queue import Empty
    from .audio import recorded_sounds, large_sound_active_record_task

    logging.basicConfig(level=logging.INFO)
    loop = asyncio.get_event_loop()


    async def main():
        while True:
            try:
                recorded_sound = recorded_sounds.get(block=False)
                logging.debug('Try to recognize sound using Google Speech API')
                recognized_words = recognize(recorded_sound)
                logging.info('Recognized words: %s' % recognized_words)
            except Empty:
                pass
            finally:
                await asyncio.sleep(1)


    task = asyncio.gather(large_sound_active_record_task(channels=1), main())

    loop.run_until_complete(task)
