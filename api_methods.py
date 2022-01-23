import requests
import artist


def make_request(url: str, params=None, headers=None):
    """
    Function to make a request to an API using the base URL and other params/headers.
    Returns a response if no HTTPError is returned, otherwise it passes the iteration.
    :param url: the base URL as a str
    :param params: a dict with the queries for the API call
    :param headers: a dict of the headers for the API call
    :return: response
    :raise LookUpError
    """
    try:
        response = requests.request("GET", url, headers=headers, params=params)
        response.raise_for_status()
        return response
    except requests.exceptions.HTTPError:
        pass


def find_artist_genius(entered_name: str) -> artist.Artist:
    """A function to use an API call to Genius find the artist from the search entry.
    :param entered_name: a string entered by the user in the cli input.
    :returns artist_obj: an Artist object with the full_name and genius_id variables set."""

    # first search for the artist on Genius API
    base_url = "https://genius.p.rapidapi.com/search"

    params = {"q": entered_name}

    headers = {
        'x-rapidapi-host': "genius.p.rapidapi.com",
        'x-rapidapi-key': "54c85d06f1mshceda12a2e078e4ep140148jsnb34cacfb54cb"
        }

    response = make_request(base_url, params=params, headers=headers)

    json_data = response.json()
    try:
        artist_id = json_data['response']['hits'][0]['result']['primary_artist']['id']
        artist_name = json_data['response']['hits'][0]['result']['primary_artist']['name']
        artist_obj = artist.Artist(genius_id=artist_id, full_name=artist_name)
        return artist_obj
    except IndexError:
        print('This artist does not exist in the Genius database')
        raise SystemExit()


def find_artist_songs_genius(artist_obj: artist.Artist) -> None:
    """A function to use an API call to Genius to find all songs for an artist,
     create Song objects for them and assign to the Artist object.
    :param artist_obj: an artist object
    :returns None"""

    # instantiate initial variables
    page_number = 1

    # the final page has a value of 'Null' for the next_page variable,
    # so loop over while page_number is of type int
    while type(page_number) == int:
        # get the songs from the artist ID
        url = f"https://genius.p.rapidapi.com/artists/{artist_obj.genius_id}/songs?"
        querystring = {"page": page_number,
                       "per_page": "50"}
        headers = {
            'x-rapidapi-host': "genius.p.rapidapi.com",
            'x-rapidapi-key': "54c85d06f1mshceda12a2e078e4ep140148jsnb34cacfb54cb"
            }

        genius_songs_response = make_request(url, headers=headers, params=querystring)
        songs = genius_songs_response.json()['response']['songs']
        artist_obj.assign_songs(songs)
        # redefine the page variable
        page_number = genius_songs_response.json()['response']['next_page']


def find_lyrics_for_songs(artist_obj: artist.Artist) -> None:
    """A function to find the lyrics for the each song in the list
     using the lyrics.ovh API

     :param artist_obj : an Artist object
     :returns avg_word_count: an integer representing the average lyrics word count
     for the artists_songs list"""

    # instantiate the word count list
    word_count_list = []
    for song_obj in artist_obj.songs:
        # Get the lyrics for the song on the lyrics.ovh API
        url = f"https://api.lyrics.ovh/v1/{artist_obj.full_name}/{song_obj.title}"

        lyrics_response = make_request(url)
        if lyrics_response:
            lyrics = lyrics_response.json()['lyrics']

            # now assign the lyrics to the song_obj
            song_obj.assign_lyrics_and_wordcount(lyrics)
    # now cal and assign the artist mean wordcount
    artist_obj.calc_mean_wordcount()
