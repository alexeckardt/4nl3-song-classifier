import json
import os
import numpy as np
from sklearn.metrics import f1_score

reference_dir = os.path.join('/app/input', 'ref')
prediction_dir = os.path.join('/app/input', 'res')
score_dir = '/app/output'
print('Reading prediction')
prediction = np.genfromtxt(os.path.join(prediction_dir, 'prediction'))
truth = np.genfromtxt(os.path.join(reference_dir, 'testing_label'))

# compute f1-score  
f1 = f1_score(truth, prediction)

# save the score in a json file 
with open(os.path.join(score_dir, 'score.json'), 'w') as f:
    json.dump({'f1_score': f1}, f) 