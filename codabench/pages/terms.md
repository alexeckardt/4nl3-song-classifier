# Overview
This benchmark is for the 4NL3 course in 2025 organized by group 17: Alex Eckardt, Neel Joshi, Sarah Simionescu, and Eric Zhou.  
We evaluate the performance of models that aim to classify the topic that best resonate with a song given its lyrics. 

# Data
The benchmark provides training, validation, and testing datasets, each split into separate `.csv` files.
- Inputs `X` (files ending with `_data.csv`) have shape `(num_samples)`. Each row is the lyrics of a given song. 
- Outputs `y` (files ending with `_label.csv`) have shape `(num_samples)`. Each row is a integer label `0-9` representing a topic. 
- The output labels correspond to the following topics: 

| column | topic |
|---|---|
| 0 | Break-up (heartbreak) |
| 1 | Dancing (clubbing/happy) |
| 2 | Death (loss/grief) |
| 3 | Desire (love/flirting) |
| 4 | Friendship |
| 5 | Jealousy (cheating, promiscuity) |
| 6 | Love (devotion) |
| 7 | Money (power/flexing) |
| 8 | Motivation (independence/confidence) |
| 9 | Struggle (mental health/societal issue) |

- The test labels are not made public. 

# Evaluation
Upload a zip file containing a model.py file with a Model class. The evaluator will train your model with the 
training data and make predictions for the testing data. 

The scoring metric used is the [F-1 score](https://scikit-learn.org/stable/modules/generated/sklearn.metrics.f1_score.html).
