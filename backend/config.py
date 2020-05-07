""" ---------------------------------------------------------------------------
# Config
# --------------------------------------------------------------------------"""

# App config
QUESTIONS_PER_PAGE = 10

# Error messages
ERROR_400 = 'bad request'
ERROR_404 = 'resource not found'
ERROR_405 = 'method not allowed'
ERROR_422 = 'request unprocessable'
ERROR_500 = 'internal server error'

# Descriptions

INVALID_SYNTAX = 'invalid syntax, or data not provided'
QUESTION_NOT_FOUND = 'question not found'
NO_CATEGORIES_FOUND = 'no categories found'
CATEGORY_NOT_FOUND = 'category not found, out of range or has no questions'
NO_QUESTIONS_FOUND = 'page out of range, no questions found'
CATEGORY_INT_ERR = ('invalid input, {category_id} in /api/categories/'
		    '{category_id}/questions must be a positive integer')
PAGE_INT_ERR = ('invalid input, {page_num} in /api/questions/?page={page_num}, '
                'must be a positive integer')
QUESTION_FIELDS_ERR = ('invalid input, a new question needs all fields: '
		       'question, answer, difficulty, category')
PREVIOUS_LIST_ERR = 'invalid input, previous_questions must be an empty list or a list of integers'
QUIZ_CATEGORY_ERR = 'invalid input, quiz_category must be zero or a positive integer'
ADD_QUESTION_CATEGORY_ERR = 'invalid input, "category" must be an integer that exists in the database'
ADD_QUESTION_DIFFICULTY_ERR = 'invalid input, "difficulty" must be an integer from 1 to 5'
