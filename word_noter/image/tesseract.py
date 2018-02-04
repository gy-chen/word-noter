import pyocr
from .text import find_all_words

tool = None
if pyocr.get_available_tools():
    tool = pyocr.get_available_tools()[0]


def recognize_words(image):
    """Recognize words from the image

    :param image: PIL image object
    :return: list of regonized words
    """
    if tool is None:
        raise ValueError("Please install tesseract")
    recognized_text = tool.image_to_string(image)
    return find_all_words(recognized_text)


if __name__ == '__main__':
    from PIL import Image

    image = Image.open('test.png')
    r1 = recognize_words(image)
