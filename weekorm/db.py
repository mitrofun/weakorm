import sqlite3

SETTINGS = {
    'db_name': '',
    'connection': '',
}


def set_db_name(db_name):
    SETTINGS['db_name'] = db_name
    SETTINGS['connection'] = sqlite3.connect(db_name)


def get_cursor():
    if not SETTINGS.get('connection'):
        SETTINGS['connection'] = sqlite3.connect(SETTINGS['db_name'])
    cursor = SETTINGS['connection'].cursor()
    return cursor


def db_commit():
    SETTINGS['connection'].commit()


def execute_sql(cursor, sql):
    try:
        cursor.execute(sql)
    except Exception as e:
        print('error')
        print(sql)
        raise e


class DataBase:

    def __init__(self, name):
        self.db_name = name
        self.connection = sqlite3.connect(name)
        self.cursor = self.connection.cursor()
        self._save_settings()

    def _save_settings(self):
        SETTINGS['connection'] = self.connection
        SETTINGS['db_name'] = self.db_name

    def __del__(self):
        self.connection.close()
