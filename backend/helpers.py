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
class CategoriesData:
    def __init__(self):
        category_query = get_all_categories()
        self.list = {category.id: category.type for
                     category in category_query}
        if len(self.list) < 1:
            raise Exception('404 : Category list not found')


# Questions data object
class QuestionsData:
    def __init__(self):
        question_query = get_all_questions()
        questions = QuestionsPage(request, question_query)
        self.list = questions.question_list
        # self.question_list = paginate_questions(request, question_query)

        if len(self.list) < 1:
            raise Exception('404')

        self.total = len(question_query)


# Page object for pagination
class QuestionsPage:
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

# Gets all categories.
def get_all_categories():
    return Category.query.order_by(Category.type).all()


# Gets all questions.
def get_all_questions():
    return Question.query.order_by(Question.id).all()


# Gets a single question by id.
def get_single_question(question_id):
    this_question = Question.query.filter(
        Question.id == question_id).one_or_none()
    if this_question is None:
        raise Exception('404')
    return(this_question)


# Handles errors.
def handle_errors(e):
    if '500' in str(e):
        abort(500)
    elif '404' in str(e):
        abort(404)
    else:
        abort(422)
