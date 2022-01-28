"""This module contains the artist class and its methods.

Classes:
Artist

Functions:
assign_songs
calc_mean_wordcount

"""
import song
import numpy as np
from colorama import init
from termcolor import colored

# use Colorama to make Termcolor work on Windows too. Initialise colorama below.
init()


class Artist(object):
    """
    A class to represent an artist.

    ...

    Attributes
    ----------
    genius_id : str
        the Genius ID of the artist
    full_name : str
        full name of the artist
    songs : list
        a list of the Song objects an artist is the primary artist for.
    mean_wordcount : int
        the mean wordcount from all the songs for this artist

    Methods
    -------
    assign_songs
    calc_mean_wordcount

    """

    def __init__(self, genius_id, full_name, songs=None, mean_wordcount=0) -> None:
        """
        Constructs all the necessary attributes for the artist object.

        Parameters
        ----------
            genius_id: str
                the Genius ID of the artist
            full_name : str
                full name of the artist
            songs : list
                a list of the Song objects an artist is the primary artist for.
            mean_wordcount : int
                the mean wordcount from all the songs for this artist
        """

        self.genius_id = genius_id
        self.full_name = full_name
        self.songs = []
        self.mean_wordcount = 0

    def assign_songs(self, artists_songs: dict) -> None:
        """
        A function to assign a list of songs to the artist object, whilst creating songs objects in that list.
        :param artists_songs: a dict of the songs returned in an api call for this artist
        :return: None
        """
        # Create new Song objects for all songs in list
        songs_objects = [song.Song(title=artist_song['title']) for artist_song in artists_songs]
        self.songs.extend(songs_objects)

    def calc_mean_wordcount(self) -> None:
        """
        For the list of song objects for an artist, calculate the mean wordcount for those songs
        and assign the value to the artist
        :return: None
        """
        # for all songs in the list that have lyrics_found set to True, find the mean word_count
        found_word_counts = [found_song.word_count for found_song in self.songs if found_song.lyrics_found]
        # Only calculate the mean if lyrics have been found for the songs in the list.
        if len(found_word_counts) > 0:
            mean = int(np.mean(found_word_counts))
            self.mean_wordcount = mean
            print(colored(text=f'The average word count for {self.full_name} is {self.mean_wordcount}.\n',
                          color='green', attrs=['bold', 'reverse']))
        else:
            print(colored(text=f'No lyrics found for {self.full_name}.', color='red', attrs=['bold', 'reverse']))
