# Alembic Migration Lint with Squawk

This GitHub Action leverages Squawk to lint Alembic migrations. It identifies changed migration files, generates the corresponding SQL, and runs Squawk to check for any issues.

## Inputs

- `migrations_path`: Path to the folder containing your 'versions' subfolder. (required)
- `alembic_config`: Path to alembic.ini. (optional, default: "alembic.ini")
- `runner`: Command prefix for running Python commands. Use "poetry" for Poetry, "pipenv" for Pipenv, "uv" for uv, or leave empty (or set to "none") to use the system interpreter. (optional, default: "poetry")

## Outputs

- `changed`: Indicates whether any new migrations were found and processed.

## Usage Example

Here is an example of how to use this action in a GitHub workflow:

```yaml
name: Lint Alembic Migrations

on:
  push:
    paths:
      - 'migrations/versions/*.py'

jobs:
  lint:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout code
        uses: actions/checkout@v2

      - name: Set up Python
        uses: actions/setup-python@v2
        with:
          python-version: '3.12'

      - name: Install dependencies
        run: |
          python -m pip install --upgrade pip
          pip install poetry
          poetry install

      - name: Lint Alembic Migrations
        uses: remedyproduct/alembic-squawk-action@v1
        with:
          migrations_path: 'migrations'
          alembic_config: 'alembic.ini'
          runner: 'poetry'
```
