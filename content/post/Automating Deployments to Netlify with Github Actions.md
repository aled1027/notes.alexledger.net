---
title: Automating Deployments to Netlify with Github Actions
date: 2023-01-01
---
# Automating Deployments to Netlify with Github Actions

I set up automated deployments to Netlify using Github Actions.

Here's the action:

```yaml
# This workflow will install Python dependencies, run tests, and lint.

name: Python Application

on:
  push:
    branches: ["main"]

permissions:
  contents: read

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Set up Python 3.10
        uses: actions/setup-python@v3
        with:
          python-version: "3.10"
      - name: Install Poetry
        uses: snok/install-poetry@v1
      - name: Install dependencies
        run: |
          python -m pip install --upgrade pip
          poetry install
      - name: Build and deploy
        run: |
          poetry run mkdocs build
          zip -r site.zip site/
          curl -H "Content-Type: application/zip" \
            -H "Authorization: Bearer ${{ secrets.NETLIFY_API_KEY }}" \
            --data-binary "@site.zip" \
            https://api.netlify.com/api/v1/sites/84c36d50-85d9-4cf6-8a9c-aee0b708ed69/deploys
```