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
<html><table border="1" class="dataframe">\n  <thead>\n    <tr style="text-align: right;">\n      <th></th>\n      <th>label</th>\n      <th>start_time</th>\n      <th>stop_time</th>\n      <th>next_tier</th>\n    </tr>\n    <tr>\n      <th>id</th>\n      <th></th>\n      <th></th>\n      <th></th>\n      <th></th>\n    </tr>\n  </thead>\n  <tbody>\n    <tr>\n      <th>0</th>\n      <td>A-L</td>\n      <td>0.0</td>\n      <td>12.0</td>\n      <td>label  start_time  stop_time  \\\nid     ...</td>\n    </tr>\n  </tbody>\n</table></html>


This extension was created using [ndx-template](https://github.com/nwb-extensions/ndx-template).
