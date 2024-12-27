import asyncio
import streamlit as st

from stream.wrapper import WrappedVideoStream, Prediction, Translator
from stream.coroutines import do_streaming
from grpc_serving import cli

stream = WrappedVideoStream.open(src=0)
container = st.empty()  # What's the type hint?
prediction = Prediction()
translator = Translator(to_language="fr")

cli.register()


async def main():
    while True:
        await do_streaming(stream, container, prediction, translator)


if __name__ == "__main__":
    asyncio.run(main())
