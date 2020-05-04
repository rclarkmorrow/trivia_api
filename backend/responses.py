""" ---------------------------------------------------------------------------
# Imports
# --------------------------------------------------------------------------"""


import random
from flask import jsonify
from helpers import CategoriesData, QuestionsData, QuestionsPage


""" ---------------------------------------------------------------------------
# Response Classes
# --------------------------------------------------------------------------"""


# Get categories response object
class GetCategoriesReponse():
    def __init__(self):
        category_data = CategoriesData()
        self.response = jsonify({
            'success': True,
            'categories': category_data.category_list
        }), 200


#  Get questions response object
class GetQuestionsResponse():
    def __init__(self):
        questions_data = QuestionsData()
        categories_data = CategoriesData()
        self.response = jsonify({
            'success': True,
            'questions': questions_data.question_list,
            'total_questions': questions_data.total_questions,
            'current_category': [],
            'categories': categories_data.category_list
        }), 200
