# InteractWithAPIs
**Welcome to my CLI app!**\
The goal of this app is to take the input of an artist by a user and produce the mean word count for that artists songs. This app was designed to meet this singular brief, with speed and ease of use at the forefront of the user experience. Any questions please email me at [hchild@outlook.com](mailto:hchild@outlook.com).

## Instructions
- This was written in Python 3.8.
- To install all dependancies, run `pip install -r config/requirements.txt`.
- To start the application, run `python3 main.py` from the command line.
- To run tests, run `python3 -m unittest` from the command line.
- To see the test coverage:
    - run `coverage run -m unittest`.
    - run `coverage html`.
    - navigate to the newly created `htmlcov/` folder and open `index.html` in your browser of choice.
    - This will show the test coverage against all the statements in the codebase.

## Structure
- This app makes three sets of API calls, the first two to [Genius](https://rapidapi.com/brianiswu/api/genius/) through RapidAPI to search for the artist and then find the lists of songs for that artist, and the third API call to [Lyrics.ovh](https://lyricsovh.docs.apiary.io/#reference/0/lyrics-of-a-song/search) to get the lyrics for that song. The data taken in as a dict and parsed from there.
- User Interface
  - I decided the keep the user interface relatively simple, with the use of some colours to highlight important text. The app is designed to be used without re-running any commands until the user has finished. This means the user can continuously search for artists unitl they have satisfied their need.
- Artist Selection
  - The user is first prompted to enter the name of an artist, which will then be used in a search in the Genius Database.
  - If an Artist name is found, the user is asked if this is the correct artist. If 'yes', the app moves to the next step. If 'no', the user is prompted to enter the name again.
  - If no artist is found in the search, the user is prompted to enter the name again.
- Song Query
  - Assuming an artist is found in the previous step, an API call to Genius is made to find the songs for that artist. The user is told how many songs have been found.
- Lyrics Query
  - The app then loops over the songs for the artist, and makes an API call for each song to get the lyrics. The user is given an estimate for how long this may take (based on an estimation of the lyrics taking 1.5 times as long as the songs take, on average).
  - If lyrics are found, they are assigned to the song with the wordcount for the lyrics. The mean wordcount for the artist is then found, across all the songs.
  - The final wordcount is presented to the user, alongside how long the process took.
  - If no lyrics are found then the user is informed and prompted to enter another artist's name.

## Limitations
- The Genius Database tends to be more extensive than the Lyrics.ovh one, so often an artist can be found but then no lyrics can be found for them.
- This app takes the first results from the Genius search for the Artist in order to streamline the process (in case of spelling errors from the user). However, in some rare cases this isn't always the correct artist, and it can be difficult to find the correct one.
- The API calls take time. I attempted to solve this in part by using multi-threading, so API calls could run concurrently, but this can still be a lengthy process.

## Next time...
- I made the decision early on to build an app that would be quick and easy to use, and meet the brief in its entirety. However, next time I would look to extend the features of this app and build the front end out of the command line and into a web app.
    - I would do this by drawing on my experince with Django to create a web app with a structured database and responsive design that allows the user to search and select the artist from a drop down in a form.
    - The app would run the core functionality to return the average word count, but allow the user to also compare against other artists, see the artists longest and shortest songs, and view the artist on their streaming app of choice.
- I would also look to improve my use of API, as the Genius song search is clunky due a max of 50 results being returned at a time. If I knew beforehand how many results there were, I could set up multi-threading for the pages to make the API calls concurrently, which would speed it up also.
