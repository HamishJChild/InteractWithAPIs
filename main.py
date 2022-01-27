import sys

import api_methods
import time
import datetime
import artist
from time import sleep
from colorama import init
from termcolor import colored

# use Colorama to make Termcolor work on Windows too. Initialise colorama below.
init()


class Main:
    def __init__(self):
        self.entered_name = None

    def initial_input(self) -> None:
        """
        A function to set up the initial display and take the entered name from input.
        :return: None
        """
        print(colored(text='Artist Word Count CLI by Hamish Child\n', color='blue', attrs=['bold', 'reverse']))
        sleep(0.5)
        # take the input from the user
        print(u'Hi and welcome to the Artist Avg Word Count CLI!\n'
              u'\n'
              u'Find the average word count for any artist with ease.\n')
        sleep(0.5)
        print('Please enter an Artist name:')
        self.entered_name = input()

    def another_artist_input(self) -> artist.Artist or None:
        """
        A function to ask the user if they want to enter another artist name. System Exit if they do not.
        :return: None
        """
        sleep(0.5)
        print('Would you like to enter another Artists name?')
        while True:
            another_artist_bool = input()
            if another_artist_bool not in ['Y', 'N', 'y', 'n']:
                print('Please enter Y or N')
                continue
            else:
                print('\n')
                break
        if another_artist_bool in ['N', 'n']:
            sys.exit()
        else:
            sleep(0.5)
            print('Please enter another Artists name:')
            self.entered_name = input()

    def artist_selection(self) -> artist.Artist or None:
        """
        A function to get the artist and then takes a response
        from the user whether this is the correct artist.
        Returns True if the user respond with yes.
        :return: validated_artist : Artist Object
        """
        # First search for the artist using the Genius API
        artist_obj = api_methods.find_artist_genius(self.entered_name)

        if artist_obj:
            print(f'You have chosen {artist_obj.full_name}, is this correct? ' +
                  colored(text='(Y/N)', color='red', attrs=['bold', 'reverse']))
            # set up a while loop to only break once the user enters Y or N,
            while True:
                correct_input = input()
                if correct_input not in ['Y', 'N', 'y', 'n']:
                    print('Please enter Y or N')
                    continue
                else:
                    print('\n')
                    break
            validated_artist = artist_obj
            if correct_input in ['N', 'n']:
                print(colored(text="The artist wasn't found, please try again", color='red', attrs=['bold', 'reverse']))
                validated_artist = None
            return validated_artist

    @staticmethod
    def get_songs_and_lyrics(artist_obj) -> float:
        """
        A function to get the songs for an artist, and the lyrics for all those songs.
        Function in here also calculate the avg word count for an artist
        The time the function might take (lyrics take 30 times longs on avg that songs) is also given.
        :param artist_obj: the artist object
        :return: lyric_time_taken + song_time_taken: float the time taken for the songs and lyrics process to take
        """
        song_start_time = time.time()
        print(f'Finding songs for {artist_obj.full_name}')
        # Using the artist object found above, find all the songs associated with this artist
        api_methods.find_artist_songs_genius(artist_obj)

        print(colored(text=f"{len(artist_obj.songs)} songs found for {artist_obj.full_name}",
                      color='green', attrs=['bold', 'reverse']))
        song_end_time = time.time()
        song_time_taken = round((song_end_time - song_start_time), 2)

        # collecting lyrics take approximately 30 times as long as it takes to collect the songs
        lyric_approx_time = datetime.timedelta(seconds=int(song_time_taken*30))
        print(f'Collecting Lyrics will take approx {lyric_approx_time}')
        lyric_start_time = time.time()
        # run the function to find the lyrics
        print('Collecting lyrics...\n')
        api_methods.find_lyrics_for_songs(artist_obj)
        lyric_end_time = time.time()
        # calculate the final time taken for lyrics
        lyric_time_taken = round((lyric_end_time-lyric_start_time), 2)
        return lyric_time_taken + song_time_taken

    def run(self) -> None:
        artist_obj = None
        self.initial_input()
        while not artist_obj:
            artist_obj = self.artist_selection()
            if artist_obj:
                time_taken = self.get_songs_and_lyrics(artist_obj)
                print(f'Thanks for using my CLI application, it took {datetime.timedelta(seconds=int(time_taken))}'
                      f' seconds to process your request.')
                # now see if the user wants to enter another Artist
                self.another_artist_input()
                artist_obj = None
            else:
                self.another_artist_input()


if __name__ == "__main__":
    Main().run()
