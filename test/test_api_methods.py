import json
from unittest import TestCase
import httpretty
import requests
import lorem
import io
import sys
import api_methods
from test import testing_functions
import artist
import song


class APIMethodsTests(TestCase):
    """
    A set of test for the API Methods used to make api requests for the necessary data.
    These tests will make use of HTTPretty, a HTTP client mocking Python Library.
    """

    def setUp(self) -> None:
        """
        Set up the test data.
        """
        # Set up an artist
        self.artist1 = artist.Artist(genius_id=123456, full_name='Nick Cave and the Bad Seeds')
        # set up another artist with songs
        self.artist2 = artist.Artist(genius_id=123456, full_name='David Bowie')
        songs_no_lyrics = [{'title': 'Song 1'},
                           {'title': 'Song 2'},
                           {'title': 'Song 3'}]
        # assign songs to artist
        self.artist2.assign_songs(songs_no_lyrics)
        # instantiate the lyrics to be used for the songs, in order to calculate the wordcount later
        self.lyrics = [lorem.paragraph(),
                       lorem.paragraph(),
                       lorem.paragraph()]

    @httpretty.activate
    def test_make_request_ok_status_code(self):
        """
        Test that the make_request method makes a get request with the given headers and params
        and returns the response if the status_code is correct
        """
        # set up the httpretty function to catch the get request and
        # return a given response and status
        httpretty.register_uri(httpretty.GET, "http://amadeupurl_forthistest.com/",
                               body="This is the response", status='200')
        # now pass the made up url to the make_request method - No params are header needed
        response = api_methods.make_request("http://amadeupurl_forthistest.com/")
        # assert that the method returns the response with the correct code
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.text, "This is the response")

    @httpretty.activate
    def test_make_request_http_error(self):
        """
        Test that the make_request method makes a get request with the given headers and params
        and returns None if the response raises a HTTPError
        """
        # set up the httpretty function to catch the get request and
        # return a given response and status
        httpretty.register_uri(httpretty.GET, "http://amadeupurl_forthistest.com/", status='403')
        # now pass the made up url to the make_request method - No params are header needed
        response = api_methods.make_request("http://amadeupurl_forthistest.com/")
        # assert that the method returns None as the status code raises a HTTPError
        self.assertEqual(response, None)

    @httpretty.activate
    def test_find_artist_genius_correct_artist(self):
        """
        Test that when a valid Artists Name is passed to the find_artist_genius function,
        it creates and returns a correct artist.Artist() object with the correct id and name
        """
        # set up the correct url that will be used in the get request
        params = {"q": "Jack White"}
        full_url = testing_functions.construct_url(url="https://genius.p.rapidapi.com/search",
                                                 params=params)
        # set up the http response body in the correct format
        body = json.dumps({"response": {"hits": [{
            "result": {"primary_artist": {"name": "Jack White", "id": 123456}}}]}})
        # Set up the httpretty http client mock with the correct url and body
        httpretty.register_uri(httpretty.GET, full_url, body=body)
        # now call the function with the search string Jack White
        artist_obj = api_methods.find_artist_genius('Jack White')
        # assert the object type returned is artist.Artist
        self.assertEqual(type(artist_obj), artist.Artist)
        # assert the name and id are correct
        self.assertEqual(artist_obj.full_name, "Jack White")
        self.assertEqual(artist_obj.genius_id, 123456)

    @httpretty.activate
    def test_find_artist_genius_invalid_artist(self):
        """
        Test that when an invalid Artists Name is passed to the find_artist_genius function,
        it raises a SystemExit and prints a response.
        """
        # capture the console output to prevent it from printing
        captured_output = io.StringIO()  # Create StringIO object
        sys.stdout = captured_output
        # set up the correct url that will be used in the mock get request,
        # with an obvious non-artist
        params = {"q": "Hamish Child"}
        full_url = testing_functions.construct_url(url="https://genius.p.rapidapi.com/search",
                                                 params=params)
        # set up the http response body in the correct format, with no response
        body = json.dumps({"response": {"hits": []}})
        # Set up the httpretty http client mock with the correct url and body
        httpretty.register_uri(httpretty.GET, full_url, body=body)
        # assert that a SystemExit is raised
        with self.assertRaises(SystemExit) as cm:
            api_methods.find_artist_genius('Hamish Child')
        # reset redirect
        sys.stdout = sys.__stdout__
        # assert the printed text is as expected
        self.assertEqual(captured_output.getvalue(), "This artist does not exist in the Genius database\n")

    @httpretty.activate
    def test_find_artists_songs_genius_next_page(self):
        """
        Test that this function finds the songs for an artists and assigns
        the new Song objects to the song attribute of the Artist object.
        This is with next page set to Nan to prevent it from going into an infinite loop
        """
        # set up the correct url that will be used in the get request
        params = {"page": 1,
                  "per_page": "50"}
        full_url = testing_functions.construct_url(
            url="https://genius.p.rapidapi.com/artists/123456/songs?",
            params=params)
        # set up the http response body in the correct format and next_page set to Nan
        body = json.dumps(
            {"response": {"songs": [{"title": "Song 1"}, {"title": "Song 2"}, {"title": "Song 3"}],
                          "next_page": "Nan"}})
        # Set up the httpretty http client mock with the correct url and body
        httpretty.register_uri(httpretty.GET, full_url, body=body)
        # now call the function with the artist obj created in setUp
        api_methods.find_artist_songs_genius(self.artist1)
        # assert there are 3 objects returned for the songs attribute
        self.assertEqual(len(self.artist1.songs), 3)
        # assert that the song objects are the correct type and the titles are correct
        title_itr = 1
        for artist_song in self.artist1.songs:
            self.assertEqual(type(artist_song), song.Song)
            self.assertEqual(artist_song.title, "Song " + str(title_itr))
            title_itr += 1

    @httpretty.activate
    def test_find_lyrics_for_songs_songs_and_lyrics(self):
        """
        Test that this function finds the lyrics for the songs for an artist,
         then calculates the avg wordcount for those lyrics.
         This is for an artist with songs and those songs have lyrics.
        """
        # capture the console output to prevent it from printing
        captured_output = io.StringIO()  # Create StringIO object
        sys.stdout = captured_output
        # reqister the 3 url's that will be used in the API calls
        i = 0
        for song_obj in self.artist2.songs:
            # set up the correct url that will be used in the get request
            url = f"https://api.lyrics.ovh/v1/David Bowie/{song_obj.title}"
            # set up the http response body with the correct lyrics
            body = json.dumps({"lyrics": self.lyrics[i]})
            # Set up the httpretty http client mock with the correct url and body
            httpretty.register_uri(httpretty.GET, url, body=body)
            i += 1
        # now call the function with the artist obj created in setUp
        api_methods.find_lyrics_for_songs(self.artist2)
        # reset redirect
        sys.stdout = sys.__stdout__
        # now assert that an avg word count has been calculated, and it is correct
        tot_wordcount = 0
        for lyric in self.lyrics:
            tot_wordcount += len(lyric.split())
        self.assertEqual(self.artist2.mean_wordcount, (int(tot_wordcount/3)))
