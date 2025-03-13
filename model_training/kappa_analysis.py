#Run the analasys
import pandas as pd
from dataset_loading import load_dataset

annotatori = 'christian'
annotatorj = 'stanley'


def construct_kappa_df(df):

    # Get all that overlap
    df = df[df.duplicated('song_hash', keep=False)].copy()

    # Remove Un-needed Columns
    df.drop(columns=['artist','year','lyrics','name','id',], inplace=True)

    # Passback
    return df

# Constuct O(1) lookup for the annotator based on the song hash.
def construct_agreement_dict(unique_df, annotator, column):

    #Resplit out the data per annotator
    df = unique_df[unique_df['annotator'] == annotator] #only get this person's stuff

    # Construct the Dictionary
    out = {}

    #Loop Over the df
    for i in range(0, len(df)):
        
        # Get the hask
        song_hash = df.iloc[i]['song_hash']
        result = df.iloc[i][column]

        # Store the Result
        out[song_hash] = result

    #Constructs O(1) lookup
    return out



def cohen_kappa(unique_pairwise_df, annotatori, annotatorj, column='topic1'):

    # Get
    iResults = construct_agreement_dict(unique_pairwise_df, annotatori, column)
    jResults = construct_agreement_dict(unique_pairwise_df, annotatorj, column)

    # Print
    for key in iResults:
        iAnswer = iResults[key]
        jAnswer = jResults[key]

        print(f'{key} {iAnswer} {jAnswer}')


if __name__ == '__main__':

    # Load dataset
    df = load_dataset();
    # annotators = df['annotator'].unique()

    # Get the Annotators with Duplicated Data (SEE ./model_training/README.md)
    dfI = df[df['annotator'] == annotatori]
    dfJ = df[df['annotator'] == annotatorj]

    # Repeat Expreiment per Columns
    columns_interested = ['topic1'] # ['topic1', 'topic2', 'decade', 'decade']
    for column in columns_interested:

        # Combine
        print(f'Comparing Agreement between {annotatori} and {annotatorj} on {column}')

        # Construct Pairwise Dataframes
        combinedDf = pd.concat([dfI, dfJ], ignore_index=True)
        uniqueDf = construct_kappa_df(combinedDf)

        print(uniqueDf.head())
        
        # Compute the Kappa
        cohen_kappa(uniqueDf, annotatori, annotatorj, column)
            