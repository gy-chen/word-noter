import asyncio
import logging
from queue import Empty
from .audio import active_record_large_sound, recorded_sounds
from .gcloud import recognize


async def recognize_word_from_recorder(in_queue, recognize_sound_func):
    while True:
        try:
            recorded_sound = in_queue.get(block=False)
            logging.debug('Try to recognize sound using Google Speech API')
            recognized_words = recognize_sound_func(recorded_sound)
            logging.info('Recognized words: %s' % recognized_words)
            return recognized_words
        except Empty:
            continue
        finally:
            await asyncio.sleep(0)


def create_recognize_word_from_recorder_task(recognize_sound_func=recognize):
    # TODO create task that will keep sending recognized sounds to websocket
    async def log_recognized_words():
        while True:
            recognized_words = await recognize_word_from_recorder(recorded_sounds, recognize_sound_func)
            logging.info('Recognized: %s' % recognized_words)
            await asyncio.sleep(0)

    return asyncio.gather(
        active_record_large_sound(recorded_sounds, channels=1),
        log_recognized_words()
    )
