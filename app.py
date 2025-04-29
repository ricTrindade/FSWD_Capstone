from http.client import responses

from models import app, Movie, Actor, db
from flask import jsonify, request

# Home route
@app.route('/')
def home():
    response = {
        'success': True,
        'message': 'Welcome to the Movie and Actor API!'
    }
    return jsonify(response), 200

# Get all movies
# TODO: This Endpoint is working - Return JSON With Success True
@app.route('/movies', methods=['GET'])
def get_movies():

    # Fetch all movies from the database
    movies = Movie.query.all()

    # Check if movies exist
    if not movies:
        return jsonify({'message': 'No movies found!'}), 404

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
    return response, 200

# Get a single movie by ID
# TODO: This Endpoint is working - Return JSON With Success True
@app.route('/movies/<int:movie_id>', methods=['GET'])
def get_movie(movie_id):
    movie = Movie.query.get_or_404(movie_id)
    return jsonify({'id': movie.id, 'title': movie.title, 'release_date': movie.release_date.strftime('%Y-%m-%d')}), 200

# Create a new movie
@app.route('/movies', methods=['POST'])
# TODO: This Endpoint is working - Return JSON With Success True
def create_movie():
    data = request.get_json()
    new_movie = Movie(title=data['title'], release_date=data['release_date'])
    db.session.add(new_movie)
    db.session.commit()
    return jsonify({'id': new_movie.id, 'title': new_movie.title, 'release_date': new_movie.release_date.strftime('%Y-%m-%d')}), 201

# Update an existing movie
@app.route('/movies/<int:movie_id>', methods=['PUT'])
# TODO: This Endpoint is working - Return JSON With Success True
def update_movie(movie_id):
    data = request.get_json()
    movie = Movie.query.get_or_404(movie_id)
    movie.title = data['title']
    movie.release_date = data['release_date']
    db.session.commit()
    return jsonify({'id': movie.id, 'title': movie.title, 'release_date': movie.release_date.strftime('%Y-%m-%d')}), 200

# Partially update an existing movie
@app.route('/movies/<int:movie_id>', methods=['PATCH'])
# TODO: This Endpoint is working - Return JSON With Success True
def patch_movie(movie_id):
    data = request.get_json()
    movie = Movie.query.get_or_404(movie_id)
    if 'title' in data:
        movie.title = data['title']
    if 'release_date' in data:
        movie.release_date = data['release_date']
    db.session.commit()
    return jsonify({'id': movie.id, 'title': movie.title, 'release_date': movie.release_date.strftime('%Y-%m-%d')}), 200

# Delete a movie
@app.route('/movies/<int:movie_id>', methods=['DELETE'])
# TODO: This Endpoint is working - Return JSON With Success True
def delete_movie(movie_id):
    movie = Movie.query.get_or_404(movie_id)
    db.session.delete(movie)
    db.session.commit()
    return jsonify({'message': 'Movie deleted successfully!'}), 200

# Get all actors
@app.route('/actors', methods=['GET'])
# TODO: This Endpoint is working - Return JSON With Success True
def get_actors():
    actors = Actor.query.all()
    return jsonify([{'id': actor.id, 'name': actor.name, 'age': actor.age, 'gender': actor.gender} for actor in actors]), 200

# Get a single actor by ID
@app.route('/actors/<int:actor_id>', methods=['GET'])
# TODO: This Endpoint is working - Return JSON With Success True
def get_actor(actor_id):
    actor = Actor.query.get_or_404(actor_id)
    return jsonify({'id': actor.id, 'name': actor.name, 'age': actor.age, 'gender': actor.gender}), 200

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
    return jsonify({'error': 'Resource not found!'}), 404

@app.errorhandler(500)
def internal_error(error):
    return jsonify({'error': 'Internal server error!'}), 500

# Error handling for invalid JSON
@app.errorhandler(400)
def bad_request(error):
    return jsonify({'error': 'Bad request! Invalid JSON format.'}), 400

# Error handling for 405 method not allowed
@app.errorhandler(405)
def method_not_allowed(error):
    return jsonify({'error': 'Method not allowed!'}), 405

# Run the app
if __name__ == '__main__':
    app.run(debug=True)
