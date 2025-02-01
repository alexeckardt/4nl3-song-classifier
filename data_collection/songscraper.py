import re
import sqlite3
import pandas as pd
import requests
import time 

START_YEAR = 1960
END_YEAR = 2024
NUM_SONGS_PER_YEAR = 7

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
    n_songs_this_year = 0 # track number of songs found for the year
    manual_years = {} # in case any year didn't have any lyrics
    for i in range(100):
        # table columns: rank, song title, artist
        row_data = re.findall('<td.*?>((.|\n)*?)</td>', rows[i+1][0])
        if len(row_data) == 3: 
            _, title, artist = row_data

            # extract artist
            artist = re.search('<a .*?</a>', artist[0])
            artist = re.sub('<.*?>', '', artist.group())

            # extract title
            title = re.sub('<.*?>|"|\n', '', title[0])

            # get lyrics from api.lyrics.ovh
            lyric_link = f'https://api.lyrics.ovh/v1/{artist}/{title}'
            lyric_html = requests.get(lyric_link)
            match = re.search('{"lyrics":"(.*)"}', lyric_html.text)

            if match:
                # found song on api
                n_songs_this_year += 1
                lyrics = match.group(1)
                lyrics = re.sub('\\\\n|\\\\r', '\n', lyrics)
                # lyrics = re.sub('\\\\r', '\r', lyrics)

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

                # add duplicate of first song found 
                if n_songs_this_year == 1:
                    songs[file_id].append(song)
                    file_id = (file_id + 1) % 8

                # move on to next year when number of songs are found
                if n_songs_this_year == NUM_SONGS_PER_YEAR:
                    break

        # prevent time out
        time.sleep(2)

    # not enough songs found
    if i == 99:
        manual_years[year] = NUM_SONGS_PER_YEAR - n_songs_this_year

# write to json
for i in range(8):

    #Object
    dbObj = songs[i]

    # Load
    df = pd.DataFrame(dbObj)

    # Add columns required by api
    df['recognized'] = -1 #Add a column
    df['name'] = df['title']
    df['topic1'] = ''
    df['topic2'] = ''
    df['decade'] = -1
    df['id'] = list(range(len(dbObj)))

    # Drop the Name

    df = df.drop(columns=['title'])
    print(df.head())
    conn = sqlite3.connect(f'./datasets/dataset_{i+1}.db')  # This will create songs.db if it doesn't exist

    # Save DataFrame to SQLite
    df.to_sql("Song", conn, if_exists="replace", index=False)  # 'songs' is the table name

    # Commit and close the connection
    conn.commit()
    conn.close()

# print years where not enough songs were found
for i in manual_years:
    print(f'{i} needs {manual_years[i]} more songs')