# GRPC generated code
The `*.proto` files are taken from the `torcheserve` [repository](https://github.com/pytorch/serve/tree/master/frontend/server/src/main/resources/proto).

Before generating the stub code, clone the `torchserve` repo:
```
git clone --recurse-submodules https://github.com/pytorch/serve

```

(In the code below it's cloned to `$HOME/Desktop`). After installing dependencies, run:
```
python -m grpc_tools.protoc -I $HOME/Desktop/serve/third_party/google/rpc --proto_path=grpc_serving/ --python_out=grpc_serving --grpc_python_out=grpc_serving grpc_serving/inference.proto grpc_serving/management.proto
 5117  python -m grpc_tools.protoc -I /Users/chad.gu/Desktop/serve/third_party/google/rpc --proto_path=. --python_out=. --grpc_python_out=. grpc_serving/inference.proto grpc_serving/management.proto
 ```
Doing it this way ensures the generated code have the correct import structure for the client. This solution was provided by [this Stack Overflow answer](https://stackoverflow.com/questions/62818183/protobuf-grpc-relative-import-path-discrepancy-in-python/76946302#76946302).
