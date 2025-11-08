import os
from dotenv import load_dotenv
from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_cors import CORS
from sqlalchemy.exc import IntegrityError, DataError

from models import db, User, Note

# Cargar variables del .env
load_dotenv()

app = Flask(__name__)
CORS(app)

# Configuración de la base de datos
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv("DATABASE_URL", "sqlite:///notes.db")
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = os.getenv("SECRET_KEY", "default_secret_key")

# Inicializamos la DB con Flask
db.init_app(app)
# Inicializamos Flask-Migrate
migrate = Migrate(app, db)

# Ruta de prueba
@app.route('/')
def home():
    return jsonify({"message": "Backend funcionando 🚀"})

@app.route('/users', methods=['POST'])
def create_user():
    data = request.get_json()
    name = data.get('name')
    lastname = data.get('lastname')
    email = data.get('email')
    password = data.get('password')

    if not all([name, lastname, email, password]):
        return jsonify({"error": "Missing required fields"}), 400

    if User.query.filter_by(email=email).first():
        return jsonify({"error": "Email already registered"}), 409

    user = User(name=name, lastname=lastname, email=email, password=password)
    db.session.add(user)

    try:
        db.session.commit()
        return jsonify({"message": "User created", "user": user.serialize()}), 201
    except Exception as error:
        db.session.rollback()
        return jsonify({"error": str(error)}), 500

@app.route('/notes', methods=['POST'])
def create_note():
    data = request.get_json()
    title = data.get('title')
    content = data.get('content')
    user_id = data.get('user_id')

    if not all([title, content, user_id]):
        return jsonify({"error": "Missing required fields"}), 400

    user = User.query.get(user_id)
    if not user:
        return jsonify({"error": "User not found"}), 404

    note = Note(title=title, content=content, user_id=user_id)
    db.session.add(note)

    try:
        db.session.commit()
        return jsonify({
            "message": "Note created",
            "note": note.serialize()
        }), 201

    except IntegrityError:
        db.session.rollback()
        return jsonify({"error": "Database integrity error"}), 400
    except DataError:
        db.session.rollback()
        return jsonify({"error": "Data type or length error"}), 400
    except Exception as error:
        db.session.rollback()
        return jsonify({"error": str(error)}), 500

if __name__ == "__main__":
    app.run(debug=True)
