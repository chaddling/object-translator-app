FROM pytorch/torchserve
USER $USERNAME
EXPOSE 8080 8081 8082

RUN apt-get update && apt-get -y install git wget openssl

WORKDIR /model

COPY ./model/config.properties /model

RUN mkdir model_store

RUN git clone https://github.com/pytorch/serve.git

RUN wget https://download.pytorch.org/models/densenet161-8d451a50.pth

RUN torch-model-archiver --model-name densenet161 --version 1.0 --model-file \
./serve/examples/image_classifier/densenet_161/model.py --serialized-file densenet161-8d451a50.pth \
--export-path model_store --extra-files ./serve/examples/image_classifier/index_to_name.json --handler image_classifier

CMD ["torchserve", "--start", "--disable-token-auth", "--ncs", "--model-store model_store", "--models densenet161.mar"]
