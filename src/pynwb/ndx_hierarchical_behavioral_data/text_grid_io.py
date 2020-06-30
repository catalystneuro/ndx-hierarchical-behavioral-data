import os
import glob
import pandas as pd
import re
from pynwb.epoch import TimeIntervals


def textgriddf_reader(path_to_files, filename_pattern='*TextGrid'):
    # Read the file and format it by \n
    fpath0 = os.path.join(path_to_files, filename_pattern)
    fpath1 = glob.glob(fpath0)[0]
    with open(fpath1, 'r') as f:
        data = f.read()
    data = data.split('\n')
    return data


def textgriddf_df(data, item_no=2):
    # Find indices of items in the dataset
    item_ind = []
    for i, term in enumerate(data):
        if re.findall(r'item \[\d+\]', term) != []:
            item_ind.append(i)
    item_ind.append(len(data))

    # Select an item by giving its number (starts from 1)
    # Extract information about that item from all the intervals
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
    textgrid_sentences = TimeIntervals(
        name='textgrid_sentences',
        description='desc'
    )

    textgrid_sentences.add_column('label', 'text of sentences')

    for i in text_df.index:
        textgrid_sentences.add_interval(label=text_df.iloc[i]['text'], start_time=float(text_df.iloc[i]['xmin']),
                                        stop_time=float(text_df.iloc[i]['xmax']))

    return textgrid_sentences
