# alembic/env.py

import sys
import os
from logging.config import fileConfig

from sqlalchemy import engine_from_config, pool
from alembic import context

# --------------------------------------------------------------------
# Add the project root directory to sys.path so that `app.*` imports work.
# --------------------------------------------------------------------
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

# --------------------------------------------------------------------
# Now we can import settings and Base from our application
# --------------------------------------------------------------------
from app.settings import settings
from app.database import Base

# --------------------------------------------------------------------
# Access the Alembic Config object, which provides access to the
# values within the .ini file in use.
# --------------------------------------------------------------------
config = context.config

# --------------------------------------------------------------------
# Override the sqlalchemy.url in alembic.ini with our DATABASE_URL from .env
# --------------------------------------------------------------------
config.set_main_option("sqlalchemy.url", settings.DATABASE_URL)

# --------------------------------------------------------------------
# Interpret the config file for Python logging.
# This line sets up loggers basically.
# --------------------------------------------------------------------
fileConfig(config.config_file_name)

# --------------------------------------------------------------------
# Tell Alembic where our model’s MetaData object is.
# This is used during `autogenerate` to compare the models to the database.
# --------------------------------------------------------------------
target_metadata = Base.metadata


def run_migrations_offline():
    """
    Run migrations in 'offline' mode.

    In this mode, we configure the context with just a URL
    and not an Engine, and then we emit the SQL statements without
    executing them against a live database.
    """
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online():
    """
    Run migrations in 'online' mode.

    In this mode, we create an Engine and associate a connection 
    with the context. The migrations then run against that connection.
    """
    connectable = engine_from_config(
        config.get_section(config.config_ini_section),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
        )

        with context.begin_transaction():
            context.run_migrations()


# --------------------------------------------------------------------
# Determine whether to run in "offline" or "online" mode,
# and invoke the appropriate function.
# --------------------------------------------------------------------
if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
