import pathlib

import appdirs
import peewee


def load_db():
    """Load database from sqlite file."""

    db_dir = pathlib.Path(appdirs.user_data_dir('uvalde'))
    if not db_dir.is_dir():
        db_dir.mkdir(parents=True)
    db_file = db_dir / 'rpms.sqlite'
    return peewee.SqliteDatabase(db_file)


class BaseModel(peewee.Model):
    class Meta:
        database = load_db()


class NVR(BaseModel):
    label = peewee.TextField(unique=True)


class Artifact(BaseModel):
    nvr = peewee.ForeignKeyField(NVR, backref='artifacts')
    path = peewee.TextField(unique=True)
