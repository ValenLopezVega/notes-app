import os
from dotenv import load_dotenv
from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_cors import CORS

from models import db, Note

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

if __name__ == "__main__":
    app.run(debug=True)
