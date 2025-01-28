# Song Classifier Annotation

alexeckardt - eckardta - 


## Structure

## Dataset

The dataset was collected using the Genius API. Each dataset has the following structure:

```json
[
    {
        "lyrics": [String]
        "original_source": [String]
        "original_decade": [Number]
    },
    { ... }
]
```

Each of the 8 dataset files can be found in the `./datasets` folder.

## Rules

Find the Annotation Guideline pdf at `./annotation_rules/guidelines.pdf`