from unittest import TestCase
import unittest.mock
import lorem
import main
import mock
import io
import sys
import httpretty
import json
from test import testing_functions
import artist
import time


class MainTests(TestCase):
    """
    A set of test for the Main class and its methods.
    These can mainly be seen an integration tests, as they test functionality that is already covered
    by other tests, but they test that functionality works together.
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

    @unittest.mock.patch('builtins.input', side_effect=['y', 'Led Zeppelin'])
    def test_another_artist_input_valid_y(self, mock):
        """
        Test that this method takes the response 'y' from the user if they want to enter another artist
        and if so the name of the artist. It asserts that self.entered name is now set to the new name.
        The mock patch decorator runs through two user inputs, the first if the user wants to enter a new artist name
        and the second the name of the artist.
        """
        # capture the console output to prevent it from printing
        captured_output = io.StringIO()  # Create StringIO object
        sys.stdout = captured_output
        # run the method
        self.main_class.another_artist_input()
        # reset redirect
        sys.stdout = sys.__stdout__
        # assert the entered_name var is the new value entered
        self.assertEqual(self.main_class.entered_name, 'Led Zeppelin')

    @unittest.mock.patch('builtins.input', side_effect=['n'])
    def test_another_artist_input_valid_n(self, mock):
        """
        Test that this method takes the response 'n' from the user if they want to enter another artist
        and so raises a SystemExit. It asserts that a SystemExit is raised and the entered_name hasn't changed.
        The mock patch decorator runs through 1 user input, if the user wants to enter a new artist name.
        """
        # capture the console output to prevent it from printing
        captured_output = io.StringIO()  # Create StringIO object
        sys.stdout = captured_output
        # set the entered_name variable
        self.main_class.entered_name = self.user_input
        # run the method, asserting a SystemExit is raised
        with self.assertRaises(SystemExit) as cm:
            self.main_class.another_artist_input()
        # reset redirect
        sys.stdout = sys.__stdout__
        # assert the entered_name var has not changed
        self.assertEqual(self.main_class.entered_name, self.user_input)

    @unittest.mock.patch('builtins.input', side_effect=['p', 'N'])
    def test_another_artist_input_invalid(self, mock):
        """
        Test that this method takes an invalid response from the user if they want to enter another artist
        and prompts the user to enter another value. It asserts that a value that is not [y n, Y, N] is not accepted.
        The mock patch decorator runs through two user inputs, the first an invalid response (p) and the second
        a valid response (N) which will kill the process.
        """
        # capture the console output to prevent it from printing
        captured_output = io.StringIO()  # Create StringIO object
        sys.stdout = captured_output
        # run the method, asserting a SystemExit is raised
        with self.assertRaises(SystemExit) as cm:
            self.main_class.another_artist_input()
        # reset redirect
        sys.stdout = sys.__stdout__
        # assert that the user is prompted to enter another value
        self.assertIn('Please enter Y or N', captured_output.getvalue())

    @httpretty.activate
    def test_artist_selection_correct_input_y(self):
        """
        Test that the function returns an Artist Object if Y is passed as user input
        """
        # capture the console output to prevent it from printing
        captured_output = io.StringIO()  # Create StringIO object
        sys.stdout = captured_output
        # set up the correct url that will be used in the get request, to prevent the get request from sending
        params = {"q": self.user_input}
        full_url = testing_functions.construct_url(url="https://genius.p.rapidapi.com/search",
                                                   params=params)
        # set up the http response body in the correct format
        body = json.dumps({"response": {"hits": [{
            "result": {"primary_artist": {"name": self.user_input, "id": 123456}}}]}})
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
        params = {"q": self.user_input}
        full_url = testing_functions.construct_url(url="https://genius.p.rapidapi.com/search",
                                                   params=params)
        # set up the http response body in the correct format
        body = json.dumps({"response": {"hits": [{
            "result": {"primary_artist": {"name": self.user_input, "id": 123456}}}]}})
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
        The mock patch decorator runs through two user inputs, one that is invalid and
        will cause the user to input again and the next which will be correct and
        cause an artist.Artist object to be returned.
        """
        # capture the console output to prevent it from printing
        captured_output = io.StringIO()  # Create StringIO object
        sys.stdout = captured_output
        # set up the correct url that will be used in the get request, to prevent the get request from sending
        params = {"q": self.user_input}
        full_url = testing_functions.construct_url(url="https://genius.p.rapidapi.com/search",
                                                   params=params)
        # set up the http response body in the correct format
        body = json.dumps({"response": {"hits": [{
            "result": {"primary_artist": {"name": self.user_input, "id": 123456}}}]}})
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
        Test that the get_songs_and_lyrics method returns a time taken for the function to run.
        """
        # capture the console output to prevent it from printing
        captured_output = io.StringIO()  # Create StringIO object
        sys.stdout = captured_output
        # register the urls that will be used in the get request, to prevent the get request from sending
        # first register the url for finding the artists songs
        songs_params = {"page": 1, "per_page": "50"}
        songs_full_url = testing_functions.construct_url(
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

    @unittest.mock.patch('builtins.input', side_effect=['David Bowie', 'y', 'n'])
    @httpretty.activate
    def test_run_method_valid_artist_no_next_artist(self, mock):
        """
        Test that the run() method correctly prints a str to the console if an artist obj is returned by
        artist_selection(). This uses a mock input, with the first being the entered name,
        the second being the response from the user to whether the artists name is correct
        and the third being the response to whether the user wants to enter a new artists name.
        Here the option for no new artists is selected.
        """
        # capture the console output to prevent it from printing
        captured_output = io.StringIO()  # Create StringIO object
        sys.stdout = captured_output
        # register the urls that will be used in the get request, to prevent the get request from sending
        # set up the url for the artist selection API
        params = {"q": "David Bowie"}
        full_url = testing_functions.construct_url(url="https://genius.p.rapidapi.com/search",
                                                   params=params)
        # set up the http response body in the correct format
        body = json.dumps({"response": {"hits": [{
            "result": {"primary_artist": {"name": "David Bowie", "id": 123456}}}]}})
        # Set up the httpretty http client mock with the correct url and body
        httpretty.register_uri(httpretty.GET, full_url, body=body)
        # register the url for finding the artists songs
        songs_params = {"page": 1, "per_page": "50"}
        songs_full_url = testing_functions.construct_url(
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
        # run the function whilst asserting a SystemExit is raised
        with self.assertRaises(SystemExit) as cm:
            self.main_class.run()
        # reset redirect
        sys.stdout = sys.__stdout__
        # assert that the response once all functions have been run is returned
        console_output = "Thanks for using my CLI application, it took 0:00:00 seconds to process your request."
        self.assertIn(console_output, captured_output.getvalue())

    @unittest.mock.patch('builtins.input', side_effect=['David Bowie', 'n', 'n'])
    @httpretty.activate
    def test_run_method_invalid_artist_no_next_artist(self, mock):
        """
        Test that the run() method correctly prints a str to the console if no artist obj is returned by
        artist_selection(), due to an invalid artist. This uses a mock input, with the first being the entered name,
        the second being the response from the user to whether the artists name is correct
        and the third being the response to whether the user wants to enter a new artists name.
        Here the option for no new artists is selected.
        """
        # capture the console output to prevent it from printing
        captured_output = io.StringIO()  # Create StringIO object
        sys.stdout = captured_output
        # register the urls that will be used in the get request, to prevent the get request from sending
        # set up the url for the artist selection API
        params = {"q": "David Bowie"}
        full_url = testing_functions.construct_url(url="https://genius.p.rapidapi.com/search",
                                                   params=params)
        # set up the http response body in the correct format
        body = json.dumps({"response": {"hits": [{
            "result": {"primary_artist": {"name": "David Bowie", "id": 123456}}}]}})
        # Set up the httpretty http client mock with the correct url and body
        httpretty.register_uri(httpretty.GET, full_url, body=body)
        # register the url for finding the artists songs
        songs_params = {"page": 1, "per_page": "50"}
        songs_full_url = testing_functions.construct_url(
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
        # run the function whilst asserting a SystemExit is raised
        with self.assertRaises(SystemExit) as cm:
            self.main_class.run()
        # reset redirect
        sys.stdout = sys.__stdout__
        # assert that the response once all functions have been run is returned
        console_output = "Thanks for using my CLI application, it took 0:00:00 seconds to process your request."
        self.assertNotIn(console_output, captured_output.getvalue())

    @unittest.mock.patch('builtins.input', side_effect=['David Bowie', 'y', 'y', 'Cat Stevens', 'n', 'n'])
    @httpretty.activate
    def test_run_method_valid_artist_and_next_artist(self, mock):
        """
        Test that the run() method function correctly if a user wants to enter the name of a second artist.
        This uses a mock input, with the first being the entered name,
        the second being the response from the user to whether the artists name is correct,
        the third being the response to whether the user wants to enter a new artists name
        and the fourth being the next artist to select.
        The final two inputs are to end the process, with the first 'n' in response to whether the artist is correct
        and the second in response to whether the user wants to enter another artists name.

        Here the option for a new artist is selected.
        """
        # capture the console output to prevent it from printing
        captured_output = io.StringIO()  # Create StringIO object
        sys.stdout = captured_output
        # register the urls that will be used in the get request, to prevent the get request from sending
        # set up the url for the artist selection API
        params = {"q": "David Bowie"}
        full_url = testing_functions.construct_url(url="https://genius.p.rapidapi.com/search",
                                                   params=params)
        # set up the http response body in the correct format
        body = json.dumps({"response": {"hits": [{
            "result": {"primary_artist": {"name": "David Bowie", "id": 123456}}}]}})
        # Set up the httpretty http client mock with the correct url and body
        httpretty.register_uri(httpretty.GET, full_url, body=body)
        # register the url for finding the artists songs
        songs_params = {"page": 1, "per_page": "50"}
        songs_full_url = testing_functions.construct_url(
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
        # run the function whilst asserting a SystemExit is raised
        with self.assertRaises(SystemExit) as cm:
            self.main_class.run()
        # reset redirect
        sys.stdout = sys.__stdout__
        # assert that the response once all functions have been run is returned
        console_output = "Thanks for using my CLI application, it took 0:00:00 seconds to process your request."
        self.assertIn(console_output, captured_output.getvalue())
