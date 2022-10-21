# Cryptos

## Run

```sh
bash run.sh
```

## Install

```sh
pip install -r requirements.txt
```

### For local development

```sh
pip install -r requirements-dev.txt
```

## Migrations

```sh
## Init (needed just the first time)
$ alembic init migrations
  Creating directory /Users/photopills/Projects/crypto/migrations ...  done
  Creating directory /Users/photopills/Projects/crypto/migrations/versions ...  done
  Generating /Users/photopills/Projects/crypto/migrations/script.py.mako ...  done
  Generating /Users/photopills/Projects/crypto/migrations/env.py ...  done
  Generating /Users/photopills/Projects/crypto/migrations/README ...  done
  File /Users/photopills/Projects/crypto/alembic.ini already exists, skipping
  Please edit configuration/connection/logging settings in '/Users/photopills/Projects/crypto/alembic.ini' before proceeding.

## Autogenerate migration
$ alembic revision --autogenerate -m "Added Cryptos table"
INFO  [alembic.runtime.migration] Context impl SQLiteImpl.
INFO  [alembic.runtime.migration] Will assume non-transactional DDL.
INFO  [alembic.autogenerate.compare] Detected added table 'cryptos'
  Generating /Users/photopills/Projects/crypto/migrations/versions/7ea49b504977_added_account_table.py ...  done

## Apply migrations to DB
$ alembic upgrade head
INFO  [alembic.runtime.migration] Context impl SQLiteImpl.
INFO  [alembic.runtime.migration] Will assume non-transactional DDL.
INFO  [alembic.runtime.migration] Running upgrade  -> d3bf16c13137, Added Cryptos table
```
