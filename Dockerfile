FROM python:3.12.0

# RUN apt-get update \
#     && apt-get upgrade -y \
#     && apt-get install -y --no-install-recommends curl git build-essential python3-setuptools \
#     && apt-get autoremove -y

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN adduser --disabled-password --gecos '' appuser

RUN pip install --upgrade pip
RUN pip install poetry

COPY pyproject.toml poetry.lock ./
RUN poetry export --without-hashes --without dev -f requirements.txt -o requirements.txt && \
        chown appuser:appuser requirements.txt && \
        pip install -r requirements.txt


USER appuser
# COPY --chown=appuser:appuser start.sh /app/
# COPY --chown=appuser:appuser app /app

EXPOSE 8000
CMD ["uvicorn", "app.main:app", "--host=0.0.0.0", "--reload", "--port", "8000"]
# RUN chmod +x /app/start.sh
# ENTRYPOINT [ "/app/start.sh" ]