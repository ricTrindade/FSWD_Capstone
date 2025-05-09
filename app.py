from models import app, Movie, Actor, db
from flask import jsonify, request, abort
from auth import requires_auth
from datetime import datetime

# Convert date string to date object
def parse_date(date_str):
    try:
        return datetime.strptime(date_str, '%Y-%m-%d').date()
    except ValueError:
        abort(400, description='Invalid date format. Use YYYY-MM-DD.')

# Home route
@app.route('/', methods=['GET'])
def home():

    # Send the response
    return jsonify({
        'success': True,
        'message': 'Welcome to the Movie and Actor API!'
    }), 200

# Login Results
@app.route('/login-results', methods=['GET'])
def login():

    # Send the response
    return jsonify({
        'success': True,
        'message': 'Login successful!'
    }), 200

# Logout
@app.route('/logout', methods=['GET'])
def logout():

    # Send the response
    return jsonify({
        'success': True,
        'message': 'Logout successful!'
    }), 200

# Get all movies
@app.route('/movies', methods=['GET'])
@requires_auth('get:movies')
def get_movies(jwt_payload):

    # Fetch all movies from the database
    movies = Movie.query.all()

    # Send the response
    return jsonify({
        'success': True,
        'movies': [
            {
                'id': movie.id,
                'title': movie.title,
                'release_date': movie.release_date.strftime('%Y-%m-%d')
            }
            for movie in movies
        ]
    }), 200

# Get a single movie by ID
@app.route('/movies/<int:movie_id>', methods=['GET'])
@requires_auth('get:movies')
def get_movie(jwt_payload, movie_id):

    # Fetch the movie by ID
    movie = Movie.query.get_or_404(movie_id, description='Movie not found with the provided ID.')

    # Request's Response
    return jsonify({
        'success': True,
        'movie': {
            'id': movie.id,
            'title': movie.title,
            'release_date': movie.release_date.strftime('%Y-%m-%d')
        }
    }), 200

# Create a new movie
@app.route('/movies', methods=['POST'])
@requires_auth('post:movies')
def create_movie(jwt_payload):

    # Check if the request contains JSON data
    if not request.is_json:
        abort(400, description='Invalid input! JSON data required.')

    # Check if the required fields are present in the JSON data
    data = request.get_json()
    if 'title' not in data or 'release_date' not in data:
        abort(400, description='Missing required fields: title and release_date.')

    # INIT the Response
    response = {}

    # Create a new movie instance and add it to the database
    try:
        release_date = parse_date(data['release_date'])
        new_movie = Movie(title=data['title'], release_date=release_date)
        db.session.add(new_movie)
        db.session.commit()
        response['success'] = True
        response['message'] = 'Movie created successfully!'
        response['movie'] = {
            'id': new_movie.id,
            'title': new_movie.title,
            'release_date': new_movie.release_date.strftime('%Y-%m-%d')
        }
    except Exception as e:
        db.session.rollback()
        abort(500, description=f'Failed to create movie: {str(e)}')
    finally:
        db.session.close()

    # Send the response
    return jsonify(response), 201

# Update an existing movie
@app.route('/movies/<int:movie_id>', methods=['PUT'])
@requires_auth('update:movies')
def update_movie(jwt_payload, movie_id):

    # Check if the request contains JSON data
    if not request.is_json:
        abort(400, description='Invalid input! JSON data required.')

    # Check if the required fields are present in the JSON data
    data = request.get_json()
    if 'title' not in data or 'release_date' not in data:
        abort(400, description='Missing required fields: title and release_date.')

    # INIT the Response
    response = {}

    # Fetch the movie by ID
    movie = Movie.query.get_or_404(movie_id, description='Movie not found with the provided ID.')

    # Update the movie instance and add it to the database
    try:
        movie.title = data['title']
        movie.release_date = parse_date(data['release_date'])
        db.session.commit()
        response['success'] = True
        response['message'] = 'Movie updated successfully!'
        response['movie'] = {
            'id': movie.id,
            'title': movie.title,
            'release_date': movie.release_date.strftime('%Y-%m-%d')
        }
    except Exception as e:
        db.session.rollback()
        abort(500, description=f'Failed to update movie: {str(e)}')
    finally:
        db.session.close()

    # Send the response
    return jsonify(response), 201

