import json
import sqlite3
import pandas as pd

def main(): 

    path = '../datasets'

    fs = range(8)
    files = [f'{path}/dataset_{x+1}.json' for x in fs]
    for fileName in files:

        dbObj = {}
        with open(fileName, 'r') as f:
            dbObj = json.load(f)

        # LOad
        df = pd.DataFrame(dbObj)

        print(df.head())

        conn = sqlite3.connect(fileName.replace('.json', '.db'))  # This will create songs.db if it doesn't exist

        # Save DataFrame to SQLite
        df.to_sql("songs", conn, if_exists="replace", index=False)  # 'songs' is the table name

        # Commit and close the connection
        conn.commit()
        conn.close()


main()