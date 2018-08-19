import os
import sys

import pytest

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

sys.path.insert(0, ROOT_DIR)
sys.path.insert(0, os.path.join(ROOT_DIR, 'weakorm'))

DB_NAME = 'test.db'


def pytest_sessionfinish(session, exitstatus):
    """ whole test run finishes. """
    if os.path.exists(os.path.join(ROOT_DIR, DB_NAME)):
        os.remove(os.path.join(ROOT_DIR, DB_NAME))


@pytest.fixture
def db():
    from weekorm.db import DataBase
    name_db = DB_NAME
    base = DataBase(name_db)
    return base
