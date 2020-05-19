""" ---------------------------------------------------------------------------
# Imports
# --------------------------------------------------------------------------"""

import random
from flask import jsonify, request
from types import SimpleNamespace
from models import Question, Category
from config import (QUESTIONS_PER_PAGE, QUESTION_NOT_FOUND,
                    NO_CATEGORIES_FOUND, NO_QUESTIONS_FOUND, CATEGORY_INT_ERR,
                    QUESTION_FIELDS_ERR, PAGE_INT_ERR, CATEGORY_NOT_FOUND,
                    PREVIOUS_LIST_ERR, QUIZ_CATEGORY_ERR,
                    ADD_QUESTION_CATEGORY_ERR, ADD_QUESTION_DIFFICULTY_ERR,
                    ERROR_404, ERROR_422, ERROR_500)

""" ---------------------------------------------------------------------------
# Error Handling
# --------------------------------------------------------------------------"""


# Raise exceptions as HTTP status code errors.
class StatusError(Exception):
    def __init__(self, message, description, status_code):
        self.message = message
        self.status_code = status_code
        self.description = description


""" ---------------------------------------------------------------------------
# Helper Functions
# --------------------------------------------------------------------------"""


# Convert string to integer and return if possible, raise 422 error if not.
def string_to_int(value, description):
    if (type(value)) != int:
        try:
            value = int(value)
        except ValueError:
            raise StatusError(ERROR_422, description, 422)
    return value


""" ---------------------------------------------------------------------------
# Response Classes
# --------------------------------------------------------------------------"""


# Gets categories to pass to views.
class Categories:
    def __init__(self):
        self.data = SimpleNamespace(success=True)
        query = self.get_all_categories()
        self.list = {category.id: category.type for category in query}
        # Returns 404 if database contains no categories.
        if len(self.list) < 1:
            raise StatusError(ERROR_404, NO_CATEGORIES_FOUND, 404)
        # Structures data and builds response JSON.
        self.data.categories = self.list
        self.response = jsonify(self.data.__dict__), 200

    def get_all_categories(self):
        # Get all categories from the database.
        return Category.query.order_by(Category.type).all()

    def category_exists(self, category_id):
        # Checks if category exists.
        return (Category.query
                .filter_by(id=category_id).scalar() is not None)


# Gets questions to pass to views.
class Questions:
    def __init__(self, search_term=None, category_id=None):
        # Init with data used by methods.
        self.search_term = search_term
        self.category_id = category_id
        self.data = SimpleNamespace(success=True)
        self.response = jsonify(self.data.__dict__), 200

    def all(self, check_page_length=True):
        # Returns all questions to views.
        self.query = self.get_all_questions()
        self.questions = QuestionsPage(request, self.query)
        self.categories = Categories()
        # Unless disabled, returns a 404 if the list of questions
        # is empty.
        if check_page_length is True and len(self.questions.list) < 1:
            raise StatusError(ERROR_404, NO_QUESTIONS_FOUND, 404)
        # Structures data and builds response JSON.
        self.data.questions = self.questions.list
        self.data.total_questions = len(self.query)
        self.data.current_category = []
        self.data.categories = self.categories.data.categories
        self.response = jsonify(self.data.__dict__), 200

    def search(self, check_page_length=False):
        # Returns questions by search query to views.
        self.query = self.get_search_questions(self.search_term)
        self.questions = QuestionsPage(request, self.query)
        # Unless enabled, does not return a 404 if the list of questions
        # is empty. I believe a search returning an empty list is a
        # better user experience than an error alert.
        if check_page_length is True and len(self.questions.list) < 1:
            raise StatusError(ERROR_404, NO_QUESTIONS_FOUND, 404)
        # Structures data and builds response JSON.
        self.data.questions = self.questions.list
        self.data.total_questions = len(self.query)
        self.data.current_category = []
        self.response = jsonify(self.data.__dict__), 200

    def by_category(self, check_page_length=True):
        # Returns questions by category to views.

        # Verifies that the category id is an integer.
        self.category_id = string_to_int(self.category_id, CATEGORY_INT_ERR)
        # Verifies that the category id is not 0 or negative.
        if self.category_id < 1:
            raise StatusError(ERROR_422, CATEGORY_INT_ERR, 422)
        # Get questions by category and paginate if requested.
        self.query = self.get_questions_by_category(self.category_id)
        self.questions = QuestionsPage(request, self.query)
        # Unless disabled, returns a 404 error if the category returns
        # no questions because it doesn't exist or has no questions.
        if check_page_length is True and len(self.questions.list) < 1:
            raise StatusError(ERROR_404, CATEGORY_NOT_FOUND, 404)
        # Structures data, and builds response JSON.
        self.data.questions = self.questions.list
        self.data.total_questions = len(self.query)
        self.data.current_category = self.category_id
        self.response = jsonify(self.data.__dict__), 200

    def get_all_questions(self):
        # Returns a list of all questions in the database.
        return Question.query.order_by(Question.id).all()

    def get_search_questions(self, search_term):
        # Returns a list of questions matching keyword(s).
        return Question.query.filter(Question.question
                                     .ilike(f'%{search_term}%')).all()

    def get_questions_by_category(self, category_id):
        # Returns a list of questions matching category id.
        return Question.query.filter(Question.category == category_id).all()


