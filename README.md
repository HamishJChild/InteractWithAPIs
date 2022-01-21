# InteractWithAPIs
To produce a program which, when given the name of an artist, will produce the average (mean) number of words in their songs.


This will use an API that will need to use the name of an artist/artists given by a user (after checking this name with another API request) to find the mean number of words in their songs. I will need to investigate what API calls I can make in order to work out how to find the mean number of words in their songs.

Structure of getting mean number of songs:
- First use API call to get the artist (or return error if artist doesn't exist).
- Then get songs for that artistand pass the songs to a method that uses another API call to get the lyrics, and count the number of words in the song.
- Add this to a list and find the avergae of all # of lyrics.

To Do:
- [ ] Set up the API so the User can enter an artist in the command line, and it will check whether they are real.
- [ ] Set up the method to find the mean number of words in an artists songs
- [ ] Wite tests after first attempt at functionality, then use them to assess the functionality to improve.
- [ ] Second round on the functionality, clean up code and make interface usable and pretty.
