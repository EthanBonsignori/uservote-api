FROM python:3.12

WORKDIR /code

ENV MONGO_URI=mongodb://localhost:27017 \
    MONGO_URL=mongodb://localhost \
    MONGO_DB=UserVote \
    MONGO_USER=root \
    MONGO_PASSWORD=root \
    MAX_CONNECTIONS_COUNT=100 \
    MIN_CONNECTIONS_COUNT=0

COPY ./requirements.txt /code/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

COPY . /code

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
