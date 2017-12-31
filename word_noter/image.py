from PIL import Image


def convert_frame_to_image(frame):
    """Convert frame to PIL image object

    :param frame: array of color data of the image
    :return: PIL image object
    """
    return Image.fromarray(frame)


if __name__ == '__main__':
    import time
    from .camera import ImageCapture

    cap = ImageCapture()
    with cap:
        time.sleep(5)
        frame = cap.capture()
    image = convert_frame_to_image(frame)
