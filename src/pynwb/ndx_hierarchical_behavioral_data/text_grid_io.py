import os
import glob
import pandas as pd
import re
from pynwb.epoch import TimeIntervals


def textgriddf_reader(path_file):
    """
    Read the TextGrid file and format it.

    Parameters
    ----------
    path_to_files : str
        Path to the files

    Returns
    ----------
    list

    """
    with open(path_file, 'r') as f:
        data = f.read()
    data = data.split('\n')
    return data


def textgriddf_df(data, item_no=2):
    """Extract sentences information from data

        For TextGrid data, and selected item, this function makes a DataFrame and stores text of sentences, start_time,
        and stop_time. It extract information about that item from all the intervals.

        Parameters
        ----------
        data : list
            data
        item_no: int
            which item to choose? (number of item)

        Returns
        ----------
        pandas.DataFrame

        """
    # Find indices of items in the dataset
    item_ind = []
    for i, term in enumerate(data):
        if re.findall(r'item \[\d+\]', term) != []:
            item_ind.append(i)
    item_ind.append(len(data))

    # Select an item by giving its number (starts from 1)
    text_list = []
    item_data = data[item_ind[item_no - 1]:item_ind[item_no]]
    for i, term in enumerate(item_data):
        if 'intervals [' in term:
            text_list.append([re.findall('\d*\.\d+|\d+', item_data[i + 1])[0],
                              re.findall('\d*\.\d+|\d+', item_data[i + 2])[0],
                              item_data[i + 3].split('=')[1].replace('"', '').strip()])

    # Make it as a dataframe
    text_df = pd.DataFrame(text_list, columns=['xmin', 'xmax', 'text'])

    return text_df


def textgriddf_converter(text_df):
    """Converts data into TimeIntervals

        For a given DataFrame this function converts the data into TimeIntervals

        Parameters
        ----------
        text_df : pandas.DataFrame
            Data related to an item

        Returns
        ----------
        pynwb.epoch.TimeIntervals

        """
    textgrid_sentences = TimeIntervals(
        name='sentences',
        description='desc'
    )

    textgrid_sentences.add_column('label', 'text of sentences')

    for i in text_df.index:
        textgrid_sentences.add_interval(label=text_df.iloc[i]['text'], start_time=float(text_df.iloc[i]['xmin']),
                                        stop_time=float(text_df.iloc[i]['xmax']))

    return textgrid_sentences
