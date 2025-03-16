from dataset_loading import load_dataset
import os
import sqlite3
from tqdm import tqdm

# specify the columns to include in our dataset
DATASET_COLUMNS = ['song_hash', 'lyrics', 'topic1', 'topic2']

print("Loading dataset...")
df = load_dataset()

# print the number of entries in the dataset
print(f"Number of entries in the dataset: {len(df)}")

print("Please review the dissagreement between the two annotators and select the most correct labels.")

# find duplicates based on song_hash
duplicates = df[df.duplicated('song_hash', keep=False)].sort_values('song_hash')
print(f"Number of duplicates: {len(duplicates)}")

# save the unique entries
unique_entries = df[~df.duplicated('song_hash', keep=False)]
print(f"Number of unique entries: {len(unique_entries)}")

# Setup database connection
parent_dir = os.path.dirname(os.path.dirname(__file__))
output_path = os.path.join(parent_dir, 'model_training', 'ground_truth_dataset.db')
conn = sqlite3.connect(output_path)

# Create songs table if it doesn't exist with UNIQUE constraint
conn.execute('''CREATE TABLE IF NOT EXISTS songs 
             (song_hash TEXT PRIMARY KEY, lyrics TEXT, topic1 TEXT, topic2 TEXT)''')

# First add all unique entries
for _, row in unique_entries.iterrows():
    conn.execute('INSERT OR REPLACE INTO songs (song_hash, lyrics, topic1, topic2) VALUES (?, ?, ?, ?)',
                (row['song_hash'], row['lyrics'], row['topic1'], row['topic2']))
conn.commit()

auto_resolved = 0  # count of duplicates automatically resolved
manual_resolved = 0  # count of duplicates manually resolved

# for each duplicate entry
for i, song_hash in enumerate(tqdm(duplicates['song_hash'].unique(), desc="Resolving duplicates")):
    # get the two duplicate entries
    duplicate_pair = duplicates[duplicates['song_hash'] == song_hash]
    row1 = duplicate_pair.iloc[0]
    row2 = duplicate_pair.iloc[1]
    
    # check if topics match (in any order)
    topics1 = {row1['topic1'], row1['topic2']}
    topics2 = {row2['topic1'], row2['topic2']}
    
    if topics1 == topics2:
        print(f"{i}/{len(duplicates)}: Automatically resolved duplicate entry: {song_hash}")
        # if they chose the same set of topics, automatically use the first annotation
        conn.execute('INSERT OR REPLACE INTO songs (song_hash, lyrics, topic1, topic2) VALUES (?, ?, ?, ?)',
                    (row1['song_hash'], row1['lyrics'], row1['topic1'], row1['topic2']))
        conn.commit()
        auto_resolved += 1
    else:
        print(f"{i}/{len(duplicates)}: Manually resolved duplicate entry: {song_hash}")
        # if they chose different topics, ask for user input
        print("\n=== ADJUDICATION REQUIRED ===")
        print(f"Song: {row1['name']} by {row1['artist']} ({row1['year']})")
        print(f"Lyrics: {row1['lyrics']}")

        print(f"{'Annotator 1':^30}|{'Annotator 2':^30}")
        print(f"{row1['recognized']:^30}|{row2['recognized']:^30}")
        print(f"{', '.join([row1['topic1'][:15], row1['topic2'][:15]]):^30}|{', '.join([row2['topic1'][:15], row2['topic2'][:15]]):^30}")

        while True:
            choice = input("Select ground truth labels (1 for Annotator 1, 2 for Annotator 2): ").strip()
            if choice in ['1', '2']:
                selected_row = row1 if choice == '1' else row2
                # Add the selected row to database
                conn.execute('INSERT OR REPLACE INTO songs (song_hash, lyrics, topic1, topic2) VALUES (?, ?, ?, ?)',
                           (selected_row['song_hash'], selected_row['lyrics'], 
                            selected_row['topic1'], selected_row['topic2']))
                conn.commit()
                manual_resolved += 1
                break
            print("Invalid choice. Please enter 1 or 2.")

# Close database connection
conn.close()

# Get final count
final_count = len(unique_entries) + auto_resolved + manual_resolved

print(f"Ground truth dataset saved to: {output_path}")
print(f"Total songs in final dataset: {final_count}")
print(f"Automatically resolved (matching topics): {auto_resolved}")
print(f"Manually resolved (different topics): {manual_resolved}")
