from datetime import datetime

from . import exception
from weekorm import db


class Field:
    """
    Base class for fields
    """
    field_type = ''
    default = ''
    is_foreign_key = False
    unique = False
    not_null = False
    python_type = str

    def field_sql(self, field_name):
        field_sql = f'"{field_name}" {self.field_type}'
        if self.unique:
            field_sql += ' UNIQUE'
        if self.not_null:
            field_sql += ' NOT NULL'
        return field_sql

    def to_python(self, value):
        if self.python_type == datetime:
            value = datetime.fromtimestamp(value)
            return value
        return self.python_type(value)


class CharField(Field):
    """
    Char field, default max length is 255 and default value is ''
    Python type is str
    """
    def __init__(self, max_length=255, default='', unique=False):
        self.field_type = f'varchar({max_length})'
        self.default = default
        self.max_length = max_length
        self.unique = unique
        self.python_type = str


class IntegerField(Field):
    """
    Integer field, default value is 0
    Python type is int
    """
    def __init__(self, default=0, unique=False):
        self.field_type = 'integer'
        self.default = default
        self.unique = unique
        self.python_type = int


class FloatField(Field):
    """
    Float field, default value is 0.0
    Python type is float
    """
    def __init__(self, default=0.0, unique=False):
        self.field_type = 'real'
        self.default = default
        self.unique = unique
        self.python_type = float


class BooleanField(Field):
    """
    Boolean field, default value is False.
    Python type is bool
    """
    def __init__(self, default=False, unique=False):
        self.field_type = 'integer'
        self.default = default
        self.unique = unique
        self.python_type = bool


class DateTimeField(Field):
    """
    Boolean field, default value is False
    Python type is datetime
    """
    def __init__(self, default=0.0, unique=False):
        self.field_type = 'real'
        self.default = default
        self.unique = unique
        self.python_type = datetime


class ForeignKey(Field):
    """
    Foreign field for other model
    """
    def __init__(self, model_class):
        self.field_type = 'foreignkey'
        self.is_foreign_key = True
        self.model_class = model_class
        self.python_type = int

    def field_sql(self, field_name):
        return f'"{field_name}" integer REFERENCES "{self.model_class.__name__.lower()}" ("id")'


class Model:

    def __init__(self, inst_id=0, **kwargs):
        self.table_name = self.__class__.__name__.lower()
        self.id = inst_id
        self.__class__.try_create_table()
        for name in self.field_names:
            field = getattr(self.__class__, name.replace("`", ""))
            setattr(self, name.replace("`", ""), field.default)
        for key, value in kwargs.items():
            # exception with field name
            if f"`{key}`" not in self.field_names + ["`id`"]:
                raise exception.ModelFieldNameException(
                    model_name=self.__class__.__name__,
                    field_name=key,
                )
            # exception with field type wrong for foreign_key
            if hasattr(self.__class__.__dict__[key], 'model_class') and \
                    not isinstance(value, self.__class__.__dict__[key].model_class):
                raise exception.ModelFieldTypeException(
                    model=self.__class__.__name__,
                    field_name=key,
                    field_type=self.__class__.__dict__[key].model_class.__name__,
                    value_type=type(value).__name__)
            # exception with field type wrong for other fields
            if not hasattr(self.__class__.__dict__[key], 'model_class') and\
                    not isinstance(value, self.__class__.__dict__[key].python_type):
                raise exception.ModelFieldTypeException(
                    model=self.__class__.__name__,
                    field_name=key,
                    field_type=self.__class__.__dict__[key].python_type.__name__,
                    value_type=type(value).__name__)
            setattr(self, key.replace("`", ""), value)

    def __str__(self):
        return f'{self.__class__.__name__}_{self.id}'

    def __repr__(self):
        return self.__str__()

    @property
    def field_names(self):
        names = []
        for name in dir(self.__class__):
            var = getattr(self.__class__, name.replace("`", ""))
            if isinstance(var, Field):
                names.append(f"`{name}`")
        return names

    @property
    def field_values(self):
        values = []
        for name in self.field_names:
            value = getattr(self, name.replace("`", ""))
            if isinstance(value, datetime):
                value = value.timestamp()
            if isinstance(value, Model):
                value = value.id
            if isinstance(value, str):
                value = value.replace("'", "''")
            values.append(f"'{value}'")
        return values

    def __insert(self):
        cursor = db.get_cursor()
        field_names_sql = ", ".join(self.field_names)
        field_values_sql = ", ".join(self.field_values)

        sql = f"insert into `{self.table_name}`({ field_names_sql}) values({field_values_sql})"
        db.execute_sql(cursor, sql)
        db.db_commit()

        sql = f"select id from `{self.table_name}` order by id desc;"
        db.execute_sql(cursor, sql)
        self.id = cursor.fetchone()[0]

    def __update(self):
        cursor = db.get_cursor()

        name_value = []

        for name, value in zip(self.field_names, self.field_values):
            name_value.append(f"{name}={value}")
        name_value_sql = ", ".join(name_value)

        sql = f"update `{self.table_name}` set {name_value_sql} where id = {self.id}"
        db.execute_sql(cursor, sql)
        db.db_commit()

    def save(self):
        if self.id:
            self.__update()
        else:
            self.__insert()
        return self

    def delete(self):
        cursor = db.get_cursor()
        sql = f"delete from `{self.table_name}` where id = {self.id}"
        db.execute_sql(cursor, sql)
        db.db_commit()

    @classmethod
    def try_create_table(cls):
        table_name = cls.__name__.lower()
        cursor = db.get_cursor()
        sql = f"select * from sqlite_master where type='table' AND name='{table_name}';"
        db.execute_sql(cursor, sql)
        if not cursor.fetchall():
            sql = f"drop table if exists `{table_name}`;"
            db.execute_sql(cursor, sql)

            fields_sql = ""
            for name in dir(cls):
                var = getattr(cls, name.replace("`", ""))
                if isinstance(var, Field):
                    field = var
                    field_sql = field.field_sql(name)
                    fields_sql += ", " + field_sql
            sql = f'create table `{table_name}` ("id" integer not null primary key {fields_sql});'
            db.execute_sql(cursor, sql)

            db.db_commit()

    @classmethod
    def query(cls):
        query = Query(cls)
        return query

    @classmethod
    def get(cls, **kwargs):
        query = Query(cls)
        return query.filter(**kwargs).first()


