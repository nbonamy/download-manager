import os
import consts
import datetime
from peewee import *

database = SqliteDatabase(consts.DATABASE_PATH, pragmas={
  'journal_mode': 'wal'
})

def create_database():
  if not os.path.exists(consts.DATABASE_PATH):
    database.connect()
    database.create_tables([Download])

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
  pid = IntegerField(default=0)
