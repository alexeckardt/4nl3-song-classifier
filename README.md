# Song Classifier Annotation

### Authors: 
- Alex Eckardt -
eckardta@mcmaster.ca
- Neel Joshi -
joshin10@mcmaster.ca
- Sarah Simionescu -
simiones@mcmaster.ca
- Eric Zhou -
zhoue16@mcmaster.ca


## Data Structure

The data to be annoated are song lyrics. ach of the following will be the lyrics to part of a song. The dataset will include the entire lyrics - here we truncate it here to save space. The song name will not be included either, it's here as a reference to the rest of the lyrics

The dataset was collected using the Genius(?) API. Each dataset has the following structure:

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
where each instance is a datapoint to be annotated.

Each of the 8 dataset files can be found in the `./datasets` folder.

## Rules

Find the Annotation Guideline pdf at `./annotation_rules/guidelines.pdf`