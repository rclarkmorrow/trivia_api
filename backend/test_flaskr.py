""" ---------------------------------------------------------------------------
# Imports
# --------------------------------------------------------------------------"""

import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from flaskr import create_app
from models import setup_db, Question, Category


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
        self.database_name = "trivia_test"
        self.database_path = ("postgres://{}:{}@{}/{}"
                              .format(self.db_user, self.db_passw,
                                      'localhost:5432', self.database_name))
        setup_db(self.app, self.database_path)

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()

    def getTest():
        print(test)

    def tearDown(self):
        """Executed after reach test."""
        pass

    def test_get_categories(self):
        """Tests category list response"""
        response = self.client().get('/api/categories')
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertTrue(len(data['categories']))
        self.assertTrue(data['categories'])

    def test_get_questions(self):
        """Test questions list response"""
        response = self.client().get('/api/questions')
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['sucess'], True)
        self.assertTrue(len(data['questions']))
        self.assertTrue(data['questions'])

    """
    TODO
    Write at least one test for each test for successful
    operation and for expected errors.
    """


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
