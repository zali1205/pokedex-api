from __main__ import db
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import relationship

class User(db.Model):
    __table__name = "users"
    id = db.Column(db.Integer, primary_key=True)
    public_id = db.Column(db.String(250), nullable=False)
    name = db.Column(db.String(250), nullable=False)
    email = db.Column(db.String(250), nullable=False, unique=True)
    password = db.Column(db.String(250), nullable=False)
    is_admin = db.Column(db.Boolean, default=False)

class Pokemon(db.Model):
    __table_name = "pokemons"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), unique=True)
    poke_type = db.Column(db.String(250), nullable=False)
    species = db.Column(db.String(250), nullable=False)
    height = db.Column(db.Integer, nullable=False)
    weight = db.Column(db.Integer, nullable=False)
    image = db.Column(db.String(250), nullable=False)
