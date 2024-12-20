.PHONY: *

venv-activate:
	pyenv local 3.11
	poetry env use 3.11
	poetry shell

install:
	poetry install

serving-build-rest-api:
	docker build --no-cache \
	--build-arg MODEL_NAME="mobilenet_v3_large" \
	--tag "pytorch-serve" \
	--target serving_rest_api \
	-f ./model/Dockerfile .

serving-build-grpc:
	docker build --no-cache \
	--build-arg MODEL_NAME="mobilenet_v3_large" \
	--tag "pytorch-serve" \
	--target serving_grpc \
	-f ./model/Dockerfile .

serving-start:
	docker run \
	-p 8080:8080 \
	-p 8081:8081 \
	-p 7070:7070 \
	-p 7071:7071 \
	-it --rm pytorch-serve:latest

app-start:
	poetry run streamlit run app/main.py