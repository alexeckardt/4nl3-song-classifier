# The scoring program compute scores from:
# - The ground truth
# - The predictions made by the candidate model

# Imports
import json
import os
import matplotlib.pyplot as plt
import io
import base64
import numpy as np
import pandas as pd
from sklearn.metrics import f1_score

# Path
input_dir = '/app/input/'    # Input from ingestion program
output_dir = '/app/output/' # To write the scores
reference_dir = os.path.join(input_dir, 'ref')   # Ground truth data
prediction_dir = os.path.join(input_dir, 'res') # Prediction made by the model
score_file = os.path.join(output_dir, 'scores.json')          # Scores
html_file = os.path.join(output_dir, 'detailed_results.html') # Detailed feedback

def write_file(file, content):
    """ Write content in file.
    """
    with open(file, 'a', encoding="utf-8") as f:
        f.write(content)

def get_dataset_names():
    """ Return the names of the datasets.
    """
    return ['testing']

def get_data(dataset):
    """ Get ground truth (y_test) and predictio0ns (y_pred) from the dataset name.
    """
    y_test = pd.read_csv(os.path.join(reference_dir, dataset + '_label.csv'), header=None)
    y_test = np.array(y_test)
    y_pred = np.genfromtxt(os.path.join(prediction_dir, dataset + '.predict'), dtype=int)
    return y_test, y_pred

def print_bar():
    """ Display a bar ('----------')
    """
    print('-' * 10)

def make_figure(scores):
    x = get_dataset_names()
    y = [scores[dataset] for dataset in x]
    fig, ax = plt.subplots()
    ax.plot(x, y, 'bo')
    ax.set_ylabel('f1 score')
    ax.set_title('Submission results')
    return fig

def fig_to_b64(fig):
    buf = io.BytesIO()
    fig.savefig(buf, format='png')
    buf.seek(0)
    fig_b64 = base64.b64encode(buf.getvalue()).decode('ascii')
    return fig_b64

def main():
    """ The scoring program.
    """
    print_bar()
    print('Scoring program.')
    # Initialized detailed results
    write_file(html_file, '<h1>Detailed results</h1>') # Create the file to give real-time feedback
    scores = {}
    for dataset in get_dataset_names(): # Loop over datasets
        print_bar()
        print(dataset)
        # Read data
        print('Reading prediction')
        y_test, y_pred = get_data(dataset)
        # Compute score
        print(y_test)
        print(y_pred)
        f1 = f1_score(y_test, y_pred, average='weighted')
        print('F1 Score: {}'.format(f1))
        scores[dataset] = f1
    # Get duration
    with open(os.path.join(prediction_dir, 'metadata.json')) as f:
        duration = json.load(f).get('duration', -1)
    scores['duration'] = duration
    # Write scores
    print_bar()
    print('Scoring program finished. Writing scores.')
    print(scores)
    write_file(score_file, json.dumps(scores))
    # Create a figure for detailed results
    figure = fig_to_b64(make_figure(scores))
    write_file(html_file, f'<img src="data:image/png;base64,{figure}">')

if __name__ == '__main__':
    main()