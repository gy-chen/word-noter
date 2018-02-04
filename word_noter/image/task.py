import asyncio
from queue import Empty
from word_noter.image.camera import ImageCapture
from word_noter.image import convert_frame_to_image, rotate_frame_horizontal_to_hough_line, get_median_hough_line
from word_noter.keybord_listener import pressed_keys
from word_noter.image.gcloud import recognize_words

trigger_key = 'k'


async def recognize_words_from_user_image(recognize_words=recognize_words):
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
                median_hough_line = get_median_hough_line(frame)
                if median_hough_line is not None:
                    frame = rotate_frame_horizontal_to_hough_line(frame, median_hough_line)
                image = convert_frame_to_image(frame)
                return recognize_words(image)
            except Empty:
                continue
            finally:
                await asyncio.sleep(0)


if __name__ == '__main__':
    import logging
    from word_noter.keybord_listener import listener

    logging.basicConfig(level=logging.INFO)

    listener.start()
    loop = asyncio.get_event_loop()


    async def main():
        while True:
            words = await recognize_words_from_user_image()
            print(words)


    loop.run_until_complete(main())
