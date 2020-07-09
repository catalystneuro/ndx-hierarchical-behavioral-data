
## Read from files - TimitSounds

```python
from ndx_hierarchical_behavioral_data.transcription_io import timitsounds_df, timitsounds_converter
from pynwb import NWBHDF5IO, NWBFile
from datetime import datetime

# Get transcriptions
path_transcription_dir = 'path_to_dir/'
phonemes_data, syllables_data, words_data, sentences_data, pitch_data, formant_data, intensity_data = timitsounds_df(path_to_files=path_transcription_dir)

phonemes, syllables, words, sentences, pitch_ts, formant_ts, intensity_ts = timitsounds_converter(
    phonemes_data=phonemes_data,
    syllables_data=syllables_data,
    words_data=words_data,
    sentences_data=sentences_data,
    pitch_data=pitch_data,
    formant_data=formant_data,
    intensity_data=intensity_data
)

# Create NWB file
nwbfile = NWBFile('description', 'id', datetime.now().astimezone())

# Create behavioral processing module
nwbfile.create_processing_module(
    name='behavior',
    description='behavioral data'
)

# Add transcription tables to behavioral processing module
nwbfile.processing['behavior'].add(phonemes)
nwbfile.processing['behavior'].add(syllables)
nwbfile.processing['behavior'].add(words)
nwbfile.processing['behavior'].add(sentences)

```

## Read from files - Mocha

```python
from ndx_hierarchical_behavioral_data.mocha_io import mocha_df, mocha_re_df, mocha_converter
from pynwb import NWBHDF5IO, NWBFile
from datetime import datetime

# Get transcriptions
path_to_dir = 'path_to_dir/'
phoneme_data, syllable_data, word_data, sentences_data = mocha_df(path_to_files=path_to_dir)

re_phoneme_data, re_syllable_data, re_word_data, re_sentence_data = mocha_re_df(
    phoneme_data=phoneme_data,
    syllable_data=syllable_data,
    word_data=word_data,
    sentences_data=sentences_data,
    subject_id='EC118',
    session_id='B6',
    trial_id='...'
)

phonemes, syllables, words, sentences = mocha_converter(
    re_phoneme_data=re_phoneme_data,
    re_syllable_data=re_syllable_data,
    re_word_data=re_word_data,
    re_sentence_data=re_sentence_data
)

# Create NWB file
nwbfile = NWBFile('description', 'id', datetime.now().astimezone())

# Create behavioral processing module
nwbfile.create_processing_module(
    name='behavior',
    description='behavioral data'
)

# Add transcription tables to behavioral processing module
nwbfile.processing['behavior'].add(phonemes)
nwbfile.processing['behavior'].add(syllables)
nwbfile.processing['behavior'].add(words)
nwbfile.processing['behavior'].add(sentences)
```

## Read from files - TextGrid
