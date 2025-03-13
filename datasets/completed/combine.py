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

        # Load the dataset as dataframe
        name = path.replace('dataset-', '').split('.db')[0]
        print(name)

        # 
        conn = sqlite3.connect(f'./datasets/completed/{path}')
        dbDf = pd.read_sql_query("SELECT * FROM Song", conn);
        print(df.head())
        conn.close()

        dbDf['annotator'] = name

        # Combine
        df = pd.concat([df, dbDf], ignore_index=True)

df = create_song_hash(df)

unique = set()
rows = 0
for _, row in df.iterrows():
    song_hash = row['song_hash']
    unique.add(song_hash)
    rows += 1

print(f'Unique Songs: {len(unique)}')
print(f'Total Rows: {rows}')

d = rows - len(unique)
print(f'Duplicated Songs Found:{d}')
print(f'Total Proportion: {d/rows}')


# Write output
df.to_csv('./datasets/combined.csv', index=False)
df.drop(columns=['lyrics'], inplace=True)
df.to_csv('./datasets/combined_no_lyrics.csv', index=False)
print(df.head())