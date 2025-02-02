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

## Content Warning

The training data constitutes of lyrics of popular music over recent decades
which may include discriminatory language that may be offensive and upsetting.
The lyrics may also contain sensitive content.


## Annotation Instructions

### Dataset 
In order to annotate, first you need to prime your assigned dataset into the program.
We're not sure how the dataset files are going to be distributed, so see the two options below.


####Dataset File Provided
If you are provided the `.db` dataset file from the instructor, use that file for the following step.

####Dataset Number Provided
If you are told which file to annotate by the instructor, navigate over to the `datasets`, subdirectory and copy the coresponding `./datasets/dataset_X.db` file.


###Priming

To add the dataset to the annotator, copy and paste your dataset file in the `/annotation_ui/public/` subdirectory.
Importantly, be sure to rename the `.db` file to `dataset.db`.

At the end, you should have a file in the following path.

`./annotation_ui/public/dataset.db`

### Running

1. Enter into the Annotation UI directory
```bash
cd ./annotation_ui
```

2. Install packages using
```bash
npm install
```

Ensure that you have npm installed, which you can do at https://www.npmjs.com/

3. Move your designed dataset file to working directory, as described above.

4. Run the following command to generate the SQL models

```bash
npx prisma generate
```

5. Run the command

```bash
npm run dev
```
and open `localhost:3000` in a browser.


## Submission of Annotation

Please send us the `dataset.db` file you renamed and placed in the `annotation_ui\public\` subdirectory.

## Data Structure

The data to be annoated are song lyrics. Each of the following will be the lyrics to part of a song. The dataset will include the entire lyrics - here we truncate it here to save space. The song name will not be included either, it's here as a reference to the rest of the lyrics

The dataset was collected using the Lyrics.OVH API. Each dataset has the following structure:

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
This is then translated into a SQL table with the following schema:

```SQL
model Song {
  id            Int     @id @default(autoincrement())
  name          String  @unique
  artist        String  @unique
  lyrics        String  @unique
  recognized    Int
  topic1        String 
  topic2        String 
  decade        Int
}
```

While updating, we constantly update the SQL server so annotations can be interrupted and continued at any time.

Each of the 8 dataset files can be found in the `./datasets/` folder.

## Rules
Find the Annotation Guideline pdf at `./Annotation_Guideline.pdf`