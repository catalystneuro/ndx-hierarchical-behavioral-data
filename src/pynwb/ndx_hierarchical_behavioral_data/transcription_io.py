import os
import glob
import pandas as pd
import numpy as np
import re
from pynwb import TimeSeries
from ndx_hierarchical_behavioral_data.definitions.transcription import TIPhonemes, HBTSyllables, HBTWords, HBTSentences


def timitsounds_reader(path_to_files, filename_pattern, add_headings, separator=' '):
    """Read a file from specific path and convert it to a DataFrame

        For a given path, and specific file name/pattern, this function reads the file
        and stores the data in a pandas DataFrame. Name of columns should be provided in add_headings.

        Parameters
        ----------
        path_to_files: str
            Path to the files
        filename_pattern: str
            name or specific pattern in the file name
        add_headings: list
            list of headers
        separator: str
            separator

        Returns
        ----------
        pandas.DataFrame

        """
    fpath0 = os.path.join(path_to_files, filename_pattern)
    f_lngg_level = glob.glob(fpath0)[0]
    lngg_level = pd.read_csv(f_lngg_level,
                             names=add_headings,
                             sep=separator)
    return lngg_level


def intensity_reader(path_to_files, filename_pattern='*Intensity', add_headings=['h1']):
    """Read intensity data and convert them to a DataFrame

        For a given path, and specific file name/pattern, this function reads the file of intensity data
        and stores the data in a pandas DataFrame. Name of columns can be provided in add_headings.

        Parameters
        ----------
        path_to_files: str
            Path to the files
        filename_pattern: str
            name or specific pattern in the file name
        add_headings: list
            list of headers

        Returns
        ----------
        pandas.DataFrame

        """
    fpath0 = os.path.join(path_to_files, filename_pattern)
    f_lngg_level = glob.glob(fpath0)[0]
    with open(f_lngg_level, 'r') as f:
        data = f.read()
    data = data.split('\n')[15:-1]

    intensity_data = []
    for i in range(len(data)):
        intensity_data.append(float(re.findall(r"[-+]?\d*\.\d+|\d+", data[i])[2]))

    intensity_data = pd.DataFrame(intensity_data, columns=add_headings)

    return intensity_data


def syllables_data_extractor(syllables_phonemes_data):
    """Applies some preprocessing steps on provided format of syllables data to extract syllable data

        For given format of syllables data, some preprocessing steps are required to extract syllables and put them
        in a DataFrame.

        Parameters
        ----------
        syllables_phonemes_data: pandas.DataFrame
            provided format of syllables data stored in a DataFrame

        Returns
        ----------
        pandas.DataFrame

        """
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


def words_syllables_ind(syllables_phonemes_data):
    """Extracts related information for the next_tier in the word table

        Provided format of the syllables data contains word information. This function extract this information for
        use in building word table and its relation to syllables.

        Parameters
        ----------
        syllables_phonemes_data: pandas.DataFrame
            provided format of syllables data stored in a DataFrame

        Returns
        ----------
        list

        """
    word_onset = [i for i, val in enumerate(list(syllables_phonemes_data['word_onset'])) if val == 2] + [
        len(syllables_phonemes_data['word_onset']) - 1]
    syllables_onset = [i for i, val in enumerate(list(syllables_phonemes_data['word_onset'])) if val == 1]

    c = 1
    key_columns = []
    for i in range(len(word_onset) - 1):
        word_syl = [c]
        for j in syllables_onset:
            if j in range(word_onset[i], word_onset[i + 1]):
                word_syl.append(c + 1)
                c = c + 1
        c = c + 1
        key_columns.append(word_syl)

    return key_columns


