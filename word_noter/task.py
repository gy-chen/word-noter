import asyncio
from .websocket import create_word_sender_server
from .image.task import create_main_task, recognized_words


def create_recognize_from_image_task():
    """Create a task that keep recognizing words from image captured by user and send the words through WebSocket.

    :return:
    """
    recognize_words_task = create_main_task()
    server = create_word_sender_server(recognized_words)
    return asyncio.gather(recognize_words_task, server)


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(create_recognize_from_image_task())
