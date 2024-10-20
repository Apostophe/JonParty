from flask import Flask, request, jsonify
from flask_cors import CORS
from models import db, Theme, Question

app = Flask(__name__)
CORS(app)

# Configuration de la base de données SQLite
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///jeopardy.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialiser la base de données avec l'application
db.init_app(app)

# Créer les tables de la base de données (si elles n'existent pas encore)
with app.app_context():
    db.create_all()

# Route pour ajouter un thème (sans questions)
@app.route('/admin/add-theme-only', methods=['POST'])
def add_theme_only():
    data = request.get_json()
    new_theme = Theme(title=data['title'])
    db.session.add(new_theme)
    db.session.commit()
    return jsonify({"message": "Thème ajouté avec succès", "theme_id": new_theme.id}), 201

# Route pour ajouter une ou plusieurs questions à un thème existant
@app.route('/admin/add-questions/<int:theme_id>', methods=['POST'])
def add_questions(theme_id):
    theme = Theme.query.get(theme_id)
    if not theme:
        return jsonify({"error": "Thème non trouvé"}), 404

    data = request.get_json()
    for q in data['questions']:
        new_question = Question(
            question=q['question'],
            answer=q['answer'],
            points=q['points'],
            theme_id=theme_id
        )
        db.session.add(new_question)

    db.session.commit()
    return jsonify({"message": "Questions ajoutées avec succès au thème"}), 201

# Route pour récupérer toutes les questions d'un thème spécifique par ID
@app.route('/theme/<int:theme_id>/questions', methods=['GET'])
def get_theme_questions(theme_id):
    theme = Theme.query.get(theme_id)
    if not theme:
        return jsonify({"error": "Thème non trouvé"}), 404

    questions = [{
        "id": q.id,
        "question": q.question,
        "answer": q.answer,
        "points": q.points
    } for q in theme.questions]

    return jsonify({"theme": theme.title, "questions": questions})

# Route pour récupérer tous les thèmes avec leurs questions
@app.route('/themes', methods=['GET'])
def get_themes():
    themes = Theme.query.all()
    result = []
    for theme in themes:
        theme_data = {
            "title": theme.title,
            "questions": [{
                "question": q.question,
                "points": q.points
            } for q in theme.questions]
        }
        result.append(theme_data)
    return jsonify(result)

# Route pour récupérer tous les thèmes avec leurs IDs
@app.route('/themes/ids', methods=['GET'])
def get_themes_with_ids():
    themes = Theme.query.all()
    result = [{"id": theme.id, "title": theme.title} for theme in themes]
    return jsonify(result)

if __name__ == "__main__":
    app.run(debug=True)
