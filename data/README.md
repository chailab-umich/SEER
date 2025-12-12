# SEER Data and Annotations

NOTE: You must obtain the original datasets licensing in order to use these annotations.

## MuSE
Request access to the original [MuSE dataset](https://ieeexplore.ieee.org/abstract/document/8682793/?casa_token=ZmgmPj71ylQAAAAA:PNN7pf9wpYrGOKfqpfdDaX-kUjGlEKaZmSkR4j7q8vsXbHNzlgyP9gfsQPQicPdYc0_OG3YqG_g) here: [link]

Then, enter the `SEER` directory to access the CSVs `Task1_Data_MuSE.csv` and `Task2_Data_MuSE.csv`.

## MSP-Podcast
Request access to the original [MSP-Podcast](https://arxiv.org/pdf/2509.09791v1) dataset version 1.11 here: [https://www.lab-msp.com/MSP/MSP-Podcast.html]


## Task 1 Data
For both datasets, the Task 1 data contains columns:
- FileName: the wav file name from the original dataset
    - MuSE example: `06_DR-100_0093_5_sentence_7.wav`
    - MSP-Podcast example: `MSP-PODCAST_0597_0382.wav`
- Dataset: 'MuSE' or 'Podcast'
- Gender
- EmoAct: the original dataset's mean activation/arousal annotation
    - MuSE: corresponds to Activation_Mean [1,9]
    - MSP-Podcast: corresponds to EmoAct [1,7]
- EmoVal: the original dataset's mean valence annotation
    - MuSE: corresponds to Valence_Mean [1,9]
    - MSP-Podcast: corresponds to EmoVal [1,7]
- GPT4.1_EmoClass: the GPT4.1-labeled and human verified emotion class
    - emotion classes: disgust, contempt, angry, surprise, sad, happy, fear (neutral-labeled samples not included in Task 1)
- GPT4.1_EmoVal: the GPT4.1-labeled and human verified valence score
    - valence classes: positive, negative (neutral-labeled samples not included in Task 1)
- Transcription: generated with `openai/whisper-large-v2`
- Gold_Spans: expert emotion evidence annotations with inline labels via \*\* markers
    - example: "This is a \*\*very happy\*\* sentence"
- Annot*: crowdsourced emotion evidence annotations with inline labels via \*\* markers

## Task 2 Data
For both datasets, the Task 2 data contains columns:
- First_FileName: the first of the five consecutive wav-file name from the original dataset. If a file contained multiple sentences, it is split into `n` parts and relabeled with an additional `_sent{i}.wav`. 
    - MuSE example: `26_DR-100_0091_1_sentence_3_sent2.wav`
    - MSP-Podcast example: `MSP-PODCAST_0202_0030_sent1.wav`
- Consecutive_FileNames: a string representation of an array containing 5 consecutive wav-file names from the original dataset.
- Dataset
- Gender
- EmoAct: the original dataset's mean activation/arousal annotation for the first sentence
- EmoVal: the original dataset's mean valence annotation for the first sentence
- Sentence{i}_Transcript: the transcription for sentence `i`, generated with `openai/whisper-large-v2`
- Combined_Transcription: the combined transcript for five consecutive sentences
- Sentence{i}_Gold_EmoClass: the expert annotation for categorical emotion for sentence `i`
- Sentence{i}_Gold_EmoVal: the expert annotation for valence for sentence `i`
- Gold_Spans
- Annot*