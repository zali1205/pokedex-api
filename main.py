from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from functools import wraps
import uuid
import jwt
import datetime
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get("FLASK_SECRET_KEY")
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///../pokedex.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy()
db.init_app(app)

from models import User

with app.app_context():
    db.create_all()

def token_required(func):
    @wraps(func)
    def decorator(*args, **kwargs):
        token = None
        if not 'Authorization' in request.headers:
            return jsonify({'Error': 'Missing Authorization Bearer Token in Header.'}), 400
        token = request.headers['Authorization']
        if not token:
            return jsonify({'Error': 'A valid token is missing.'}), 400
        try:
            data = jwt.decode(token, app.config['SECRET_KEY'], algorithms=["HS256"])
            current_user = User.query.filter_by(public_id=data['public_id']).first()
        except:
            return jsonify({'Error': 'Token is invalid.'}), 400
        
        return func(current_user, *args, **kwargs)

    return decorator

@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    hashed_password = generate_password_hash(data['password'], method='pbkdf2:sha256', salt_length=8)
    new_user = User(public_id=str(uuid.uuid4()), name=data['name'], email=data['email'], password=hashed_password, is_admin=False)
    db.session.add(new_user)
    db.session.commit()
    return jsonify({'Message': 'Registered Successfully!'})

@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    email = data['email']
    check_user = User.query.filter_by(email=email).first()
    if check_user == None:
        return jsonify({'Error': 'Invalid login. Account does not exist.'}),  401
    password = data['password']
    if not check_password_hash(check_user.password, password):
        return jsonify({'Error': 'Invalid login.'}), 401
    
    token = jwt.encode({'public_id': check_user.public_id, 'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=30)}, app.config['SECRET_KEY'], algorithm='HS256')
    return jsonify({'Token': token})

if __name__ == '__main__':
    app.run(debug=True, port=8000)