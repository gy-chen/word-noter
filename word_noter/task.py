import asyncio
from .websocket import create_word_sender_server


def create_recognize_from_image_task():
    """Create a task that keep recognizing words from image captured by user and send the words through WebSocket.

    :return:
    """
    from .image.task import create_main_task, recognized_words
    recognize_words_task = create_main_task(recognized_words)
    server = create_word_sender_server(recognized_words)
    return asyncio.gather(recognize_words_task, server)


def create_fake_words_task():
    """Generate a task that keep generating fake words and the words through WebSocket.

    This task is useful for testing.

    :return:
    """
    from .fake import generate_words, fake_words
    generate_words_task = generate_words(fake_words)
    server = create_word_sender_server(fake_words)
    return asyncio.gather(generate_words_task, server)


if __name__ == '__main__':
    import logging

    # TODO maybe put this to console script
    logging.basicConfig(level=logging.DEBUG)
    loop = asyncio.get_event_loop()
    loop.run_until_complete(create_fake_words_task())
