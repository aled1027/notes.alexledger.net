---
date: 2023-03-05
tags:
    - python
    - fly.io
    - django
title: Django and Fly
---

# Django and Fly

The Django fly.io [starting tutorial](https://www.fly.io/docs/django/getting-started/) is a great place to start when deploying a Django app to fly.

[This](https://learndjango.com/tutorials/django-hello-world-flyio-deployment) starter guide is similar and also great. It has [this](https://learndjango.com/tutorials/deploy-django-postgresql-flyio) follow up.

This post has four sections: Troubleshooting, Branches, Extensions, and Reference to facilitate deploying on fly.

## Troubleshooting

Some common errors encountered when setting up django.
### Troubleshoot 1: Make sure the port of the server matches the fly port

In your fly.toml file, make sure that the internal port matches what the Django process is listening to in the dockerfile.

Most of the time, django apps use `8000`, so you'd have the following in your app.toml file:

```toml
[[services]]
  http_checks = []
  internal_port = 8000
  processes = ["app"]
  protocol = "tcp"
  script_checks = []
  [services.concurrency]
    hard_limit = 25
    soft_limit = 20
    type = "connections"

  [[services.ports]]
    force_https = true
    handlers = ["http"]
    port = 80

  [[services.ports]]
    handlers = ["tls", "http"]
    port = 443

  [[services.tcp_checks]]
    grace_period = "1s"
    interval = "15s"
    restart_limit = 0
    timeout = "2s"
```

## Branching off the Starter Guide

Like any tutorial, there are some pieces that may not apply to your use case. The sections below go over some of the cases I've run into and approaches to them.

### Branch 1: Using Poetry instead of requirements.txt

There are a few approaches to this. The one I've used the most is installing dependencies with poetry instead of pip. So inside of `Dockerfile`,
change the line:
```
# OLD:
RUN pip install requirements.txt

# NEW:
RUN pip install poetry
RUN poetry config virtualenvs.create false \
  && poetry install
```

## Extending the Starter Guide

In addition to adjusting the starter guide, you may need to extend it to support more sophisticated behavior. 

### Extension 1: Migrations

Migrations can be done with the fly deploy configuration ([docs](https://fly.io/docs/reference/configuration/)). Add the following to your fly.toml file:

```
[deploy]
  release_command = "python manage.py migrate"
```

### Extension 2: Structured Logging

I like [structlog](https://www.structlog.org/en/stable/index.html), so for Django, check out [django-structlog](https://django-structlog.readthedocs.io/en/latest/). 

I have notes on setting it up for fastapi [here](https://notes.alexledger.net/site/posts/16).

### Extension 3: Log Management

The common pattern in fly, once you're up and running and need robust logs and alerts, is to use the [fly-log-shipper](https://github.com/superfly/fly-log-shipper).

The quick-start guide in the repo is pretty good. I found that datadog was good enough for me: cheap enough, easy to use, and easy to set up.

This [blog post](https://github.com/superfly/fly-log-shipper#quick-start) is also useful.

## Reference

### Reference 1: A sample Dockerfile

```
FROM python:3.10

WORKDIR /usr/src/app

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

COPY . .

# install dependencies
RUN pip install poetry
RUN poetry config virtualenvs.create false \
  && poetry install

EXPOSE 8000

CMD ["poetry", "run", "python", "-m", "uvicorn", "config.asgi:application", "--host", "0.0.0.0", "--port", "8000"]

# Or use this if you're just getting set up.
# This will run the server on port 8000
CMD ["poetry", "run", "python", "manage.py", "runserver"]
```

### Reference 2: Sample asgi.py

```python
"""
It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.1/howto/deployment/asgi/
"""

import os

from django.core.asgi import get_asgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "myapp.settings")

application = get_asgi_application()
```
