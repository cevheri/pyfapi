# PyFApi

Python FastAPI MongoDB CRUD Application end-to-end example

## Overview

This project is a web application built with [FastAPI](https://fastapi.tiangolo.com/)
and [MongoDB](https://www.mongodb.com/).
It provides a RESTful API for managing users and integrates Docker for containerization. The application is designed
following best practices for a clean architecture, making it easy to maintain and extend.
It is a simple CRUD application that allows to create, read, update, and delete.

Also, this project use pydantic, motor, beanie, and docker.

---

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
- **[Oauth2](https://fastapi.tiangolo.com/tutorial/security)**: OAuth2 with Password (and hashing), Bearer with JWT
  tokens.

---

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

---

### Before you begin

- change the environment values with your own values in the .env.dev and .env.prod files
- Find the change-me and replace it with your own values in source code

---

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
python3 -m venv venv
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

- Run the application production mode with python

```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000 --env-file .env.prod
```

#### python (development mode)

```bash
python3 main_dev.py
```

#### python (production mode)

```bash
python3 main_prod.py
```

#### Docker (development mode)

* docker-compose.yaml file has three services: app, mongo, and mongo-express.

```bash
docker-compose up --build
```

### Access the application

- Open your browser and go to root url [http://localhost:8000](http://localhost:8000) to access the FastAPI application.
- Open your browser and go to [http://localhost:8000/api/v1/docs](http://localhost:8000/api/v1/docs) to access the
  Swagger UI.
- Open your browser and go to [http://localhost:8081](http://localhost:8081) to access the MongoDB Express.

---

## Security

Security is a critical aspect of any application. This project uses OAuth2 with Password (and hashing), Bearer with JWT
tokens.

* Security settings are defined in the [app/security](app/security) directory.
* Security middleware is defined in the [app/middleware/security.py](app/middleware/security_middleware.py) file.

### Allowed endpoints

- if you want to allow the endpoint without authentication, you can add the endpoint to the env file like this:

```bash
SECURITY_ALLOWED_PATHS=/api/v1/public/products
```

---

## Folder Structure

| ...               | ...                           |
|-------------------|-------------------------------|
| -- app            | Main application directory    | 
| -- app/api        | API endpoints and routes      |
| -- app/config     | Configuration settings        |
| -- app/entity     | Database models               |
| -- app/repository | Data access layer             |
| -- app/service    | Business logic layer          |
| -- app/schema     | API models                    |
| -- app/security   | Security settings             |
| -- app/utils      | Utility functions             |
| -- app/main.py    | Main application file         |
| -- tests          | Test cases                    |
| -- .env.default   | Default environment variables |
| ...               | ...                           |

---

## Adding new features

This project use a clean architecture, separation of concerns, and single responsibility principles.
If you want to add a new feature, you need to follow the structure of the project.

For example, you need product management features. You can follow the steps below.

1. product_api.py: API endpoints and routes, request, and response models, and API logic. OpenAPI documentation, and
   Swagger UI.
2. product_service.py: Business logic layer
3. product_dto.py: API models for API endpoints
4. product_repository.py: Data access layer for database operations
5. product.py: Database models for MongoDB (Beanie ODM)

### Add new schema

- Create a new file in the [app/schema](app/schema) like **product_dto.py** (use the existing files as a
  reference [user_dto.py](app/schema/user_dto.py)) Classes: ProductDTO, ProductCreate, ProductUpdate

### Add a new API endpoint / Route

- Create a new file in the app/api directory like **product_api.py** (use the existing files as a
  reference [user_api.py](app/api/user_api.py))
- Edit the [app/api/__init__.py](app/api/__init__.py) file and add the new route

### Add new service

- Create a new file in the [app/service](app/service) like **product_service.py** (use the existing files as a
  reference [user_service.py](app/service/user_service.py)) Classes: ProductService

### Add new db-entity

This project use Beanie ODM for MongoDB. You can create a new entity for the database.

- Create a new file in the [app/entity](app/entity) like **product.py** (use the existing files as a
  reference [user.py](app/entity/user_entity.py)) Classes: Product
- Edit the [app/entity/__init__.py](app/entity/__init__.py) file and add the new entity
- Edit the [app/conf/env/db_config.py](app/conf/env/db_config.py) file and add the new entity **init_beanie()**
-

### Add new repository

- Create a new file in the [app/repository](app/repository) like **product_repository.py** (use the existing files as a
  reference [user_repository.py](app/repository/user_repository.py)) Classes: ProductRepository

---

## Run tests

Unit tests and integration tests are essential for ensuring the quality of the application. This project uses pytest for
testing.

- Folder structure

| ...              | ...                            |
|------------------|--------------------------------|
| test             | Test cases                     |
| tests/api        | API endpoints and routes tests |
| tests/service    | Business logic layer tests     | 
| tests/repository | Data access layer tests        |

- Run all tests

```bash
PYTHONPATH=. pytest
```

Sample result :

```bash
22 passed in 0.52s
```

---

## Conclusion

This FastAPI MongoDB application is structured to provide a robust and scalable API solution. By leveraging Docker and
CI/CD practices, the application can be easily deployed and maintained.

Feel free to contribute to this project by submitting issues or pull requests!

---

## References

- [FastAPI](https://fastapi.tiangolo.com/)
- [FastAPI & MongoDB - the full guide](https://github.com/fastapi/fastapi/discussions/9074)
- [Build a Cocktail API with Beanie and MongoDB](https://www.mongodb.com/developer/languages/python/beanie-odm-fastapi-cocktails//)
- [Pydantic](https://docs.pydantic.dev/dev/)
- [Motor](https://motor.readthedocs.io/en/stable/tutorial-asyncio.html)
- [Beanie Tutorial](https://beanie-odm.dev/getting-started/)
