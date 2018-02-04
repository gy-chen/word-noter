import io
from google.cloud import vision
from google.cloud.vision import types
from ..text import find_all_words


def recognize_words(image):
    image_content = io.BytesIO()
    image.save(image_content, format='png')
    client = vision.ImageAnnotatorClient()
    response = client.annotate_image({
        'image': types.Image(content=image_content.getvalue()),
        'features': [{'type': vision.enums.Feature.Type.DOCUMENT_TEXT_DETECTION}]
    })
    full_recognized_text = response.full_text_annotation.text
    return find_all_words(full_recognized_text)


if __name__ == '__main__':
    from PIL import Image

    image = Image.open('test.png')
    r1 = recognize_words(image)
