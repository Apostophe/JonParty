from flask_sqlalchemy import SQLAlchemy

# Initialiser SQLAlchemy
db = SQLAlchemy()

# Modèle pour les Thèmes
class Theme(db.Model):
    __tablename__ = 'themes'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    questions = db.relationship('Question', backref='theme', lazy=True)

# Modèle pour les Questions
class Question(db.Model):
    __tablename__ = 'questions'
    id = db.Column(db.Integer, primary_key=True)
    question = db.Column(db.String(200), nullable=False)
    answer = db.Column(db.String(100), nullable=False)
    points = db.Column(db.Integer, nullable=False)
    theme_id = db.Column(db.Integer, db.ForeignKey('themes.id'), nullable=False)
