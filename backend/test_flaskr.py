""" ---------------------------------------------------------------------------
# Imports
# --------------------------------------------------------------------------"""

import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy
from flaskr import create_app
from types import SimpleNamespace
from models import setup_db, Question, Category
from config import (QUESTIONS_PER_PAGE, ERROR_400,  ERROR_404, ERROR_405,
                    ERROR_422, ERROR_500, INVALID_SYNTAX, QUESTION_NOT_FOUND,
                    NO_CATEGORIES_FOUND, NO_QUESTIONS_FOUND, CATEGORY_INT_ERR,
                    QUESTION_FIELDS_ERR, PAGE_INT_ERR, CATEGORY_NOT_FOUND,
                    PREVIOUS_LIST_ERR, QUIZ_CATEGORY_ERR)


""" ---------------------------------------------------------------------------
# Tests
# --------------------------------------------------------------------------"""


class TriviaTestCase(unittest.TestCase):
    """This class represents the trivia test case."""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.db_user = 'postgres'
        self.db_passw = 'postgres'
        self.database_name = 'trivia_test'
        self.database_path = ('postgres://{}:{}@{}/{}'
                              .format(self.db_user, self.db_passw,
                                      'localhost:5432', self.database_name))
        setup_db(self.app, self.database_path)

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()

    def tearDown(self):
        """Executed after reach test."""
        pass

    # Tests for get_categories
    def test_get_categories(self):
        """Tests category list response."""
        response = self.client().get('/api/categories')
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(len(data['categories']))
        self.assertTrue(data['categories'])

    def test_405_post_get_categories(self):
        """Tests post method not allowed on get_categories."""
        response = self.client().post('api/categories', json={
            'type': 'Monty Python'
        })
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 405)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], ERROR_405)

    def test_405_patch_get_categories(self):
        """Tests patch method not allowed on get_categories."""
        response = self.client().patch('api/categories', json={
            'id': 1,
            'type': 'Monty Python'
        })
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 405)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], ERROR_405)

    def test_405_put_get_categories(self):
        """Tests put method not allowed on get_categories."""
        response = self.client().put('api/categories', json={
            'id': 1,
            'type': 'Monty Python'
        })
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 405)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], ERROR_405)

    def test_405_delete_get_categories(self):
        """Tests delete method not allowed on get_categories."""
        response = self.client().delete('api/categories')
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 405)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], ERROR_405)

    # Tests for get_questions
    def test_get_questions_all(self):
        """Test questions list response with no args."""
        response = self.client().get('/api/questions')
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(len(data['questions']))
        self.assertTrue(data['questions'])
        self.assertTrue(data['total_questions'])
        self.assertEqual(data['current_category'], [])
        self.assertTrue(data['categories'])

    def test_get_questions_all_pagination(self):
        """Test questions list response with pagination."""
        response = self.client().get('/api/questions?page=2')
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertLessEqual(len(data['questions']), QUESTIONS_PER_PAGE)
        self.assertTrue(data['questions'])
        self.assertTrue(data['total_questions'])
        self.assertEqual(data['current_category'], [])
        self.assertTrue(data['categories'])

    def test_404_get_questions_page_out_of_range(self):
        """Tests request for a page out of range."""
        response = self.client().get('/api/questions?page=10000000000')
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], ERROR_404)
        self.assertEqual(data['description'], NO_QUESTIONS_FOUND)

    def test_405_patch_questions(self):
        """Tests patch method not allowed on questions."""
        response = self.client().patch('api/questions', json={
            'id': 1,
            'question': 'What is the airspeed velocity of an unladen swallow?',
            'answer': 'What do you mean? An African or European swallow?',
            'difficulty': 5,
            'category': 1
        })
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 405)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], ERROR_405)

    def test_405_put_questions(self):
        """Tests put method not allowed on questions."""
        response = self.client().put('api/questions', json={
            'id': 1,
            'question': 'What is the airspeed velocity of an unladen swallow?',
            'answer': 'What do you mean? An African or European swallow?',
            'difficulty': 5,
            'category': 1
        })
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 405)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], ERROR_405)

    def test_422_get_questions_less_than_one(self):
        """Test 422 error on requesting page number less than one."""
        response = self.client().get('/api/questions?page=0')
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], ERROR_422)
        self.assertEqual(data['description'], PAGE_INT_ERR)

    def test_422_get_questions_str(self):
        """Test 422 error on requesting page number as int."""
        response = self.client().get('/api/questions?page=junk')
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], ERROR_422)
        self.assertEqual(data['description'], PAGE_INT_ERR)

    # Tests for delete_questions
    def test_delete_question(self):
        """Create test question and add to database."""
        test_question = Question(
            question='What is the air speed velocity of an unladen swallow?',
            answer='What do you mean? An African or European swallow?',
            difficulty=5,
            category=1
        )
        test_question.insert()
        test_question_id = test_question.id

        """Delete test question from database."""
        response = self.client().delete(f'/api/questions/{test_question_id}')
        data = json.loads(response.data)

        question_exists = Question.query.filter(
            Question.id == test_question_id).one_or_none()

        self.assertEqual(question_exists, None)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['deleted'], test_question_id)
        self.assertTrue(data['questions'])
        self.assertTrue(data['total_questions'])

    def test_404_delete_question(self):
        """Test delete method for 404 on non-existent question."""
        response = self.client().delete('/api/questions/1000000000000000000')
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], ERROR_404)
        self.assertEqual(data['description'], QUESTION_NOT_FOUND)

    # Tests for post_question
    def test_post_question(self):
        """Test whether a new question posts."""
        response = self.client().post('/api/questions', json={
            'question': 'What is the airspeed velocity of an unladen swallow?',
            'answer': 'What do you mean? An African or European swallow?',
            'difficulty': 5,
            'category': 1
        })

        """ Get latest question to verify id matches."""
        new_question = Question.query.order_by(Question.id.desc()).first()
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['created'], new_question.id)

    def test_422_post_empty_question(self):
        """Tests post with empty fields returns 422"""
        response = self.client().post('/api/questions', json={
            'question': '',
            'answer': '',
            'difficulty': '',
            'category': '',
        })
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], ERROR_422)
        self.assertEqual(data['description'], QUESTION_FIELDS_ERR)

    # Tests for search
    def test_search(self):
        """Tests that search returns valid response."""
        response = self.client().post('api/questions', json={
            'search_term': 'the'
        })
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertTrue(data['questions'])
        self.assertTrue(len(data['questions']))

    # Test for bad request
    def test_400_bad_request(self):
        """Tests posts requests with unrecognizable data."""
        response = self.client().post('/api/questions', json={
            'junk': 'junk data'
        })
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 400)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], ERROR_400)
        self.assertEqual(data['description'], INVALID_SYNTAX)

    # Tests for questions by category
    def test_get_questions_by_category_no_args(self):
        """Tests that questions return for valid category with no args."""
        category_id = 1
        response = self.client().get(
            f'/api/categories/{category_id}/questions')
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['questions'])
        self.assertTrue(data['total_questions'])
        self.assertEqual(data['current_category'], category_id)

    def test_get_questions_by_category_pagination(self):
        """Tests that questions return for valid category with pagination."""
        category_id = 1
        response = self.client().get(
            f'/api/categories/{category_id}/questions?page=1')
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertLessEqual(len(data['questions']), QUESTIONS_PER_PAGE)
        self.assertTrue(data['total_questions'])
        self.assertEqual(data['current_category'], category_id)

    def test_404_get_question_by_page_out_of_range(self):
        """Tests 404 for a page out of range by category."""
        response = self.client().get('/api/categories/1/questions?page=100000')
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], ERROR_404, CATEGORY_NOT_FOUND)

    def test_404_get_question_by_category_out_of_range(self):
        """Tests 404 for a category out of range."""
        response = self.client().get('/api/categories/1000000000000/questions')
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], ERROR_404, CATEGORY_NOT_FOUND)

    def test_422_get_questions_by_category_page_less_than_one(self):
        """Tests 422 for questions by category with page less than one."""
        category_id = 1
        response = self.client().get(
            f'/api/categories/{category_id}/questions?page=0')
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], ERROR_422, PAGE_INT_ERR)

    def test_422_get_questions_by_category_page_str(self):
        """Tests 422 for questions by category with page as str."""
        category_id = 1
        response = self.client().get(
            f'/api/categories/{category_id}/questions?page=junk')
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], ERROR_422, PAGE_INT_ERR)

    def test_422_get_question_by_category_unprocessable(self):
        """Tests 422 for category with a zero id."""
        response = self.client().get('/api/categories/0/questions')
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], ERROR_422)
        self.assertEqual(data['description'], CATEGORY_INT_ERR)

    # Tests for play_quiz
    def test_play_quizz(self):
        """Tests a round of quiz play for valid data throughout."""
        quiz_round = 1
        is_duplicate = False
        quiz_data = SimpleNamespace(previous_questions=[],
                                    quiz_category=0)
        """Simulates five quiz rounds."""
        while quiz_round < 11:
            """For each round, format JSON post."""
            quiz_post = {
                'previous_questions': quiz_data.previous_questions,
                'quiz_category': quiz_data.quiz_category
            }
            response = self.client().post('/api/quizzes', json=quiz_post)
            data = json.loads(response.data)
            this_question = SimpleNamespace(**data['question'])
            """Verifies that the question is new"""
            if this_question.id in quiz_data.previous_questions:
                is_duplicate = True
            """Update previous questions list to simulate frontend."""
            quiz_data.previous_questions.append(this_question.id)

            self.assertEqual(response.status_code, 200)
            self.assertEqual(data['success'], True)
            self.assertTrue(data['question'])
            self.assertEqual(len(quiz_data.previous_questions), quiz_round)
            self.assertEqual(is_duplicate, False)

            quiz_round += 1

    def test_404_play_quiz(self):
        """Test 404 response when quiz category out of range."""
        response = self.client().post('/api/quizzes', json={
            'previous_questions': [],
            'quiz_category': 100000000000
        })
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], ERROR_404)
        self.assertEqual(data['description'], CATEGORY_NOT_FOUND)

    def test_422_play_quiz_previous_questions_not_int(self):
        """Test 422 when previous questions contains list items that are
           not integers."""
        response = self.client().post('/api/quizzes', json={
            'previous_questions': ['this is', 'not a list', 'of ints'],
            'quiz_category': 0
        })
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], ERROR_422)
        self.assertEqual(data['description'], PREVIOUS_LIST_ERR)

    def test_422_play_quiz_previous_questions_not_list(self):
        """Test 422 when previous questions is not a list."""
        response = self.client().post('/api/quizzes', json={
            'previous_questions': 'this is not a list',
            'quiz_category': 0
        })
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], ERROR_422)
        self.assertEqual(data['description'], PREVIOUS_LIST_ERR)

    def test_422_play_quiz_category_not_int(self):
        """Test 422 error when category id not an integer."""
        response = self.client().post('/api/quizzes', json={
            'previous_questions': [],
            'quiz_category': 'this is not an int'
        })
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], ERROR_422)
        self.assertEqual(data['description'], QUIZ_CATEGORY_ERR)

    def test_422_play_quiz_category_less_than_zero(self):
        """Test 422 when category id is less than zero."""
        response = self.client().post('/api/quizzes', json={
            'previous_questions': [],
            'quiz_category': -1
        })
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], ERROR_422)
        self.assertEqual(data['description'], QUIZ_CATEGORY_ERR)


# Make the tests conveniently executable
if __name__ == '__main__':
    unittest.main()
