WeakORM
===
[![Build Status](https://travis-ci.org/mitrofun/weakorm.svg?branch=master)](https://travis-ci.org/mitrofun/weakorm) [![Scrutinizer Code Quality](https://scrutinizer-ci.com/g/mitrofun/weakorm/badges/quality-score.png?b=master)](https://scrutinizer-ci.com/g/mitrofun/weakorm/?branch=master) 

Simple ORM for sqlite.

Installation
====
```bash
pip3 install git+https://github.com/mitrofun/weakorm
```
Use
====
An example of using work with ORM can be found in the file `example.py`

Create database
---
To create a database, run
```python
from weekorm.db import DataBase
db = DataBase('example.sqlite')
```    
Creating database models
---
Create a class inherited from Model
```python
from weekorm import model

class User(model.Model):
    name = model.CharField(max_length=20)
    email = model.CharField(max_length=40, unique=True)
    is_admin = model.BooleanField(default=False)
```
The following types of fields exist in ORM
* **CharField** - Text field, max_length parameters-maximum field size, default 255.The default value ".
* **IntegerField** - Numeric integer field, default value 0
* **FloatField** - Numeric floating-point field field, default 0.0
* **BooleanField** - Boolean field, default False
* **DateTimeField** - Field with date and time.Example of use.
```python
from weekorm import model
from datetime import datetime
  
class Article(model.Model):
    title = model.CharField(max_length=100)
    ....
    created = model.DateTimeField(default=datetime.now())
```
* **ForeignKey** - Field with a foreign key.Example of use.
```python
from weekorm import model
  
class User(model.Model):
    name = model.CharField(max_length=20)
    email = model.CharField(max_length=40, unique=True)
    birthday = model.DateTimeField()

    def __str__(self):
        return self.name

class Stuff(model.Model):
    user = model.ForeignKey(User)
    position = model.CharField(max_length=40)

    def __str__(self):
        return f'{self.position} - {self.user.name}'
```
Saving data to database
---
```python
user = User(
    name='Mik',
    email='mik@gmail.com',
    birthday=datetime(year=1983, month=12, day=6)
)
user.save()
staff = Stuff(user=user, position='Tester')
staff.save()
```
Testing
===
Local
---
To develop and test locally, install the dependencies
```bash
pip3 install -r requirements/qa.txt
```
Running tests
```bash
pytest
```
Docker
---
You don't need to install dependencies locally to run tests in Docker.Just run the command
```bash
make docker-build && make docker-test
```

Requirements
=====
- python 3.6+

Contributors
=====
- [mitri4](https://github.com/mitrofun)

License
=====
weakorm is released under the MIT License. See the LICENSE file for more details.
