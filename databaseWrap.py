import peewee
import sqlite3
import datetime
import sys

db = peewee.SqliteDatabase('events.db')

class BaseModel(peewee.Model):
    class Meta:
        database = db

class Coord(BaseModel):
    peewee.PrimaryKeyField(index=True, unique=True, primary_key=True)
    lat = peewee.DoubleField()
    lng = peewee.DoubleField()
    radius = peewee.DoubleField()
    comment = peewee.TextField()

class Event(BaseModel):
    id = peewee.PrimaryKeyField(index=True, unique=True, primary_key=True)
    name = peewee.TextField()
    url = peewee.TextField()
    description = peewee.TextField()
    coordId = peewee.ForeignKeyField(Coord, null=True)
    dateStart = peewee.DateField()
    dateEnd = peewee.DateField()
    partOf = peewee.ForeignKeyField('self', related_name='parts', null=True)

class Country(BaseModel):
    id = peewee.PrimaryKeyField(index=True, unique=True, primary_key=True)
    name = peewee.TextField()
    eventId = peewee.ForeignKeyField(Event)

def createTables():
    db.connect()
    db.create_tables([Coord, Event, Country], safe=True)
