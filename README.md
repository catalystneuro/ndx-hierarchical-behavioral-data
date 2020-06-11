# ndx-hierarchical-behavioral-data Extension for NWB

## Installation


## Usage
Use pre-made hierarchical transcription tables:

```python
from ndx_hierarchical_behavioral_data.definitions.transcription import phonemes, syllables, words, sentences

for i, p in enumerate('abcdefghijkl'):
    phonemes.add_interval(label=p, start_time=float(i), stop_time=float(i+1))

syllables.add_interval(label='abc', next_tier=[0, 1, 2])
syllables.add_interval(label='def', next_tier=[3, 4, 5])
syllables.add_interval(label='ghi', next_tier=[6, 7, 8])
syllables.add_interval(label='jkl', next_tier=[9, 10, 11])

words.add_interval(label='A-F', next_tier=[0, 1])
words.add_interval(label='G-L', next_tier=[2, 3])

sentences.add_interval(label='A-L', next_tier=[0, 1])
```

Different view modes:
```python
sentences.to_dataframe()
```
<html><table border="1" class="dataframe">\n  <thead>\n    <tr style="text-align: right;">\n      <th></th>\n      <th>label</th>\n      <th>start_time</th>\n      <th>stop_time</th>\n      <th>next_tier</th>\n    </tr>\n    <tr>\n      <th>id</th>\n      <th></th>\n      <th></th>\n      <th></th>\n      <th></th>\n    </tr>\n  </thead>\n  <tbody>\n    <tr>\n      <th>0</th>\n      <td>A-L</td>\n      <td>0.0</td>\n      <td>12.0</td>\n      <td>label  start_time  stop_time  \\\nid                                \n0    A-F         0.0        6.0   \n1    G-L         6.0       12.0   \n\n                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                               next_tier  \nid                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                        \n0      label  start_time  stop_time  \\\nid                                \n0    abc         0.0        3.0   \n1    def         3.0        6.0   \n\n                                                                                                                                                          next_tier  \nid                                                                                                                                                                   \n0       start_time  stop_time label\nid                             \n0          0.0        1.0     a\n1          1.0        2.0     b\n2          2.0        3.0     c  \n1       start_time  stop_time label\nid                             \n3          3.0        4.0     d\n4          4.0        5.0     e\n5          5.0        6.0     f    \n1      label  start_time  stop_time  \\\nid                                \n2    ghi         6.0        9.0   \n3    jkl         9.0       12.0   \n\n                                                                                                                                                          next_tier  \nid                                                                                                                                                                   \n2       start_time  stop_time label\nid                             \n6          6.0        7.0     g\n7          7.0        8.0     h\n8          8.0        9.0     i  \n3       start_time  stop_time label\nid                             \n9          9.0       10.0     j\n10        10.0       11.0     k\n11        11.0       12.0     l</td>\n    </tr>\n  </tbody>\n</table></html>


This extension was created using [ndx-template](https://github.com/nwb-extensions/ndx-template).
