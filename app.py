from http.client import responses

from models import app, Movie, Actor, db
from flask import jsonify, request, abort


# Home route
@app.route('/', methods=['GET'])
def home():

    # Request's Response
    response = {
        'success': True,
        'message': 'Welcome to the Movie and Actor API!'
    }

    # Send the response
    return jsonify(response), 200

# Get all movies
@app.route('/movies', methods=['GET'])
def get_movies():

    # Fetch all movies from the database
    movies = Movie.query.all()

    # Check if movies exist
    if not movies:
        abort(404, description='No movies found!')

    # Request's Response
    response = {
        'success': True,
        'movies': [
            {
                'id': movie.id,
                'title': movie.title,
                'release_date': movie.release_date.strftime('%Y-%m-%d')
            }
            for movie in movies
        ]
    }

    # Send the response
    return response, 200

# Get a single movie by ID
@app.route('/movies/<int:movie_id>', methods=['GET'])
def get_movie(movie_id):

    # Fetch the movie by ID
    movie = Movie.query.get_or_404(movie_id)

    # Request's Response
    response = {
        'success': True,
        'movie': {
            'id': movie.id,
            'title': movie.title,
            'release_date': movie.release_date.strftime('%Y-%m-%d')
        }
    }

    # Send the response
    return response, 200

# Create a new movie
@app.route('/movies', methods=['POST'])
def create_movie():

    # Check if the request contains JSON data
    if not request.is_json:
        return jsonify({'error': 'Invalid input! JSON data required.'}), 400

    # Check if the required fields are present in the JSON data
    data = request.get_json()
    if 'title' not in data or 'release_date' not in data:
        return jsonify({'error': 'Missing required fields: title and release_date.'}), 400

    # Set up a flag to check for errors and INIT the Response
    is_there_error = False
    response = {}

    # Create a new movie instance and add it to the database
    try:
        new_movie = Movie(title=data['title'], release_date=data['release_date'])
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
        is_there_error = True
        db.session.rollback()
        response['success'] = False
        response['error'] = f'Failed to create movie: {str(e)}'
    finally:
        db.session.close()

    # Send the response
    return jsonify(response), 201 if not is_there_error else 500

# Update an existing movie
@app.route('/movies/<int:movie_id>', methods=['PUT'])
def update_movie(movie_id):

    # Check if the request contains JSON data
    if not request.is_json:
        return jsonify({'error': 'Invalid input! JSON data required.'}), 400

    # Check if the required fields are present in the JSON data
    data = request.get_json()
    if 'title' not in data or 'release_date' not in data:
        return jsonify({'error': 'Missing required fields: title and release_date.'}), 400

    # Set up a flag to check for errors and INIT the Response
    is_there_error = False
    response = {}

    # Fetch the movie by ID
    movie = Movie.query.get_or_404(movie_id)

    # Update the movie instance and add it to the database
    try:
        movie.title = data['title']
        movie.release_date = data['release_date']
        db.session.commit()
        response['success'] = True
        response['message'] = 'Movie updated successfully!'
        response['movie'] = {
            'id': movie.id,
            'title': movie.title,
            'release_date': movie.release_date.strftime('%Y-%m-%d')
        }
    except Exception as e:
        is_there_error = True
        db.session.rollback()
        response['success'] = False
        response['error'] = f'Failed to update movie: {str(e)}'
    finally:
        db.session.close()

    # Send the response
    return jsonify(response), 201 if not is_there_error else 500

# Partially update an existing movie
@app.route('/movies/<int:movie_id>', methods=['PATCH'])
def patch_movie(movie_id):

    # Check if the request contains JSON data
    if not request.is_json:
        return jsonify({'error': 'Invalid input! JSON data required.'}), 400

    # Check if the required fields are present in the JSON data
    data = request.get_json()
    if 'title' not in data and 'release_date' not in data:
        return jsonify({'error': 'Missing required fields: title and release_date.'}), 400

    # Set up a flag to check for errors and INIT the Response
    is_there_error = False
    response = {}

    # Fetch the movie by ID
    movie = Movie.query.get_or_404(movie_id)

    # Update the movie instance and add it to the database
    try:
        if 'title' in data:
            movie.title = data['title']
        if 'release_date' in data:
            movie.release_date = data['release_date']
        db.session.commit()
        response['success'] = True
        response['message'] = 'Movie updated successfully!'
        response['movie'] = {
            'id': movie.id,
            'title': movie.title,
            'release_date': movie.release_date.strftime('%Y-%m-%d')
        }
    except Exception as e:
        is_there_error = True
        db.session.rollback()
        response['success'] = False
        response['error'] = f'Failed to update movie: {str(e)}'
    finally:
        db.session.close()

    # Send the response
    return jsonify(response), 201 if not is_there_error else 500

