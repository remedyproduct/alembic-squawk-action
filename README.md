# Alembic Migration Lint with Squawk
Lint Alembic Postgres migrations and report violations as a comment in a GitHub Pull Request.

- It identifies changed migration files, generates the corresponding SQL, and runs [Squawk](https://github.com/sbdchd/squawk) to check for any issues.
- Based on [squawk-action](https://github.com/sbdchd/squawk-action)

## Inputs

- `migrations_path`: Path to the folder containing your 'versions' subfolder. (required)
- `alembic_config`: Path to alembic.ini. (optional, default: "alembic.ini")
- `runner`: Command prefix for running Python commands. Use "poetry" for Poetry, "pipenv" for Pipenv, "uv" for uv, or leave empty (or set to "none") to use the system interpreter. (optional, default: "poetry")

## Outputs

- `changed`: Indicates whether any new migrations were found and processed.

## Usage Example (uv)

```yaml
name: Lint Alembic Migrations

on:
  pull_request:
    types: [ opened, synchronize, reopened, ready_for_review ]
    branches: [main]

permissions:
  contents: read
  pull-requests: write

env:
  UV_PYTHON: "3.13"

jobs:
  lint:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout code
        uses: actions/checkout@v6

      - name: Set up Python and uv
        uses: astral-sh/setup-uv@v7
        with:
          python-version: '3.13'
          enable-cache: true

      - name: Install dependencies
        run: uv sync

      - name: Lint Alembic Migrations
        uses: remedyproduct/alembic-squawk-action@v0.0.3
        with:
          migrations_path: 'migrations'
          alembic_config: 'alembic.ini'
          runner: 'uv'
```

If you prefer Poetry or Pipenv, set `runner` to `poetry` or `pipenv` instead. Leaving `runner` empty uses the system interpreter.
