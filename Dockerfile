FROM python:3.8-slim-buster

WORKDIR /app

COPY chat_moder/ /app

ENV VIRUS_TOTAL_APIKEY=""
ENV TELEGRAM_BOT_TOKEN=""
ENV TELEGRAM_CHAT_ID=""

COPY poetry.lock pyproject.toml /app/
RUN pip install -U setuptools && pip install --no-cache-dir poetry && poetry install --no-dev

CMD ["poetry", "run", "python", "-m", "chat_moder"]