FROM pytorch/torchserve AS serving_base
USER $USERNAME
EXPOSE 8080 8081 

ARG MODEL_NAME

RUN apt-get update && apt-get -y install git wget

WORKDIR /model

COPY ./model/config.properties /model
COPY ./model/index_to_name.json /model
COPY ./model/download.py /model
COPY ./model/$MODEL_NAME/model.py /model

RUN python download.py --model_name $MODEL_NAME

RUN mkdir model_store

# NOTE: archiving a torchvision model as a scripted model won't work with torchserve, but can be done explicitly with c++
# Set SERIALIZED_FILE to the *.pth file we just downloaded in the step above
RUN SERIALIZED_FILE=$(ls | grep pth); torch-model-archiver --model-name fasterrcnn --version 1.0 --model-file \
./model.py --serialized-file $SERIALIZED_FILE \
--extra-files ./index_to_name.json --export-path model_store --handler object_detector

FROM serving_base AS serving_rest_api
CMD ["torchserve", "--start", "--disable-token-auth", "--ncs", "--model-store model_store", "--models fasterrcnn.mar"]

FROM serving_base as serving_grpc
# Should manage these with poetry, but will need to downgrade to python 3.9
EXPOSE 7070 7071
RUN pip install grpcio protobuf grpcio-tools googleapis-common-protos
ADD ./grpc_serving /model/grpc_serving

CMD ["torchserve", "--start", "--disable-token-auth", "--enable-model-api", "--model-store", "models"]