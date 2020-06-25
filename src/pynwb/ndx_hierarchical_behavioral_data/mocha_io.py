import os
import glob
import pandas as pd


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


def mocha_subject_df(phoneme_data, syllable_data, word_data, sentences_data, subject):

    subject_phoneme_data = phoneme_data[phoneme_data['subject'] == subject]
    subject_syllable_data = syllable_data[syllable_data['subject'] == subject][['syllable', 'onset', 'offset']]
    subject_word_data = word_data[word_data['subject'] == subject][['word', 'onset', 'offset']]
    subject_sentences_data = sentences_data[sentences_data['subject'] == subject][['sentence_text', 'onset', 'offset']]

    return subject_phoneme_data, subject_syllable_data, subject_word_data, subject_sentences_data
