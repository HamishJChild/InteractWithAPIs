from unittest import TestCase
import lorem
import main
import mock
import io
import sys
import httpretty
import json
from test import testing_methods


class MainTests(TestCase):
    """
    A set of test for the Main class and its methods.
    """

    def setUp(self) -> None:
        """
        Set up the test data.
        """
        # Set up the main class
        self.main_class = main.Main()
        # set up the user entered name
        self.user_input = 'Kasabian'

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
    def test_artist_selection_y(self):
        """
        Test that the function returns the correct input (Y, N, y, n) and the method
        returns an Artist Object
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
        # set the input by the user with a mock input value
        # CONSIDER CHANGING THIS TO S TIME SENSITIVE TEST FOR THE INFINITE LOOP
        self.main_class.test_var = True
        with mock.patch('builtins.input', return_value="p"):
            artist_obj = self.main_class.artist_selection()
        # reset redirect
        sys.stdout = sys.__stdout__
