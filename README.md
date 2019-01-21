# NLP Backend

## API
See the swagger documentation of the api
```
http://127.0.0.1:3002/api/1/
```

## Frameworks
* Spacy
* Google Lang Detect
* Apache Tika
* Flask
* Vader


## Authors
* Sebastian Erhardt

## Environment variables

Environment variables can be passed through docker compose script located in endorse-elk repository.

```
ELASTIC_SERACH_HOST=XXX
ELASTIC_SERACH_USERNAME=XXX
ELASTIC_SERACH_PASSWORD=XXX
CREATE_ADMIN=TRUE
ADMIN_PASSWORD=XXXX
```

## Credentials

[Go to credentials](./CREDENTIALS.md)

## Run with docker compose
In order to start the project using the docker configuration, please refer to the README file located
in the repository endorse-elk.