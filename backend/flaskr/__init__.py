""" ---------------------------------------------------------------------------
# Imports
# --------------------------------------------------------------------------"""


import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from types import SimpleNamespace
from models import setup_db, Question, Category
from config import (ERROR_400, ERROR_404, ERROR_405, ERROR_422, ERROR_500,
                    INVALID_SYNTAX)
from responses import Categories, Questions, DeleteQuestion, PostQuestion, Quiz


""" ---------------------------------------------------------------------------
#  Helpers
# --------------------------------------------------------------------------"""


# Parses HTTP aborts, and passes additional context to
# reponse JSON. Defaults to a 500 error.
def handle_errors(e):
    if '400' in str(e):
        abort(400, e.description)
    if '404' in str(e):
        abort(404, e.description)
    elif '405' in str(e):
        abort(405, e.description)
    elif '422' in str(e):
        abort(422, e.description)
    else:
        print(e)
        abort(500)


""" ---------------------------------------------------------------------------
# App config, routes and error handlers
# --------------------------------------------------------------------------"""


# App config
def create_app(test_config=None):
    # Create and configure the app.
    app = Flask(__name__)
    setup_db(app)
    # Setup CORS. Allow '*' for origins
    cors = CORS(app, resources={r'/api/*': {'origins': '*'}})

    @app.after_request
    def after_request(response):
        # Setup headers
        response.headers.add('Access-Control-Allow-Headers',
                             'Content-Type, Authorization')
        response.headers.add('Access-Control-Allow-Methods',
                             'GET, POST, DELETE, OPTIONS')
        return response

# App routes
    @app.route('/api/categories', methods=['GET'])
    # Provides a list of categories to the view.
    def get_categories():
        try:
            categories = Categories()
            return categories.response
        except Exception as e:
            handle_errors(e)

    @app.route('/api/questions', methods=['GET', 'POST'])
    # Handles GET requests to return questions to the view, and POST requests
    # for search terms and adding new questions to the database.
    def get_questions():
        try:
            if request.method == 'POST':
                this_request = request.get_json()
                # Checks POST for data, if none errors.
                if not this_request:
                    abort(400, INVALID_SYNTAX)
                form_data = SimpleNamespace(**this_request)
                # Checks POST for a search term and runs search present.
                if hasattr(form_data, 'search_term'):
                    questions = Questions(search_term=form_data.search_term)
                    questions.search()
                    return questions.response
                # Checks POST for question data and runs post_question
                # if present.
                elif (hasattr(form_data, 'question') or
                      hasattr(form_data, 'answer') or
                      hasattr(form_data, 'difficulty') or
                      hasattr(form_data, 'category')):

                    post_question = PostQuestion(form_data)
                    return post_question.response
                else:
                    # All other POST requests return a 400 error.
                    abort(400, INVALID_SYNTAX)
            else:
                # If no POST data, returns all questions to view.
                questions = Questions()
                questions.all()
                return questions.response
        except Exception as e:
            handle_errors(e)

    @app.route('/api/questions/<int:question_id>', methods=['DELETE'])
    # Deletes a question from the database.
    def delete_question(question_id):
        try:
            delete_question = DeleteQuestion(question_id)
            return delete_question.response
        except Exception as e:
            handle_errors(e)

    @app.route('/api/categories/<int:category_id>/questions', methods=['GET'])
    # Gets questions by category id.
    def get_questions_by_category(category_id):
        try:
            questions = Questions(category_id=category_id)
            questions.by_category()
            return questions.response
        except Exception as e:
            handle_errors(e)

    @app.route('/api/quizzes', methods=['POST'])
    # Launches quiz game based on user selection.
    def play_quizz():
        try:
            this_request = request.get_json()
            if not this_request:
                abort(400, INVALID_SYNTAX)
            form_data = SimpleNamespace(**this_request)
            if (hasattr(form_data, 'quiz_category') or
                    hasattr(form_data, 'previous_questions')):
                quiz = Quiz(form_data=form_data)
                return quiz.response
            else:
                abort(400, INVALID_SYNTAX)
        except Exception as e:
            handle_errors(e)

# Error handlers
    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({
            'success': False,
            'error': 400,
            'message': ERROR_400,
            'description': error.description
        }), 400

    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
            'success': False,
            'error': 404,
            'message': ERROR_404,
            'description': error.description
        }), 404

    @app.errorhandler(405)
    def not_allowed(error):
        return jsonify({
            'success': False,
            'error': 405,
            'message': ERROR_405,
            'description': error.description
        }), 405

    @app.errorhandler(422)
    def unprocessable(error):
        return jsonify({
            'success': False,
            'error': 422,
            'message': ERROR_422,
            'description': error.description
        }), 422

    @app.errorhandler(500)
    def internal_server_error(error):
        return jsonify({
            'success': False,
            'error': 500,
            'message': ERROR_500
        }), 500

    return app
