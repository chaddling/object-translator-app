# NOTE Dockerfile doesn't really work when hosting from MacOS
# may abandon this
FROM python:3.11.10
USER $USERNAME
EXPOSE 8501

ENV POETRY_HOME="/usr/local" \
POETRY_CACHE_DIR="/var/cache/pypoetry"

RUN apt-get update && apt-get -y install curl libgl1

RUN curl -sSL https://install.python-poetry.org | python3 -

WORKDIR /app

COPY ./poetry.lock ./pyproject.toml /app/

RUN poetry install --no-root

COPY ./main.py /app/
ADD ./stream /app/stream

CMD ["poetry", "run", "streamlit", "run", "main.py"]
