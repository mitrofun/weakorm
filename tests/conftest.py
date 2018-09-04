import os
import sys

import pytest

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

sys.path.insert(0, ROOT_DIR)
sys.path.insert(0, os.path.join(ROOT_DIR, 'weakorm'))

DB_NAME = 'test.db'

from weekorm import model  # noqa


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


@pytest.fixture
def model_user(db):
    class User(model.Model):
            first_name = model.CharField()
            last_name = model.CharField()
            is_staff = model.BooleanField(default=False)
    return User


@pytest.fixture
def model_city(db):
    class City(model.Model):
            name = model.CharField()
            capital = model.BooleanField(default=False)

    return City


@pytest.fixture
def model_country(db):
    class Country(model.Model):
        name = model.CharField()

        def __str__(self):
            return f'Country: {self.name}'
    return Country


@pytest.fixture
def model_language(db, model_country):
    class Language(model.Model):
        name = model.CharField()
        country = model.ForeignKey(model_country)

        def __str__(self):
            return f'Language: {self.name}'

    return Language
