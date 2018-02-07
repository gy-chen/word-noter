import asyncio
import websockets
from queue import Empty

# TODO put these in separate setting file
HOST = '127.0.0.1'
PORT = 4413


def create_word_sender(in_queue):
    async def word_sender(websocket):
        while True:
            try:
                word = in_queue.get(block=False)
                await websocket.send(word)
            except Empty:
                pass
            finally:
                await asyncio.sleep()

    return word_sender


def create_word_sender_server(in_queue, host=HOST, port=PORT):
    word_sender = create_word_sender(in_queue)
    return websockets.serve(word_sender, host, port)
