""" ---------------------------------------------------------------------------
# Imports
# --------------------------------------------------------------------------"""


from flask import request, abort
from models import Category, Question
from config import QUESTIONS_PER_PAGE


""" ---------------------------------------------------------------------------
# Helpers
# --------------------------------------------------------------------------"""


# -----------------------------------------------------------------------------
# Helper Classes
# -----------------------------------------------------------------------------

# Categories data object
class CategoriesData():
    def __init__(self):
        category_query = Category.query.order_by(Category.type).all()
        self.category_list = {category.id: category.type for
                              category in category_query}
        if len(self.category_list) < 1:
            raise Exception('404 : Category list not found')


# Questions data object
class QuestionsData():
    def __init__(self):
        question_query = Question.query.order_by(Question.id).all()
        questions = QuestionsPage(request, question_query)
        self.question_list = questions.question_list
        # self.question_list = paginate_questions(request, question_query)

        if len(self.question_list) < 1:
            raise Exception('404')

        self.total_questions = len(question_query)


# Page object for pagination
class QuestionsPage():
    def __init__(self, request, question_list):
        if request is None or question_list is None:
            raise Exception('args not provided')

        page = request.args.get('page', 1, type=int)

        if page < 1:
            raise Exception('422')

        start = (page - 1) * QUESTIONS_PER_PAGE
        stop = start + QUESTIONS_PER_PAGE

        self.question_list = (([question.format() for question
                                in question_list])[start:stop])


# -----------------------------------------------------------------------------
# Helper Functions
# -----------------------------------------------------------------------------


# Handles errors
def handle_errors(e):
    if '500' in str(e):
        abort(500)
    elif '404' in str(e):
        abort(404)
    else:
        abort(422)
