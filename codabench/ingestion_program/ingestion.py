import sys
import pandas as pd
import os 
import numpy as np
import time
import json

input_dir = '/app/input_data/' # Data
output_dir = '/app/output/'    # For the predictions
program_dir = '/app/program'
submission_dir = '/app/ingested_program' # The code submitted
sys.path.append(output_dir)
sys.path.append(program_dir)
sys.path.append(submission_dir)

def get_testing_data():
    """ Get X_train, y_train and X_test from the dataset name.
    """
    # Read data
    X_train = pd.read_csv(os.path.join(input_dir, 'training_data.csv'))
    y_train = pd.read_csv(os.path.join(input_dir, 'training_label.csv'))
    X_test = pd.read_csv(os.path.join(input_dir, 'testing_data.csv'))
    # Convert to numpy arrays
    X_train, y_train, X_test = np.array(X_train), np.array(y_train), np.array(X_test)
    return X_train, y_train, X_test

def get_validation_data():
    """ Get X_train, y_train and X_test from the dataset name.
    """
    # Read data
    X_train = pd.read_csv(os.path.join(input_dir, 'validation_data.csv'))
    y_train = pd.read_csv(os.path.join(input_dir, 'validation_label.csv'))
    X_test = pd.read_csv(os.path.join(input_dir, 'testing_data.csv'))
    # Convert to numpy arrays
    X_train, y_train, X_test = np.array(X_train), np.array(y_train), np.array(X_test)
    return X_train, y_train, X_test


def main():
    """ The ingestion program.
    """
    print('-' * 20)
    print('Ingestion program.')
    from model import Model # The model submitted by the participant
    for data in ['testing', 'validation']:
        start = time.time()
        print('-' * 20)
        # Read data
        print('Reading data')
        X_train, y_train, X_test = get_validation_data() if data == 'validation' else get_testing_data()
        # Initialize model
        print('Initializing the model')
        m = Model()
        # Train model
        print('Training the model')
        m.fit(X_train, y_train)
        # Make predictions
        print('Making predictions')
        y_pred = m.predict(X_test)
        # Save predictions
        np.savetxt(os.path.join(output_dir, f'{data}.predict'), y_pred)
        duration = time.time() - start
        print(f'Time elapsed so far: {duration}')
    # End
    duration = time.time() - start
    print(f'Completed. Total duration: {duration}')
    with open(os.path.join(output_dir, 'metadata.json'), 'w+') as f:
        json.dump({'duration': duration}, f)
    print('Ingestion program finished. Moving on to scoring')
    print('-' * 20)

if __name__ == '__main__':
    main()