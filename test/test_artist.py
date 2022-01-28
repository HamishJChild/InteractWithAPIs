from unittest import TestCase
import lorem
import artist
import io
import sys


class ArtistTests(TestCase):
    """
    A set of test for the Artist class and its methods.
    """

    def setUp(self) -> None:
        """
        Set up the test data.
        """
        # Set up artist
        self.new_artist = artist.Artist(genius_id='123456', full_name='New Artist Name')
        # Set up a dict of songs with no lyrics
        self.songs_no_lyrics = [{'title': 'Song 1'},
                                {'title': 'Song 2'},
                                {'title': 'Song 3'},
                                {'title': 'Song 4'},
                                {'title': 'Song 5'}]
        self.songs_no_lyrics_expected = ['Song 1', 'Song 2', 'Song 3',
                                         'Song 4', 'Song 5']

    def test_assign_songs(self):
        """
        Test that the song titles passed to the assign_songs method have Song objects created for them
        and are assigned to the songs attribute for an artist
        """
        # First assign the songs to the artist attr Songs
        self.new_artist.assign_songs(self.songs_no_lyrics)
        # assert the number of songs created matches
        self.assertEqual(len(self.new_artist.songs), len(self.songs_no_lyrics))
        # assert the titles of the new objects created is present in the list of expected titles
        for song_obj in self.new_artist.songs:
            self.assertIn(song_obj.title, self.songs_no_lyrics_expected)

    def test_calc_mean_wordcount_lyrics(self):
        """
        Test that the calculated word count for a list of songs is correct.
        This is for a list of songs with lyrics
        """
        # capture the console output to prevent it from printing
        captured_output = io.StringIO()  # Create StringIO object
        sys.stdout = captured_output
        word_count_list = []
        # First assign the songs to the artist attr Songs
        self.new_artist.assign_songs(self.songs_no_lyrics)
        # For each song, assign lyrics and set lyrics_found=True, and record the word count of the lyrics
        for song_obj in self.new_artist.songs:
            song_obj.assign_lyrics_and_wordcount(lorem.paragraph())
            word_count_list.append(len(song_obj.lyrics.split()))
        # now run function to calc mean wordcount
        self.new_artist.calc_mean_wordcount()
        # reset redirect
        sys.stdout = sys.__stdout__
        # calc mean word count
        mean_word_count = int((sum(word_count_list)/len(word_count_list)))
        self.assertEqual(self.new_artist.mean_wordcount, mean_word_count)
        # assert the console output is correct
        output_pred = f'The average word count for {self.new_artist.full_name} is {mean_word_count}.'
        # Console output contains ascii escape codes, so assert predicted is 'in' actual
        self.assertIn(output_pred, captured_output.getvalue())

    def test_calc_mean_wordcount_no_lyrics(self):
        """
        Test that for a list of songs with no lyrics, the mean wordcount is 0
        and the expected console output is returned
        """
        # capture the console output to prevent it from printing
        captured_output = io.StringIO()  # Create StringIO object
        sys.stdout = captured_output
        # First assign the songs to the artist attr Songs
        self.new_artist.assign_songs(self.songs_no_lyrics)
        # now run function to calc mean wordcount - this should do nothing as there are no lyrics
        self.new_artist.calc_mean_wordcount()
        # reset redirect
        sys.stdout = sys.__stdout__
        # assert the console output is correct
        output_pred = f'No lyrics found for {self.new_artist.full_name}.'
        # Console output contains ascii escape codes, so assert predicted is 'in' actual
        self.assertIn(output_pred, captured_output.getvalue())
