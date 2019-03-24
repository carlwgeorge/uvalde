import pathlib

import appdirs
import peewee


def get_db_file():
    """Generate path for database file."""

    db_dir = pathlib.Path(appdirs.user_data_dir('uvalde'))
    if not db_dir.is_dir():
        db_dir.mkdir(parents=True)
    return db_dir / 'rpms.sqlite'


db = peewee.SqliteDatabase(get_db_file())


class BaseModel(peewee.Model):
    class Meta:
        database = db


class NVR(BaseModel):
    label = peewee.TextField(unique=True)


class Artifact(BaseModel):
    nvr = peewee.ForeignKeyField(NVR, backref='artifacts')
    path = peewee.TextField(unique=True)
