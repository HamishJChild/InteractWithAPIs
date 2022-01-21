import requests

print('Enter an Artist name:')
entered_name = input()

# instantiate some variables
word_count_list = []

# first search for the artist on Genius API
url = "https://genius.p.rapidapi.com/search"

querystring = {"q": entered_name}

headers = {
    'x-rapidapi-host': "genius.p.rapidapi.com",
    'x-rapidapi-key': "54c85d06f1mshceda12a2e078e4ep140148jsnb34cacfb54cb"
    }

response = requests.request("GET", url, headers=headers, params=querystring)

json_data = response.json()
artist_id = json_data['response']['hits'][0]['result']['primary_artist']['id']
artist_name = json_data['response']['hits'][0]['result']['primary_artist']['name']
print('Searched Artist:', artist_name)

page = 1
while type(page) == int:
    # next get the songs from the artist ID
    url = f"https://genius.p.rapidapi.com/artists/{artist_id}/songs?"
    querystring = {"page": page}
    headers = {
        'x-rapidapi-host': "genius.p.rapidapi.com",
        'x-rapidapi-key': "54c85d06f1mshceda12a2e078e4ep140148jsnb34cacfb54cb"
        }

    genius_songs_response = requests.request("GET", url, headers=headers, params=querystring)
    songs = genius_songs_response.json()['response']['songs']
    # now loop over songs for artist on page
    for song in songs:
        song_name = song['title']

        # Get the lyrics for the song on the lyrics.ovh API
        url = f"https://api.lyrics.ovh/v1/{artist_name}/{song_name}"

        lyrics_response = requests.request("GET", url)
        if lyrics_response.status_code == 200:
            lyrics = lyrics_response.json()['lyrics']

            # now get count of words in lyrics
            word_count = len(lyrics.split())
            word_count_list.append(word_count)
        else:
            print(song_name, ' does not have lyrics')
    # move to the next page, if next page is Null then set it to None
    page = genius_songs_response.json()['response']['next_page']
avg_word_count = sum(word_count_list)/len(word_count_list)
print(int(avg_word_count))
