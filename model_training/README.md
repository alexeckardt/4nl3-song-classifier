# Model Training

## Kappa Analysis

To run, ensure you are in the home directory. Then run the following command:

```bash
py model_training/kappa_analysis.py
```

Do to an error in our dataset splitting, only datasets_1 (`dataset-christian.db`) and dataset_2 (`dataset-stanley.db`)
contained duplicated entires. Every requirement layed out in the project description was met, (15% of the total instances are duplicated, just not split up correctly).
The error was not caught until after the data was split and recombined.

Thus, we decided to use Cohens' Kappa (Pairwise Agreement between two Annotators). This is a measure of how much two annotators agree on a set of items -- which in this case is 
between the duplicated 15% of the two datasets.