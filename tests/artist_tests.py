from unittest import TestCase
import lorem
import artist
import song


class ArtistTests(TestCase):
    """
    A set of tests for the Artist class and its methods.
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
        # set up the lyrics for the 5 songs

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
        word_count_list = []
        # First assign the songs to the artist attr Songs
        self.new_artist.assign_songs(self.songs_no_lyrics)
        # For each song, assign lyrics and set lyrics_found=True, and record the word count of the lyrics
        for song_obj in self.new_artist.songs:
            song_obj.assign_lyrics_and_wordcount(lorem.paragraph())
            word_count_list.append(len(song_obj.lyrics.split()))
        # now run function to calc mean wordcount
        self.new_artist.calc_mean_wordcount()
        # calc mean word count
        mean_word_count = int((sum(word_count_list)/len(word_count_list)))
        self.assertEqual(self.new_artist.mean_wordcount, mean_word_count)
