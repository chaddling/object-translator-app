FROM python:3.11.10
USER $USERNAME
EXPOSE 8501

ENV POETRY_HOME="/usr/local" \
POETRY_CACHE_DIR="/var/cache/pypoetry"

RUN apt-get update && apt-get -y install curl libgl1

RUN curl -sSL https://install.python-poetry.org | python3 -

WORKDIR /app

COPY ./app/* /app/

COPY ./poetry.lock ./pyproject.toml /app/

RUN poetry install --no-root

CMD ["poetry", "run", "streamlit", "run", "main.py"]

