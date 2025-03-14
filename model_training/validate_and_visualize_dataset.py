import sqlite3
import os
import pandas as pd
import matplotlib.pyplot as plt
from collections import Counter

# Setup database connection
parent_dir = os.path.dirname(os.path.dirname(__file__))
db_path = os.path.join(parent_dir, 'model_training', 'ground_truth_dataset.db')
conn = sqlite3.connect(db_path)

# Load data
df = pd.read_sql_query("SELECT * FROM songs", conn)
conn.close()

# Ensure there are no duplicates
# Check for duplicates based on song_hash
duplicate_songs = df[df.duplicated('song_hash', keep=False)]
if len(duplicate_songs) > 0:
    raise ValueError(f"Found {len(duplicate_songs)} duplicate song entries in ground truth dataset. Each song should only appear once.")


# Count individual topics (combining topic1 and topic2 since order doesn't matter)
all_topics = pd.concat([df['topic1'], df['topic2']]).value_counts()

# Create bar plot for individual topics
plt.figure(figsize=(12, 6))
all_topics.plot(kind='bar')
plt.title('Distribution of Individual Topics')
plt.xlabel('Topic')
plt.ylabel('Count')
plt.xticks(rotation=45, ha='right')
plt.tight_layout()
plt.savefig('model_training/individual_topics.png')
plt.close()

# Count topic pairs (as sets)
topic_pairs = []
for _, row in df.iterrows():
    # Sort topics to treat (A,B) and (B,A) as the same pair
    pair = tuple(sorted([row['topic1'], row['topic2']]))
    topic_pairs.append(pair)

pair_counts = Counter(topic_pairs)

# Sort pairs by count before plotting
sorted_pairs = sorted(pair_counts.items(), key=lambda x: x[1], reverse=True)
pairs = [p[0] for p in sorted_pairs]
counts = [p[1] for p in sorted_pairs]

# Create bar plot for topic pairs
plt.figure(figsize=(20, 7))  # Made figure wider
plt.bar(range(len(pairs)), counts)
plt.title('Distribution of Topic Pairs')
plt.xlabel('Topic Pair')
plt.ylabel('Count')
plt.xticks(range(len(pairs)), [f'{p[0].split("(")[0]} and {p[1].split("(")[0]}' for p in pairs], rotation=45, ha='right')
plt.subplots_adjust(bottom=0.2)  # Add more space at bottom
plt.tight_layout()
plt.savefig('model_training/topic_pairs.png')
plt.close()

print(f"Total number of records: {len(df)}")
print("\nAll individual topics:")
print(all_topics.apply(lambda x: x.split('(')[0] if isinstance(x, str) else x))
print("\nAll topic pairs:")
for pair, count in sorted_pairs:
    print(f"{pair[0].split('(')[0]}, {pair[1].split('(')[0]}: {count}")
