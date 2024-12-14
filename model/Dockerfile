FROM pytorch/torchserve
USER $USERNAME
EXPOSE 8080 8081 8082

RUN apt-get update && apt-get -y install git wget

WORKDIR /model

COPY ./model/config.properties /model
COPY ./model/mobilenet_v3.py /model

RUN mkdir model_store

# Only getting this for index_to_name.json, is this even the correct one for mobilenet?
RUN git clone https://github.com/pytorch/serve.git

RUN wget https://download.pytorch.org/models/fasterrcnn_mobilenet_v3_large_fpn-fb6a3cc7.pth

# NOTE: archiving a torchvision model as a scripted model won't work with torchserve, but can be done explicitly with c++
RUN torch-model-archiver --model-name fasterrcnn --version 1.0 --model-file \
./mobilenet_v3.py --serialized-file fasterrcnn_mobilenet_v3_large_fpn-fb6a3cc7.pth \
--extra-files ./serve/examples/object_detector/fast-rcnn/index_to_name.json --export-path model_store --handler object_detector

CMD ["torchserve", "--start", "--disable-token-auth", "--ncs", "--model-store model_store", "--models fasterrcnn.mar"]