import asyncio
import streamlit as st

from stream.wrapper import WrappedVideoStream, Prediction
from stream.coroutines import do_streaming


stream = WrappedVideoStream.open(src=0)
container = st.empty()  # What's the type hint?
prediction = Prediction()


async def main():
    while True:
        await do_streaming(stream, container, prediction)


if __name__ == "__main__":
    asyncio.run(main())
