# Object detection app PoC

For learning computer vision systems in general, an app that detects objects(eventually, do instance segmentation instead) and translates the object names into different languages.

The model currently handles a video stream and returns the bounding box the primary object in the stream.

# Installation
## Building `torchserve` container
``` 
make serving-build
```
Is used to build the docker image. By default, the `mobilenet_v3_large` is used. Eager-mode pre-trained Pytorch models are defined in the `model` directory and can be expanded to add new backbone architectures to the object detection model. To use a different model, the image can be built with a `MODEL_NAME` arg:
```
make serving-build MODEL_NAME=resnet50
```

## Installing dependencies
Before installing the app dependencies via `make`, `pyenv` and `poetry` have to be installed on your system. Running:
```
make venv-activate
make install
```
will install the app's dependencies.

<b>NOTE:</b> the `Dockerfile` in the root directory packages the step above, but on MacOS the webcam will not work inside a container.

## Running the app locally
1. Bring up the `torchserve` container:
```
make serving-start
```
to bring up the model service at `http://localhost:8080`.

2. Start the app:
```
poetry run streamlit run app/main.py
```