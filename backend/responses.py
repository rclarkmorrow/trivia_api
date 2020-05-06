""" ---------------------------------------------------------------------------
# Imports
# --------------------------------------------------------------------------"""

import random
from flask import jsonify, request
from types import SimpleNamespace
from models import Question, Category
from config import QUESTIONS_PER_PAGE


""" ---------------------------------------------------------------------------
# Response Classes
# --------------------------------------------------------------------------"""


# Gets categories response object.
class Categories:
    def __init__(self):
        self.data = SimpleNamespace(success=True)
        category_query = self.get_all_categories()
        category_list = {category.id: category.type for
                         category in category_query}
        if len(category_list) < 1:
            raise Exception('404')

        self.data.categories = category_list
        self.response = jsonify(self.data.__dict__), 200

    def get_all_categories(self):
        return Category.query.order_by(Category.type).all()


class Questions:
    def __init__(self, search_term=None):
        self.search_term = search_term
        self.data = SimpleNamespace(success=True)
        self.response = jsonify(self.data.__dict__), 200

    def all(self, check_page_range=True):
        # Returns all questions to view.
        question_query = self.get_all_questions()
        questions = QuestionsPage(request, question_query)
        categories = Categories()
        if check_page_range and len(questions.list) < 1:
            raise Exception('404')
        self.data.questions = questions.list
        self.data.total_questions = len(question_query)
        self.data.current_category = []
        self.data.categories = categories.data.categories
        self.response = jsonify(self.data.__dict__), 200

    def search(self):
        question_query = self.get_search_questions(self.search_term)
        questions = QuestionsPage(request, question_query)
        self.data.questions = questions.list
        self.data.total_questions = len(question_query)
        self.data.current_category = []
        self.response = jsonify(self.data.__dict__), 200

    def get_all_questions(self):
        return Question.query.order_by(Question.id).all()

    def get_search_questions(self, search_term):
        return Question.query .filter(Question.question
                                      .ilike(f'%{self.search_term}%')).all()


# Gets delete question response object.
class DeleteQuestion:
    def __init__(self, question_id):
        self.data = SimpleNamespace(success=True)
        this_question = self.get_single_question(question_id)

        if this_question is None:
            raise Exception('404')

        this_question.delete()
        questions = Questions()
        questions.all(check_page_range=False)

        self.data.deleted = question_id
        self.data.questions = questions.data.questions
        self.data.total_questions = (
            questions.data.total_questions
        )
        self.response = jsonify(self.data.__dict__), 200

    def get_single_question(self, question_id):
        return Question.query .filter(Question.id == question_id).one_or_none()


# Gets post question response object.
class PostQuestion:
    def __init__(self, form_data=None):
        self.data = SimpleNamespace(success=True)
        # Checks that form data is not empty strings.
        if (form_data.question.strip() == '' or form_data.answer.strip() == ''
                or form_data.difficulty == '' or form_data.category == ''):
            raise Exception('422')

        this_question = Question(
            question=form_data.question.strip(),
            answer=form_data.answer.strip(),
            difficulty=form_data.difficulty,
            category=form_data.category
        )
        # Get latest question before insert.
        last_question = self.get_last_question()
        this_question.insert()
        # Get latest question after insert.
        new_question = self.get_last_question()
        # Check new question id is greater than latest question id
        # before insert.
        if last_question.id >= new_question.id:
            raise Exception('422')

        self.data.created = new_question.id
        self.response = jsonify(self.data.__dict__), 200

    def get_last_question(self):
        return Question.query.order_by(Question.id.desc()).first()


# -----------------------------------------------------------------------------
# Helpers
# -----------------------------------------------------------------------------

class QuestionsPage:
    def __init__(self, request, question_list):
        if request is None or question_list is None:
            raise Exception('422')

        page = request.args.get('page', 1, type=int)

        if page < 1:
            raise Exception('422')

        start = (page - 1) * QUESTIONS_PER_PAGE
        stop = start + QUESTIONS_PER_PAGE

        self.list = (([question.format() for question
                       in question_list])[start:stop])
