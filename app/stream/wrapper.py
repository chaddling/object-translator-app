import cv2 as cv
import logging

from typing import Self


class WrappedVideoStream:
    """
    Wrapper class of the OpenCV VideoCapture object.
    """

    @classmethod
    def open(cls, device_id: int = 0) -> Self:
        cls.stream = cv.VideoCapture(device_id)
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
