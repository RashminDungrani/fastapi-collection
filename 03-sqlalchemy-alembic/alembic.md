# Alembic - A Migration Tool

## Common Questions and Answers

### 1. What is Alembic?

Alembic is a database migrations tool written by the author of SQLAlchemy. It provides functionality to emit ALTER statements to a database for changing table structures and other constructs. Additionally, Alembic allows the creation of "migration scripts" that can upgrade or downgrade a target database to a new version in a sequential manner.

## Official Documentation

- [Alembic Documentation](https://alembic.sqlalchemy.org/en/latest/)
- [Alembic on PyPI](https://pypi.org/project/alembic/)

## Useful Commands

### 1. Initialize Migration

Initialize Alembic migrations in your project:
```shell
alembic init alembic
```

### 2. Update `alembic.ini` Configuration

Open `alembic.ini` and modify the `file_template` line as follows:
```python
file_template = %%(year)d-%%(month).2d-%%(day).2d-%%(hour).2d-%%(minute).2d-%%(second).2d_%%(slug)s
```

### 3. Create Initial Migration

Generate the initial migration script:
```shell
alembic revision --autogenerate -m "init"
```

### 4. Review and Apply Migration

Review the generated migration file and apply the migration to the database:
```shell
alembic upgrade head
```

### 5. View Migration History

View the migration history:
```shell
alembic history
```

### 6. Downgrade or Undo Migration

Downgrade the database to the previous migration or undo the last migration:
```shell
alembic downgrade -1
```

### 7. Stamp Database State

Indicate that the current state of the database represents the application of all migrations:
```shell
alembic stamp head
```
