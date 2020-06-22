import os
import glob
import pandas as pd
import numpy as np
from ndx_hierarchical_behavioral_data.definitions.transcription import phonemes, syllables, words, sentences


def read_transcription_data(path_to_files, filename_pattern, add_headings, separator=' '):
    fpath0 = os.path.join(path_to_files, filename_pattern)
    f_lngg_level = glob.glob(fpath0)[0]
    lngg_level = pd.read_csv(f_lngg_level,
                             names=add_headings,
                             sep=separator)
    return lngg_level


def extract_syllables_data(syllables_phonemes_data):
    uniq_syl = syllables_phonemes_data['syllable_number'].unique()
    syllables_data = pd.DataFrame(columns=['start_time', 'stop_time', 'label', 'syllable_number'])
    for i in uniq_syl:
        x = syllables_phonemes_data[syllables_phonemes_data['syllable_number'] == i].reset_index()
        data = [
            [x['start_time'].iloc[0], x['stop_time'].iloc[-1], '-'.join(x["phonemes"]), x['syllable_number'].iloc[0]]]
        uniq_row = pd.DataFrame(data, columns=['start_time', 'stop_time', 'label', 'syllable_number'])
        syllables_data = syllables_data.append(uniq_row, ignore_index=True)
    last_row = pd.DataFrame([[syllables_data['stop_time'].iloc[-1], syllables_data['stop_time'].iloc[0], 'h#', 0]],
                            columns=syllables_data.columns)
    syllables_data = syllables_data.append(last_row, ignore_index=True)
    syllables_data['stop_time'].iloc[0] = syllables_data['start_time'].iloc[1]
    syllables_data['label'].iloc[0] = 'h#'
    return syllables_data


dpath = 'C:/Users/Admin/Desktop/Ben Dichter/Chang Lab/convert/TimitSounds (Transcriptions)/TimitSounds (' \
        'Transcriptions)/fadg'

# Read data
phonemes_data = read_transcription_data(dpath, '*phn', ['start_time', 'stop_time', 'label'])
syllables_phonemes_data = read_transcription_data(dpath, '*syll', ['start_time', 'stop_time', 'phonemes', 'word_onset',
                                                                   'syllable_number', 'speech_sound'])
words_data = read_transcription_data(dpath, '*wrd', ['start_time', 'stop_time', 'label'])
sentences_data = read_transcription_data(dpath, '*[0-9].txt', ['start_time', 'stop_time', 'label'], separator='\n')

# Join words
for i in range(sentences_data.shape[0]):
    sentences_data['stop_time'].loc[i] = sentences_data['start_time'].loc[i].split()[1]
    sentences_data['label'].loc[i] = ' '.join(sentences_data['start_time'].loc[i].split()[2:])
    sentences_data['start_time'].loc[i] = sentences_data['start_time'].loc[i].split()[0]

# Create syllables data
syllables_data = extract_syllables_data(syllables_phonemes_data)

# phonemes
for ind in phonemes_data.index:
    phonemes.add_interval(label=phonemes_data['label'][ind], start_time=float(phonemes_data['start_time'][ind]),
                          stop_time=float(phonemes_data['stop_time'][ind]))

# syllables
cum_phonemes_count = 0
tier_ind = []
for ind in syllables_data.index:
    phonemes_count = len(syllables_data['label'][ind].split('-'))
    tier_ind = list(range(cum_phonemes_count, cum_phonemes_count + phonemes_count))
    cum_phonemes_count = cum_phonemes_count + phonemes_count
    syllables.add_interval(label=syllables_data['label'][ind],
                           start_time=float(syllables_data['start_time'][ind]),
                           stop_time=float(syllables_data['stop_time'][ind]),
                           next_tier=np.array(tier_ind))

# To figure out how to assign list of indices to next_tier automatically?
key_columns = [[1], [2], [3], [4, 5, 6, 7]] # TODO: automate it
words_data['key_columns'] = key_columns
for ind in words_data.index:
    words.add_interval(start_time=float(words_data['start_time'][ind]),
                       stop_time=float(words_data['stop_time'][ind]),
                       label=words_data['label'][ind],
                       next_tier=words_data['key_columns'][ind])

for ind in sentences_data.index:
    sentences.add_interval(start_time=float(sentences_data['start_time'][ind]),
                           stop_time=float(sentences_data['stop_time'][ind]),
                           label=sentences_data['label'][ind],
                           next_tier=list(range(words_data.shape[0])))
