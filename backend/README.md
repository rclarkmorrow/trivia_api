# Trivia API Backend

This is a functional backend for a trivia game. It's core features allow questions to be viewed, searched, created and deleted.

## Optional configuration

By default the questions are provided with pagination. The default number of questions per page is set to 10. This can be changed by editing the constant 'QUESTIONS\_PER\_PAGE' in:

`/backend/config.py`

The API also comees with unittesting so functionality can be verified after making changes.


## Endpoints

### Success/failure
All endpoints return success/failure key value pairs in the response objects:

```
Success: { 
'success' : true
}

Failure: {
  "description": "<additional context, or instructions>", 
  "error": 4xx, 
  "message": "<message for 4xx>", 
  "success": false
}

```

#### Categories

Fetches a dictionary of categories in which the keys are the ids and the value is the corresponding string of the category

* Method: GET
*  Request Arguments: None
* Returns:
	* category key with key-value pairs
	* success

```
GET '/api/categories'

returns: {
   "categories": {
   "1": "Science", 
   "2": "Art", 
   "3": "Geography", 
   "4": "History", 
   "5": "Entertainment", 
   "6": "Sports"
   },
   "success": true
}

```
#### Questions
Fetches questions from the database, with categories, total questions, and a current category.

* Method: GET
* Request arguments (optional): '?page=<int\>'  returns a paginated list of 10 questions.
* Returns an object with keys of type string:
	* categories as a key with key-value pairs
	* current_category as empty list
	* questions as a key with key-value pairs
	* total_questions with an integer (total questions in the database)
	* success
```
GET '/api/questions'
// returns all questions
GET '/api/questions?page=1'
// returns paginated questions

returns: {
  "categories": {
    "1": "Science", 
    "2": "Art", 
    "3": "Geography", 
    "4": "History", 
    "5": "Entertainment", 
    "6": "Sports"
  }, 
  "current_category": [],
  "questions": [
    {
      "answer": "Tom Cruise", 
      "category": 5,
      "difficulty": 4,
      "id": 4,
      "question": "What actor did author Anne Rice first denounce, then praise in the role of her beloved Lestat?"
    }, 
    {
      "answer": "Maya Angelou", 
      "category": 4,
      "difficulty": 2,
      "id": 5, 
      "question": "Whose autobiography is entitled 'I Know Why the Caged Bird Sings'?"
    },
    "total_questions": 31,
    "success": true
}
   
```
### Questions by category
Fetches questions by category id and returns a list of questions, and total question count.

* method: GET
* Required arguments: category_id integer,  '?page=<int>' (optional) returns a paginated list of 10 questions.
* Returns:
	* current\_category as category_id
	* questions as a key with a list of key-value pairs
	* total_questions with an integer (in the caregory)
	* success
```
GET `/api/categories/1/questions`
// returns all questions for category
GET `/api/categories/1/questions?page=1`
// returns paginated questions for category

returns: {
  "current_category": 2,
  "questions": [
    {
      "answer": "Mona Lisa", 
      "category": 2,
      "difficulty": 3,
      "id": 17,
      "question": "La Giaconda is better known as what?"
    }, 
    {
      "answer": "One", 
      "category": 2,
      "difficulty": 4,
      "id": 18,
      "question": "How many paintings did Van Gogh sell in his lifetime?"
    }
  ], 
  "total_questions": 3,
  "success": true
}
```
### Questions by search
Returns quesstion based on search terms. The search is case-insensitve and matches on any string value in a question body (e.g. 'A' will return questions with any words containing 'a' or 'A')

* method: POST
* required arguments: JSON body
* Returns:
	* current_category as empty list
	* questions as a key with a list of key-value pairs
	* success
```
POST `/api/questions/`
JSON: {
  "search_term": "<key words>"
}

returns: {
  "current_category": [], 
  "questions": [
    {
      "answer": "Maya Angelou", 
      "category": 4, // integer
      "difficulty": 2, // integer
      "id": 5, // integer
      "question": "Whose autobiography is entitled 'I Know Why the Caged Bird Sings'?"
    }, 
    {
      "answer": "Tom Cruise", 
      "category": 5, // integer
      "difficulty": 4, // integer
      "id": 4,  // integer 
      "question": "What actor did author Anne Rice first denounce, then praise in the role of her beloved Lestat?"
    }, 
    "total_questions": 13 // integer
    "success": true 
}
```
### Add question
Adds a new question to the database. All question fields are required for a successful request.

* method: POST
* Request arguments: JSON body
* Returns: success, or failure response
```
POST `/api/questions`
JSON: {
   "question": "What is the airspeed velocity of an unladen swallow?",
   "answer": "What do you mean? An African or European swallow?",
   "difficulty": 5, 
   "category": 1 
}
        
 returns: {
  "created": 77, //  id for new question
  "success": true
}

```
### Delete questions
Deletes a question from the database.

* method: DELETE
* Request arguments: question_id integer
* Returns: 
	* deleted question id
	* questions as a key with key-value pairs
	* total_questions
	* success
