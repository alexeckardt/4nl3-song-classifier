import json
import sqlite3
import pandas as pd

#
#   Converts files created by songscraper.py
#   from the JSON format into the .db format.
#

def main(): 

    path = './datasets'

    fs = range(8)
    files = [f'{path}/dataset_{x+1}.json' for x in fs]
    for fileName in files:

        dbObj = []
        with open(fileName, 'r') as f:
            dbObj = json.load(f)

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
        conn = sqlite3.connect(fileName.replace('.json', '.db'))  # This will create songs.db if it doesn't exist

        # Save DataFrame to SQLite
        df.to_sql("Song", conn, if_exists="replace", index=False)  # 'songs' is the table name

        # Commit and close the connection
        conn.commit()
        conn.close()

if __name__ == '__main__':
    main()