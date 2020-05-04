""" ---------------------------------------------------------------------------
# Imports
# --------------------------------------------------------------------------"""

import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from flaskr import create_app
from models import setup_db, Question, Category
from config import (QUESTIONS_PER_PAGE, ERROR_404, ERROR_405,
                    ERROR_422, ERROR_500)


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

    def test_get_categories(self):
        """Tests category list response"""
        response = self.client().get('/api/categories')
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(len(data['categories']))
        self.assertTrue(data['categories'])

    def test_405_post_get_categories(self):
        """Tests post method not allowed on get_categories"""
        response = self.client().post('api/categories',
                                      data={'junk': 'junk data'})
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 405)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], ERROR_405)

    def test_405_patch_get_categories(self):
        """Tests patch method not allowed on get_categories"""
        response = self.client().patch('api/categories',
                                       data={'junk': 'junk data'})
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 405)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], ERROR_405)

    def test_405_delete_get_categories(self):
        """Tests delete method not allowed on get_categories"""
        response = self.client().delete('api/categories',
                                        data={'junk': 'junk data'})
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 405)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], ERROR_405)

    def test_get_questions(self):
        """Test questions list response"""
        response = self.client().get('/api/questions')
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(len(data['questions']), QUESTIONS_PER_PAGE)
        self.assertTrue(data['questions'])
        self.assertTrue(data['total_questions'])
        self.assertEqual(data['current_category'], [])
        self.assertTrue(data['categories'])

    def test_404_questions_invalid_page_range(self):
        """Tests request for a page out of range."""
        response = self.client().get('/api/questions?page=10000000000')
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], ERROR_404)

    def test_405_post_get_questions(self):
        """Tests post method not allowed on get_questions"""
        response = self.client().post('api/questions',
                                      data={'junk': 'junk data'})
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 405)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], ERROR_405)

    def test_405_patch_get_questions(self):
        """Tests patch method not allowed on get_questions"""
        response = self.client().patch('api/questions',
                                       data={'junk': 'junk data'})
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 405)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], ERROR_405)

    def test_405_delete_get_questions(self):
        """Tests delete method not allowed on get_questions"""
        response = self.client().delete('api/questions',
                                        data={'junk': 'junk data'})
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 405)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], ERROR_405)

    def test_422_questions(self):
        response = self.client().get('/api/questions?page=0')
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], ERROR_422)

    """
    TODO
    Write at least one test for each test for successful
    operation and for expected errors.
    """


# Make the tests conveniently executable
if __name__ == '__main__':
    unittest.main()
