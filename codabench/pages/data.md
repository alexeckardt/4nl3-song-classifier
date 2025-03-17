# Data

This benchmark features the following datasets

|Phase|Nickname|Task|
|---|---|---|
| Feedback | training | Classification |
| Feedback | validation | Classification |
| Feedback | testing | Classification |
| Final | training | Classification |
| Final | validation | Classification |
| Final | testing | Classification |

Only the training data will be made public.

Each dataset is sent independently to the candidate model as:
- `X`: a `np.array` of shape `(num_samples, num_features)`,
   This will be a dataframe of lyrics 
- `y`: a `np.array` of shape `(num_samples)`, representing the labels
   This will be a dataframe of vectors. Each vector will contain 11 columns each representing a topic.
   The j-th column will be 1 if a song falls under the j-th topic and so forth. There will be exactly 2
   entries set to 1 and the others will be 0. This is because 2 topics will be assigned to each song.
