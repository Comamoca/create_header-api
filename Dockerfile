FROM python:3.10.5-slim-buster 

ENV PYTHONUNBUFFERED=1

WORKDIR /app

# ホストからコピー
COPY pyproject.toml .

RUN apt-get update \
    && apt-get install --no-install-recommends -y curl git build-essential

RUN pip install poetry

RUN poetry config virtualenvs.create false \
    # ふつうにvenvにインストールする
    && poetry install
    # && rm pyproject.toml
COPY ./src ./src

CMD ["uvicorn", "src.server:app", "--host", "0.0.0.0", "--port", "8000" ]
