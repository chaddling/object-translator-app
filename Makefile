.PHONY: venv-activate
venv-activate:
	pyenv local 3.11
	poetry env use 3.11
	poetry shell

.PHONY: install
install:
	poetry install

.PHONY: serving-build
serving-build:
	docker build --tag "pytorch-serve" -f ./model/Dockerfile .

.PHONY: serving-start
serving-start:
	docker run -p 8080:8080 -it --rm pytorch-serve:latest