import logging
import websockets

# TODO put these in separate setting file
HOST = '127.0.0.1'
PORT = 4413


# TODO may be consider support for multiple WebSocket connections.
def create_word_sender(in_queue):
    async def word_sender(websocket, path):
        while True:
            word = await in_queue.get()
            logging.debug('Send word through websocket: %s' % word)
            await websocket.send(word)

    return word_sender


def create_word_sender_server(in_queue, host=HOST, port=PORT):
    word_sender = create_word_sender(in_queue)
    return websockets.serve(word_sender, host, port)
