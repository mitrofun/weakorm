import os

import pytest

from tests.conftest import DB_NAME
from weekorm import exception


class TestDataBase:

    def test_create_db(self, db):
        assert os.path.exists(DB_NAME)

    def test_crud_model(self, db, model_city):

        city = model_city(name='Moscow', capital=False)
        city.save()
        assert len(model_city.query().all()) == 1
        _city = model_city.query().first()
        _city.capital = True
        _city.save()
        assert model_city.query().filter(capital=False).all() == []
        # get first element
        city = model_city.get()
        assert city.capital is True
        # update
        city.name = 'New Name'
        city.save()
        assert len(model_city.query().filter(name='New Name').all()) == 1
        # delete
        city.delete()
        assert len(model_city.query().all()) == 0

    def test_update_in_query(self, db, model_user):
        model_user(first_name='Ivan', last_name='Ivanov', is_staff=False).save()
        model_user(first_name='Ivan', last_name='Petrov', is_staff=False).save()
        model_user(first_name='Nikolai', last_name='Smirnoff', is_staff=False).save()
        assert len(model_user.query().filter(is_staff=False).all()) == 3
        model_user.query().filter(first_name='Ivan').update(is_staff=True)
        assert len(model_user.query().filter(is_staff=False).all()) == 1

    def test_related_data(self, db, model_country, model_language):
        country = model_country(name='Russia').save()
        model_language(name='Russian', country=country).save()
        language = model_language.query().first()
        assert language.country.name == 'Russia'


class TestModelException:

    def test_exception_field_name_in_query(self, db, model_country):
        with pytest.raises(exception.ModelFieldNameException):
            model_country.query().filter(nam='Russia').first()

    def test_exception_field_name_in_instance(self, db, model_country):
        with pytest.raises(exception.ModelFieldNameException):
            new_country = model_country(nam=1)
            new_country.save()

    def test_exception_type_value(self, db, model_country):
        with pytest.raises(exception.ModelFieldTypeException):
            new_country = model_country(name=1)
            new_country.save()

    def test_exception_type_value_foreign_key(self, db, model_language, model_country):
        with pytest.raises(exception.ModelFieldTypeException):
            new_language = model_language(name='New', country='New')
            new_language.save()
        new_country = model_country(name='Italy').save()
        model_language(name='Italian', country=new_country).save()
        assert len(model_language.query().filter(name='Italian').all()) == 1
