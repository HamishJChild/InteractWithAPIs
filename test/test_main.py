from unittest import TestCase
import unittest.mock
import lorem
import main
import mock
import io
import sys
import httpretty
import json
from test import testing_methods
import artist
import time


class MainTests(TestCase):
    """
    A set of test for the Main class and its methods.
    These can mainly be seen an integration tests, as they test functionality that is already covered
    by other tests, but they test that functionality working concurrently.
    """

    def setUp(self) -> None:
        """
        Set up the test data.
        """
        # Set up the main class
        self.main_class = main.Main()
        # set up the user entered name
        self.user_input = 'Kasabian'
        # set up an artist with songs
        self.artist1 = artist.Artist(genius_id=123456, full_name='David Bowie')
        songs_no_lyrics = [{'title': 'Song 1'}]
        # assign songs to artist
        self.artist1.assign_songs(songs_no_lyrics)
        # instantiate the lyrics to be used for the songs, in order to calculate the wordcount later
        self.lyrics = [lorem.paragraph()]

    def test_initial_input(self):
        """
        Test that this method assigns the entered_name var to the Main class
        """
        # capture the console output to prevent it from printing
        captured_output = io.StringIO()  # Create StringIO object
        sys.stdout = captured_output
        # set the input by the user with a mock input value
        with mock.patch('builtins.input', return_value=self.user_input):
            self.main_class.initial_input()
        # reset redirect
        sys.stdout = sys.__stdout__
        self.assertEqual(self.main_class.entered_name, self.user_input)

    @httpretty.activate
    def test_artist_selection_correct_input_y(self):
        """
        Test that the function returns an Artist Object if Y is passed as user input
        """
        # capture the console output to prevent it from printing
        captured_output = io.StringIO()  # Create StringIO object
        sys.stdout = captured_output
        # set up the correct url that will be used in the get request, to prevent the get request from sending
        params = {"q": "Kasabian"}
        full_url = testing_methods.construct_url(url="https://genius.p.rapidapi.com/search",
                                                 params=params)
        # set up the http response body in the correct format
        body = json.dumps({"response": {"hits": [{
            "result": {"primary_artist": {"name": "Kasabian", "id": 123456}}}]}})
        # Set up the httpretty http client mock with the correct url and body
        httpretty.register_uri(httpretty.GET, full_url, body=body)
        # use mock input of y
        with mock.patch('builtins.input', return_value="y"):
            artist_obj = self.main_class.artist_selection()
        # reset redirect
        sys.stdout = sys.__stdout__
        # assert that the correct artist object is returned
        self.assertEqual(type(artist_obj), artist.Artist)

    @httpretty.activate
    def test_artist_selection_correct_input_n(self):
        """
        Test that the function returns None if n is passed as user input
        """
        # capture the console output to prevent it from printing
        captured_output = io.StringIO()  # Create StringIO object
        sys.stdout = captured_output
        # set up the correct url that will be used in the get request, to prevent the get request from sending
        params = {"q": "Kasabian"}
        full_url = testing_methods.construct_url(url="https://genius.p.rapidapi.com/search",
                                                 params=params)
        # set up the http response body in the correct format
        body = json.dumps({"response": {"hits": [{
            "result": {"primary_artist": {"name": "Kasabian", "id": 123456}}}]}})
        # Set up the httpretty http client mock with the correct url and body
        httpretty.register_uri(httpretty.GET, full_url, body=body)
        # use mock input of N
        with mock.patch('builtins.input', return_value="N"):
            artist_obj = self.main_class.artist_selection()
        # reset redirect
        sys.stdout = sys.__stdout__
        # assert that None is returned by th function
        self.assertEqual(artist_obj, None)

    @unittest.mock.patch('builtins.input', side_effect=['p', 'Y'])
    @httpretty.activate
    def test_artist_selection_incorrect_input(self, mock):
        """
        Test that the function will prompt the user to continue to input an answer if they don't input (Y, N, y, n).
        The mock patch decorator runs through two user inputs, one that will cause the user to input again
        and the next which will be correct and cause an artist.Artist object to be returned.
        """
        # capture the console output to prevent it from printing
        captured_output = io.StringIO()  # Create StringIO object
        sys.stdout = captured_output
        # set up the correct url that will be used in the get request, to prevent the get request from sending
        params = {"q": "Kasabian"}
        full_url = testing_methods.construct_url(url="https://genius.p.rapidapi.com/search",
                                                 params=params)
        # set up the http response body in the correct format
        body = json.dumps({"response": {"hits": [{
            "result": {"primary_artist": {"name": "Kasabian", "id": 123456}}}]}})
        # Set up the httpretty http client mock with the correct url and body
        httpretty.register_uri(httpretty.GET, full_url, body=body)
        artist_obj = self.main_class.artist_selection()
        # reset redirect
        sys.stdout = sys.__stdout__
        # assert that 'Please enter Y or N' is outputted to the console
        self.assertIn('Please enter Y or N', captured_output.getvalue())
        # assert that an artist.Artist obj is finally returned
        self.assertEqual(type(artist_obj), artist.Artist)

    @httpretty.activate
    def test_get_songs_and_lyrics_time(self):
        """
        Test that the method returns a time taken for the function to run.
        """
        # capture the console output to prevent it from printing
        captured_output = io.StringIO()  # Create StringIO object
        sys.stdout = captured_output
        # register the urls that will be used in the get request, to prevent the get request from sending
        # first register the url for finding the artists songs
        songs_params = {"page": 1, "per_page": "50"}
        songs_full_url = testing_methods.construct_url(
            url="https://genius.p.rapidapi.com/artists/123456/songs?", params=songs_params)
        # set up the http response body in the correct format and next_page set to Nan
        songs_body = json.dumps(
            {"response": {"songs": [{"title": "Song 1"}],
                          "next_page": "Nan"}})
        # Set up the httpretty http client mock with the correct url and body
        httpretty.register_uri(httpretty.GET, songs_full_url, body=songs_body)
        # now register the url for finding the lyrics for the songs
        # set up the correct url that will be used in the get request
        url = f"https://api.lyrics.ovh/v1/David Bowie/{self.artist1.songs[0].title}"
        # set up the http response body with the correct lyrics
        body = json.dumps({"lyrics": self.lyrics[0]})
        # Set up the httpretty http client mock with the correct url and body
        httpretty.register_uri(httpretty.GET, url, body=body)
        # run the function
        time_taken = self.main_class.get_songs_and_lyrics(self.artist1)
        # reset redirect
        sys.stdout = sys.__stdout__
        # assert that the value returned is of type time.time()
        self.assertEqual(type(time_taken), type(time.time()))

    @unittest.mock.patch('builtins.input', side_effect=['David Bowie', 'y'])
    @httpretty.activate
    def test_run_method_valid_artist(self, mock):
        """
        Test that the run() method correctly prints a str to the console if an artist obj is returned by
        artist_selection(). This uses a mock input, with the first being the enetered name
        and the second being the response from the user
        """
        # capture the console output to prevent it from printing
        captured_output = io.StringIO()  # Create StringIO object
        sys.stdout = captured_output
        # register the urls that will be used in the get request, to prevent the get request from sending
        # set up the url for the artist selection API
        params = {"q": "David Bowie"}
        full_url = testing_methods.construct_url(url="https://genius.p.rapidapi.com/search",
                                                 params=params)
        # set up the http response body in the correct format
        body = json.dumps({"response": {"hits": [{
            "result": {"primary_artist": {"name": "David Bowie", "id": 123456}}}]}})
        # Set up the httpretty http client mock with the correct url and body
        httpretty.register_uri(httpretty.GET, full_url, body=body)
        # register the url for finding the artists songs
        songs_params = {"page": 1, "per_page": "50"}
        songs_full_url = testing_methods.construct_url(
            url="https://genius.p.rapidapi.com/artists/123456/songs?", params=songs_params)
        # set up the http response body in the correct format and next_page set to Nan
        songs_body = json.dumps(
            {"response": {"songs": [{"title": "Song 1"}],
                          "next_page": "Nan"}})
        # Set up the httpretty http client mock with the correct url and body
        httpretty.register_uri(httpretty.GET, songs_full_url, body=songs_body)
        # now register the url for finding the lyrics for the songs
        # set up the correct url that will be used in the get request
        url = f"https://api.lyrics.ovh/v1/David Bowie/{self.artist1.songs[0].title}"
        # set up the http response body with the correct lyrics
        body = json.dumps({"lyrics": self.lyrics[0]})
        # Set up the httpretty http client mock with the correct url and body
        httpretty.register_uri(httpretty.GET, url, body=body)
        # run the function
        self.main_class.run()
        # reset redirect
        sys.stdout = sys.__stdout__
        # assert that the response once all functions have been run is returned
        console_output = "Thanks for using my CLI application, it took 0:00:00 seconds to process your request."
        self.assertIn(console_output, captured_output.getvalue())

    @unittest.mock.patch('builtins.input', side_effect=['David Bowie', 'n'])
    @httpretty.activate
    def test_run_method_invalid_artist(self, mock):
        """
        Test that the run() method correctly prints a str to the console if an artist obj is returned by
        artist_selection(). This uses a mock input, with the first being the enetered name
        and the second being the response from the user
        """
        # capture the console output to prevent it from printing
        captured_output = io.StringIO()  # Create StringIO object
        sys.stdout = captured_output
        # register the urls that will be used in the get request, to prevent the get request from sending
        # set up the url for the artist selection API
        params = {"q": "David Bowie"}
        full_url = testing_methods.construct_url(url="https://genius.p.rapidapi.com/search",
                                                 params=params)
        # set up the http response body in the correct format
        body = json.dumps({"response": {"hits": [{
            "result": {"primary_artist": {"name": "David Bowie", "id": 123456}}}]}})
        # Set up the httpretty http client mock with the correct url and body
        httpretty.register_uri(httpretty.GET, full_url, body=body)
        # register the url for finding the artists songs
        songs_params = {"page": 1, "per_page": "50"}
        songs_full_url = testing_methods.construct_url(
            url="https://genius.p.rapidapi.com/artists/123456/songs?", params=songs_params)
        # set up the http response body in the correct format and next_page set to Nan
        songs_body = json.dumps(
            {"response": {"songs": [{"title": "Song 1"}],
                          "next_page": "Nan"}})
        # Set up the httpretty http client mock with the correct url and body
        httpretty.register_uri(httpretty.GET, songs_full_url, body=songs_body)
        # now register the url for finding the lyrics for the songs
        # set up the correct url that will be used in the get request
        url = f"https://api.lyrics.ovh/v1/David Bowie/{self.artist1.songs[0].title}"
        # set up the http response body with the correct lyrics
        body = json.dumps({"lyrics": self.lyrics[0]})
        # Set up the httpretty http client mock with the correct url and body
        httpretty.register_uri(httpretty.GET, url, body=body)
        # run the function
        self.main_class.run()
        # reset redirect
        sys.stdout = sys.__stdout__
        # assert that the response once all functions have been run is returned
        console_output = "Thanks for using my CLI application, it took 0:00:00 seconds to process your request."
        self.assertNotIn(console_output, captured_output.getvalue())
