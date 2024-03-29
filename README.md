Apply pep8 to all files:
```
pdm run pep8
```
Show the recomendations of pylint:
```
pdm pylint
```

Execute test coverage
```
pdm run test
pdm run test_cov
pdm run test_cov_html
```

Add package
```
pdm add package-name
```

Run dev containers
```
docker compose --profile dev up
```

Execute specific test with E2E env
```
pdm run test_e2e
```
or
```
APP_ENV=e2e pytest src/core/category/tests/e2e/categories/test_e2e_post.py
```
or
```
pytest -s --env=e2e src/core/category/tests/e2e/categories/test_e2e_post.py
```


Access test database:
```
$ docker compose exec db_test bash
$ mysql -uroot -proot
$ show databases;
```


## Libraries:
Colorama - Colored output