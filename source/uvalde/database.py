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
    filename = peewee.TextField(unique=True)
    architecture = peewee.TextField()
    debug = peewee.BooleanField(default=False)


def load_db():
    """Load database from sqlite file."""

    db_dir = pathlib.Path(appdirs.user_data_dir('uvalde'))
    if not db_dir.is_dir():
        db_dir.mkdir(parents=True)

    old_db_files = [
        db_dir / 'rpms.sqlite',
    ]
    for old_db_file in old_db_files:
        if old_db_file.exists():
            raise SystemExit(
                f'Old database {old_db_file} detected.  '
                'Delete it and run `uvalde index` to create a new database.'
            )

    db_file = db_dir / 'index.1.db'
    db.init(str(db_file))
    db.connect()
    db.create_tables([NVR, Artifact])

    return db
