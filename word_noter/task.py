import asyncio
import logging
from queue import Empty
from .camera import ImageCapture
from .image import convert_frame_to_image, rotate_frame_horizontal_to_hough_line, get_median_hough_line
from .keybord_listener import pressed_keys
from .tesseract import recognize_words
from .audio import recorded_sounds, active_record_large_sound

trigger_key = 'k'


async def recognize_words_from_user_image():
    """Recognize words from image that captured by user intent

    :return: list of recognized words
    """
    cap = ImageCapture()
    with cap:
        while True:
            try:
                frame = cap.capture()
                pressed_key = pressed_keys.get(block=False)
                if pressed_key.__dict__.get('char') != trigger_key:
                    continue
                image = convert_frame_to_image(frame)
                image = rotate_frame_horizontal_to_hough_line(image, get_median_hough_line(image))
                # TODO maybe make recognize_words as a parameter so can use different methods to recognize words
                return recognize_words(image)
            except Empty:
                continue
            finally:
                await asyncio.sleep(0)


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


def create_recognize_word_from_recorder_task(recognize_sound_func):
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


if __name__ == '__main__':
    import logging
    from .speech import recognize
    from .keybord_listener import listener

    logging.basicConfig(level=logging.INFO)

    listener.start()
    loop = asyncio.get_event_loop()


    async def main():
        while True:
            words = await recognize_words_from_user_image()
            print(words)


    loop.run_until_complete(create_recognize_word_from_recorder_task(recognize))
