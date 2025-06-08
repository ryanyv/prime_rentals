# Deployment Guide

## Heroku

1. Create Heroku app and add Heroku Postgres.
2. Set `DJANGO_SETTINGS_MODULE=primerentals.settings.prod`.
3. Push code and run migrations.

## Docker

Build and run using docker-compose:

```bash
docker-compose build
docker-compose up
```
