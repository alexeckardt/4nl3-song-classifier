import pandas as pd
from sklearn.model_selection import train_test_split

data = pd.read_csv('combined.csv')

train = data['lyrics']

t1 = pd.get_dummies(data['topic1'])
t2 = pd.get_dummies(data['topic2'])
test = t1.add(t2, fill_value=0).astype(int)

train_data, test_data, train_label, test_label = train_test_split(train, test, test_size=0.2, random_state=42)

train_data.to_csv('input_data/training_data.csv', header=False, index=False)
test_data.to_csv('input_data/testing_data.csv', header=False, index=False)
train_label.to_csv('input_data/training_label.csv', header=False, index=False)
test_label.to_csv('reference_data/testing_label.csv', header=False, index=False)