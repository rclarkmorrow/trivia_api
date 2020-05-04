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


""" ---------------------------------------------------------------------------
# Helpers
# --------------------------------------------------------------------------"""


def get_category_list():
    # Queries database for a list of categories and returns with
    # id and type.
    category_query = Category.query.order_by(Category.type).all()

    return({category.id: category.type for category in category_query})


def paginate_questions(request, question_list):
    # Handles pagination for questions results.
    page = request.args.get('page', 1, type=int)

    if page < 1:
        raise Exception('422')

    start = (page - 1) * QUESTIONS_PER_PAGE
    stop = start + QUESTIONS_PER_PAGE

    return(([question.format() for question in question_list])[start:stop])


""" ---------------------------------------------------------------------------
# App and routes
# --------------------------------------------------------------------------"""


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

    @app.route('/api/categories', methods=['GET'])
    # Returns a list of trivia question categories.
    def get_categories():
        try:
            category_list = get_category_list()

            if len(category_list) < 1:
                raise Exception('404')

            return jsonify({
                'success': True,
                'categories': category_list
            }), 200
        except Exception as e:
            print('Exception: ', e)
            if '500' in str(e):
                abort(500)
            elif '404' in str(e):
                abort(404)
            else:
                abort(422)

    @app.route('/api/questions', methods=['GET'])
    def get_questions():
        try:
            question_query = Question.query.order_by(Question.id).all()
            question_list = paginate_questions(request, question_query)

            if len(question_list) < 1:
                raise Exception('404')

            return jsonify({
                'success': True,
                'questions': question_list,
                'total_questions': len(question_query),
                'current_category': [],
                'categories': get_category_list()

            }), 200
        except Exception as e:
            print('Exception: ', e)
            if '500' in str(e):
                abort(500)
            elif '404' in str(e):
                abort(404)
            else:
                abort(422)

    '''
    @TODO:
    Create an endpoint to handle GET requests for questions,
    including pagination (every 10 questions).
    This endpoint should return a list of questions,
    number of total questions, current category, categories.

    TEST: At this point, when you start the application
    you should see questions and categories generated,
    ten questions per page and pagination at the bottom of the screen for
    three pages. Clicking on the page numbers should update the questions.
    '''

    '''
    @TODO:
    Create an endpoint to DELETE question using a question ID.

    TEST: When you click the trash icon next to a question, the question will
    be removed. This removal will persist in the database and when you
    refresh the page.
    '''

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

    '''
    @TODO:
    Create error handlers for all expected errors
    including 404 and 422.
    '''
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
