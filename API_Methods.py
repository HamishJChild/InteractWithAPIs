import requests


def make_request(url, params=None, headers=None):
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


def find_artist_genius(entered_name) -> tuple:
    """A function to use an API call to Genius find the artist from the search entry.
    :param entered_name: a string entered by the user in the cli input.
    :returns artist_id: a string that represents the unique artist ID in the Genius database.
    :returns artist_name: a string; the name of the artist found in the Genius database."""

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
        return artist_id, artist_name
    except IndexError:
        print('This artist does not exist in the Genius database')
        raise SystemExit()


def find_artist_songs_genius(artist_id) -> list:
    """A function to use an API call to Genius to find and return all songs for an artist
    :param artist_id: a string that represents the unique artist ID in the Genius database.
    :returns artists_songs: a list of all the songs for the given artist"""

    # instantiate initial variables
    page_number = 1
    artists_songs = []

    # the final page has a value of 'Null' for the next_page variable,
    # so loop over while page_number is of type int
    while type(page_number) == int:
        # get the songs from the artist ID
        url = f"https://genius.p.rapidapi.com/artists/{artist_id}/songs?"
        querystring = {"page": page_number,
                       "per_page": "50"}
        headers = {
            'x-rapidapi-host': "genius.p.rapidapi.com",
            'x-rapidapi-key': "54c85d06f1mshceda12a2e078e4ep140148jsnb34cacfb54cb"
            }

        genius_songs_response = make_request(url, headers=headers, params=querystring)
        songs = genius_songs_response.json()['response']['songs']
        # use list comprehension to get a list of all artists songs
        artists_songs.extend([song['title'] for song in songs])
        # redefine the page variable
        page_number = genius_songs_response.json()['response']['next_page']

    return artists_songs


def find_lyrics_word_count(artists_songs, artist_name) -> int:
    """A function to find the lyrics for the each song in the list
     using the lyrics.ovh API

     :param artists_songs: a list of the songs found for an artist
     :param artist_name: a string of the artists name
     :returns avg_word_count: an integer representing the average lyrics word count
     for the artists_songs list"""

    # instantiate the word count list
    word_count_list = []
    for song_name in artists_songs:
        # Get the lyrics for the song on the lyrics.ovh API
        url = f"https://api.lyrics.ovh/v1/{artist_name}/{song_name}"

        lyrics_response = make_request(url)
        if lyrics_response:
            lyrics = lyrics_response.json()['lyrics']

            # now get count of words in lyrics
            word_count = len(lyrics.split())
            word_count_list.append(word_count)

    avg_word_count = int(sum(word_count_list)/len(word_count_list))
    return avg_word_count
