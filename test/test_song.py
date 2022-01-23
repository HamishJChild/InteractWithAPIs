from unittest import TestCase
import lorem
import song


class SongTests(TestCase):
    """
    A set of tests1 for the Song class and its methods.
    """

    def setUp(self) -> None:
        """
        Set up the test data.
        """
        self.new_song = song.Song(title='A New Song')
        self.lyrics = lorem.paragraph()

    def test_assign_lyrics(self):
        """
        Test that the lyrics are assigned to the lyrics attr for the Song object
        and lyrics_found is now == True
        """
        self.new_song.assign_lyrics_and_wordcount(self.lyrics)
        # assert that the lyrics have been assigned and lyrics_found is now True
        self.assertEqual(self.new_song.lyrics, self.lyrics)
        self.assertEqual(self.new_song.lyrics_found, True)

    def test_wordcount(self):
        """
        Test that the word count for the lyrics is assigned to the Song word_count attr
        """
        self.new_song.assign_lyrics_and_wordcount(self.lyrics)
        lyrics_wordcount = len(self.lyrics.split())
        # assert that the lyrics wordcount assigned to the attr is the same as the once calculated
        self.assertEqual(self.new_song.word_count, lyrics_wordcount)
