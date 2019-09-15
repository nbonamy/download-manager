import datetime
import consts
from peewee import *

database = SqliteDatabase('../data/downloads.db', pragmas={
  'journal_mode': 'wal'
})

class BaseModel(Model):
  class Meta:
    database = database

class Download(BaseModel):
  url = CharField()
  download_url = CharField()
  filename = CharField()
  filesize = IntegerField(default=0)
  started_at = DateTimeField(default=datetime.datetime.now)
  status = IntegerField(default=consts.STATUS_CREATED)
  pid = IntegerField(default=0)
