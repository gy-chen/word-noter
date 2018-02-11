import asyncio
from queue import Empty
from word_noter.image.camera import ImageCapture
from word_noter.image import convert_frame_to_image, rotate_frame_horizontal_to_hough_line, get_median_hough_line
from word_noter.keybord_listener import pressed_keys
from word_noter.image.gcloud import recognize_words

# TODO put this setting in separate file
trigger_key = 'k'
captured_images = asyncio.Queue()
recognized_words = asyncio.Queue()


async def keep_capture_image_from_user(captured_image_out_queue=captured_images, pressed_key_queue=pressed_keys):
    with ImageCapture() as cap:
        while True:
            try:
                frame = cap.capture()
                pressed_key = pressed_key_queue.get(block=False)
                if pressed_key.__dict__.get('char') != trigger_key:
                    continue
                await captured_image_out_queue.put(frame)
            except Empty:
                pass
            finally:
                await asyncio.sleep(0)


async def keep_recognize_words_from_image(image_in_queue=captured_images, recognized_word_out_queue=recognized_words,
                                          recognize_words=recognize_words):
    """Recognize words from image that captured by user intent

    :return: list of recognized words
    """
    while True:
        frame = await image_in_queue.get()
        median_hough_line = get_median_hough_line(frame)
        if median_hough_line is not None:
            frame = rotate_frame_horizontal_to_hough_line(frame, median_hough_line)
        image = convert_frame_to_image(frame)
        await recognized_word_out_queue.put(recognize_words(image))


def create_main_task():
    return asyncio.gather(
        keep_capture_image_from_user(),
        keep_recognize_words_from_image()
    )


if __name__ == '__main__':
    import logging
    from word_noter.keybord_listener import listener

    logging.basicConfig(level=logging.INFO)

    listener.start()
    loop = asyncio.get_event_loop()


    async def print_recognized_words():
        while True:
            words = await recognized_words.get()
            print(words)


    loop.run_until_complete(asyncio.gather(
        create_main_task(),
        print_recognized_words())
    )
