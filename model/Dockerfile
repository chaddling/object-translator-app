FROM pytorch/torchserve
USER $USERNAME
EXPOSE 8080 8081 8082

RUN apt-get update && apt-get -y install git wget

WORKDIR /model

COPY ./model/config.properties /model
COPY ./model/index_to_name.json /model
COPY ./model/download_serialized.py /model
COPY ./model/mobilenet_v3_large/model.py /model

RUN python download.py --model_name mobilenet_v3_large

RUN mkdir model_store

# NOTE: archiving a torchvision model as a scripted model won't work with torchserve, but can be done explicitly with c++
RUN torch-model-archiver --model-name fasterrcnn --version 1.0 --model-file \
./model.py --serialized-file fasterrcnn_mobilenet_v3_large_fpn-fb6a3cc7.pth \
--extra-files ./index_to_name.json --export-path model_store --handler object_detector

CMD ["torchserve", "--start", "--disable-token-auth", "--ncs", "--model-store model_store", "--models fasterrcnn.mar"]