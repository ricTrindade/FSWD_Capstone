from models import app, Movie, Actor, db
from flask import jsonify, request, abort

# Home route
@app.route('/', methods=['GET'])
def home():

    # Send the response
    return jsonify({
        'success': True,
        'message': 'Welcome to the Movie and Actor API!'
    }), 200

# Get all movies
@app.route('/movies', methods=['GET'])
def get_movies():

    # Fetch all movies from the database
    movies = Movie.query.all()

    # Check if movies exist
    if not movies:
        abort(404, description='No movies found!')

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
def get_movie(movie_id):

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
def create_movie():

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
        db.session.rollback()
        abort(500, description=f'Failed to create movie: {str(e)}')
    finally:
        db.session.close()

    # Send the response
    return jsonify(response), 201

# Update an existing movie
@app.route('/movies/<int:movie_id>', methods=['PUT'])
def update_movie(movie_id):

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
        db.session.rollback()
        abort(500, description=f'Failed to update movie: {str(e)}')
    finally:
        db.session.close()

    # Send the response
    return jsonify(response), 201

# Partially update an existing movie
@app.route('/movies/<int:movie_id>', methods=['PATCH'])
def patch_movie(movie_id):

    # Check if the request contains JSON data
    if not request.is_json:
        abort(400, description='Invalid input! JSON data required.')

    # Check if the required fields are present in the JSON data
    data = request.get_json()
    if 'title' not in data and 'release_date' not in data:
        abort(400, description='Missing required fields: title and release_date.')

    # INIT the Response
    response = {}

    # Fetch the movie by ID
    movie = Movie.query.get_or_404(movie_id, description='Movie not found with the provided ID.')

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
        db.session.rollback()
        abort(500, description=f'Failed to update movie: {str(e)}')
    finally:
        db.session.close()

    # Send the response
    return jsonify(response), 201

# Delete a movie
@app.route('/movies/<int:movie_id>', methods=['DELETE'])
def delete_movie(movie_id):

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
def get_actors():

    # Fetch all actors from the database
    actors = Actor.query.all()

    # Check if actors exist
    if not actors:
        abort(404, description='No actors found!')

    # Send the response
    return jsonify({
        'success': True,
        'actors': [
            {
                'id': actor.id,
                'name': actor.name,
                'age': actor.age,
            }
            for actor in actors
        ]
    }), 200

# Get a single actor by ID
@app.route('/actors/<int:actor_id>', methods=['GET'])
def get_actor(actor_id):

    # Fetch the actor by ID
    actor = Actor.query.get_or_404(actor_id, description='Actor not found with the provided ID.')

    # Request's Response
    return jsonify({
        'success': True,
        'actor': {
            'id': actor.id,
            'name': actor.name,
            'age': actor.age,
        }
    }), 200

# Create a new actor
@app.route('/actors', methods=['POST'])
def create_actor():

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
def update_actor(actor_id):

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
        actor.gander = data['gender']
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

# Partially update an existing actor
@app.route('/actors/<int:actor_id>', methods=['PATCH'])
def patch_actor(actor_id):

    # Check if the request contains JSON data
    if not request.is_json:
        abort(400, description='Invalid input! JSON data required.')

    # Check if the required fields are present in the JSON data
    data = request.get_json()
    if 'name' not in data and 'age' not in data and 'gender' not in data:
        abort(400, description='Missing required fields: name, age, and gender.')

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
            'gender': actor
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
def delete_actor(actor_id):

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
