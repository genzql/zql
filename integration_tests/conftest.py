import sqlite3

import pytest


@pytest.fixture
def session():
    connection = sqlite3.connect(":memory:")
    db_session = connection.cursor()
    yield db_session
    connection.close()


@pytest.fixture
def setup_db(session):
    session.execute(
        """CREATE TABLE apples
                          (owner text, num_apples int)"""
    )
    session.execute('INSERT INTO apples VALUES ("Vinesh", 5)')
    session.connection.commit()
