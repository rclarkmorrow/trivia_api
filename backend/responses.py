""" ---------------------------------------------------------------------------
# Imports
# --------------------------------------------------------------------------"""


import random
from flask import jsonify
from helpers import CategoriesData, QuestionsData, QuestionsPage
from helpers import get_single_question

""" ---------------------------------------------------------------------------
# Response Classes
# --------------------------------------------------------------------------"""


# Gets categories response object.
class Categories:
    def __init__(self):
        category_data = CategoriesData()
        self.response = jsonify({
            'success': True,
            'categories': category_data.list
        }), 200


#  Gets questions response object.
class Questions:
    def __init__(self):
        questions_data = QuestionsData()
        categories_data = CategoriesData()
        self.response = jsonify({
            'success': True,
            'questions': questions_data.list,
            'total_questions': questions_data.total,
            'current_category': [],
            'categories': categories_data.list
        }), 200


# Gets delete question response object.
class DeleteQuestion:
    def __init__(self, question_id):
        this_question = get_single_question(question_id)
        this_question.delete()
        questions_data = QuestionsData()

        self.response = jsonify({
            'success': True,
            'deleted': question_id,
            'questions': questions_data.list,
            'total_questions': questions_data.total
        })
