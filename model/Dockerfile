FROM pytorch/torchserve
USER $USERNAME
EXPOSE 8080 8081 8082

RUN apt-get update && apt-get -y install git wget

WORKDIR /model

COPY ./model/config.properties /model

RUN mkdir model_store

RUN git clone https://github.com/pytorch/serve.git

RUN wget https://download.pytorch.org/models/fasterrcnn_resnet50_fpn_coco-258fb6c6.pth

# NOTE: archiving a torchvision model as a scripted model won't work with torchserve, but can be done explicitly with c++
RUN torch-model-archiver --model-name fasterrcnn --version 1.0 --model-file \
./serve/examples/object_detector/fast-rcnn/model.py --serialized-file fasterrcnn_resnet50_fpn_coco-258fb6c6.pth \
--extra-files ./serve/examples/object_detector/fast-rcnn/index_to_name.json --export-path model_store --handler object_detector

CMD ["torchserve", "--start", "--disable-token-auth", "--ncs", "--model-store model_store", "--models fasterrcnn.mar"]
