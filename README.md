# shoppy

A Django demo shop

## Tests

### Run

```shell
docker-compose run --rm app sh -c "pytest"
docker-compose run --rm app sh -c "python manage.py test"
```

### Coverage

Run this commands to get coverage report:

```shell
docker-compose run --rm app sh -c "coverage run --source='.' manage.py test"
docker-compose run --rm app sh -c "coverage report"
```
