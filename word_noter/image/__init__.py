import cv2
import numpy as np
from PIL import Image


def convert_frame_to_image(frame):
    """Convert frame to PIL image object

    :param frame: array of color data of the image
    :return: PIL image object
    """
    return Image.fromarray(frame)


def get_hough_lines(frame):
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    edges = cv2.Canny(gray, 50, 150, apertureSize=3)
    return cv2.HoughLines(edges, 1, np.pi / 180, 200)


def get_median_hough_line(frame):
    """Get a hough line that with median theta of all hough lines of the image

    :param frame:
    :return:
    """
    lines = get_hough_lines(frame)
    if lines is None:
        return None
    lines = lines.reshape((-1, 2))
    median_index = np.argsort(lines, axis=0)[len(lines) // 2][1]
    return lines[median_index]


def rotate_frame_horizontal_to_hough_line(frame, line):
    if line is None:
        return frame
    _, theta = line
    rows, cols = frame.shape[:2]
    degree = np.rad2deg(theta) % 90
    M = cv2.getRotationMatrix2D((cols / 2, rows / 2), degree, 1)
    return cv2.warpAffine(frame, M, (cols, rows))


if __name__ == '__main__':
    # import time
    # from .camera import ImageCapture
    #
    # cap = ImageCapture()
    # with cap:
    #     time.sleep(5)
    #     frame = cap.capture()
    # image = convert_frame_to_image(frame)
    img = cv2.imread('test.png')
    line = get_median_hough_line(img)
    # rho, theta = line
    # a = np.cos(theta)
    # b = np.sin(theta)
    # x0 = a * rho
    # y0 = b * rho
    # x1 = int(x0 + 1000 * (-b))
    # y1 = int(y0 + 1000 * (a))
    # x2 = int(x0 - 1000 * (-b))
    # y2 = int(y0 - 1000 * (a))
    #
    # cv2.line(img, (x1, y1), (x2, y2), (0, 0, 255), 2)

    cv2.imwrite('test_out.jpg', rotate_frame_horizontal_to_hough_line(img, line))
