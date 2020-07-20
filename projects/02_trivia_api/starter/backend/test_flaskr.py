import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from flaskr import create_app
from models import setup_db, Question, Category


class TriviaTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = "trivia_test"
        # Added database username & password in next 
        self.database_path = "postgres://{}:{}@{}/{}".format('postgres', 'root', 'localhost:5432', self.database_name)
        # self.database_path = "postgres://{}/{}".format('postgres', 'root', 'localhost:5432', self.database_name)
        setup_db(self.app, self.database_path)

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()
    
    def tearDown(self):
        """Executed after reach test"""
        pass


    # Tests starting
    def test_get_categories_with_results(self):
        response = self.client().get('/categories')
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['code'], 200)
        self.assertEqual(data['success'], True)
        self.assertGreaterEqual(len(data['data']), 1)
    
    def test_get_questions_with_results(self):
        response = self.client().get('/questions')
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['code'], 200)
        self.assertEqual(data['success'], True)
        self.assertGreaterEqual(len(data['data']), 1)
    
    def test_delete_question_with_result(self):
        response = self.client().delete('/questions/21')
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['code'], 200)
        self.assertEqual(data['success'], True)
        self.assertGreaterEqual(len(data['data']), 1)
    
    def test_delete_question_with_error(self):
        response = self.client().delete('/questions/10000')
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 400)
        self.assertEqual(data['code'], 400)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Bad request as maybe the resource requested is not found, missing fields or wrong request.')
    
    def test_add_question_with_result(self):
        response = self.client().post('/questions', json={
            'question': 'Test question, what do u think?',
            'answer': 'Yes but sometimes no :D !',
            'category': 2,
            'difficulty': 3
        })
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['code'], 200)
        self.assertEqual(data['success'], True)
    
    def test_add_question_with_error(self):
        response = self.client().post('/questions', json={'question': 'question only, right?'})
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 400)
        self.assertEqual(data['code'], 400)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Bad request as maybe the resource requested is not found, missing fields or wrong request.')
        
    def test_search_question_with_result(self):
        response = self.client().post('/questions/search', json={'search_term': 'box'})
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['code'], 200)
        self.assertEqual(data['success'], True)
        self.assertGreaterEqual(len(data['data']), 1)
    
    def test_search_question_with_error(self):
        response = self.client().post('/questions/search')
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 400)
        self.assertEqual(data['code'], 400)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Bad request as maybe the resource requested is not found, missing fields or wrong request.')

    def test_get_category_question_with_result(self):
        response = self.client().get('/categories/1/questions')
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['code'], 200)
        self.assertEqual(data['success'], True)
        self.assertGreaterEqual(len(data['data']), 1)
    
    def test_get__category_question_with_error(self):
        response = self.client().get('/categories/0/questions')
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['code'], 400)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Invalid category #ID is provided.')
    
    def test_quiz_question_with_result(self):
        response = self.client().post('/quiz', json={
            'category_id': 1,
            'previous_questions': []
        })
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['code'], 200)
        self.assertEqual(data['success'], True)
        self.assertGreaterEqual(len(data['data']), 0)
    
    def test_quiz_question_with_error(self):
        response = self.client().post('/quiz')
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 400)
        self.assertEqual(data['code'], 400)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Bad request as maybe the resource requested is not found, missing fields or wrong request.')

    def test_not_found_route_handler(self):
        response = self.client().get('/not-found-route')
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 404)
        self.assertEqual(data['code'], 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Invalid endpoint or maybe HTTP request method is not support for this endpoint.')

# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()