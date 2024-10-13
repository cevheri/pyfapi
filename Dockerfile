# Python FastAPI Dockerfile
FROM python:3.10-slim

RUN apt-get update -qq \
    && apt-get install \
        -yqq --no-install-recommends \
        build-essential

RUN pip install --upgrade pip

WORKDIR /app

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY . .

EXPOSE 8000

# Set the environment variables
ENV ENV_FILE=.env.dev

#CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--env-file", "${ENV_FILE}"]
CMD ["sh", "-c", "uvicorn app.main:app --host 0.0.0.0 --port 8000 --env-file ${ENV_FILE}"]

# docker run --network="host" -e ENV_FILE=.env.dev -p 8000:8000 pyfapi:latest