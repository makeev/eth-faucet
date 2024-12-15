# Faucet App

Application to send testnet tokens to users

Api endpoints:
- POST /api/faucet/fund - Fund a user with testnet tokens
- GET /api/faucet/stats - Get the faucet statistics for last 24hrs

Manage command to update transaction statuses:
```
docker-compose exec faucet python manage.py update_transaction_statuses
```

# DDD (Domain-Driven Design)

The application is divided into 4 layers: application, domain, infrastructure and user_interface.
More information about the DDD can be found [here](DDD.md)

# Install

Rename .env.sample to .env and update the values, then run the following command
```
docker-compose up --build
```