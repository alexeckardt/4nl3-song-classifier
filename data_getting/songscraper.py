import re
import requests
import time 
import json

START_YEAR = 1960
END_YEAR = 2024
SEARCH_SONGS = [1,2,3]

billboard_link = 'https://en.wikipedia.org/wiki/Billboard_Year-End_Hot_100_singles_of_'

songs = [[] for _ in range(8)]
file_id = 0

# find songs from each year on wikipedia pages
for year in range(START_YEAR, END_YEAR+1):
    print(f'Getting songs from {year}...')

    # get billboard data 
    billboard_html = requests.get(billboard_link + str(year))
    table = re.search('<table class="wikitable sortable(.|\n)*?</table>', billboard_html.text)
    tbody = re.search('<tbody>((.|\n)*?)</tbody>', table.group())
    rows = re.findall('<tr>((.|\n)*?)</tr>', tbody.group(1))

    # get specific songs data from table
    if year % 2 == 1: song_ranks = [SEARCH_SONGS[0]] + SEARCH_SONGS
    else: song_ranks = SEARCH_SONGS
    for i in song_ranks:
        # table columns: rank, song title, artist
        row_data = re.findall('<td.*?>((.|\n)*?)</td>', rows[i][0])
        if len(row_data) == 3: 
            _, title, artist = row_data

            # extract artist
            artist = re.search('<a .*?</a>', artist[0])
            artist = re.sub('<.*?>', '', artist.group())
        
        else:
            _, title = row_data
            artist = ''

        # extract title
        title = re.sub('<.*?>|"|\n', '', title[0])

        # get lyrics from api.lyrics.ovh
        lyric_link = f'https://api.lyrics.ovh/v1/{artist}/{title}'
        lyric_html = requests.get(lyric_link)
        match = re.search('{"lyrics":"(.*)"}', lyric_html.text)
        if match:
            lyrics = match.group(1)
            lyrics = re.sub('\\\\n', '\n', lyrics)
            lyrics = re.sub('\\\\r', '\r', lyrics)
        else:
            lyrics = 'error'

        # create dictionary for song data
        song = {
            'title' : title, 
            'artist' : artist,
            'year' : year,
            'lyrics' : lyrics
            }

        # add song to file
        songs[file_id].append(song)
        file_id = (file_id + 1) % 8
        
        # prevent time out
        time.sleep(2)

# write to json
for i in range(8):
    with open(f'./datasets/dataset_{i+1}.json', 'w', encoding='utf-8') as f:
        f.write(json.dumps(songs[i], indent=4))

# songs to get lyrics for manually
print('\nSongs with no lyrics found: ')
for i in range(8):
    for song in songs[i]:
        if song['lyrics'] == 'error':
            print(f"- {song['title']} ({song['artist']}, {song['year']})")

