# InteractWithAPIs
To produce a program which, when given the name of an artist, will produce the average (mean) number of words in their songs.


This will use an API that will need to use the name of an artist/artists given by a user (after checking this name with another API request) to find the mean number of words in their songs. I will need to investigate what API calls I can make in order to work out how to find the mean number of words in their songs.

Structure of getting mean number of songs:
- First use API call to get the artist (or return error if artist doesn't exist). This should get the Artist ID. Check that the name of the artist found atches the one entered. If they don't match then return error.
- Then get songs for that artist using the Artist ID. This will require adding the Song name to a list and paging through the genius results (incrementing the `page` param until `next_page` returns `NULL`).
- Pass the songs to a method that uses another API (Mourits Lyrics) call to get the lyrics, and count the number of words in the song.
- Add this to a list and find the avergae of all # of lyrics.

To Do:
- [ ] Set up the API so the User can enter an artist in the command line, and it will check whether they are real.
- [ ] Set up the method to find the mean number of words in an artists songs
- [ ] Wite tests after first attempt at functionality, then use them to assess the functionality to improve.
- [ ] Second round on the functionality, clean up code and make interface usable and pretty.
