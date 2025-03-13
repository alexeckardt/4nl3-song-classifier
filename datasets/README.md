# ./datasets

This directory holds each dataset split up into 8 groups.

The data found in `./datasets/dataset_x.db` is unannotated, created when you run `./data_colection/songscraper.py`.
Data found in `./datasets/completed/<something>.db` is annotated, Passed back through email. The names are irrelavant.

Running `./datasets/completed/combine.py` will merge together all the annotated datasets into one large dataset CSV file; found in `./datasets/combined.csv`.

This is the dataset to be used in `./model_training`.