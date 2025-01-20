# user_audit_no_data_loss


## Docker
To run this app in docker, you will need docker.

- Docker https://docs.docker.com/engine/install/
- Docker compose


### To run the user audit:
```bash
    docker compose up --build fast-api
```

it will connect to http://0.0.0.0:80


### To run tests(pytest)

```bash
    docker-compose run --rm pytest-fast-api && docker-compose down
```

### NOTE: if you run this command it will also  drop the fast-api container.

It will auto run them and close them when it finishes it, also output the stdout

