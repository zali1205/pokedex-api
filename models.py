from __main__ import db
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import relationship

class User(db.Model):
    __table__name = "users"
    id = db.Column(db.Integer, primary_key=True)