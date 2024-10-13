# PyFApi 
Python FastAPI MongoDB CRUD Application end-to-end example

## Overview

This project is a web application built with [FastAPI](https://fastapi.tiangolo.com/)
and [MongoDB](https://www.mongodb.com/).
It provides a RESTful API for managing users and integrates Docker for containerization. The application is designed
following best practices for a clean architecture, making it easy to maintain and extend.
It is a simple CRUD application that allows to create, read, update, and delete.

Also, this project use pydantic, motor, beanie, and docker.

## Technologies

- **[FastAPI](https://fastapi.tiangolo.com/)**: A modern, fast (high-performance) web framework for building APIs with
  Python 3.6+ based on standard Python type hints.
- **[MongoDB](https://www.mongodb.com/)**: A NoSQL database for storing user data.
- **[Uvicorn](https://www.uvicorn.org/)**: Uvicorn is an ASGI web server implementation for Python.
- **[Pydantic](https://pydantic-docs.helpmanual.io/)**: Pydantic is the most widely used data validation library for
  Python.
- **[Motor](https://motor.readthedocs.io/en/stable/)**: Motor presents a coroutine-based API for non-blocking access to
  MongoDB from Tornado or asyncio.
- **[Beanie](https://beanie-odm.dev/)**: Beanie - is an asynchronous Python object-document mapper (ODM) for MongoDB.
  Data models are based on Pydantic.
- **[Docker](https://www.docker.com/)**: Docker is a set of platform as a service products that use OS-level
  virtualization to deliver software in packages called containers.

## Setup and Installation

### Prerequisites

- Python 3.10+
- Docker
- Docker Compose
- MongoDB
- Git
- FastAPI
- Pydantic
- Motor
- Beanie
- Uvicorn

### Build and Run

#### Uvicorn (development mode)

- Clone the repository

```bash
git clone https://github.com/cevheri/pyfapi.git
```

- Change the directory

```bash
cd pyfapi
```

- create a virtual environment

```bash
python -m venv venv
```

- Activate the virtual environment

```bash
source venv/bin/activate
```

- Install the dependencies

```bash
pip install -r requirements.txt
```

- Create a .env file in the root directory and add the following environment variables

```bash
cp .env.default .env.dev
cp .env.default .env.prod
```

- Run the application on local machine (development mode)

```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000 --env-file .env.dev
```

#### python (development mode)

```bash
python main-dev.py
```

#### Docker (development mode)

* docker-compose.yaml file has three services: app, mongo, and mongo-express.

```bash
docker-compose up --build
```

### Access the application

- Open your browser and go to root url http://localhost:8000 to access the FastAPI application.
- Open your browser and go to http://localhost:8000/api/v1/docs to access the Swagger UI.
- Open your browser and go to http://localhost:8081 to access the MongoDB Express.

## Folder Structure

```plaintext
.
├── app
│   ├── api
│   ├── config
│   ├── entity
│   ├── repository
│   ├── service
│   ├── security
│   ├── utils
│   ├── main.py
├── tests

```



## Conclusion
This FastAPI MongoDB application is structured to provide a robust and scalable API solution. By leveraging Docker and CI/CD practices, the application can be easily deployed and maintained.

Feel free to contribute to this project by submitting issues or pull requests!

## References
- [FastAPI](https://fastapi.tiangolo.com/)
- [FastAPI & MongoDB - the full guide](https://github.com/fastapi/fastapi/discussions/9074)
- [Build a Cocktail API with Beanie and MongoDB](https://www.mongodb.com/developer/languages/python/beanie-odm-fastapi-cocktails//)
- [Pydantic](https://docs.pydantic.dev/dev/)
- [Motor](https://motor.readthedocs.io/en/stable/tutorial-asyncio.html)
- [Beanie Tutorial](https://beanie-odm.dev/getting-started/)
- 