# Partially update a movie
@app.route('/movies/<int:movie_id>', methods=['PATCH'])
@requires_auth('update:movies')
def patch_movie(jwt_payload, movie_id):

    # Check if the request contains JSON data
    if not request.is_json:
        abort(400, description='Invalid input! JSON data required.')

    # Check if the required fields are present in the JSON data
    data = request.get_json()
    if 'title' not in data and 'release_date' not in data:
        abort(400, description='Missing required fields: title and/or release_date.')

    # INIT the Response
    response = {}

    # Fetch the movie by ID
    movie = Movie.query.get_or_404(movie_id, description='Movie not found with the provided ID.')

    # Update the movie instance and add it to the database
    try:
        if 'title' in data:
            movie.title = data['title']
        if 'release_date' in data:
            movie.release_date = parse_date(data['release_date'])
        db.session.commit()
        response['success'] = True
        response['message'] = 'Movie updated successfully!'
        response['movie'] = {
            'id': movie.id,
            'title': movie.title,
            'release_date': movie.release_date.strftime('%Y-%m-%d')
        }
    except Exception as e:
        db.session.rollback()
        abort(500, description=f'Failed to update movie: {str(e)}')
    finally:
        db.session.close()

    # Send the response
    return jsonify(response), 201

# Delete a movie
@app.route('/movies/<int:movie_id>', methods=['DELETE'])
@requires_auth('delete:movies')
def delete_movie(jwt_payload, movie_id):

    # Check if the movie exists
    movie = Movie.query.get_or_404(movie_id, description='Movie not found with the provided ID.')

    # INIT the Response
    response = {}

    # Delete the movie from the database
    try:
        db.session.delete(movie)
        db.session.commit()
        response['success'] = True
        response['message'] = 'Movie deleted successfully!'
    except Exception as e:
        db.session.rollback()
        abort(500, description=f'Failed to delete movie: {str(e)}')
    finally:
        db.session.close()

    # Send the response
    return jsonify(response), 200

# Get all actors
@app.route('/actors', methods=['GET'])
@requires_auth('get:actors')
def get_actors(jwt_payload):

    # Fetch all actors from the database
    actors = Actor.query.all()

    # Send the response
    return jsonify({
        'success': True,
        'actors': [
            {
                'id': actor.id,
                'name': actor.name,
                'age': actor.age,
                'gender': actor.gender
            }
            for actor in actors
        ]
    }), 200

# Get a single actor by ID
@app.route('/actors/<int:actor_id>', methods=['GET'])
@requires_auth('get:actors')
def get_actor(jwt_payload, actor_id):

    # Fetch the actor by ID
    actor = Actor.query.get_or_404(actor_id, description='Actor not found with the provided ID.')

    # Request's Response
    return jsonify({
        'success': True,
        'actor': {
            'id': actor.id,
            'name': actor.name,
            'age': actor.age,
            'gender': actor.gender
        }
    }), 200

# Create a new actor
@app.route('/actors', methods=['POST'])
@requires_auth('post:actors')
def create_actor(jwt_payload):

    # Check if the request contains JSON data
    if not request.is_json:
        abort(400, description='Invalid input! JSON data required.')

    # Check if the required fields are present in the JSON data
    data = request.get_json()
    if 'name' not in data or 'age' not in data or 'gender' not in data:
        abort(400, description='Missing required fields: name, age, and gender.')

    # INIT the Response
    response = {}

    # Create a new actor instance and add it to the database
    try:
        new_actor = Actor(name=data['name'], age=data['age'], gender=data['gender'])
        db.session.add(new_actor)
        db.session.commit()
        response['success'] = True
        response['message'] = 'Actor created successfully!'
        response['actor'] = {
            'id': new_actor.id,
            'name': new_actor.name,
            'age': new_actor.age,
            'gender': new_actor.gender
        }
    except Exception as e:
        db.session.rollback()
        abort(500, description=f'Failed to create actor: {str(e)}')
    finally:
        db.session.close()

    # Send the response
    return jsonify(response), 201

