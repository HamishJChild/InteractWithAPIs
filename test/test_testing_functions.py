from test import testing_functions
from unittest import TestCase


class TestingMethods(TestCase):
    """A class of tests to test the methods found in 'testing_functions"""

    def test_construct_url(self):
        """
        Test that the construct_url function appends params to the end of a url string.
        """
        url = "https://thisisamadeupapi.com/search"
        params = {"q": "SearchQuery"}
        expected_result = url + '?' + "q" + '=' + str(params.get("q"))
        actual_result = testing_functions.construct_url(url, params)
        self.assertEqual(expected_result, actual_result)
