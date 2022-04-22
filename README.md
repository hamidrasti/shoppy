# Shoppy

A dockerized Django demo shop

## Run the project

1. clone the project
2. create a `.env` file in the root of project directory
3. config `.env` variables based on `.env.example`

### with docker

4. make sure you have `docker` and `docker-compose` installed:
    ```shell
    docker --version
    docker-compose --version
    ```
5. run the project using `docker-compose`:
    ```shell
    docker-compose up
    ```

### without docker

4. make sure you already have `postgres` installed, then run the following in a virtual environment:
    ```shell
    pip install -r requirements.txt
    python manage.py migrate
    python manage.py runserver
    ```

## Tests

### with docker

```shell
docker-compose run --rm app sh -c "pytest"
```

or

```shell
docker-compose run --rm app sh -c "python manage.py test"
```

### without docker

```shell
pytest
```

or

```shell
python manage.py test
```

## Test Coverage

Run this commands to get coverage report:

### with docker

```shell
docker-compose run --rm app sh -c "coverage run --source='.' manage.py test"
docker-compose run --rm app sh -c "coverage report"
```

### without docker

```shell
coverage run --source='.' manage.py test
coverage report
```

## Routes

To see api documentation:

- redoc: `GET /api/schema/redoc/`
- swagger: `GET /api/schema/swagger/`

To download the api schema and use it with apps like `postman`:

- schema download url: `GET /api/schema/`

To see all url routes, run:

```shell
docker-compose run --rm app sh -c "python manage.py show_urls"
```

## Load Data

To create two users for testing, run:

```shell
docker-compose run --rm app sh -c "python manage.py loaddata users"
```

now we have two user with this info:

- superadmin
    ```json
    {
      "password": "pass123456",
      "username": "superadmin",
      "email": "superadmin@shoppy.com"
    }
    ```

- superadmin
    ```json
    {
      "password": "pass123456",
      "username": "admin",
      "email": "admin@shoppy.com"
    }
    ```
