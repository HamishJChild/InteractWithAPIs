import API_Methods
import time
from time import sleep
from colorama import init
from termcolor import colored

# use Colorama to make Termcolor work on Windows too. Initialise colorama below.
init()


def main() -> None:
    print(colored(text='Artist Word Count CLI by Hamish Child', color='red', attrs=['bold', 'reverse']))

    # take the input from the user
    print(u'Hi and welcome to the Artist Avg Word Count CLI!\n'
          u'\n'
          u'Find the average word count for any artist with ease.\n')
    print('Please enter an Artist name:')
    entered_name = input()

    # First search for the artist using the Genius API
    artist_details = API_Methods.find_artist_genius(entered_name)

    print(f'You have chosen {artist_details[1]}, is this correct? ' +
          colored(text='(Y/N)', color='red', attrs=['bold', 'reverse']))
    # set up a while loop to only break once the user enters Y or N
    while True:
        correct_bool = input()
        if correct_bool not in ['Y', 'N', 'y', 'n']:
            print('Please enter Y or N')
            continue
        else:
            break

    if correct_bool in ['N', 'n']:
        print("The artist wasn't found, please try again")
        # add something to kill the process here
    else:
        start_time = time.time()
        print(f'Finding songs for {artist_details[1]}')
        # Using the artist ID found above, find all the songs associated with this artist
        artists_songs = API_Methods.find_artist_songs_genius(artist_details[0])
        print(f"{len(artists_songs)} songs found for {artist_details[1]}")
        print('Collecting lyrics...')
        lyrics_count_list = API_Methods.find_lyrics_word_count(artists_songs, artist_details[1])
        print(f'The average word count for {artist_details[1]} is {lyrics_count_list}.\n')
        end_time = time.time()
        print(f'Thanks for using my CLI application, it took {round((end_time-start_time), 2)}'
              f' seconds to process your request.')


if __name__ == "__main__":
    main()
