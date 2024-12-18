import ast
import aiohttp
import asyncio
import cv2 as cv

from stream.wrapper import WrappedVideoStream, Prediction

URL = "http://localhost:8080/predictions/fasterrcnn"


async def get_prediction(image: cv.typing.MatLike):
    _, encoded = cv.imencode(".jpg", image)

    async with aiohttp.ClientSession() as client:
        res = await client.post(
            url=URL, data=encoded.tostring(), headers={"content-type": "image/jpeg"}
        )
        return await res.text()


async def display_one_frame(
    stream: WrappedVideoStream, container, prediction: Prediction
):
    image = stream.read()

    if prediction.has_prediction:
        label, bounding_box, score = prediction.get()

        xmin, ymin, xmax, ymax = [int(x) for x in bounding_box]
        cv.rectangle(
            image, pt1=(xmin, ymin), pt2=(xmax, ymax), color=(0, 255, 0), thickness=5
        )
        cv.putText(
            image,
            text=f"{label}: {round(score, 2)}",
            org=(xmin, ymin - 20),
            fontFace=0,
            fontScale=2.0,
            color=(0, 255, 0),
            thickness=5,
        )

    container.image(image, channels="RGB")


async def do_streaming(stream: WrappedVideoStream, container, prediction: Prediction):
    image = stream.read()
    prediction_task = asyncio.create_task(get_prediction(image))

    while not prediction_task.done():
        display_task = asyncio.create_task(
            display_one_frame(stream, container, prediction)
        )
        await display_task

    results = ast.literal_eval(prediction_task.result())
    if results:
        label, bounding_box = next(iter(results[0].items()))
        score = results[0]["score"]
        prediction.set(label=label, bounding_box=bounding_box, score=score)
