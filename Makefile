.PHONY: *

venv-activate:
	pyenv local 3.11
	poetry env use 3.11
	poetry shell

install:
	poetry install

serving-build:
	docker build --tag "pytorch-serve" -f ./model/Dockerfile .

serving-start:
	docker run -p 8080:8080 -it --rm pytorch-serve:latest