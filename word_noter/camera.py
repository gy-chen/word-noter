import cv2
from contextlib import AbstractContextManager


class ImageCapture(AbstractContextManager):
    def __init__(self):
        self._cap = None

    def open(self):
        self._cap = cv2.VideoCapture(0)

    def close(self):
        self._cap.release()
        self._cap = None

    def capture(self):
        if self._cap is None:
            raise ValueError("Please use with statement or open method to this instance before invoke this method")
        return self._cap.read()[1]

    def __enter__(self):
        self.open()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()
