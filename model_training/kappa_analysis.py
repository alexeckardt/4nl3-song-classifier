#Run the analasys
from dataset_loading import load_dataset


if __name__ == '__main__':

    df = load_dataset();
    print(df.head())