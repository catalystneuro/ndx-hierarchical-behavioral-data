
import os
import glob
from ndx_hierarchical_behavioral_data.definitions.transcription import phonemes, syllables, words, sentences


def read_transcription_data(path_to_files, filename_pattern):
    fpath0 = os.path.join(path_to_files, filename_pattern)
    f_lngg_level = glob.glob(fpath0)[0]
    with open(f_lngg_level, "r") as f:
        lngg_level = []
        for x in f:
            lngg_level.append(x.split())
    f.close()
    return lngg_level



path_to_files = 'C:/Users/Admin/Desktop/Ben Dichter/Chang Lab/convert/TimitSounds (Transcriptions)/TimitSounds (Transcriptions)/fadg'

# Read data
phonemes_data = read_transcription_data(path_to_files, '*phn')
syllables_data = read_transcription_data(path_to_files, '*syll')
words_data = read_transcription_data(path_to_files, '*wrd')
sentences_data = read_transcription_data(path_to_files, '*[0-9].txt')

# Join words
for i in range(len(sentences_data)):
    sentences_data[i] = sentences_data[i][0:2] + [' '.join(sentences_data[i][2:])]


# phonemes
for phonemes_sample in phonemes_data:
    phonemes.add_interval(label=phonemes_sample[2], start_time=float(phonemes_sample[0]), stop_time=float(phonemes_sample[1]))

# syllables
## To figure out how to create syllables_keys automatically?
syllables_keys = {'0': 'h#', '1': 'bricks', '2': 'are', '3': 'an', '4': 'al', 
                  '5': 'ter', '6': 'na', '7': 'tive'}

syllables.add_column('phonemes', '')
syllables.add_column('word_onset', '')
syllables.add_column('syllable_number', '')
syllables.add_column('speech_sound', '')


for j, syllables_sample in enumerate(syllables_data):
    syllables.add_interval(label=syllables_keys[syllables_sample[4]],
                           start_time=float(syllables_sample[0]),
                           stop_time=float(syllables_sample[1]),
                           phonemes=syllables_sample[2],
                           word_onset=syllables_sample[3],
                           syllable_number=syllables_sample[4],
                           speech_sound=syllables_sample[5],
                           next_tier=[j])

## To figure out how to assign list of indices to next_tier automatically?
words_keys = {'bricks': [1], 'are': [2], 'an': [3], 'alternative': [4, 5, 6, 7]}
for words_sample in words_data:
    words.add_interval(start_time=float(words_sample[0]), stop_time=float(words_sample[1]), label=words_sample[2], next_tier=words_keys[words_sample[2]])


for sentences_sample in sentences_data:
    sentences.add_interval(start_time=float(sentences_sample[0]), stop_time=float(sentences_sample[1]), label=sentences_sample[2], next_tier=list(range(len(words_data))))
