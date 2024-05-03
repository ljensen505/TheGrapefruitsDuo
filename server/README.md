# Backend for The Grapefruits Duo

This is the backend for thegrapefruitsduo.com and is deployed at api.thegrapefruitsduo.com. It is a FastAPI app that serves information about the chamber music, the group's members, and upcoming events. It allows authorized users to modify most information. Data is persisted with MariaDB.

The general flow of this program is as follows, starting from the database layer:

- `python-mysql` is used to interact with the MariaDB database. This happens in `app/db`
- `app/controllers` contains the business logic for the app and consumes the database layer. Each controller is responsible for a different part of the app, with one main controller `app/controllers/controller.py` which imports, instantiates, and uses the other controllers.
- `app/routes` contains the FastAPI routes that consume the single controller. This controller is instantiated in `app/controllers/__init__.py` and passed to the routes.

No formal api specification is provided, but the routes are documented with FastAPI's Swagger UI at `/docs`.

## Basic Usage

Use of [poetry](https://python-poetry.org/docs/) is required. Creating the virtual environment with poetry is easy and should be done in the main project directory. `.venv` should be alongside `pyproject.toml`.

To install dependencies (venv will be created automatically if it doesn't exist):

```bash
poetry install
```

The following steps require proper environment variables to be set. An example can be found in `.env.example`

To seed the mysql database:

```bash
poetry run seed
```

Automated tests can be run with:

```bash
poetry run pytest
```

To run the FastAPI app in development mode:

```bash
poetry run dev
```

### Deployment

This app is deployed on a Linode Ubuntu Server instance. NGINX is used as a reverse proxy and the app itself is managed by `systemd` and `uvicorn` as a service, and listens on port 6000. The app is served over HTTPS with a Let's Encrypt certificate.