# Deletes question from database.
class DeleteQuestion:
    def __init__(self, question_id):
        self.data = SimpleNamespace(success=True)
        this_question = self.get_single_question(question_id)
        # Returns 404 if a delete request is sent for a non-existent
        # question.
        if this_question is None:
            raise StatusError(ERROR_404, QUESTION_NOT_FOUND, 404)

        this_question.delete()
        questions = Questions()
        # Disables page length check so user does not receive
        # an error when deleting last question on page.
        questions.all(check_page_length=False)

        self.data.deleted = question_id
        self.data.questions = questions.data.questions
        self.data.total_questions = (
            questions.data.total_questions
        )
        self.response = jsonify(self.data.__dict__), 200

    def get_single_question(self, question_id):
        # Returns a question from the database by id.
        return Question.query .filter(Question.id == question_id).one_or_none()


# Posts question to database
class PostQuestion:
    def __init__(self, form_data=None):
        self.data = SimpleNamespace(success=True)
        # Checks attributes exist.
        if (not hasattr(form_data, 'question') or
                not hasattr(form_data, 'answer') or
                not hasattr(form_data, 'difficulty') or
                not hasattr(form_data, 'category')):
            raise StatusError(ERROR_422, QUESTION_FIELDS_ERR, 422)

        # Checks that form data is not empty strings.
        if (form_data.question.strip() == '' or form_data.answer.strip() == ''
                or form_data.difficulty == '' or form_data.category == ''):
            raise StatusError(ERROR_422, QUESTION_FIELDS_ERR, 422)
        # Verify integer and category exists or error.
        if (type(form_data.category)) != int:
            try:
                form_data.category = int(form_data.category)
            except ValueError:
                raise StatusError(ERROR_422, ADD_QUESTION_CATEGORY_ERR, 422)
        elif not Categories().category_exists(form_data.category):
            raise StatusError(ERROR_422, ADD_QUESTION_CATEGORY_ERR, 422)
        # Verify integer and in range or error.
        form_data.difficulty = string_to_int(form_data.difficulty,
                                             ADD_QUESTION_DIFFICULTY_ERR)
        if form_data.difficulty < 1 or form_data.difficulty > 5:
            raise StatusError(ERROR_422, ADD_QUESTION_DIFFICULTY_ERR, 422)

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
            raise StatusError(ERROR_500, None, 500)
        # Structures data and builds response JSON.
        self.data.created = new_question.id
        self.response = jsonify(self.data.__dict__), 200

    def get_last_question(self):
        # Returns newest question from the database.
        return Question.query.order_by(Question.id.desc()).first()


# Gets quiz questions to pass to views.
class Quiz:
    def __init__(self, form_data=None):
        self.form_data = form_data
        self.data = SimpleNamespace(success=True)
        # Verifies fields
        if (not hasattr(form_data, 'quiz_category') or
                not hasattr(form_data, 'previous_questions')):
            raise StatusError(ERROR_422, QUIZ_CATEGORY_ERR, 422)
        # Verifies that category id is an integer and not a negative value.
        form_data.quiz_category = string_to_int(form_data.quiz_category,
                                                QUIZ_CATEGORY_ERR)
        if form_data.quiz_category < 0:
            raise StatusError(ERROR_422, QUIZ_CATEGORY_ERR, 422)
        # Verifies that previous questions are passed as a list
        # and are only integers.
        if type(form_data.previous_questions) == list:
            for question in form_data.previous_questions:
                question = string_to_int(question, PREVIOUS_LIST_ERR)
        else:
            raise StatusError(ERROR_422, PREVIOUS_LIST_ERR, 422)

        all_questions = self.get_quizz_questions(form_data.quiz_category)
        # Verifies that there are quiz questions.
        if len(all_questions) < 1:
            raise StatusError(ERROR_404, CATEGORY_NOT_FOUND, 404)
        # Selects list of questions that are not in previous questions.
        available_questions = [question for question in all_questions if
                               question.id not in form_data.previous_questions]
        # If the list of available questions becomes empty, passes
        # None to the view as a quiz end condition.
        if available_questions:
            this_question = random.choice(available_questions).format()
        else:
            this_question = None
        # Structures data and builds reponse JSON.
        self.data.question = this_question
        self.response = jsonify(self.data.__dict__), 200

    def get_quizz_questions(self, category_id):
        # Gets questions by category, or gets all questions
        # if category id is set to 0.
        if category_id != 0:
            return Questions().get_questions_by_category(str(category_id))
        else:
            return Questions().get_all_questions()


# Creates pagination for views.
class QuestionsPage:
    def __init__(self, request, question_query):
        page = request.args.get('page')

        # If page is none, returns all questions
        if page is None:
            start = 0
            stop = None
        # Checks if page can be converted to a positive integer, and
        # paginates response. Otherwise, returns a 422 error.
        else:
            page = string_to_int(page, PAGE_INT_ERR)
            if page < 1:
                raise StatusError(ERROR_422, PAGE_INT_ERR, 422)
            # Page length can be configured in config.py
            start = (page - 1) * QUESTIONS_PER_PAGE
            stop = start + QUESTIONS_PER_PAGE
        # Formats questions for views.
        self.list = (([question.format() for question
                       in question_query])[start:stop])
