from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy

server = Flask(__name__)
server.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://eu-west-1.compute.amazonaws.com:5432/dagcaoe4fctvff'
### dev 'postgresql://postgres:postgres@localhost:5432/'
server.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(server)

class Bot_ex(db.Model):
    ___tablename__ = 'exchange_telebot'
    id = db.Column(db.Integer, primary_key=True)
    currency = db.Column(db.String(20))#, unique=True)
    value = db.Column(db.Float())
    timestamp = db.Column(db.Integer())
