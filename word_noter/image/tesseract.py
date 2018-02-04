import re
import pyocr

word_pattern = re.compile(r'([a-z]+)', re.IGNORECASE)

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
    return word_pattern.findall(recognized_text)


if __name__ == '__main__':
    from PIL import Image

    image = Image.open('test.png')
    r1 = recognize_words(image)
