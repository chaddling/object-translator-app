import asyncio
import time
import streamlit as st

from stream.wrapper import WrappedVideoStream
from stream.coroutines import get_prediction, async_get_prediction

stream = WrappedVideoStream.open(0)

frame = st.empty()
text = st.empty()


async def async_foo():
    image = stream.read()
    frame.image(image, channels="RGB")
    s = time.perf_counter()
    res = await async_get_prediction(image)

    elapsed = time.perf_counter() - s

    print(elapsed)
    return res

def foo():
    image = stream.read()
    frame.image(image, channels="RGB")
    s = time.perf_counter()
    res = get_prediction(image)

    elapsed = time.perf_counter() - s

    print(elapsed)
    print(res)
    return res

async def async_main():
    for i in range(1000000):
        task = asyncio.create_task(async_foo())
        await task

        print(task.result())

def main():
    for i in range(10000000):
        foo()

if __name__ == "__main__":
    asyncio.run(async_main())
    #main()