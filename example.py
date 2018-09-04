from datetime import datetime

from weekorm import model
from weekorm.db import DataBase

db = DataBase('example.sqlite')


class User(model.Model):
    name = model.CharField(max_length=20)
    email = model.CharField(max_length=40, unique=True)
    birthday = model.DateTimeField()
    is_admin = model.BooleanField(default=False)

    def __str__(self):
        return self.name


class Staff(model.Model):
    user = model.ForeignKey(User)
    position = model.CharField(max_length=40)

    def __str__(self):
        return f'{self.position} - {self.user.name}'


user = User(
    name='Mik',
    email='mik@gmail.com',
    birthday=datetime(year=2000, month=1, day=1)
)
staff = Staff(user=user, position='Tester')

if User.query().filter(email=user.email).first():
    print('This user is already in the database')
else:
    print('Create user ans stuff')
    print(f'user: {user}')
    print(f'staff {staff}')
    user.save()
    staff.save()
