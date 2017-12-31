import asyncio
from queue import Empty
from .camera import ImageCapture
from .image import convert_frame_to_image
from .keybord_listener import pressed_keys
from .tesseract import recognize_words

trigger_key = 'k'


async def recognize_words_from_user_image():
    """Recognize words from image that captured by user intent

    :return: list of recognized words
    """
    cap = ImageCapture()
    with cap:
        while True:
            try:
                pressed_key = pressed_keys.get(block=False)
                if pressed_key.__dict__.get('char') != trigger_key:
                    continue
                frame = cap.capture()
                image = convert_frame_to_image(frame)
                return recognize_words(image)
            except Empty:
                continue
            finally:
                await asyncio.sleep(1)


if __name__ == '__main__':
    from .keybord_listener import listener
    listener.start()
    loop = asyncio.get_event_loop()
    async def main():
        while True:
            frame = await recognize_words_from_user_image()
            print(frame)
    loop.run_until_complete(main())
