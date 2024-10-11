from flask import Flask, render_template, request
import os
import requests  
import json
import random

app = Flask(__name__)


API_KEY = '707467aa44d78b11be2c7fc399a682a5'
base_url = 'https://api.themoviedb.org/3/'
genres = {
    "28": "Action",
    "12": "Adventure",
    "16": "Animation",
    "35": "Comedy",
    "80": "Crime",
    "99": "Documentary",
    "18": "Drama",
    "10751": "Family",
    "14": "Fantasy",
    "36": "History",
    "27": "Horror",
    "10402": "Music",
    "9648": "Mystery",
    "10749": "Romance",
    "878": "Science Fiction",
    "10770": "TV Movie",
    "53": "Thriller",
    "10752": "War",
    "37": "Western"
}


@app.route('/')
def home():
    return render_template('index.html')

@app.route('/search', methods=['POST'])
def search_movie():
    search_query = request.form['query']
    url = f'{base_url}search/movie?api_key={API_KEY}&query={search_query}'
    
    headers = {
        "accept": "application/json",
        "Authorization": "Bearer eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiI3MDc0NjdhYTQ0ZDc4YjExYmUyYzdmYzM5OWE2ODJhNSIsIm5iZiI6MTcyODMyOTY1My41Mzc3NzksInN1YiI6IjY0YWJiOTA0ZmE3OGNkMDBhZGMxY2Q4ZiIsInNjb3BlcyI6WyJhcGlfcmVhZCJdLCJ2ZXJzaW9uIjoxfQ.n6ez6qTAYJqa0cMaz1m7NojWjaQVglBEBuw9Zb341-w"
    }

    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        data = response.json()
        clean_data = []

        for movie in data['results']:
            movie_id = movie['id']
            credits_url = f'{base_url}movie/{movie_id}/credits?api_key={API_KEY}'
            credits_response = requests.get(credits_url, headers=headers)

            if credits_response.status_code == 200:
                credits_data = credits_response.json()
                genre_names = [genres[str(genre_id)] for genre_id in movie['genre_ids'] if str(genre_id) in genres]
                producers = [crew_member['name'] for crew_member in credits_data['crew'] if crew_member['job'] == 'Producer']

                movie_info = {
                    'Poster': f"https://image.tmdb.org/t/p/w500/{movie['poster_path']}" if movie['poster_path'] else None,
                    'Title': movie['title'],
                    'Release Date': movie['release_date'],
                    'Vote Average': movie['vote_average'],
                    'Overview': movie['overview'],
                    'Popularity': movie['popularity'],
                    'Genres': genre_names,
                    'Producers': producers
                }
                clean_data.append(movie_info)


                sorted_data = sorted(clean_data, key=lambda x: x['Popularity'], reverse=True)
        
        return render_template('results.html', movies=sorted_data)
    else:
        return f"Error, unable to fetch data. Status code: {response.status_code}"

if __name__ == '__main__':
    app.run(debug=True)