```
DELETE `/api/questions/42'

returns: {
  "deleted": 42, // id of deleed question
  "questions": [
    {
      "answer": "Tom Cruise", 
      "category": 5, 
      "difficulty": 4, 
      "id": 4, 
      "question": "What actor did author Anne Rice first denounce, then praise in the role of her beloved Lestat?"
    }, 
    {
      "answer": "Maya Angelou", 
      "category": 4, 
      "difficulty": 2, 
      "id": 5, 
      "question": "Whose autobiography is entitled 'I Know Why the Caged Bird Sings'?"
    },
   "success": true, 
  "total_questions": 40
}
```
### Play quiz

* method: POST
* Required arguments: JSON Body 
* Returns: 
	* random question from the database by category, or from all questions if category is set to 0 (zero).
	* success
```
POST `/api/quizzes'
JSON {
"previous_questions": [], 
"quiz_category": 1
}
 // Previous_questions is a list of quetion id integers, any question ids included here will be excluded from random results. Use case: prevent a player from receiving a questions more than once.

returns: {
  "question": {
    "answer": "Tom Cruise", 
    "category": 5, 
    "difficulty": 4, 
    "id": 4, 
    "question": "What actor did author Anne Rice first denounce, then praise in the role of her beloved Lestat?"
  }, 
  "success": true
}
```

## Getting Started

### Installing Dependencies

#### Python 3.7

Follow instructions to install the latest version of python for your platform in the [python docs](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python)

#### Virtual Enviornment

We recommend working within a virtual environment whenever using Python for projects. This keeps your dependencies for each project separate and organaized. Instructions for setting up a virual enviornment for your platform can be found in the [python docs](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/)

#### PIP Dependencies

Once you have your virtual environment setup and running, install dependencies by naviging to the `/backend` directory and running:

```bash
pip install -r requirements.txt
```

This will install all of the required packages we selected within the `requirements.txt` file.

##### Key Dependencies

- [Flask](http://flask.pocoo.org/)  is a lightweight backend microservices framework. Flask is required to handle requests and responses.

- [SQLAlchemy](https://www.sqlalchemy.org/) is the Python SQL toolkit and ORM we'll use handle the lightweight sqlite database. You'll primarily work in app.py and can reference models.py. 

- [Flask-CORS](https://flask-cors.readthedocs.io/en/latest/#) is the extension we'll use to handle cross origin requests from our frontend server. 

## Database Setup
With Postgres running, restore a database using the trivia.psql file provided. From the backend folder in terminal run:
```bash
psql trivia < trivia.psql
```

## Running the server

From within the `backend` directory first ensure you are working using your created virtual environment.

To run the server, execute:

```bash
export FLASK_APP=flaskr
export FLASK_ENV=development
flask run
```

Setting the `FLASK_ENV` variable to `development` will detect file changes and restart the server automatically.

Setting the `FLASK_APP` variable to `flaskr` directs flask to use the `flaskr` directory and the `__init__.py` file to find the application. 


####Original instructions preserved below:

<br /><br />

## Tasks

One note before you delve into your tasks: for each endpoint you are expected to define the endpoint and response data. The frontend will be a plentiful resource because it is set up to expect certain endpoints and response data formats already. You should feel free to specify endpoints in your own way; if you do so, make sure to update the frontend or you will get some unexpected behavior. 

1. Use Flask-CORS to enable cross-domain requests and set response headers. 
2. Create an endpoint to handle GET requests for questions, including pagination (every 10 questions). This endpoint should return a list of questions, number of total questions, current category, categories. 
3. Create an endpoint to handle GET requests for all available categories. 
4. Create an endpoint to DELETE question using a question ID. 
5. Create an endpoint to POST a new question, which will require the question and answer text, category, and difficulty score. 
6. Create a POST endpoint to get questions based on category. 
7. Create a POST endpoint to get questions based on a search term. It should return any questions for whom the search term is a substring of the question. 
8. Create a POST endpoint to get questions to play the quiz. This endpoint should take category and previous question parameters and return a random questions within the given category, if provided, and that is not one of the previous questions. 
9. Create error handlers for all expected errors including 400, 404, 422 and 500. 

REVIEW_COMMENT
```
This README is missing documentation of your endpoints. Below is an example for your endpoint to get all categories. Please use it as a reference for creating your documentation and resubmit your code. 

Endpoints
GET '/categories'
GET ...
POST ...
DELETE ...

GET '/categories'
- Fetches a dictionary of categories in which the keys are the ids and the value is the corresponding string of the category
- Request Arguments: None
- Returns: An object with a single key, categories, that contains a object of id: category_string key:value pairs. 
{'1' : "Science",
'2' : "Art",
'3' : "Geography",
'4' : "History",
'5' : "Entertainment",
'6' : "Sports"}

```


## Testing
To run the tests, run
```
dropdb trivia_test
createdb trivia_test
psql trivia_test < trivia.psql
python test_flaskr.py
```