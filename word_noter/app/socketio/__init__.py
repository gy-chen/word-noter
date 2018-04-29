def create_socketio_app():
    """A app that receive image from and send recognized words through SocketIO

    :return:
    """
    from aiohttp import web
    from word_noter.image.socketio import sio
    app = web.Application()
    sio.attach(app)
    return app


app = create_socketio_app()
