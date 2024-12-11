import requests
import cv2 as cv
import streamlit as st

from app.stream.wrapper import WrappedVideoStream

URL = "http://localhost:8080/predictions/densenet161"


def main():
    stream = WrappedVideoStream.open(0)

    frame = st.empty()
    text = st.empty()
    stop_button = st.button("Stop")

    while stream.is_opened() and not stop_button:
        image = stream.read()
        frame.image(image, channels="RGB")

        _, encoded = cv.imencode(".jpg", image)
        img_string = encoded.tostring()

        res = requests.post(URL, data=img_string, headers={'content-type': 'image/jpeg'})
        text.write(res.text)
    
        if stop_button:
            break

    stream.release()

if __name__ == "__main__":
    main()