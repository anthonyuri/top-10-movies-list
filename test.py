import requests
import pprint

api_key = "af5a744440bd1b9defc86acf28484561"
movie_api_id = 80271


movie_api_url = f"https://api.themoviedb.org/3/movie/{movie_api_id}?"
print(movie_api_url)
# The language parameter is optional, if you were making the website for a different audience
# e.g. Hindi speakers then you might choose "hi-IN"
response = requests.get(movie_api_url, params={"api_key": api_key, "language": "en-US"})
data = response.json()
print(data)
