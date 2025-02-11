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
  pull_request:
    types: [ opened, synchronize, reopened, ready_for_review ]
    branches: [main]

permissions:
  contents: read
  pull-requests: write 

jobs:
  lint:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout code
        uses: actions/checkout@v2

      - name: Setup Python
        uses: actions/setup-python@v5
        with:
          python-version-file: 'pyproject.toml'
          cache: 'poetry'

      - name: Install dependencies
        run: poetry install

      - name: Lint Alembic Migrations
        uses: remedyproduct/alembic-squawk-action@v0.0.1
        with:
          migrations_path: 'migrations'
          alembic_config: 'alembic.ini'
          runner: 'poetry'
```
