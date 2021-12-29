from unittest.mock import Mock
import tmdb_client
import pytest
from main import app


def test_get_single_movie(monkeypatch):
    single_movie_id = ['Movie 1', 'Movie 2']
    my_mock = Mock()
    response = my_mock.return_value
    response.json.return_value = single_movie_id
    monkeypatch.setattr("tmdb_client.requests.get", my_mock)
    single_movie = tmdb_client.get_single_movie(1)
    assert single_movie == single_movie_id


def test_get_movie_images(monkeypatch):
    url = "https://image.tmdb.org/t/p/"
    size = "w342"
    poster = "poster"
    my_mock = Mock()
    response = my_mock.return_value
    response.return_value = url + size + poster
    monkeypatch.setattr("tmdb_client.requests.get", my_mock)
    single_movie = tmdb_client.get_poster_url(poster)
    expected_url = url + size + "/" + poster
    assert single_movie == expected_url

    
def test_get_movie_cast(monkeypatch):
    id = {"cast": "movie1"}
    my_mock = Mock()
    response = my_mock.return_value
    response.json.return_value = id
    monkeypatch.setattr("tmdb_client.requests.get", my_mock)
    single_movie = tmdb_client.get_single_movie_cast(1)
    assert single_movie == "movie1"


@pytest.mark.parametrize("list_type", ("now_playing", "popular", "upcoming", "top_rated"))
def test_homepage(monkeypatch, list_type):
    api_mock = Mock(return_value={'results': []})
    monkeypatch.setattr("tmdb_client.call_tmdb_api", api_mock)

    with app.test_client() as client:
        response = client.get('/')
        assert response.status_code == 200