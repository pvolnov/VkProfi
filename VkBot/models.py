
import sqlite3
from datetime import date
from peewee import *

db = SqliteDatabase('db.sqlite3')

class Subs(Model):
    vk_id=IntegerField()
    name = TextField()
    qnow = IntegerField()
    bals = TextField(null=True)
    result = BooleanField(null=True)

    class Meta:
        database = db
        db_table='Subs'

class Quizs(Model):
    text=TextField()
    tbals = TextField()
    fbals = TextField()


    class Meta:
        database = db
        db_table='Quizs'

class rTest(Model):
    text=TextField()
    ans = TextField()
    photoname = TextField()

    class Meta:
        database = db
        db_table='rTest'

class Works(Model):
    name=TextField(null=True)
    winfo=TextField(null=True)
    photoname = TextField(null=True)

    class Meta:
        database = db
        db_table='Works'


#Works.create_table()
# Quizs.create_table()
