import requests
import pprint

API_KEY = "af5a744440bd1b9defc86acf28484561"
API_URL = "https://api.themoviedb.org/3/search/movie?"
MOVIE_DB_IMAGE_URL = "https://image.tmdb.org/t/p/w500"

def get_movies(movie):
    import requests

    params = {
        "api_key": API_KEY,
        "query": movie
    }

    response = requests.get(API_URL, params=params)
    data = response.json()['results']

    return data

# for movie in data:
#     print(movie['original_title'], movie['release_date'])

# movie_api_url = f"https://api.themoviedb.org/3/movie/{80271}?"
# # The language parameter is optional, if you were making the website for a different audience
# # e.g. Hindi speakers then you might choose "hi-IN"
# response = requests.get(movie_api_url, params={"api_key": "af5a744440bd1b9defc86acf28484561", "language": "en-US"})
# data = response.json()
# title = data["original_title"]
# year = data["release_date"].split("-")[0]
# img_url = f"{MOVIE_DB_IMAGE_URL}{data['poster_path']}"
# description = data["overview"]
# pprint.pprint(data)