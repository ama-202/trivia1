# Full Stack Trivia API Backend

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


REVIEW_COMMENT


Endpoints

GET '/categories'
- Fetches a dictionary of categories in which the keys are the ids and the value is the corresponding string of the category
- Request Arguments: None
- Returns: An object with a single key, categories, that contains a object of id: category_string key:value pairs. 
'''
{'1' : "Science",
'2' : "Art",
'3' : "Geography",
'4' : "History",
'5' : "Entertainment",
'6' : "Sports"}
'''

GET '/questions'
- Returns a list questions.
- Request Arguments: None

curl http://127.0.0.1:5000/questions
  {
      "categories": {
          "1": "Science",
          "2": "Art",
          "3": "Geography",
          "4": "History",
          "5": "Entertainment",
          "6": "Sports"
      },
      "questions": [
          {
              "answer": "Colorado, New Mexico, Arizona, Utah",
              "category": 3,
              "difficulty": 3,
              "id": 164,
              "question": "Which four states make up the 4 Corners region of the US?"
          }
          
DELETE /questions/int:id
Request Arguments: id ,an integer
Deletes a question by id using url parameters.
Returns id of deleted question upon success.

Sample: curl http://127.0.0.1:5000/questions/6 -X DELETE

  {
      "deleted": 6,
      "success": true
  }
  
  
POST /questions
creates a new question
Request Arguments: Creates a new question using JSON request parameters.
Returns JSON object with newly created question, as well as paginated questions.

Sample: curl http://127.0.0.1:5000/questions -X POST -H "Content-Type: application/json" -d '{ "question": "Which US state contains an area known as the Upper Penninsula?", "answer": "Michigan", "difficulty": 3, "category": "3" }'

  {
      "created": 173,
      "question_created": "Which US state contains an area known as the Upper Penninsula?",
      "questions": [
          {
              "answer": "Apollo 13",
              "category": 5,
              "difficulty": 4,
              "id": 2,
              "question": "What movie earned Tom Hanks his third straight Oscar nomination, in 1996?"
          }
    
POST /questions/search    
    Searches for questions 
    Request Arguments: search term in JSON request parameters.
    Returns JSON object with paginated matching questions.

Sample: curl http://127.0.0.1:5000/questions -X POST -H "Content-Type: application/json" -d '{"searchTerm": "which"}'

  {
      "questions": [
          {
              "answer": "Brazil",
              "category": 6,
              "difficulty": 3,
              "id": 10,
              "question": "Which is the only team to play in every soccer World Cup tournament?"
          }
          ],
      "success": true,
      "total_questions": 18
  }


POST /quizzes
 -Allows users to play the quiz game.
 -Uses JSON request parameters of category and previous questions.
 -Returns JSON object with random question not among previous questions.

Sample: curl http://127.0.0.1:5000/quizzes -X POST -H "Content-Type: application/json" -d '{"previous_questions": [20, 21], "quiz_category": {"type": "Science", "id": "1"}}'

  {
      "question": {
          "answer": "Blood",
          "category": 1,
          "difficulty": 4,
          "id": 22,
          "question": "Hematology is a branch of medicine involving the study of what?"
      },
      "success": true
  }


## Testing
To run the tests, run
```
dropdb trivia_test
createdb trivia_test
psql trivia_test < trivia.psql
python test_flaskr.py
```
