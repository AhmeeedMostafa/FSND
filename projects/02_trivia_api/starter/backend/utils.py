from flask import jsonify

def success_response(data, code = 200):
  response = {
    'success': True,
    'data': data,
    'code': code
  }

  return jsonify(response)

def error_response(message = 'Bad request as maybe the resource requested is not found, missing fields or wrong request.', code = 400):
  response = {
    'success': False,
    'message': message,
    'code': code
  }

  return jsonify(response)