# Full Stack Trivia API Backend

## Getting Started

### Requirements & Installing Dependencies
Developers must have Python 3.7 & pip3 installed on their device to be able to run the server.

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
First make sure to modify the database credentials in models.py (db username & password) are added.
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


## Endpoints
### Error handler
- Returns: a simple object as the following,
in case of invalid endpoint, un-supported HTTP request method to some known endpoint.
```
{
"code": 404,
"message": "Invalid endpoint or maybe HTTP request method is not support for this endpoint.",
"success": false
}
```
> or if the request didn't fullfil the expectations or there are some missing params. not sent with the request.
```
{
"code": 400,
"message": "Bad request as maybe the resource requested is not found, missing fields or wrong request.",
"success": false
}
```
> ...etc, other codes (422 => un-processable request).

### Success request handler
- Returns: Any successful request would have the following output with different/variable data values
```
{
  "code": 200,
  "data": [...] or {...} or null,
  "success": true
}
```

### GET /categories
- Fetches a list of dictionaries of categories 
- Request Arguments: None
- Returns: A list of objects each with two key value pairs which are categories, (id: 'category_id', type: 'category_title').
- Sample request: ```curl http://127.0.0.1:5000/categories```
```
{
  "data": [
    {
      "id": 1,
      "type": "Science"
    },
    {
      "id": 2,
      "type": "Art"
    },
    {
      "id": 3,
      "type": "Geography"
    },
    ...
  ],
  "code": 200,
  "success": true
}
```

### GET /questions
- Fetches a list of dictionaries of available questions 
- Request Arguments: None
- Request queries/parameters: ?page={int} - page refers to the page number of questions page (10 questions retrieved at max. in each request). 
- Returns: An object with
> categories: object that has all the available categories each with two key value pairs like the returned data of /categories endpoint.
> current_category: the id of the current category.
> questions: object that contains a list of objects of the questions.
> total_questions: declares the number of total questions in database.
```
- Sample request: ```curl http://127.0.0.1:5000/questions```

{
  "code": 200,
  "data": {
    "categories": [
        {
          "id": 1,
          "type": "Science"
        },
        {
          "id": 2,
          "type": "Art"
        },
        ...
      ],
      "current_category": 4,
      "questions": [
        {
          "answer": "Maya Angelou",
          "category": 4,
          "difficulty": 2,
          "id": 5,
          "question": "Whose autobiography is entitled 'I Know Why the Caged Bird Sings'?"
        },
        {
          "answer": "Muhammad Ali",
          "category": 4,
          "difficulty": 1,
          "id": 9,
          "question": "What boxer's original name is Cassius Clay?"
        },
        ...
      ],
    "total_questions": 18
  },
  "success": true
}
```

### DELETE /questions/<int:question_id>
- Delete a specific question from the database.
- Request Arguments:
  > question_id (int): the id of the target question to be deleted.
- Returns: An object with the deleted question data.
- Sample request: ```curl http://127.0.0.1:5000/questions/20 -X DELETE```
```
{
  "code": 200,
  "data": {
    "answer": "Hello, World!",
    "category": 4,
    "difficulty": 1,
    "id": 20,
    "question": "First sentence most beginner programmers write?"
  },
  "success": true
}
```

### POST /questions
- Adds a new question to a specfic category.
- Request Arguments: None
- Request Body:
    >> question(string): The question text.
    > answer(string): The answer text.
    > category(int): The id of the category that will have that question.
    > difficulty(int): The difficulty score of that question's answer.
- Returns: An object with the added question data.
- Sample request: ```curl http://127.0.0.1:5000/questions -X POST -H "Content-Type: application/json" -d '{"question":"who is the CEO of google?","answer":"Sundar Pichai","category":"3","difficulty":"4"}'```
```
{
  "code": 200,
  "data": {
    "answer": "Sundar Pichai",
    "category": 3,
    "difficulty": 4,
    "id": 7,
    "question": "who is the CEO of google?"
  },
  "success": true
}
```

### POST /questions/search
- Search for questions that contains the search term
- Request Arguments: None
- Request Body:
  > search_term(string): the query text that the questions would contain it.
- Returns: A list with the found questions objects
- Sample request: ```curl http://127.0.0.1:5000/questions/search -X POST -H "Content-Type: application/json" -d '{"search_term":"bo"}'```
```
{
  "code": 200,
  "data": [
    {
      "answer": "Muhammad Ali",
      "category": 4,
      "difficulty": 1,
      "id": 9,
      "question": "What boxer's original name is Cassius Clay?"
    },
    {
      "answer": "Edward Scissorhands",
      "category": 5,
      "difficulty": 3,
      "id": 6,
      "question": "What was the title of the 1990 fantasy directed by Tim Burton about a young man with multi-bladed appendages?"
    }
  ]
  "success": true
}
```

### GET /categories/<int:category_id>/questions
- Fetches a list of dictionaries of available questions for a specific category 
- Request Arguments:
  > category_id(int): the ID of the category to retrieve its questions.
- Returns: An object with
  > current_category: the type of the current category
  > questions: A list that has category's questions objects.
  > total_questions: declares the number of total questions in database for this category.
- Sample request: ```curl http://127.0.0.1:5000/categories/2/questions```
```
{
  "code": 200,
  "data": {
      "current_category": "History",
      "questions": [
        {
          "answer": "Escher",
          "category": 2,
          "difficulty": 1,
          "id": 16,
          "question": "Which Dutch graphic artist\u2013initials M C was a creator of optical illusions?"
        },
        {
          "answer": "Mona Lisa",
          "category": 2,
          "difficulty": 3,
          "id": 17,
          "question": "La Giaconda is better known as what?"
        },
        ...
      ],
    "total_questions": 18
  },
  "success": true
}
```

### POST /quiz
- Fetches a non-repeated random question for being shown in the game
- Request Arguments: None
- Request Body:
  > category_id(int): the ID of the category to get a question related to.
  > previous_questions(list or array): the list of previous questions' IDs for being ignored in having new question.
- Returns: An object with the question object
- Sample request: ```curl http://127.0.0.1:5000/quiz -X POST -H "Content-Type: application/json" -d '{"category_id":3,"previous_questions":[1, 3]}'```
```
{
  "code": 200,
  "data": {
    "answer": "Lake Victoria", 
    "category": 3,
    "difficulty": 2,
    "id": 13,
    "question": "What is the largest lake in Africa?"
  },
  "success": true
}
```


## Testing
To run the tests, run
```
dropdb trivia_test (if it exists)
createdb trivia_test
psql trivia_test < trivia.psql
-- make sure that you modified your database credentials of (test_falskr.py) as added db username & password --
python test_flaskr.py
```

## Authors
Team of Udacity, Ahmed M.