# Update an existing actor
@app.route('/actors/<int:actor_id>', methods=['PUT'])
@requires_auth('update:actors')
def update_actor(jwt_payload, actor_id):

    # Check if the request contains JSON data
    if not request.is_json:
        abort(400, description='Invalid input! JSON data required.')

    # Check if the required fields are present in the JSON data
    data = request.get_json()
    if 'name' not in data or 'age' not in data or 'gender' not in data:
        abort(400, description='Missing required fields: name, age, and gender.')

    # INIT the Response
    response = {}

    # Fetch the actor by ID
    actor = Actor.query.get_or_404(actor_id, description='Actor not found with the provided ID.')

    # Update the actor instance and add it to the database
    try:
        actor.name = data['name']
        actor.age = data['age']
        actor.gender = data['gender']
        db.session.commit()
        response['success'] = True
        response['message'] = 'Actor updated successfully!'
        response['actor'] = {
            'id': actor.id,
            'name': actor.name,
            'age': actor.age,
            'gender': actor.gender
        }
    except Exception as e:
        db.session.rollback()
        abort(500, description=f'Failed to update actor: {str(e)}')
    finally:
        db.session.close()

    # Send the response
    return jsonify(response), 201

# Partially update an actor
@app.route('/actors/<int:actor_id>', methods=['PATCH'])
@requires_auth('update:actors')
def patch_actor(jwt_payload, actor_id):

    # Check if the request contains JSON data
    if not request.is_json:
        abort(400, description='Invalid input! JSON data required.')

    # Check if the required fields are present in the JSON data
    data = request.get_json()
    if 'name' not in data and 'age' not in data and 'gender' not in data:
        abort(400, description='Missing required fields: name, age, and/or gender.')

    # INIT the Response
    response = {}

    # Fetch the actor by ID
    actor = Actor.query.get_or_404(actor_id, description='Actor not found with the provided ID.')

    # Update the actor instance and add it to the database
    try:
        if 'name' in data:
            actor.name = data['name']
        if 'age' in data:
            actor.age = data['age']
        if 'gender' in data:
            actor.gender = data['gender']
        db.session.commit()
        response['success'] = True
        response['message'] = 'Actor updated successfully!'
        response['actor'] = {
            'id': actor.id,
            'name': actor.name,
            'age': actor.age,
            'gender': actor.gender
        }
    except Exception as e:
        db.session.rollback()
        abort(500, description=f'Failed to update actor: {str(e)}')
    finally:
        db.session.close()

    # Send the response
    return jsonify(response), 201

# Delete an actor
@app.route('/actors/<int:actor_id>', methods=['DELETE'])
@requires_auth('delete:actors')
def delete_actor(jwt_payload, actor_id):

    # Check if the actor exists
    actor = Actor.query.get_or_404(actor_id, description='Actor not found with the provided ID.')

    # INIT the Response
    response = {}

    # Delete the actor from the database
    try:
        db.session.delete(actor)
        db.session.commit()
        response['success'] = True
        response['message'] = 'Actor deleted successfully!'
    except Exception as e:
        db.session.rollback()
        abort(500, description=f'Failed to delete actor: {str(e)}')
    finally:
        db.session.close()

    # Send the response
    return jsonify(response), 200

# Error handlers
@app.errorhandler(400)
def bad_request(error):
    return jsonify({
        'success': False,
        'error_code': 400,
        'message': f'Bad Request: {error}'
    }), 400

@app.errorhandler(401)
def unauthorized(error):
    return jsonify({
        'success': False,
        'error_code': 401,
        'message': f'Unauthorized: {error}'
    }), 401

@app.errorhandler(403)
def forbidden(error):
    return jsonify({
        'success': False,
        'error_code': 403,
        'message': f'Forbidden: {error}'
    }), 403

@app.errorhandler(404)
def not_found(error):
    return jsonify({
        'success': False,
        'error_code': 404,
        'message': f'Not Found: {error}'
    }), 404

@app.errorhandler(405)
def method_not_allowed(error):
    return jsonify({
        'success': False,
        'error_code': 405,
        'message': f'Method Not Allowed: {error}'
    }), 405

@app.errorhandler(500)
def internal_error(error):
    return jsonify({
        'success': False,
        'error_code': 500,
        'message': f'Internal Server Error: {error}'
    }), 500

if __name__ == '__main__':
    app.run(debug=True)
