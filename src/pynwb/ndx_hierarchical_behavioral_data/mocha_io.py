import os
import glob
import pandas as pd
from ndx_hierarchical_behavioral_data.definitions.transcription import TIPhonemes, HBTSyllables, HBTWords, HBTSentences


def mocha_reader(path_to_files, filename_pattern, col_list, separator=' '):
    """Read a file from specific path and convert it to a DataFrame

        For a given path, and specific file name/pattern, this function reads the file
        and stores the data in a pandas DataFrame. Name of columns should be provided.

        Parameters
        ----------
        path_to_files : str
            Path to the files
        filename_pattern: str
            name or specific pattern in the file name
        col_list: list
            list of columns' headers
        separator: str
            separator

        Returns
        ----------
        pandas.DataFrame

        """
    fpath0 = os.path.join(path_to_files, filename_pattern)
    fpath1 = glob.glob(fpath0)[0]
    data_df = pd.read_csv(fpath1,
                          names=col_list,
                          sep=separator)
    return data_df


def sentences_txt_reader(path_to_files, filename_pattern, col_list):
    """Read mocha sentences.txt data and convert them to a DataFrame

        For a given path, and specific file name/pattern, this function reads the file
        and stores the data in a pandas DataFrame. Name of columns should be provided.

        Parameters
        ----------
        path_to_files : str
            Path to the files
        filename_pattern: str
            name or specific pattern in the file name
        col_list: list
            list of headers

        Returns
        ----------
        pandas.DataFrame

        """
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
    """Read and organize phonemes, syllables, words, and sentences data in DataFrame

        For a given path, this function reads all the files related to phonemes, syllables, words, and sentences data,
        and stores them in pandas DataFrames. This function gives appropriate names to the columns.

        Parameters
        ----------
        path_to_files : str
            Path to the files

        Returns
        ----------
        phoneme_data
            pandas.DataFrame
        syllable_data
            pandas.DataFrame
        word_data
            pandas.DataFrame
        sentences_data
            pandas.DataFrame

        """
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
    """Given phonemes, syllables, words, and sentences data, this function extracts specified id's

        For given phonemes, syllables, words, and sentences data, this function extracts information about
        specified trials/session/or subjects

        Parameters
        ----------
        phoneme_data: pandas.DataFrame
            phonemes DataFrame
        syllable_data: pandas.DataFrame
            syllable DataFrame
        word_data: pandas.DataFrame
            word DataFrame
        sentences_data: pandas.DataFrame
            sentences DataFrame
        subject_id: str
            subject's id
        session_id: str
            session's id
        trial_id: str
            trial's id

        Returns
        ----------
        re_phoneme_data
            pandas.DataFrame
        re_syllable_data
            pandas.DataFrame
        re_word_data
            pandas.DataFrame
        re_sentence_data
            pandas.DataFrame

        """
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
    """Converts phonemes, syllables, words, and sentences data from a particular trials/session/or subjects into
        hierarchical table format

        For given phonemes, syllables, words, and sentences data from a particular trials/session/or subjects, this
        function converts the data into hierarchical table format.

        Parameters
        ----------
        re_phoneme_data: pandas.DataFrame
            phonemes DataFrame
        re_syllable_data: pandas.DataFrame
            syllable DataFrame
        re_word_data: pandas.DataFrame
            word DataFrame
        re_sentence_data: pandas.DataFrame
            sentences DataFrame

        Returns
        ----------
        phonemes
            pynwb.epoch.TimeIntervals
        syllables
            ndx_hierarchical_behavioral_data.hierarchical_behavioral_data.HierarchicalBehavioralTable
        words
            ndx_hierarchical_behavioral_data.hierarchical_behavioral_data.HierarchicalBehavioralTable
        sentences
            ndx_hierarchical_behavioral_data.hierarchical_behavioral_data.HierarchicalBehavioralTable

        """

    # phonemes
    phonemes = TIPhonemes()
    phonemes.add_column('preceding_phoneme', 'preceding phoneme')
    phonemes.add_column('proceeding_phoneme', 'proceeding phoneme')

    for ind in re_phoneme_data.index:
        phonemes.add_interval(label=re_phoneme_data['current_phoneme'][ind],
                              preceding_phoneme=re_phoneme_data['preceding_phoneme'][ind],
                              proceeding_phoneme=re_phoneme_data['proceeding_phoneme'][ind],
                              start_time=float(re_phoneme_data['onset'][ind]),
                              stop_time=float(re_phoneme_data['offset'][ind]))

    # syllables
    syllables = HBTSyllables(lower_tier_table=phonemes)
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
    words = HBTWords(lower_tier_table=syllables)
    for ind in re_word_data.index:
        start_ind = re_syllable_data[re_syllable_data['onset'] == re_word_data['onset'][ind]].index[0]

        if ind == len(re_word_data) - 1:
            stop_ind = len(re_syllable_data) - 1
        else:
            stop_ind = re_syllable_data[re_syllable_data['onset'] == re_word_data['onset'][ind + 1]].index[0]

        if start_ind == stop_ind:
            nt = [start_ind]
        else:
            nt = list(range(start_ind, stop_ind))

        words.add_interval(start_time=float(re_word_data['onset'][ind]),
                           stop_time=float(re_word_data['offset'][ind]),
                           label=re_word_data['word'][ind],
                           next_tier=nt)

    # sentences
    sentences = HBTSentences(lower_tier_table=words)
    for ind in re_sentence_data.index:
        sentences.add_interval(start_time=float(re_sentence_data['onset'][ind]),
                               stop_time=float(re_sentence_data['offset'][ind]),
                               label=re_sentence_data['sentence_text'][ind],
                               next_tier=list(re_word_data[re_word_data['subject']==re_sentence_data['subject'][ind]].index))

    return phonemes, syllables, words, sentences
