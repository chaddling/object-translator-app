import grpc
import logging

from . import inference_pb2, inference_pb2_grpc, management_pb2, management_pb2_grpc

MODEL_NAME = "fasterrcnn"
METADATA = (("protocol", "gRPC"),)


def register(model_name=MODEL_NAME, metadata=METADATA):
    marfile = f"./{model_name}.mar"

    logging.info(f"Registered marfile: {marfile}\n")
    params = {
        "url": marfile,
        "initial_workers": 1,
        "synchronous": True,
        "model_name": model_name,
    }
    try:
        with grpc.insecure_channel("localhost:7071") as channel:
            stub = management_pb2_grpc.ManagementAPIsServiceStub(channel)
            response = stub.RegisterModel(
                management_pb2.RegisterModelRequest(**params), metadata=metadata
            )
            logging.info(f"Model {model_name} registered successfully")
    except grpc.RpcError as e:
        logging.error(e)
        exit(1)


async def infer(data, model_name=MODEL_NAME, metadata=METADATA):
    input_data = {"data": data}
    async with grpc.aio.insecure_channel("localhost:7070") as channel:
        stub = inference_pb2_grpc.InferenceAPIsServiceStub(channel)
        response = await stub.Predictions(
            inference_pb2.PredictionsRequest(model_name=model_name, input=input_data),
            metadata=metadata,
        )

    try:
        prediction = response.prediction.decode("utf-8")
        return prediction
    except grpc.RpcError as e:
        logging.error(e)
        exit(1)
