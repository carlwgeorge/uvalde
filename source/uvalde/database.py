import pathlib

import appdirs
import peewee


# Creating this with None defers the initialization, which is necessary for
# pytest monkeypatching to work correctly.
db = peewee.SqliteDatabase(None)


class BaseModel(peewee.Model):
    class Meta:
        database = db


class NVR(BaseModel):
    label = peewee.TextField(unique=True)


class Artifact(BaseModel):
    nvr = peewee.ForeignKeyField(NVR, backref='artifacts')
    path = peewee.TextField(unique=True)


def load_db():
    """Load database from sqlite file."""

    db_dir = pathlib.Path(appdirs.user_data_dir('uvalde'))
    if not db_dir.is_dir():
        db_dir.mkdir(parents=True)

    db_file = db_dir / 'rpms.sqlite'
    db.init(str(db_file))

    return db
