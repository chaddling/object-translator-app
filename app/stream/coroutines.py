import aiohttp
import requests
import time
import cv2 as cv

URL = "http://localhost:8080/predictions/densenet161"


async def async_get_prediction(image: cv.typing.MatLike):
    _, encoded = cv.imencode(".jpg", image)

    async with aiohttp.ClientSession() as client:
        res = await client.post(
            url=URL,
            data=encoded.tostring(),
            headers={"content-type": "image/jpeg"}
        )
        return await res.text()
    
def get_prediction(image: cv.typing.MatLike):
    s = time.perf_counter()

    _, encoded = cv.imencode(".jpg", image)
    elapsed = time.perf_counter() - s

    print(elapsed)

    res = requests.post(
        URL,
        encoded.tostring(),
        headers={"content-type": "image/jpeg"}
    )
    return res.text
