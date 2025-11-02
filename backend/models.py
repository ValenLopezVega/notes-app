from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import String, Boolean, Text, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

# Creamos la instancia de SQLAlchemy
db = SQLAlchemy()

# Ejemplo de modelo para notas
class User(db.Model):
    __tablename__= 'user'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    fullname: Mapped[str] = mapped_column(String(50), nullable=False)
    email: Mapped[str] = mapped_column(String(120), unique=True, nullable=False)
    password: Mapped[str] = mapped_column(String(120), nullable=False)

    def serialize(self):
        return {
            'id': self.id,
            'fullname': self.fullname,
            'email': self.email
        }
