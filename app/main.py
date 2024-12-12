import asyncio
import streamlit as st

from stream.wrapper import WrappedVideoStream
from stream.coroutines import do_streaming


stream = WrappedVideoStream.open(0)
container = st.empty() # What's the type hint?

async def main():
    while True:
        await do_streaming(stream, container)

if __name__ == "__main__":
    asyncio.run(main())
