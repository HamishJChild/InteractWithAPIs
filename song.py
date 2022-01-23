"""This module contains the song class and its methods.

Classes:
Song


Functions:
assign_lyrics_and_wordcount

"""


class Song:
    """
    A class to represent an song.

    ...

    Attributes
    ----------
    title : str
        the title of the song
    lyrics_found : bool
        whether the lyrics for the song were found with a lyricsovh api call
    lyrics : str
        the lyrics for the song.
    word_count : int
        the word count for the lyrics

    Methods
    -------

    """

    def __init__(self, title) -> None:
        """
        Constructs all the necessary attributes for the song object.

        Parameters
        ----------
            title : str
                the title of the song
        """

        self.title = title
        self.lyrics = None
        self.lyrics_found = False
        self.word_count = 0

    def assign_lyrics_and_wordcount(self, lyrics: str) -> None:
        """
        A function to assign the lyrics and the lyrics wordcount for a song to the song object.
        Also sets lyrics_found to True for this object
        :param lyrics: a str of the lyrics for the song
        :return: None
        """
        # assign the lyrics to the object and set lyrics_found to True
        self.lyrics = lyrics
        self.lyrics_found = True
        # calculate the word count for the lyrics
        word_count = len(lyrics.split())
        self.word_count = word_count