# Delete a movie
@app.route('/movies/<int:movie_id>', methods=['DELETE'])
def delete_movie(movie_id):

    # Check if the movie exists
    movie = Movie.query.get_or_404(movie_id)

    # Set up a flag to check for errors and INIT the Response
    is_there_error = False
    response = {}

    # Delete the movie from the database
    try:
        db.session.delete(movie)
        db.session.commit()
        response['success'] = True
        response['message'] = 'Movie deleted successfully!'
    except Exception as e:
        db.session.rollback()
        is_there_error = True
        response['success'] = False
        response['error'] = f'Failed to delete movie: {str(e)}'
    finally:
        db.session.close()

    # Send the response
    return jsonify(response), 200 if not is_there_error else 500

# Get all actors
@app.route('/actors', methods=['GET'])
def get_actors():

    # Fetch all actors from the database
    actors = Actor.query.all()

    # Check if actors exist
    if not actors:
        return jsonify(
            {
                'success': False,
                'message': 'No actors found!'
            }
        ), 404

    # Request's Response
    response = {
        'success': True,
        'actors': [
            {
                'id': actor.id,
                'name': actor.name,
                'age': actor.age,
            }
            for actor in actors
        ]
    }

    # Send the response
    return jsonify(response), 200

# Get a single actor by ID
@app.route('/actors/<int:actor_id>', methods=['GET'])
# TODO: This Endpoint is working - Return JSON With Success True
def get_actor(actor_id):

    # Fetch the actor by ID
    actor = Actor.query.get_or_404(actor_id)

    # Request's Response
    response = {
        'success': True,
        'actor': {
            'id': actor.id,
            'name': actor.name,
            'age': actor.age,
        }
    }

    # Send the response
    return jsonify(response), 200

# Create a new actor
@app.route('/actors', methods=['POST'])
# TODO: This Endpoint is working - Return JSON With Success True
def create_actor():
    data = request.get_json()
    new_actor = Actor(name=data['name'], age=data['age'], gender=data['gender'])
    db.session.add(new_actor)
    db.session.commit()
    return jsonify({'id': new_actor.id, 'name': new_actor.name, 'age': new_actor.age, 'gender': new_actor.gender}), 201

# Update an existing actor
@app.route('/actors/<int:actor_id>', methods=['PUT'])
# TODO: This Endpoint is working - Return JSON With Success True
def update_actor(actor_id):
    data = request.get_json()
    actor = Actor.query.get_or_404(actor_id)
    actor.name = data['name']
    actor.age = data['age']
    actor.gender = data['gender']
    db.session.commit()
    return jsonify({'id': actor.id, 'name': actor.name, 'age': actor.age, 'gender': actor.gender}), 200

@app.route('/actors/<int:actor_id>', methods=['PATCH'])
# TODO: This Endpoint is working - Return JSON With Success True
def patch_actor(actor_id):
    data = request.get_json()
    actor = Actor.query.get_or_404(actor_id)
    if 'name' in data:
        actor.name = data['name']
    if 'age' in data:
        actor.age = data['age']
    if 'gender' in data:
        actor.gender = data['gender']
    db.session.commit()
    return jsonify({'id': actor.id, 'name': actor.name, 'age': actor.age, 'gender': actor.gender}), 200

# Delete an actor
@app.route('/actors/<int:actor_id>', methods=['DELETE'])
# TODO: This Endpoint is working - Return JSON With Success True
def delete_actor(actor_id):
    actor = Actor.query.get_or_404(actor_id)
    db.session.delete(actor)
    db.session.commit()
    return jsonify({'message': 'Actor deleted successfully!'}), 200

# Error handling
@app.errorhandler(404)
def not_found(error):
    response = {
        'success': False,
        'error_code': 404,
        'message': f'Error: {error}'
    }
    return jsonify(response), 404

@app.errorhandler(500)
def internal_error(error):
    response = {
        'success': False,
        'error': 500,
        'message': f'Internal server error: {error}'
    }
    return jsonify(response), 500

# Error handling for invalid JSON
@app.errorhandler(400)
def bad_request(error):
    response = {
        'success': False,
        'error': 400,
        'message': f'Bad request: {error}'
    }
    return jsonify(response), 400

# Error handling for 405 method not allowed
@app.errorhandler(405)
def method_not_allowed(error):
    response = {
        'success': False,
        'error': 405,
        'message': f'Method not allowed: {error}'
    }
    return jsonify(response), 405

# Run the app
if __name__ == '__main__':
    app.run(debug=True)
