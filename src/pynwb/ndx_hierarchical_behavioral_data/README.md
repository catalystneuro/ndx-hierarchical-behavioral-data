
## Read from files - TimitSounds

```python
from ndx_hierarchical_behavioral_data.transcription_io import timitsounds_df, timitsounds_converter
from pynwb import NWBHDF5IO, NWBFile
from datetime import datetime

nwbfile = NWBFile('description', 'id', datetime.now().astimezone())

nwbfile.create_processing_module(name='behavior', description='behavioral data')
nwbfile.processing['behavior'].add(sentences)

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


## Read from files - Mocha
