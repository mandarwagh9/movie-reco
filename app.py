from flask import Flask, jsonify, render_template
import requests
from requests.adapters import HTTPAdapter
from requests.exceptions import ConnectionError, Timeout

app = Flask(__name__)

API_KEY = "23c93ba760857662a2a907b737241ae6"
BASE_URL = "https://api.themoviedb.org/3"

def get_genres():
    url = f"{BASE_URL}/genre/movie/list?api_key={API_KEY}"

    session = requests.Session()
    session.mount("https://", HTTPAdapter(max_retries=3))

    try:
        response = session.get(url, timeout=5)
        response.raise_for_status()
        genres = response.json().get("genres", [])
        return genres
    except (ConnectionError, Timeout) as e:
        return {"error": f"Connection error: {e}"}
    except Exception as e:
        return {"error": f"An unexpected error occurred: {e}"}

def get_movies_by_genre(genre_id):
    url = f"{BASE_URL}/discover/movie?api_key={API_KEY}&with_genres={genre_id}"

    session = requests.Session()
    session.mount("https://", HTTPAdapter(max_retries=3))

    try:
        response = session.get(url, timeout=5)
        response.raise_for_status()
        movies = response.json().get("results", [])
        return [{"id": movie["id"], "title": movie["title"], "overview": movie["overview"]} for movie in movies]
    except (ConnectionError, Timeout) as e:
        return {"error": f"Connection error: {e}"}
    except Exception as e:
        return {"error": f"An unexpected error occurred: {e}"}

def get_movie_details(movie_id):
    url = f"{BASE_URL}/movie/{movie_id}?api_key={API_KEY}"

    session = requests.Session()
    session.mount("https://", HTTPAdapter(max_retries=3))

    try:
        response = session.get(url, timeout=5)
        response.raise_for_status()
        movie_details = response.json()
        return movie_details
    except (ConnectionError, Timeout) as e:
        return {"error": f"Connection error: {e}"}
    except Exception as e:
        return {"error": f"An unexpected error occurred: {e}"}

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/genres', methods=['GET'])
def genres():
    genres_list = get_genres()
    return jsonify(genres_list)

@app.route('/movies/<int:genre_id>', methods=['GET'])
def movies(genre_id):
    movies_list = get_movies_by_genre(genre_id)
    return jsonify(movies_list)

@app.route('/movie/<int:movie_id>', methods=['GET'])
def movie(movie_id):
    movie_details = get_movie_details(movie_id)
    return jsonify(movie_details)

if __name__ == '__main__':
    app.run(debug=True)
