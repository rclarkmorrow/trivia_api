""" ---------------------------------------------------------------------------
# Imports
# --------------------------------------------------------------------------"""


import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random

from models import setup_db, Question, Category
from config import (QUESTIONS_PER_PAGE, ERROR_404, ERROR_405,
                    ERROR_422, ERROR_500)
from responses import Categories, Questions, DeleteQuestion
from helpers import handle_errors


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
                             'GET, POST, PATCH, DELETE, OPTIONS')
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

    @app.route('/api/questions', methods=['GET'])
    # Provides a paginated list of questions to the view.
    def get_questions():
        try:
            questions = Questions()
            return questions.response
        except Exception as e:
            handle_errors(e)

    @app.route('/api/questions/<int:question_id>', methods=['DELETE'])
    def delete_question(question_id):
        try:
            delete_question = DeleteQuestion(question_id)
            return delete_question.response
        except Exception as e:
            handle_errors(e)

    '''
    @TODO:
    Create an endpoint to POST a new question,
    which will require the question and answer text,
    category, and difficulty score.

    TEST: When you submit a question on the "Add" tab,
    the form will clear and the question will appear at the end of
    the last page of the questions list in the "List" tab.
    '''

    '''
    @TODO:
    Create a POST endpoint to get questions based on a search term.
    It should return any questions for whom the search term
    is a substring of the question.

    TEST: Search by any phrase. The questions list will update to include
    only question that include that string within their question.
    Try using the word "title" to start.
    '''

    '''
    @TODO:
    Create a GET endpoint to get questions based on category.

    TEST: In the "List" tab / main screen, clicking on one of the
    categories in the left column will cause only questions of that
    category to be shown.
    '''

    '''
    @TODO:
    Create a POST endpoint to get questions to play the quiz.
    This endpoint should take category and previous question parameters
    and return a random questions within the given category,
    if provided, and that is not one of the previous questions.

    TEST: In the "Play" tab, after a user selects "All" or a category,
    one question at a time is displayed, the user is allowed to answer
    and shown whether they were correct or not.
    '''

# Error handlers
    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
            'success': False,
            'error': 404,
            'message': ERROR_404
        }), 404

    @app.errorhandler(405)
    def not_allowed(error):
        return jsonify({
            'success': False,
            'error': 405,
            'message': ERROR_405
        }), 405

    @app.errorhandler(422)
    def unprocessable(error):
        return jsonify({
            'success': False,
            'error': 422,
            'message': ERROR_422
        }), 422

    @app.errorhandler(500)
    def internal_server_error(error):
        return jsonify({
            'success': False,
            'error': 500,
            'message': ERROR_500
        }), 500

    return app
