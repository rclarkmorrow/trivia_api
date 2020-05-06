""" ---------------------------------------------------------------------------
# Imports
# --------------------------------------------------------------------------"""

import random
from flask import jsonify, request, abort
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
        query = self.get_all_categories()
        self.list = {category.id: category.type for category in query}
        if len(self.list) < 1:
            abort(404)

        self.data.categories = self.list
        self.response = jsonify(self.data.__dict__), 200

    def get_all_categories(self):
        return Category.query.order_by(Category.type).all()


class Questions:
    def __init__(self, search_term=None, category_id=None):
        self.search_term = search_term
        self.category_id = category_id
        self.data = SimpleNamespace(success=True)
        self.response = jsonify(self.data.__dict__), 200

    def all(self, check_page_range=True):
        # Returns all questions to view.
        self.query = self.get_all_questions()
        self.questions = QuestionsPage(request, self.query)
        self.categories = Categories()
        if check_page_range and len(self.questions.list) < 1:
            abort(404)
        self.data.questions = self.questions.list
        self.data.total_questions = len(self.query)
        self.data.current_category = []
        self.data.categories = self.categories.data.categories
        self.response = jsonify(self.data.__dict__), 200

    def search(self):
        self.query = self.get_search_questions(self.search_term)
        self.questions = QuestionsPage(request, self.query)
        self.data.questions = self.questions.list
        self.data.total_questions = len(self.query)
        self.data.current_category = []
        self.response = jsonify(self.data.__dict__), 200

    def by_category(self):
        self.query = self.get_questions_by_category(self.category_id)

        if len(self.query) < 1:
            abort(404)

        self.questions = QuestionsPage(request, self.query)
        self.data.questions = self.questions.list
        self.data.total_questions = len(self.query)
        self.data.current_category = self.category_id
        self.response = jsonify(self.data.__dict__), 200

    def get_all_questions(self):
        return Question.query.order_by(Question.id).all()

    def get_search_questions(self, search_term):
        return Question.query.filter(Question.question
                                     .ilike(f'%{search_term}%')).all()

    def get_questions_by_category(self, category_id):
        return Question.query.filter(Question.category == category_id).all()


# Gets delete question response object.
class DeleteQuestion:
    def __init__(self, question_id):
        self.data = SimpleNamespace(success=True)
        this_question = self.get_single_question(question_id)

        if this_question is None:
            abort(404)

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
            abort(422)

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
            abort(422)

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
            abort(422)
        page = request.args.get('page', 1, type=int)

        if page < 1:
            abort(422)

        start = (page - 1) * QUESTIONS_PER_PAGE
        stop = start + QUESTIONS_PER_PAGE

        self.list = (([question.format() for question
                       in question_list])[start:stop])
