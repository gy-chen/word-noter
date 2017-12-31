from queue import Queue
from pynput import keyboard

__ALL__ = ['listener', 'pressed_keys']

pressed_keys = Queue()


def on_press(key):
    """Listen to user's key press.
    """
    pressed_keys.put(key, block=False)


listener = keyboard.Listener(on_press=on_press)