def timitsounds_df(path_to_files):
    """Given path to the files, this function reads the files and stores the data in appropriate form in DataFrame

        For given path to the files, this function reads the files, extracts related phonemes, syllables, words, and
        sentences data and also pitch, intensity, and formant data and stores them in DataFrames.

        Parameters
        ----------
        path_to_files: str
            Path to the files

        Returns
        ----------
        phonemes_data
            pandas.DataFrame
        syllables_data
            pandas.DataFrame
        words_data
            pandas.DataFrame
        sentences_data
            pandas.DataFrame
        pitch_data
            pandas.DataFrame
        formant_data
            pandas.DataFrame
        intensity_data
            pandas.DataFrame

        """
    # Create phonemes dataframe
    phonemes_data = timitsounds_reader(path_to_files, '*phn', ['start_time', 'stop_time', 'label'])

    # Create syllables dataframe
    syllables_phonemes_data = timitsounds_reader(path_to_files, '*syll',
                                                 ['start_time', 'stop_time', 'phonemes', 'word_onset',
                                                  'syllable_number', 'speech_sound'])
    syllables_data = syllables_data_extractor(syllables_phonemes_data)

    # Create words dataframe
    words_data = timitsounds_reader(path_to_files, '*wrd', ['start_time', 'stop_time', 'label'])
    key_columns = words_syllables_ind(syllables_phonemes_data)
    words_data['key_columns'] = key_columns

    # Create sentences dataframe
    sentences_data = timitsounds_reader(path_to_files, '*[0-9].txt', ['start_time', 'stop_time', 'label'],
                                        separator='\n')
    for i in range(sentences_data.shape[0]):
        sentences_data['stop_time'].loc[i] = sentences_data['start_time'].loc[i].split()[1]
        sentences_data['label'].loc[i] = ' '.join(sentences_data['start_time'].loc[i].split()[2:])
        sentences_data['start_time'].loc[i] = sentences_data['start_time'].loc[i].split()[0]

    # Create other dataframes
    pitch_data = timitsounds_reader(path_to_files, '*f0', ['h1', 'h2', 'h3', 'h4'])
    formant_data = timitsounds_reader(path_to_files, '*frm', ['h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'h7', 'h8'])
    intensity_data = intensity_reader(path_to_files)

    return phonemes_data, syllables_data, words_data, sentences_data, pitch_data, formant_data, intensity_data


def timitsounds_converter(phonemes_data, syllables_data, words_data, sentences_data, pitch_data, formant_data,
                          intensity_data):
    """Converts phonemes, syllables, words, sentences, pitch, formant, and intensity data into
        hierarchical table format

        For given phonemes, syllables, words, sentences, pitch, formant, and intensity data, this
        function converts the data into hierarchical table format.

        Parameters
        ----------
        phonemes_data: pandas.DataFrame
            phonemes DataFrame
        syllables_data: pandas.DataFrame
            syllable DataFrame
        words_data: pandas.DataFrame
            word DataFrame
        sentences_data: pandas.DataFrame
            sentences DataFrame
        pitch_data: pandas.DataFrame
            pitch DataFrame
        formant_data: pandas.DataFrame
            formant DataFrame
        intensity_data: pandas.DataFrame
            intensity DataFrame

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
        pitch_ts
            pynwb.base.TimeSeries
        formant_ts
            pynwb.base.TimeSeries
        intensity_ts
            pynwb.base.TimeSeries

        """
    # phonemes
    phonemes = TIPhonemes()
    for ind in phonemes_data.index:
        phonemes.add_interval(label=phonemes_data['label'][ind], start_time=float(phonemes_data['start_time'][ind]),
                              stop_time=float(phonemes_data['stop_time'][ind]))

    # syllables
    syllables = HBTSyllables(lower_tier_table=phonemes)
    cum_phonemes_count = 0
    for ind in syllables_data.index:
        phonemes_count = len(syllables_data['label'][ind].split('-'))
        tier_ind = list(range(cum_phonemes_count, cum_phonemes_count + phonemes_count))
        cum_phonemes_count = cum_phonemes_count + phonemes_count
        syllables.add_interval(label=syllables_data['label'][ind],
                               start_time=float(syllables_data['start_time'][ind]),
                               stop_time=float(syllables_data['stop_time'][ind]),
                               next_tier=np.array(tier_ind))

    # words
    words = HBTWords(lower_tier_table=syllables)
    for ind in words_data.index:
        words.add_interval(start_time=float(words_data['start_time'][ind]),
                           stop_time=float(words_data['stop_time'][ind]),
                           label=words_data['label'][ind],
                           next_tier=words_data['key_columns'][ind])

    # sentences
    sentences = HBTSentences(lower_tier_table=words)
    for ind in sentences_data.index:
        sentences.add_interval(start_time=float(sentences_data['start_time'][ind]),
                               stop_time=float(sentences_data['stop_time'][ind]),
                               label=sentences_data['label'][ind],
                               next_tier=list(range(words_data.shape[0])))

    # others
    pitch_ts = TimeSeries(name='pitch_timeseries', data=np.array(pitch_data), starting_time=0.0, unit='s', rate=1.0)
    formant_ts = TimeSeries(name='formant_timeseries', data=np.array(formant_data), starting_time=0.0, unit='s',
                            rate=1.0) #TODO: rate information for pitch and formant
    intensity_ts = TimeSeries(name='intensity_timeseries', data=np.array(intensity_data), starting_time=0.032, unit='s',
                              rate=1000.0)

    return phonemes, syllables, words, sentences, pitch_ts, formant_ts, intensity_ts
