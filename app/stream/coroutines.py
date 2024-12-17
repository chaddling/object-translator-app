import aiohttp
import asyncio
import cv2 as cv

from stream.wrapper import WrappedVideoStream

URL = "http://localhost:8080/predictions/fasterrcnn"


async def get_prediction(image: cv.typing.MatLike):
    _, encoded = cv.imencode(".jpg", image)

    async with aiohttp.ClientSession() as client:
        res = await client.post(
            url=URL, data=encoded.tostring(), headers={"content-type": "image/jpeg"}
        )
        return await res.text()


async def display_one_frame(stream: WrappedVideoStream, container):
    image = stream.read()
    container.image(image, channels="RGB")


async def do_streaming(stream: WrappedVideoStream, container):
    image = stream.read()
    prediction_task = asyncio.create_task(get_prediction(image))

    while not prediction_task.done():
        display_task = asyncio.create_task(display_one_frame(stream, container))
        await display_task

    print(prediction_task.result())
