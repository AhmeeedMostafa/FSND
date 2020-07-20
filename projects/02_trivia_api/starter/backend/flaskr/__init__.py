import os
import sys
import random
from flask import Flask, request, abort
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS


from models import setup_db, Question, Category
from utils import success_response, error_response

QUESTIONS_PER_PAGE = 10

def create_app(test_config=None):
  # create and configure the app
  app = Flask(__name__)
  setup_db(app)
  
  '''
  Set up CORS. Allow '*' for origins.
  '''
  CORS(app,
    resources={
      '*': {
        'origins': '*'
      }
    }
  )

  '''
  Use the after_request decorator to set Access-Control-Allow
  '''
  @app.after_request
  def after_request(response):
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Methods'] = 'GET, POST, DELETE'
    return response

  '''
  Create an endpoint categories to handle GET requests for all available categories.
  '''
  @app.route('/categories')
  def categories():    
    categories = get_formatted_categories()
    if categories:
      return success_response(categories)
    else:
      return error_response()


  '''
  Create an endpoint to handle GET requests for questions, 
  including pagination (every 10 questions). 
  This endpoint should return a list of questions, 
  number of total questions, current category, categories. 
  '''
  @app.route('/questions')
  def questions():
    try:
      page = request.args.get('page', 1, type=int)
      offset = (page - 1) * QUESTIONS_PER_PAGE
      take = offset + QUESTIONS_PER_PAGE

      questions = Question.query.all()
      requested_questions = questions[offset:take]

      formatted_questions = [question.format() for question in requested_questions]
      categories = get_formatted_categories()

      data = {
        'questions': formatted_questions,
        'total_questions': len(questions),
        'categories': categories,
        'current_category': requested_questions[0].category
      }

      return success_response(data)
    except:
      return abort(400)


  '''
  Create an endpoint to DELETE question using a question ID.
  '''
  @app.route('/questions/<int:question_id>', methods=['DELETE'])
  def delete_question(question_id):
    try:
      if question_id:
        question = Question.query.get(question_id)
        question.delete()
        

        return success_response(question.format())
      else:
        return error_response(message='Question #ID is required.')
    except:
      return abort(400)

  '''
  An endpoint to POST a new question,  which will require the question and answer text, category, and difficulty score.
  '''
  @app.route('/questions', methods=['POST'])
  def add_question():
    try:
      form_data = request.get_json()

      if form_data['question'] \
        and form_data['answer'] \
        and form_data['category'] \
        and form_data['difficulty']:
          question = Question(**form_data)
          question.insert()

          return success_response(question.format())
      else:
        return error_response(message='Question, answer, category & difficulty score are required fields.')

    except:
      return abort(400)
        

  '''
  A POST endpoint to get questions based on a search term. 
  It should return any questions for whom the search term 
  is a substring of the question. 
  '''
  # Notice: It's better to make the search GET request passing the search term in param (?search=)
  # but it's impelmented as this route (which is not the best endpoint) for avoiding duplications of same endpoint & method.
  @app.route('/questions/search', methods=['POST'])
  def search_questions():
    try:
      search_term = request.get_json()['search_term']

      if search_term:
        found_questions = Question.query.filter(Question.question.ilike(f'%{search_term}%')).all()
        questions = [question.format() for question in found_questions]

        data = {
          'questions': questions,
          'total_questions': len(questions)
        }

        return success_response(data)
      else:
        return error_response(message="Empty search query.")

    except:
      return abort(400)

  '''
  Create a GET endpoint to get questions based on category.  
  '''
  @app.route('/categories/<int:category_id>/questions')
  def get_category_questions(category_id):
    try:
      if category_id:
        questions = Question.query.filter(Question.category == category_id).all()
        if len(questions) == 0:
          return error_response(message="No questions are founds inside this category.")
        
        formatted_questions = [question.format() for question in questions]
        category = Category.query.get(category_id).type

        data = {
          'current_category': category,
          'questions': formatted_questions,
          'total_questions': len(formatted_questions)
        }

        return success_response(data)
      else:
        return error_response(message="Invalid category #ID is provided.")
    except:
      return abort(400)


  '''
  A POST endpoint to get questions to play the quiz. 
  This endpoint should take category and previous question parameters 
  and return a random questions within the given category, 
  if provided, and that is not one of the previous questions. 
  '''
  @app.route('/quiz', methods=['POST'])
  def get_unique_question():
    try:
      category_id = request.get_json()['category_id']
      previous_questions = request.get_json()['previous_questions']

      if (category_id or category_id == 0) and isinstance(previous_questions, list):
        if category_id == 0:
          questions = Question.query.filter(~Question.id.in_(previous_questions)).all()
        else:
          questions = Question.query.filter(Question.category == category_id, ~Question.id.in_(previous_questions)).all()
        
        if len(questions) == 0:
          return success_response(None)

        selected_question = random.choice(questions).format()

        return success_response(selected_question)
      else:
        return success_response(message='Category #ID and previous questions must be provided.')
    except:
      return abort(400)


  def get_formatted_categories():
    categories = Category.query.all()
    if len(categories) == 0:
      return False;

    formatted_categories = [category.format() for category in categories]

    return formatted_categories

  '''
  Error handlers for all expected errors 
  including 404, 422. and 400 
  '''
  @app.errorhandler(404)
  def endpoint_not_found(error):
    return error_response(message='Invalid endpoint or maybe HTTP request method is not support for this endpoint.',
      code=404), 404
  
  @app.errorhandler(422)
  def content_processing_failed(error):
    return error_response(message='Unable to process your request, please try again later.', code=422), 422
  
  @app.errorhandler(400)
  def endpoint_not_found(error):
    return error_response(), 400

  
  return app

    