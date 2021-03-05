import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS, cross_origin
import random

from models import setup_db, Question, Category
from flask.templating import render_template


QUESTIONS_PER_PAGE = 10


def paginate_questions(request, selection):
    page = request.args.get('page', 1, type=int)
    start = (page - 1) * QUESTIONS_PER_PAGE
    end = start + QUESTIONS_PER_PAGE

    questions = [question.format() for question in selection]
    current_questions = questions[start:end]

    return current_questions


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    setup_db(app)

    # CORS(app)
    ##
    # cors = CORS(app, resources={r"/api/*": {"origins": "*"}})
    CORS(app, resources={r"/api/*": {'origins': '*'}})

    '''
  
  @TODO: Set up CORS. Allow '*' for origins. Delete the sample route after completing the TODOs
  '''

    '''
  @TODO: Use the after_request decorator to set Access-Control-Allow
  '''
    @app.after_request
    def after_request(response):
        response.headers.add('Access-Control-Allow-Headers',
                             'Content-Type,Authorization,true')
        response.headers.add('Access-Control-Allow-Methods',
                             'GET,PATCH,POST,DELETE,OPTIONS')
        return response

    '''
  
  @TODO: 
  Create an endpoint to handle GET requests 
  for all available categories.
  '''
    @app.route('/categories')
    def retrieve_categories():
        categories = Category.query.order_by(Category.type).all()

        if len(categories) == 0:
            abort(404)

        return jsonify({
            'success': True,
            'categories': {category.id: category.type for category in categories}
        })

    '''
  @TODO: 
  Create an endpoint to handle GET requests for questions, 
  including pagination (every 10 questions). 
  This endpoint should return a list of questions, 
  number of total questions, current category, categories. 
  
  

  TEST: At this point, when you start the application
  you should see questions and categories generated,
  ten questions per page and pagination at the bottom of the screen for three pages.
  Clicking on the page numbers should update the questions. 
  '''
    @app.route('/questions', methods=['GET'])
    def retrieve_questions():
        page = request.args.get('page', 1, type=int)
        selection = Question.query.order_by(Question.id).all()
        current_questions = paginate_questions(request, selection)
        total_questions = len(selection)
        categories = Category.query.all()
        categories_dict = {}
        for category in categories:
            categories_dict[category.id] = category.type

        if len(current_questions) == 0:
            abort(404)

        return jsonify({
            'success': True,
            'questions': current_questions,
            'total_questions': total_questions,
            'categories': categories_dict

        })
    '''
  @TODO: 
  Create an endpoint to DELETE question using a question ID. 

  TEST: When you click the trash icon next to a question, the question will be removed.
  This removal will persist in the database and when you refresh the page. 
  '''
    @app.route('/questions/<int:question_id>', methods=['DELETE'])
    def delete_question(question_id):

        try:
            question = Question.query.filter(
                Question.id == question_id).one_or_none()

            if question is None:
                abort(404)

            question.delete()
            selection = Question.query.order_by(Question.id).all()
            current_questions = paginate_questions(request, selection)

            return jsonify({
                'success': True,
                'deleted': question_id,
                'questions': current_questions,
                'total_questions': len(Question.query.all())
            })
        except:
            abort(422)
    '''
  @TODO: 
  Create an endpoint to POST a new question, 
  which will require the question and answer text, 
  category, and difficulty score.

  TEST: When you submit a question on the "Add" tab, 
  the form will clear and the question will appear at the end of the last page
  of the questions list in the "List" tab.  
  '''

    @app.route('/questions', methods=['POST'])
    def create_question():
        body = request.get_json()

        new_question = body.get('question', None)
        new_answer = body.get('answer', None)
        new_category = body.get('category', None)
        new_difficulty = body.get('difficulty', None)

        try:
            question = Question(question=new_question, answer=new_answer,
                                category=new_category, difficulty=new_difficulty)
            question.insert()

            selection = Question.query.order_by(Question.id).all()
            current_questions = paginate_questions(request, selection)

            return jsonify({
                'success': True,
                'created': question.id,
                'questions': current_questions,
                'total_questions': len(Question.query.all())
            })

        except:
            abort(422)

    '''
  @TODO: 
  Create a POST endpoint to get questions based on a search term. 
  It should return any questions for whom the search term 
  is a substring of the question. 

  TEST: Search by any phrase. The questions list will update to include 
  only question that include that string within their question. 
  Try using the word "title" to start. 
  '''

    @app.route('/questions/search', methods=['GET', 'POST'])
    def search_questions():
        """This endpoint returns questions from a search term. """

        data = request.get_json()
        ##
        if(data['searchTerm']):
            #search_term = data['searchTerm']
            search_term = data.get('searchTerm', '')

        # if search_term == '':
        #     abort(422)

        questions = Question.query.filter(
            Question.question.ilike(f'%{search_term}%')).all()
        # questions = Question.query.filter(Question.question.ilike('%{}%'.format(search_term))).all()
        if questions == []:
            abort(404)

        output = paginate_questions(request, questions)

        return jsonify({
            'success': True,
            'questions': output,
            'total_questions': len(questions)
        })

        # questions = Question.query.filter(Question.question.ilike(f'%{search_term}%')).all()

        # if len(questions) == 0:
        #     abort(404)

        #   # paginate questions
        # paginated_questions = paginated_questions(request, questions)

        # return jsonify({
        #     'success': True,
        #     'questions': paginated_questions,
        #     'total_questions': len(questions)
        # }), 200

    '''
  @TODO: 
  Create a GET endpoint to get questions based on category. 

  TEST: In the "List" tab / main screen, clicking on one of the 
  categories in the left column will cause only questions of that 
  category to be shown. 
  '''
    @app.route('/categories/<int:category_id>/questions', methods=['GET', 'POST'])
    def get_question_by_category(category_id):
        # question = Question.query.filter(Question.id == question_id).one_or_none()
        #category = Category.query.filter(Category.id==id).one_or_none()
        category = Category.query.get(category_id)
        # print (category,id)
        if (category is None):
            abort(404)
        else:
            try:
                questions = Question.query.filter(
                    Question.category == str(category_id)).all()
                # book = Book.query.filter(Book.id == book_id).one_or_none()
                # questions = Question.query.filter_by(category=category.id).all()
                current_questions = paginate_questions(request, questions)
                #[question.format() for question in questions]
                return jsonify({
                    'success': True,
                    'questions': current_questions,
                    # 'questions': [question.format() for question in questions],
                    'total_questions': len(questions),
                    'current_category': category_id
                })
            except:
                abort(500)

    '''
    # body = request.get_json()
    
    # try:

    #   category = Category.query.filter(Category.id == category_id).one_or_none()
    #   if category is None:
    #     abort(404)

    #   questions = Question.query.filter_by(category=category.id).all()
    #   current_questions = paginate_questions(request, questions)
    #   return jsonify({
        
    #     'success':True,
    #     'questions': current_questions,
    #     'current_category':category.type,
    #     'total_questions':len(questions)

    #   })
    # except:
    #   abort(500)

  
    # category=Category.query.get(id)

    # if (category is None):

    #   abort(404)
    # try:

    #   questions = Question.query.filter_by(category=category.id).all()
    
    #   current_questions = paginate_questions(request, questions)

    #   return jsonify({

    #     'success':True,
    #     'questions': current_questions,
    #     'current_category':category.type,
    #     'total_questions':len(questions)

    #   })
    # except:
    #   abort(500)

  '''

    '''
  @TODO: 
  Create a POST endpoint to get questions to play the quiz. 
  This endpoint should take category and previous question parameters 
  and return a random questions within the given category, 
  if provided, and that is not one of the previous questions. 

  TEST: In the "Play" tab, after a user selects "All" or a category,
  one question at a time is displayed, the user is allowed to answer
  and shown whether they were correct or not. 
  '''
    @app.route('/quizzes', methods=['POST'])
    def get_random_quiz_question():
        '''
        Handles POST requests for playing quiz.
        '''
        body = request.get_json()

        previous = body.get('previous_questions')

        category = body.get('quiz_category')

        if ((category is None) or (previous is None)):
            abort(400)

        if (category['id'] == 0):
            questions = Question.query.all()
        else:
            questions = Question.query.filter_by(category=category['id']).all()

        total = len(questions)

        def get_random_question():
            return questions[random.randrange(0, len(questions), 1)]

        def check_if_used(question):
            used = False
            for q in previous:
                if (q == question.id):
                    used = True

            return used

        question = get_random_question()
        while (check_if_used(question)):
            question = get_random_question()

            if (len(previous) == total):
                return jsonify({
                    'success': True
                })

        return jsonify({
            'success': True,
            'question': question.format()
        })

    '''
  @TODO: 
  Create error handlers for all expected errors 
  including 404 and 422. 
  '''
    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
            "success": False,
            "error": 404,
            "message": "resource not found"
        }), 404

    @app.errorhandler(422)
    def unprocessable(error):

        return jsonify({
            "success": False,
            "error": 422,
            "message": "unprocessable"
        }), 422

    @app.errorhandler(400)
    def bad_request(error):

        return jsonify({
            "success": False,
            "error": 400,
            "message": "bad request"
        }), 400

    @app.errorhandler(500)
    def Internal_Server_Error(error):

        return jsonify({
            "success": False,
            "error": 500,
            "message": "Internal Server Error"
        }), 500

    return app
