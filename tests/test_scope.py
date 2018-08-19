import os

from tests.conftest import DB_NAME
from weekorm import model


class TestDataBase:

    def test_create_db(self, db):
        assert os.path.exists(DB_NAME)

    def test_crud_model(self, db):
        class City(model.Model):
            name = model.CharField()
            capital = model.BooleanField(default=False)

        city = City(name='Moscow', capital=False)
        city.save()
        assert len(City.query().all()) == 1
        _city = City.query().first()
        _city.capital = True
        _city.save()
        assert City.query().filter(capital=False).all() == []
        city = City.query().filter(capital=True).first()
        city.delete()
        assert len(City.query().all()) == 0

    def test_related_data(self, db):
        class Country(model.Model):
            name = model.CharField()

            def __str__(self):
                return f'Country: {self.name}'

        class Language(model.Model):
            name = model.CharField()
            country = model.ForeignKey(Country)

            def __str__(self):
                return f'Language: {self.name}'

        country = Country(name='Russia').save()
        Language(name='Russian', country=country).save()
        language = Language.query().first()
        assert language.country.name == 'Russia'
