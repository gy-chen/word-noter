"""Provides features through socketio

Provides:
  - to let user upload image, and received recognized words through socketio

"""
import io
import socketio
from PIL import Image
from word_noter.image.gcloud import recognize_words

sio = socketio.Server()


@sio.on('image')
def image(sid, data):
    """Recognize word from the image received by channel image.

    This method will send recognized words through channel word.

    :param sid:
    :param data:
    """
    image = Image.open(io.BytesIO(data))
    words = recognize_words(image)
    for word in words:
        sio.emit('word', word)


if __name__ == '__main__':
    import eventlet

    app = socketio.Middleware(sio)

    eventlet.wsgi.server(eventlet.listen(('', 4413)), app)
