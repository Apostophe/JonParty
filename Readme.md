# Jeopardy Game Backend API

This is a backend API built with Flask and SQLite to host and manage Jeopardy-style games. The API allows you to create themes, add questions, and retrieve questions for a specific theme. It also includes an admin panel for adding new themes and questions.

## Features

- Create new themes.
- Add one or more questions to existing themes.
- Retrieve all questions for a specific theme.
- Retrieve all themes with their IDs and titles.
- Easy-to-use API with JSON input/output.

## Table of Contents

- [Installation](#installation)
- [Running the App](#running-the-app)
- [API Endpoints](#api-endpoints)
  - [POST `/admin/add-theme-only`](#post-adminadd-theme-only)
  - [POST `/admin/add-questions/<theme_id>`](#post-adminadd-questionstheme_id)
  - [GET `/theme/<theme_id>/questions`](#get-themetheme_idquestions)
  - [GET `/themes`](#get-themes)
  - [GET `/themes/ids`](#get-themesids)
- [Models](#models)
- [License](#license)

---

## Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/your-username/jeopardy-backend.git
   cd jeopardy-backend
   ```

2. Create a virtual environment (optional but recommended):

    ```bash
    python3 -m venv venv
    source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
    ```

3. Install the dependencies:

    ```bash
    pip install -r requirements.txt
    ```

4. Run the Flask app:

    ```bash
    python app.py
    ```

    The server will run at `http://localhost:5000`.


## Running the App

After installation, you can run the app by executing:

```bash

python app.py

```

This will start the server, and you can interact with the API through `http://localhost:5000`.

## API Endpoints
### POST `/admin/add-theme-only`

Description: Adds a new theme without any questions.

Request Body:

```json
{
  "title": "Science"
}
```

Response:

```json
{
  "message": "Thème ajouté avec succès",
  "theme_id": 1
}
```

### POST `/admin/add-questions/<theme_id>`

Description: Adds one or multiple questions to an existing theme by its ID.

Request Body:

```json
{
  "questions": [
    {
      "question": "What is the capital of France?",
      "answer": "Paris",
      "points": 100
    },
    {
      "question": "Which continent is the largest by land area?",
      "answer": "Asia",
      "points": 200
    }
  ]
}
```

Response:

```json
{
  "message": "Questions ajoutées avec succès au thème"
}
```

### GET `/theme/<theme_id>/questions`

Description: Retrieves all questions for a specific theme by its ID.

Response:

```json
{
  "theme": "Science",
  "questions": [
    {
      "id": 1,
      "question": "What is the chemical symbol for water?",
      "answer": "H2O",
      "points": 100
    },
    {
      "id": 2,
      "question": "What planet is known as the Red Planet?",
      "answer": "Mars",
      "points": 200
    }
  ]
}
```

### GET `/themes`

Description: Retrieves all themes with their corresponding questions.

Response:

```json
[
  {
    "title": "Science",
    "questions": [
      {
        "question": "What is the chemical symbol for water?",
        "points": 100
      },
      {
        "question": "What planet is known as the Red Planet?",
        "points": 200
      }
    ]
  },
  {
    "title": "Geography",
    "questions": [
      {
        "question": "What is the capital of France?",
        "points": 100
      },
      {
        "question": "Which continent is the largest by land area?",
        "points": 200
      }
    ]
  }
]
```

### GET `/themes/ids`

Description: Retrieves all themes with their corresponding IDs.

Response:

```json
[
  {
    "id": 1,
    "title": "Science"
  },
  {
    "id": 2,
    "title": "Geography"
  }
]
```

## Models
### Theme

The `Theme` model represents a theme (or category) in the Jeopardy game.

- id: Integer, primary key, auto-increment.
- title: String, the name of the theme.
- questions: A relationship to the `Question` model (one-to-many).

### Question

The `Question` model represents a question under a specific theme.

- id: Integer, primary key, auto-increment.
- question: String, the content of the question.
- answer: String, the correct answer to the question.
- points: Integer, the point value for the question.
- theme_id: Foreign key linking to the `Theme` model.