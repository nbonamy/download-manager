import os
import consts
import datetime
from peewee import *
from playhouse.migrate import *
from playhouse.shortcuts import model_to_dict

database = SqliteDatabase(consts.DATABASE_PATH, pragmas={
  'journal_mode': 'wal'
})

def create_database():
  if not os.path.exists(consts.DATABASE_PATH):
    database.connect()
    database.create_tables([Download])
  migrate_database()

def migrate_database():

  # init
  migrator = SqliteMigrator(database)
  columns = database.get_columns('download')

  # progress
  if not column_exists(columns, 'progress'):
    migrate(
      migrator.add_column('download', 'progress', CharField(null=True, max_length=8192)),
    )

def column_exists(columns, column_name):
  return next((x for x in columns if x.name == column_name), None) is not None

class BaseModel(Model):
  class Meta:
    database = database

class Download(BaseModel):
  url = CharField()
  download_url = CharField()
  filepath = CharField()
  filename = CharField()
  filesize = IntegerField(default=0)
  started_at = DateTimeField(default=datetime.datetime.now)
  status = IntegerField(default=consts.STATUS_CREATED)
  progress = CharField(null=True, max_length=8192)
  pid = IntegerField(default=0)

  def to_dict(self):
    return model_to_dict(self, exclude=[Download.started_at])
