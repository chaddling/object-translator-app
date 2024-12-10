.PHONY: venv-activate
venv-activate:
	pyenv local 3.11
	poetry env use 3.11
	poetry shell