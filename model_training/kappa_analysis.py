#Run the analasys
import pandas as pd
from dataset_loading import load_dataset
from kappas import binary_proportion, cohen_kappa, ordinal_kappa, cohen_set_kappa, single_cohen_set_kappa

#
#   See ./model_training/README.md
#
annotatori = 'christian'
annotatorj = 'stanley'

# Cull the dataframe for only the annotation data.
def construct_kappa_df(df):
    df = df[df.duplicated('song_hash', keep=False)].copy() # Get all that overlap
    return df.drop(columns=['artist','year','lyrics','name','id',])  # Remove Un-needed Columns

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

def buffer():
    print('=========='*2)


if __name__ == '__main__':

    # Load dataset
    print('\n'*4)
    df = load_dataset();

    # Get the Annotators with Duplicated Data (SEE ./model_training/README.md)
    dfI = df[df['annotator'] == annotatori]
    dfJ = df[df['annotator'] == annotatorj]

    # Repeat Expreiment per Columns

    # Combine
    print(f'Comparing Agreement between {annotatori} and {annotatorj}\n')

    # Construct Pairwise Dataframes
    combinedDf = pd.concat([dfI, dfJ], ignore_index=True)
    uniqueDf = construct_kappa_df(combinedDf)

    # Checking Decade
    column = 'decade'

    # Construct O(1) lookup time for each duplicate song
    iDecades = construct_agreement_dict(uniqueDf, annotatori, 'decade')
    jDecades = construct_agreement_dict(uniqueDf, annotatorj, 'decade')

    iTopic1 = construct_agreement_dict(uniqueDf, annotatori, 'topic1')
    jTopic1 = construct_agreement_dict(uniqueDf, annotatorj, 'topic1')

    iTopic2 = construct_agreement_dict(uniqueDf, annotatori, 'topic2')
    jTopic2 = construct_agreement_dict(uniqueDf, annotatorj, 'topic2')

    #
    #  Compute the Binary Kappa of the overlap
    #   What's the proprotion of the annotation that matched?
    #
    proportion = binary_proportion(iDecades, jDecades)
    kappa = cohen_kappa(iDecades, jDecades)
    print(f'Proportion on \'decade\' is {proportion:.4f}')
    print(f'Cohen Kappa on \'decade\' is {kappa:.4f}')


    #
    # Compute the Ordianl Kappa of the overlap
    #   how different were the year annotations?
    #
    kappa = ordinal_kappa(iDecades, jDecades)
    print(f'Ordinal Kappa on \'decade\' is {kappa:.4f}')
    buffer()

    #
    #   Compute the Binary Kappa of the overlap between topic 1
    #       What's the proprotion of the top topics that matched?
    #
    kappa = cohen_kappa(iTopic1, jTopic1)
    proportion = binary_proportion(iTopic1, jTopic1)
    print(f'Cohen Kappa on \'topic1\' is {kappa:.4f}')
    print(f'Proportion on \'topic1\' is {proportion:.4f}')
    
    buffer()
    #
    #   Compute the Binary Kappa of the overlap between topic 2
    #       What's the proprotion of the secondary topics that matched?
    #
    kappa = cohen_kappa(iTopic2, jTopic2)
    proportion = binary_proportion(iTopic2, jTopic2)
    print(f'Cohen Kappa on \'topic2\' is {kappa:.4f}')
    print(f'Proportion on \'topic2\' is {proportion:.4f}')

    buffer()
    
    #
    #   Compute the Setwise Kappa of the overlap between topics
    #       They might still have the same topics selected?
    #       What's the proprotion of both topics that matched (any order)?
    #
    def combine_into_set(topic1, topic2):
        
        topics = {}
        for topic in topic1:
            topics[topic] = {topic1[topic], topic2[topic]}
        return topics
    
    iTopics = combine_into_set(iTopic1, iTopic2)
    jTopics = combine_into_set(jTopic1, jTopic2)
    kappa = cohen_set_kappa(iTopics, jTopics)
    proportion = binary_proportion(iTopics, jTopics)
    print(f'Setwise Cohen Kappa on \'topic1, topic2\' is {kappa:.4f}')
    print(f'Proportion of Matching \'topic1, topic2\' is {proportion:.4f}')
    buffer()
    

    #
    #   Compute the Setwise Kappa of the overlap between topics
    #       They might still have the same topics selected?
    #       What's the proprotion of both topics that matched (any order)?
    #
    iTopics = [iTopic1, iTopic2]
    jTopics = [jTopic1, jTopic2]
    kappa = single_cohen_set_kappa(iTopics, jTopics)
    print(f'Extra: Any Agreement Setwise Proportion on \'topic1, topic2\' is {kappa:.4f}')
    print(f'\tProportion of songs with {1-kappa:.4f} completely different annotated topics')
    print('\n\n')