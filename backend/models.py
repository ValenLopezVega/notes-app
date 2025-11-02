from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import String, Boolean, Text, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

# Creamos la instancia de SQLAlchemy
db = SQLAlchemy()

class User(db.Model):
    __tablename__= 'user'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    fullname: Mapped[str] = mapped_column(String(50), nullable=False)
    email: Mapped[str] = mapped_column(String(120), unique=True, nullable=False)
    password: Mapped[str] = mapped_column(String(120), nullable=False)

    notes: Mapped[list['Note']] = relationship('Note', back_populates='user')

    def serialize(self):
        return {
            'id': self.id,
            'fullname': self.fullname,
            'email': self.email
        }

class Note(db.Model):
    __tablename__= 'note'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    title: Mapped[str] = mapped_column(String(100), nullable=False)
    content: Mapped[str] = mapped_column(Text, nullable=False)

    user_id: Mapped[int] = mapped_column(ForeignKey('user.id', name="fk_note_user"), nullable=False)

    user: Mapped['User'] = relationship('User', back_populates='notes')

    def serialize(self):
        return {
            'id': self.id,
            'title': self.title,
            'content': self.content,
            'user_id': self.user_id
        }
