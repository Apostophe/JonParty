from flask import Flask, request, jsonify
from flask_cors import CORS
from models import db, Theme, Question

import os


app = Flask(__name__)
CORS(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///jeopardy.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['UPLOAD_FOLDER'] = 'uploads/'  # Folder to store uploaded media
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

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

@app.route('/admin/add-questions/<int:theme_id>', methods=['POST'])
def add_questions(theme_id):
    theme = Theme.query.get_or_404(theme_id)
    data = request.get_json()

    questions = []
    for item in data['questions']:
        question = Question(
            question=item['question'],
            answer=item['answer'],
            points=item['points'],
            theme=theme,
            media_type=item.get('media_type'),  # Get media type if provided
            media_path=item.get('media_path')   # Get media path if provided
        )
        questions.append(question)

    db.session.add_all(questions)
    db.session.commit()
    return jsonify(message="Questions ajoutées avec succès au thème"), 201


@app.route('/theme/<int:theme_id>/questions', methods=['GET'])
def get_questions(theme_id):
    theme = Theme.query.get_or_404(theme_id)
    questions = Question.query.filter_by(theme_id=theme_id).all()
    questions_list = [{
        'id': q.id,
        'question': q.question,
        'answer': q.answer,
        'points': q.points,
        'media_type': q.media_type,  # Include media type
        'media_path': q.media_path    # Include media path
    } for q in questions]
    return jsonify(theme=theme.title, questions=questions_list)

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

@app.route('/admin/upload-media', methods=['POST'])
def upload_media():
    if 'file' not in request.files:
        return jsonify({'message': 'No file part'}), 400
    file = request.files['file']
    if file.filename == '':
        return jsonify({'message': 'No selected file'}), 400

    # Save the file
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
    file.save(file_path)

    return jsonify({'message': 'File uploaded successfully', 'file_path': file_path}), 201

# Route pour récupérer tous les thèmes avec leurs IDs
@app.route('/themes/ids', methods=['GET'])
def get_themes_with_ids():
    themes = Theme.query.all()
    result = [{"id": theme.id, "title": theme.title} for theme in themes]
    return jsonify(result)

if __name__ == "__main__":
    app.run(debug=True)
