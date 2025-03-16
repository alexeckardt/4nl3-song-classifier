import pandas as pd
from sklearn.model_selection import train_test_split

# read csv
data = pd.read_csv('./codabench/feedback_phase/combined.csv')

# train on lyrics
train = data['lyrics']

# one hot encoding for topics 1 and 2, then adding the encodings together to have 2 topics to be classified
t1 = pd.get_dummies(data['topic1'])
t2 = pd.get_dummies(data['topic2'])
test = t1.add(t2, fill_value=0).astype(int)

# split data to train and test set
train_data, test_data, train_label, test_label = train_test_split(train, test, test_size=0.2, random_state=42)

# split train data to have validation set
train_data, val_data, train_label, val_label = train_test_split(train_data, train_label, test_size=0.2, random_state=42)

# write input data
train_data.to_csv('./codabench/feedback_phase/input_data/training_data.csv', header=False, index=False)
val_data.to_csv('./codabench/feedback_phase/input_data/validation_data.csv', header=False, index=False)
test_data.to_csv('./codabench/feedback_phase/input_data/testing_data.csv', header=False, index=False)

# write labels
train_label.to_csv('./codabench/feedback_phase/input_data/training_label.csv', header=False, index=False)
val_label.to_csv('./codabench/feedback_phase/input_data/validataion_data.csv', header=False, index=False)
test_label.to_csv('./codabench/feedback_phase/reference_data/testing_label.csv', header=False, index=False)