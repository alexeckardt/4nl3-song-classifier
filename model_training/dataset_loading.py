import pandas as pd
import os

# Load Dataframe
def load_dataset() -> pd.DataFrame:
    # Load the dataset as dataframe

    parent_dir = os.path.dirname(os.path.dirname(__file__))
    path = os.path.join(parent_dir, 'datasets', 'combined.csv')
    dataset = pd.read_csv(path)
    return dataset