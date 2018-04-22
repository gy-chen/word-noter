import asyncio
import logging
from queue import Empty
from word_noter.image.camera import ImageCapture
from word_noter.image import convert_frame_to_image, rotate_frame_horizontal_to_hough_line, get_median_hough_line

from word_noter.image import gcloud
from word_noter.keybord_listener import listener

captured_images = asyncio.Queue()
recognized_words = asyncio.Queue()


async def keep_capture_image_from_user(captured_image_out_queue, pressed_key_queue,
                                       trigger_key='k'):
    """Capture image when user press specific key

    :param captured_image_out_queue: queue to store captured images
    :param pressed_key_queue: queue to receive input key
    :param trigger_key: the key that user press to capture image
    """
    with ImageCapture() as cap:
        while True:
            try:
                frame = cap.capture()
                pressed_key = pressed_key_queue.get(block=False)
                if pressed_key.__dict__.get('char') != trigger_key:
                    continue
                logging.debug('Captured a frame')
                await captured_image_out_queue.put(frame)
            except Empty:
                pass
            finally:
                await asyncio.sleep(0)


async def keep_recognize_words_from_image(image_in_queue, recognized_word_out_queue,
                                          recognize_words=gcloud.recognize_words):
    """Recognize words from image

    :param image_in_queue: queue to stored images need to recognize
    :param recognized_word_out_queue: queue to store recognized words
    :param recognize_words: function that used to recognize words
    :return: list of recognized words
    """
    while True:
        frame = await image_in_queue.get()
        median_hough_line = get_median_hough_line(frame)
        if median_hough_line is not None:
            frame = rotate_frame_horizontal_to_hough_line(frame, median_hough_line)
        image = convert_frame_to_image(frame)
        logging.debug('Try to recognize words from captured image')
        for word in recognize_words(image):
            logging.debug('recognized web: %s' % word)
            await recognized_word_out_queue.put(word)


async def start_keyboard_listener():
    listener.start()


def create_main_task():
    from word_noter.keybord_listener import pressed_keys
    return asyncio.gather(
        start_keyboard_listener(),
        keep_capture_image_from_user(captured_images, pressed_keys),
        keep_recognize_words_from_image(captured_images, recognized_words)
    )


if __name__ == '__main__':
    import logging

    logging.basicConfig(level=logging.INFO)

    loop = asyncio.get_event_loop()


    async def print_recognized_words():
        while True:
            words = await recognized_words.get()
            print(words)


    loop.run_until_complete(asyncio.gather(
        create_main_task(),
        print_recognized_words())
    )
