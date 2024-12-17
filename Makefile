.PHONY: *

venv-activate:
	pyenv local 3.11
	poetry env use 3.11
	poetry shell

install:
	poetry install

serving-build:
	docker build --no-cache \
	--build-arg MODEL_NAME="mobilenet_v3_large" \
	--tag "pytorch-serve" \
	-f ./model/Dockerfile .

serving-start:
	docker run -p 8080:8080 -it --rm pytorch-serve:latest

app-start:
	poetry run streamlit run app/main.py