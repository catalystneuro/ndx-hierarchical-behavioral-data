import os
import glob
import pandas as pd
from ndx_hierarchical_behavioral_data.definitions.transcription import phonemes, syllables, words, sentences


def mocha_reader(path_to_files, filename_pattern, col_list, separator=' '):
    # Read the file
    fpath0 = os.path.join(path_to_files, filename_pattern)
    fpath1 = glob.glob(fpath0)[0]
    data_df = pd.read_csv(fpath1,
                          names=col_list,
                          sep=separator)
    return data_df


def sentences_txt_reader(path_to_files, filename_pattern, col_list):
    # Read the file
    fpath0 = os.path.join(path_to_files, filename_pattern)
    fpath1 = glob.glob(fpath0)[0]
    with open(fpath1, 'r') as f:
        data = f.read()
    data = data.split('\n')
    data = data[0:-1]
    for i, val in enumerate(data):
        splt_data = val.split()
        data[i] = [splt_data[1], ' '.join(splt_data[2:-2]).replace('"', ''), splt_data[-2]]
    data_df = pd.DataFrame(data, columns=col_list)
    return data_df


def mocha_df(path_to_files):
    phoneme_data = mocha_reader(path_to_files, 'phoneme.times', col_list=['current_phoneme', 'preceding_phoneme',
                                                                          'proceeding_phoneme', 'subject',
                                                                          'onset', 'offset'])

    syllable_data = mocha_reader(path_to_files, 'syllable.times', col_list=['syllable', 'subject',
                                                                            'onset', 'offset'])

    word_data = mocha_reader(path_to_files, 'word.times', col_list=['word', 'subject',
                                                                    'onset', 'offset'])

    sentences_time_data = mocha_reader(path_to_files, 'sentences.times', col_list=['subject',
                                                                                   'onset', 'offset'])

    sentences_txt_data = sentences_txt_reader(path_to_files, 'sentences.txt', col_list=['subject',
                                                                                        'sentence_text', 'go_cue'])

    sentences_data = pd.concat([sentences_txt_data, sentences_time_data[['onset', 'offset']]], axis=1)

    return phoneme_data, syllable_data, word_data, sentences_data


def mocha_re_df(phoneme_data, syllable_data, word_data, sentences_data, subject_id='.....', session_id='...?',
                trial_id='...'):
    re_kw = subject_id + '_' + session_id + '_' + trial_id
    re_phoneme_data = phoneme_data[phoneme_data['subject'].str.contains(re_kw)].reset_index(drop=True)
    re_syllable_data = syllable_data[syllable_data['subject'].str.contains(re_kw)][['syllable', 'onset',
                                                                                    'offset',
                                                                                    'subject']].reset_index(drop=True)
    re_word_data = word_data[word_data['subject'].str.contains(re_kw)][['word', 'onset',
                                                                        'offset', 'subject']].reset_index(drop=True)
    re_sentence_data = sentences_data[sentences_data['subject'].str.contains(re_kw)][['sentence_text', 'onset',
                                                                                      'offset',
                                                                                      'subject']].reset_index(drop=True)

    return re_phoneme_data, re_syllable_data, re_word_data, re_sentence_data


def mocha_converter(re_phoneme_data, re_syllable_data, re_word_data, re_sentence_data):
    # phonemes
    phonemes.add_column('preceding_phoneme', 'preceding phoneme')
    phonemes.add_column('proceeding_phoneme', 'proceeding phoneme')

    for ind in re_phoneme_data.index:
        phonemes.add_interval(label=re_phoneme_data['current_phoneme'][ind],
                              preceding_phoneme=re_phoneme_data['preceding_phoneme'][ind],
                              proceeding_phoneme=re_phoneme_data['proceeding_phoneme'][ind],
                              start_time=float(re_phoneme_data['onset'][ind]),
                              stop_time=float(re_phoneme_data['offset'][ind]))

    # syllables
    nt_list = [[0]]
    for ind in re_syllable_data.index:
        phonemes_indices = re_syllable_data['syllable'][ind].split('_')
        phonemes_indices = [i for i in phonemes_indices if i]
        start_ind = nt_list[ind][-1] + 1
        nt = list(range(start_ind, start_ind + len(phonemes_indices)))
        nt_list.append(nt)
        syllables.add_interval(label=re_syllable_data['syllable'][ind],
                               start_time=float(re_syllable_data['onset'][ind]),
                               stop_time=float(re_syllable_data['offset'][ind]),
                               next_tier=nt)

    # words
    for ind in re_word_data.index:
        words.add_interval(start_time=float(re_word_data['onset'][ind]),
                           stop_time=float(re_word_data['offset'][ind]),
                           label=re_word_data['word'][ind],
                           next_tier=[0])  # TODO: words-to-syllables map required

    # sentences
    for ind in re_sentence_data.index:
        sentences.add_interval(start_time=float(re_sentence_data['onset'][ind]),
                               stop_time=float(re_sentence_data['offset'][ind]),
                               label=re_sentence_data['sentence_text'][ind],
                               next_tier=list(re_word_data[re_word_data['subject']==re_sentence_data['subject'][ind]].index))

    return phonemes, syllables, words, sentences
