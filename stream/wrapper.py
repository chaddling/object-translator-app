import cv2 as cv
import logging

from typing import Self


class WrappedVideoStream:
    """
    Wrapper class of the OpenCV VideoCapture object.
    """

    @classmethod
    def open(cls, src: int) -> Self:
        cls.stream = cv.VideoCapture(src)
        if not cls.is_opened():
            logging.error("Cannot open camera!")
        return cls

    @classmethod
    def is_opened(cls) -> bool:
        return cls.stream.isOpened()

    @classmethod
    def release(cls) -> None:
        cls.stream.release()
        cv.destroyAllWindows()

    @classmethod
    def read(cls):
        returned, frame = cls.stream.read()

        if not returned:
            logging.error("Stream cannot be read!")

        frame = cv.cvtColor(frame, cv.COLOR_BGR2RGB)
        return frame


class Prediction:
    """
    An object used to persist prediction results across frames.
    """

    def __init__(self):
        self.label = None
        self.bounding_box = None
        self.score = None
        self.has_prediction = False

    def set(self, label, bounding_box, score):
        self.label = label
        self.bounding_box = bounding_box
        self.score = score
        self.has_prediction = True

    def get(self):
        return self.label, self.bounding_box, self.score
