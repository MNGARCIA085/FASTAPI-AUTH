from typing import Any, Generator

import pytest,sys,os
from fastapi import FastAPI
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# crear la base de datos si no existe ya
from sqlalchemy import create_engine
from sqlalchemy_utils import database_exists, create_database

# settings
from config import settings


sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))) 
#this is to include backend dir in sys.path so that we can import from db,main.py

# por modularidad defino ciertas fixtures en otro archivo
#from .fixtures import add_user, add_group, add_groups_user


from databases.config import Base, get_db




#from auth.routes import router


def start_application():
    app = FastAPI()
    #app.include_router(router)
    return app


# testing database

SQLALCHEMY_DATABASE_URL = settings.DB_URL_TEST
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})


if not database_exists(engine.url):
    create_database(engine.url)


SessionTesting = sessionmaker(autocommit=False, autoflush=False, bind=engine)



@pytest.fixture(scope="function")
def app() -> Generator[FastAPI, Any, None]:
    """
    Create a fresh database on each test case.
    """
    Base.metadata.create_all(engine)  # Create the tables.
    _app = start_application()
    yield _app
    Base.metadata.drop_all(engine)


@pytest.fixture(scope="function")
def db_session(app: FastAPI) -> Generator[SessionTesting, Any, None]:
    connection = engine.connect()
    transaction = connection.begin()
    session = SessionTesting(bind=connection)
    yield session  # use the session in tests.
    session.close()
    transaction.rollback()
    connection.close()


@pytest.fixture(scope="function")
def client(
    app: FastAPI, db_session: SessionTesting
) -> Generator[TestClient, Any, None]:
    """
    Create a new FastAPI TestClient that uses the `db_session` fixture to override
    the `get_db` dependency that is injected into routes.
    """

    def _get_test_db():
        try:
            yield db_session
        finally:
            pass

    app.dependency_overrides[get_db] = _get_test_db
    with TestClient(app) as client:
        yield client




