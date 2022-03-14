# bank

use this examples on your .env file
```
DB_ENGINE=djongo
DB_NAME=bank-db
DB_USER=root
DB_PASS=example
DB_HOST=bank-db
DB_PORT=27017
TRANSACTION_HOST=bank-api:8000
BROKER_HOST=rabbitmq
BROKER_USER=guest
BROKER_PASS=guest
BROKER_PORT=5672
QUEUE=events_queue
ROUTING_KEY=events
CELERY_BROKER_URL=amqp://rabbitmq:5672
SECRET_KEY=django-insecure-aph)+&tb0vh$c+hq9kvlo&)@7ax_!)4i*0w)^ssof0k6jdu&cp
```

### Up all container using docker compose
```
make up-all
```

### Up all container using docker compose
```
make logs
```


### Cash out Queue
```
Queue chash_out in virtual host dev
```

### Cash in Queue
```
Queue chash_in in virtual host dev
```

### Queue payload example
```
Headers: payload_encoding=string
Properties: content-type=application/json
{"headers": {"Authorization": "Bearer JWT TOKEN"}, "body": {"user": "Patreze", "account": "1234-3", "value": "10000.0", "currency": "BRL"}}
```