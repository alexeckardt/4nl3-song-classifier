import pandas as pd
import os
import sqlite3

df = pd.DataFrame()
paths = os.listdir('./datasets/completed')
print(paths)

def create_song_hash(df):
    df['song_hash'] = df['name'] + df['artist']
    return df

for path in paths:
    if path.endswith('.db'):

        # 
        conn = sqlite3.connect(f'./datasets/completed/{path}')
        dbDf = pd.read_sql_query("SELECT * FROM Song", conn);
        print(df.head())
        conn.close()

        # Combine
        df = pd.concat([df, dbDf], ignore_index=True)

df = create_song_hash(df)

# Write output
df.to_csv('./datasets/combined.csv', index=False)
print(df.head())