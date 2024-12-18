import grpc
import logging

from . import inference_pb2, inference_pb2_grpc, management_pb2, management_pb2_grpc

MODEL_NAME = "fasterrcnn"
METADATA = (("protocol", "gRPC"),)


def get_inference_stub():
    channel = grpc.insecure_channel("localhost:7070")
    stub = inference_pb2_grpc.InferenceAPIsServiceStub(channel)
    return stub


def get_management_stub():
    channel = grpc.insecure_channel("localhost:7071")
    stub = management_pb2_grpc.ManagementAPIsServiceStub(channel)
    return stub


def register(stub, model_name, metadata):
    marfile = f"./{MODEL_NAME}.mar"

    logging.info(f"Registered marfile: {marfile}\n")
    params = {
        "url": marfile,
        "initial_workers": 1,
        "synchronous": True,
        "model_name": model_name,
    }
    try:
        response = stub.RegisterModel(
            management_pb2.RegisterModelRequest(**params), metadata=metadata
        )
        logging.info(f"Model {model_name} registered successfully")
    except grpc.RpcError as e:
        logging.error(e)
        exit(1)


def infer(stub, model_name, model_input, metadata):
    with open(model_input, "rb") as f:
        data = f.read()

    input_data = {"data": data}
    response = stub.Predictions(
        inference_pb2.PredictionsRequest(model_name=model_name, input=input_data),
        metadata=metadata,
    )

    try:
        prediction = response.prediction.decode("utf-8")
        logging.info(prediction)
    except grpc.RpcError as e:
        logging.error(e)
        exit(1)
