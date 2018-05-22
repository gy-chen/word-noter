"""Provides features through socketio

Provides:
  - to let user upload image, and receive recognized words through socketio

"""
import asyncio
import io
import socketio
from PIL import Image
from word_noter.image.gcloud import recognize_words

sio = socketio.AsyncServer()


class SocketIOImageRecognizer:
    """Receive image and send recognized words through SocketIO

    - Receive image from channel 'image'
    - Send recognized words through channel 'web'
    """

    def __init__(self, sio):
        self._sio = sio
        self._received_images = asyncio.Queue()
        self._setup_tasks()
        self._setup_sio()

    def _setup_tasks(self):
        loop = asyncio.get_event_loop()
        loop.create_task(self.recognize_job())

    def _setup_sio(self):
        self._sio.on('image', handler=self.receive_image)

    async def receive_image(self, sid, data):
        """Recognize web from the image received by channel image.

        This method will send recognized words through channel web.

        :param sid:
        :param data:
        """
        image = Image.open(io.BytesIO(data))
        await self._received_images.put(image)

    async def recognize_job(self):
        while True:
            image = await self._received_images.get()
            words = recognize_words(image)
            for word in words:
                await self._sio.emit('word', word)


socket_io_image_recognizer = SocketIOImageRecognizer(sio)

if __name__ == '__main__':
    from aiohttp import web

    app = web.Application()
    sio.attach(app)

    web.run_app(app, port=4413)
