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


dpath = 'C:/Users/Admin/Desktop/Ben Dichter/Chang Lab/convert/Transcriptions/Transcriptions/EC118_mocha_block_GKA'

phoneme_data = mocha_reader(dpath, 'phoneme.times', col_list=['current_phoneme', 'preceding_phoneme',
                                                              'proceeding_phoneme', 'subject',
                                                              'onset', 'offset'])

word_data = mocha_reader(dpath, 'word.times', col_list=['word', 'subject',
                                                        'onset', 'offset'])

trial_data = mocha_reader(dpath, 'trial.times', col_list=['subject', 'onset',
                                                          'offset'])

syllable_data = mocha_reader(dpath, 'syllable.times', col_list=['syllable', 'subject',
                                                                'onset', 'offset'])

sentences_time_data = mocha_reader(dpath, 'sentences.times', col_list=['subject',
                                                                       'onset', 'offset'])

sentences_txt_data = sentences_txt_reader(dpath, 'sentences.txt', col_list=['subject',
                                                                            'sentence_text', 'go_cue'])

sentences_data = pd.concat([sentences_txt_data, sentences_time_data[['onset', 'offset']]], axis=1)