class Query:

    def __init__(self, model_class):
        model_class.try_create_table()
        self.model_class = model_class
        self.table_name = self.model_class.__name__
        self.where_sql = "1=1"

    def __str__(self):
        return f"{self.__class__.__name__}_{self.table_name,}_{self.query_sql}"

    def __repr__(self):
        return self.__str__()

    @property
    def field_names(self):
        names = []
        for name in dir(self.model_class):
            var = getattr(self.model_class, name.replace("`", ""))
            if isinstance(var, Field):
                names.append(f"`{name}`")
        return names

    @property
    def query_sql(self):
        sql = f"select * from `{self.table_name}` where {self.where_sql};"
        return sql

    def filter(self, operator="=", **kwargs):
        where_sql = self.where_sql
        for name, value in kwargs.items():
            if f"`{name}`" not in self.field_names + ["`id`"]:
                raise exception.ModelFieldNameException(
                    model_name=self.model_class.__name__,
                    field_name=name,
                )
            if isinstance(value, Model):
                value = value.id
            if isinstance(value, str):
                value = value.replace("'", "''")
            where_sql += f" and `{name}` {operator} '{value}'"
        query = self.__class__(self.model_class)
        query.where_sql = where_sql
        return query

    def _r2ob(self, item):
        value = ''
        inst_id = item[0]
        obj = self.model_class(inst_id=inst_id)
        for i in range(1, len(item)):
            name = self.field_names[i - 1]
            field = getattr(self.model_class, name.replace("`", ""))
            if not field.is_foreign_key:
                value = field.to_python(item[i])
            if field.is_foreign_key:
                if field.field_type == "foreignkey":
                    fid = item[i]
                    value = field.model_class.get(id=fid)
            setattr(obj, name.replace("`", ""), value)
        return obj

    def all(self):
        cursor = db.get_cursor()
        sql = self.query_sql
        db.execute_sql(cursor, sql)
        rows = cursor.fetchall()
        obs = []
        for item in rows:
            ob = self._r2ob(item)
            obs.append(ob)
        return obs

    def first(self):
        cursor = db.get_cursor()
        sql = self.query_sql
        db.execute_sql(cursor, sql)
        rows = cursor.fetchall()
        if not rows:
            return None
        r = rows[0]
        ob = self._r2ob(r)
        return ob

    def delete(self):
        cursor = db.get_cursor()
        sql = f"delete from `{self.table_name}` where {self.where_sql}"
        db.execute_sql(cursor, sql)
        db.db_commit()

    def update(self, **kwargs):
        cursor = db.get_cursor()
        update_sql = ''
        for name, value in kwargs.items():
            if f"`{name}`" not in self.field_names + ["`id`"]:
                raise exception.ModelFieldNameException(
                    model_name=self.model_class.__name__,
                    field_name=name,
                )
            if isinstance(value, Model):
                value = value.id
            if isinstance(value, str):
                value = value.replace("'", "''")
            update_sql += f"`{name}` = '{value}',"
        if update_sql:
            update_sql = update_sql[:-1]
        sql = f"update `{self.table_name}` set {update_sql} where {self.where_sql}"
        db.execute_sql(cursor, sql)
        db.db_commit()
