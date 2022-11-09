# ndx-hierarchical-behavioral-data Extension for NWB

[![PyPI version](https://badge.fury.io/py/ndx-hierarchical-behavioral-data.svg)](https://badge.fury.io/py/ndx-hierarchical-behavioral-data)

![schema schema](https://github.com/catalystneuro/ndx-hierarchical-behavioral-data/blob/master/docs/media/hierarchical_behavioral_data.png?raw=true)

## Installation

```
pip install ndx-hierarchical-behavioral-data
```

## Usage
Use pre-made hierarchical transcription tables:

```python
from ndx_hierarchical_behavioral_data.definitions.transcription import TIPhonemes, HBTSyllables, HBTWords, HBTSentences

# Phonemes level
phonemes = TIPhonemes()
phonemes.add_column('max_pitch', 'maximum pitch for this phoneme. NaN for unvoiced')
for i, p in enumerate('abcdefghijkl'):
    phonemes.add_interval(label=p, start_time=float(i), stop_time=float(i+1), max_pitch=i**2)

# Syllables level
syllables = HBTSyllables(lower_tier_table=phonemes)
syllables.add_interval(label='abc', next_tier=[0, 1, 2])
syllables.add_interval(label='def', next_tier=[3, 4, 5])
syllables.add_interval(label='ghi', next_tier=[6, 7, 8])
syllables.add_interval(label='jkl', next_tier=[9, 10, 11])

# Words level
words = HBTWords(lower_tier_table=syllables)
words.add_column('emphasis', 'boolean indicating whether this word was emphasized')
words.add_interval(label='A-F', next_tier=[0, 1], emphasis=False)
words.add_interval(label='G-L', next_tier=[2, 3], emphasis=True)

# Sentences level
sentences = HBTSentences(lower_tier_table=words)
sentences.add_interval(label='A-L', next_tier=[0, 1])
```

View individual tiers:

```python
sentences.to_dataframe()
```
<html><table border="1" class="dataframe"><thead><tr style="text-align: right;"><th></th><th>label</th><th>start_time</th><th>stop_time</th><th>next_tier</th></tr><tr><th>id</th><th></th><th></th><th></th><th></th></tr></thead><tbody><tr><th>0</th><td>A-L</td><td>0.0</td><td>12.0</td><td>label  start_time  stop_time  \\id     ...</td></tr></tbody></table></html>


```python
words.to_dataframe()
```

<html><table border="1" class="dataframe"> <thead> <tr style="text-align: right;"> <th></th> <th>label</th> <th>start_time</th> <th>stop_time</th> <th>next_tier</th> <th>emphasis</th> </tr> <tr> <th>id</th> <th></th> <th></th> <th></th> <th></th> <th></th> </tr> </thead> <tbody> <tr> <th>0</th> <td>A-F</td> <td>0.0</td> <td>6.0</td> <td>label  start_time  stop_time  \\ id                                 0    abc         0.0        3.0    1    def         3.0        6.0     next_tier   id                                                                                                                                                                                                                           0       start_time  stop_time label  max_pitch id                                         0          0.0        1.0     a          0 1          1.0        2.0     b          1 2          2.0        3.0     c          4   1       start_time  stop_time label  max_pitch id                                         3          3.0        4.0     d          9 4          4.0        5.0     e         16 5          5.0        6.0     f         25</td> <td>False</td> </tr> <tr> <th>1</th> <td>G-L</td> <td>6.0</td> <td>12.0</td> <td>label  start_time  stop_time  \\ id                                 2    ghi         6.0        9.0    3    jkl         9.0       12.0     next_tier   id                                                                                                                                                                                                                           2       start_time  stop_time label  max_pitch id                                         6          6.0        7.0     g         36 7          7.0        8.0     h         49 8          8.0        9.0     i         64   3       start_time  stop_time label  max_pitch id                                         9          9.0       10.0     j         81 10        10.0       11.0     k        100 11        11.0       12.0     l        121</td> <td>True</td> </tr> </tbody> </table></html>

```python
syllables.to_dataframe()
```

<html><table border="1" class="dataframe"><thead><tr style="text-align: right;"><th></th><th>label</th><th>start_time</th><th>stop_time</th><th>next_tier</th></tr> <tr> <th>id</th> <th></th> <th></th> <th></th> <th></th> </tr> </thead> <tbody> <tr> <th>0</th> <td>abc</td> <td>0.0</td> <td>3.0</td> <td>start_time  stop_time label id                              0          0.0        1.0     a 1          1.0        2.0     b 2          2.0        3.0     c</td> </tr> <tr> <th>1</th> <td>def</td> <td>3.0</td> <td>6.0</td> <td>start_time  stop_time label id                              3          3.0        4.0     d 4          4.0        5.0     e 5          5.0        6.0     f</td> </tr> <tr> <th>2</th> <td>ghi</td> <td>6.0</td> <td>9.0</td> <td>start_time  stop_time label id                              6          6.0        7.0     g 7          7.0        8.0     h 8          8.0        9.0     i</td> </tr> <tr> <th>3</th> <td>jkl</td> <td>9.0</td> <td>12.0</td> <td>start_time  stop_time label id                              9          9.0       10.0     j 10        10.0       11.0     k 11        11.0       12.0     l</td> </tr> </tbody> </table></html>

```python
phonemes.to_dataframe()
```

<html><table border="1" class="dataframe"> <thead> <tr style="text-align: right;"> <th></th> <th>start_time</th> <th>stop_time</th> <th>label</th> <th>max_pitch</th> </tr> <tr> <th>id</th> <th></th> <th></th> <th></th> <th></th> </tr> </thead> <tbody> <tr> <th>0</th> <td>0.0</td> <td>1.0</td> <td>a</td> <td>0</td> </tr> <tr> <th>1</th> <td>1.0</td> <td>2.0</td> <td>b</td> <td>1</td> </tr> <tr> <th>2</th> <td>2.0</td> <td>3.0</td> <td>c</td> <td>4</td> </tr> <tr> <th>3</th> <td>3.0</td> <td>4.0</td> <td>d</td> <td>9</td> </tr> <tr> <th>4</th> <td>4.0</td> <td>5.0</td> <td>e</td> <td>16</td> </tr> <tr> <th>5</th> <td>5.0</td> <td>6.0</td> <td>f</td> <td>25</td> </tr> <tr> <th>6</th> <td>6.0</td> <td>7.0</td> <td>g</td> <td>36</td> </tr> <tr> <th>7</th> <td>7.0</td> <td>8.0</td> <td>h</td> <td>49</td> </tr> <tr> <th>8</th> <td>8.0</td> <td>9.0</td> <td>i</td> <td>64</td> </tr> <tr> <th>9</th> <td>9.0</td> <td>10.0</td> <td>j</td> <td>81</td> </tr> <tr> <th>10</th> <td>10.0</td> <td>11.0</td> <td>k</td> <td>100</td> </tr> <tr> <th>11</th> <td>11.0</td> <td>12.0</td> <td>l</td> <td>121</td> </tr> </tbody> </table></html>


Hierarchical dataframe:
```python
sentences.to_hierarchical_dataframe()
```
<html><table border="1" class="dataframe"> <thead> <tr> <th></th> <th></th> <th></th> <th></th> <th></th> <th></th> <th></th> <th></th> <th></th> <th></th> <th></th> <th></th> <th>source_table</th> <th colspan="5" halign="left">phonemes</th> </tr> <tr> <th></th> <th></th> <th></th> <th></th> <th></th> <th></th> <th></th> <th></th> <th></th> <th></th> <th></th> <th></th> <th>label</th> <th>id</th> <th>start_time</th> <th>stop_time</th> <th>label</th> <th>max_pitch</th> </tr> <tr> <th>sentences_id</th> <th>sentences_label</th> <th>sentences_start_time</th> <th>sentences_stop_time</th> <th>words_id</th> <th>words_label</th> <th>words_start_time</th> <th>words_stop_time</th> <th>words_emphasis</th> <th>syllables_id</th> <th>syllables_label</th> <th>syllables_start_time</th> <th>syllables_stop_time</th> <th></th> <th></th> <th></th> <th></th> <th></th> </tr> </thead> <tbody> <tr> <th rowspan="12" valign="top">0</th> <th rowspan="12" valign="top">A-L</th> <th rowspan="12" valign="top">0.0</th> <th rowspan="12" valign="top">12.0</th> <th rowspan="6" valign="top">0</th> <th rowspan="6" valign="top">A-F</th> <th rowspan="6" valign="top">0.0</th> <th rowspan="6" valign="top">6.0</th> <th rowspan="6" valign="top">False</th> <th rowspan="3" valign="top">0</th> <th rowspan="3" valign="top">abc</th> <th rowspan="3" valign="top">0.0</th> <th>3.0</th> <td>0</td> <td>0.0</td> <td>1.0</td> <td>a</td> <td>0</td> </tr> <tr> <th>3.0</th> <td>1</td> <td>1.0</td> <td>2.0</td> <td>b</td> <td>1</td> </tr> <tr> <th>3.0</th> <td>2</td> <td>2.0</td> <td>3.0</td> <td>c</td> <td>4</td> </tr> <tr> <th rowspan="3" valign="top">1</th> <th rowspan="3" valign="top">def</th> <th rowspan="3" valign="top">3.0</th> <th>6.0</th> <td>3</td> <td>3.0</td> <td>4.0</td> <td>d</td> <td>9</td> </tr> <tr> <th>6.0</th> <td>4</td> <td>4.0</td> <td>5.0</td> <td>e</td> <td>16</td> </tr> <tr> <th>6.0</th> <td>5</td> <td>5.0</td> <td>6.0</td> <td>f</td> <td>25</td> </tr> <tr> <th rowspan="6" valign="top">1</th> <th rowspan="6" valign="top">G-L</th> <th rowspan="6" valign="top">6.0</th> <th rowspan="6" valign="top">12.0</th> <th rowspan="6" valign="top">True</th> <th rowspan="3" valign="top">2</th> <th rowspan="3" valign="top">ghi</th> <th rowspan="3" valign="top">6.0</th> <th>9.0</th> <td>6</td> <td>6.0</td> <td>7.0</td> <td>g</td> <td>36</td> </tr> <tr> <th>9.0</th> <td>7</td> <td>7.0</td> <td>8.0</td> <td>h</td> <td>49</td> </tr> <tr> <th>9.0</th> <td>8</td> <td>8.0</td> <td>9.0</td> <td>i</td> <td>64</td> </tr> <tr> <th rowspan="3" valign="top">3</th> <th rowspan="3" valign="top">jkl</th> <th rowspan="3" valign="top">9.0</th> <th>12.0</th> <td>9</td> <td>9.0</td> <td>10.0</td> <td>j</td> <td>81</td> </tr> <tr> <th>12.0</th> <td>10</td> <td>10.0</td> <td>11.0</td> <td>k</td> <td>100</td> </tr> <tr> <th>12.0</th> <td>11</td> <td>11.0</td> <td>12.0</td> <td>l</td> <td>121</td> </tr> </tbody> </table></html>


Hierachical columns, flattened rows:

```python
from hdmf.common.hierarchicaltable import flatten_column_index

flatten_column_index(sentences.to_hierarchical_dataframe(), 1)
```

<html><table border="1" class="dataframe"> <thead> <tr style="text-align: right;"> <th></th> <th></th> <th></th> <th></th> <th></th> <th></th> <th></th> <th></th> <th></th> <th></th> <th></th> <th></th> <th></th> <th>id</th> <th>start_time</th> <th>stop_time</th> <th>label</th> <th>max_pitch</th> </tr> <tr> <th>sentences_id</th> <th>sentences_label</th> <th>sentences_start_time</th> <th>sentences_stop_time</th> <th>words_id</th> <th>words_label</th> <th>words_start_time</th> <th>words_stop_time</th> <th>words_emphasis</th> <th>syllables_id</th> <th>syllables_label</th> <th>syllables_start_time</th> <th>syllables_stop_time</th> <th></th> <th></th> <th></th> <th></th> <th></th> </tr> </thead> <tbody> <tr> <th rowspan="12" valign="top">0</th> <th rowspan="12" valign="top">A-L</th> <th rowspan="12" valign="top">0.0</th> <th rowspan="12" valign="top">12.0</th> <th rowspan="6" valign="top">0</th> <th rowspan="6" valign="top">A-F</th> <th rowspan="6" valign="top">0.0</th> <th rowspan="6" valign="top">6.0</th> <th rowspan="6" valign="top">False</th> <th rowspan="3" valign="top">0</th> <th rowspan="3" valign="top">abc</th> <th rowspan="3" valign="top">0.0</th> <th>3.0</th> <td>0</td> <td>0.0</td> <td>1.0</td> <td>a</td> <td>0</td> </tr> <tr> <th>3.0</th> <td>1</td> <td>1.0</td> <td>2.0</td> <td>b</td> <td>1</td> </tr> <tr> <th>3.0</th> <td>2</td> <td>2.0</td> <td>3.0</td> <td>c</td> <td>4</td> </tr> <tr> <th rowspan="3" valign="top">1</th> <th rowspan="3" valign="top">def</th> <th rowspan="3" valign="top">3.0</th> <th>6.0</th> <td>3</td> <td>3.0</td> <td>4.0</td> <td>d</td> <td>9</td> </tr> <tr> <th>6.0</th> <td>4</td> <td>4.0</td> <td>5.0</td> <td>e</td> <td>16</td> </tr> <tr> <th>6.0</th> <td>5</td> <td>5.0</td> <td>6.0</td> <td>f</td> <td>25</td> </tr> <tr> <th rowspan="6" valign="top">1</th> <th rowspan="6" valign="top">G-L</th> <th rowspan="6" valign="top">6.0</th> <th rowspan="6" valign="top">12.0</th> <th rowspan="6" valign="top">True</th> <th rowspan="3" valign="top">2</th> <th rowspan="3" valign="top">ghi</th> <th rowspan="3" valign="top">6.0</th> <th>9.0</th> <td>6</td> <td>6.0</td> <td>7.0</td> <td>g</td> <td>36</td> </tr> <tr> <th>9.0</th> <td>7</td> <td>7.0</td> <td>8.0</td> <td>h</td> <td>49</td> </tr> <tr> <th>9.0</th> <td>8</td> <td>8.0</td> <td>9.0</td> <td>i</td> <td>64</td> </tr> <tr> <th rowspan="3" valign="top">3</th> <th rowspan="3" valign="top">jkl</th> <th rowspan="3" valign="top">9.0</th> <th>12.0</th> <td>9</td> <td>9.0</td> <td>10.0</td> <td>j</td> <td>81</td> </tr> <tr> <th>12.0</th> <td>10</td> <td>10.0</td> <td>11.0</td> <td>k</td> <td>100</td> </tr> <tr> <th>12.0</th> <td>11</td> <td>11.0</td> <td>12.0</td> <td>l</td> <td>121</td> </tr> </tbody> </table></html>

Denormalized dataframe:
```python
from hdmf.common.hierarchicaltable import to_hierarchical_dataframe

to_hierarchical_dataframe(sentences).reset_index()
```

<html><table border="1" class="dataframe"> <thead> <tr> <th>source_table</th> <th colspan="4" halign="left">sentences</th> <th colspan="5" halign="left">words</th> <th colspan="4" halign="left">syllables</th> <th colspan="5" halign="left">phonemes</th> </tr> <tr> <th>label</th> <th>id</th> <th>label</th> <th>start_time</th> <th>stop_time</th> <th>id</th> <th>label</th> <th>start_time</th> <th>stop_time</th> <th>emphasis</th> <th>id</th> <th>label</th> <th>start_time</th> <th>stop_time</th> <th>id</th> <th>start_time</th> <th>stop_time</th> <th>label</th> <th>max_pitch</th> </tr> </thead> <tbody> <tr> <th>0</th> <td>0</td> <td>A-L</td> <td>0.0</td> <td>12.0</td> <td>0</td> <td>A-F</td> <td>0.0</td> <td>6.0</td> <td>False</td> <td>0</td> <td>abc</td> <td>0.0</td> <td>3.0</td> <td>0</td> <td>0.0</td> <td>1.0</td> <td>a</td> <td>0</td> </tr> <tr> <th>1</th> <td>0</td> <td>A-L</td> <td>0.0</td> <td>12.0</td> <td>0</td> <td>A-F</td> <td>0.0</td> <td>6.0</td> <td>False</td> <td>0</td> <td>abc</td> <td>0.0</td> <td>3.0</td> <td>1</td> <td>1.0</td> <td>2.0</td> <td>b</td> <td>1</td> </tr> <tr> <th>2</th> <td>0</td> <td>A-L</td> <td>0.0</td> <td>12.0</td> <td>0</td> <td>A-F</td> <td>0.0</td> <td>6.0</td> <td>False</td> <td>0</td> <td>abc</td> <td>0.0</td> <td>3.0</td> <td>2</td> <td>2.0</td> <td>3.0</td> <td>c</td> <td>4</td> </tr> <tr> <th>3</th> <td>0</td> <td>A-L</td> <td>0.0</td> <td>12.0</td> <td>0</td> <td>A-F</td> <td>0.0</td> <td>6.0</td> <td>False</td> <td>1</td> <td>def</td> <td>3.0</td> <td>6.0</td> <td>3</td> <td>3.0</td> <td>4.0</td> <td>d</td> <td>9</td> </tr> <tr> <th>4</th> <td>0</td> <td>A-L</td> <td>0.0</td> <td>12.0</td> <td>0</td> <td>A-F</td> <td>0.0</td> <td>6.0</td> <td>False</td> <td>1</td> <td>def</td> <td>3.0</td> <td>6.0</td> <td>4</td> <td>4.0</td> <td>5.0</td> <td>e</td> <td>16</td> </tr> <tr> <th>5</th> <td>0</td> <td>A-L</td> <td>0.0</td> <td>12.0</td> <td>0</td> <td>A-F</td> <td>0.0</td> <td>6.0</td> <td>False</td> <td>1</td> <td>def</td> <td>3.0</td> <td>6.0</td> <td>5</td> <td>5.0</td> <td>6.0</td> <td>f</td> <td>25</td> </tr> <tr> <th>6</th> <td>0</td> <td>A-L</td> <td>0.0</td> <td>12.0</td> <td>1</td> <td>G-L</td> <td>6.0</td> <td>12.0</td> <td>True</td> <td>2</td> <td>ghi</td> <td>6.0</td> <td>9.0</td> <td>6</td> <td>6.0</td> <td>7.0</td> <td>g</td> <td>36</td> </tr> <tr> <th>7</th> <td>0</td> <td>A-L</td> <td>0.0</td> <td>12.0</td> <td>1</td> <td>G-L</td> <td>6.0</td> <td>12.0</td> <td>True</td> <td>2</td> <td>ghi</td> <td>6.0</td> <td>9.0</td> <td>7</td> <td>7.0</td> <td>8.0</td> <td>h</td> <td>49</td> </tr> <tr> <th>8</th> <td>0</td> <td>A-L</td> <td>0.0</td> <td>12.0</td> <td>1</td> <td>G-L</td> <td>6.0</td> <td>12.0</td> <td>True</td> <td>2</td> <td>ghi</td> <td>6.0</td> <td>9.0</td> <td>8</td> <td>8.0</td> <td>9.0</td> <td>i</td> <td>64</td> </tr> <tr> <th>9</th> <td>0</td> <td>A-L</td> <td>0.0</td> <td>12.0</td> <td>1</td> <td>G-L</td> <td>6.0</td> <td>12.0</td> <td>True</td> <td>3</td> <td>jkl</td> <td>9.0</td> <td>12.0</td> <td>9</td> <td>9.0</td> <td>10.0</td> <td>j</td> <td>81</td> </tr> <tr> <th>10</th> <td>0</td> <td>A-L</td> <td>0.0</td> <td>12.0</td> <td>1</td> <td>G-L</td> <td>6.0</td> <td>12.0</td> <td>True</td> <td>3</td> <td>jkl</td> <td>9.0</td> <td>12.0</td> <td>10</td> <td>10.0</td> <td>11.0</td> <td>k</td> <td>100</td> </tr> <tr> <th>11</th> <td>0</td> <td>A-L</td> <td>0.0</td> <td>12.0</td> <td>1</td> <td>G-L</td> <td>6.0</td> <td>12.0</td> <td>True</td> <td>3</td> <td>jkl</td> <td>9.0</td> <td>12.0</td> <td>11</td> <td>11.0</td> <td>12.0</td> <td>l</td> <td>121</td> </tr> </tbody> </table></html>

Denormalized dataframe with flattened columns:
```python
from hdmf.common.hierarchicaltable import flatten_column_index

flatten_column_index(sentences.to_hierarchical_dataframe(), 1).reset_index()
```

<html><table border="1" class="dataframe"> <thead> <tr style="text-align: right;"> <th></th> <th>sentences_id</th> <th>sentences_label</th> <th>sentences_start_time</th> <th>sentences_stop_time</th> <th>words_id</th> <th>words_label</th> <th>words_start_time</th> <th>words_stop_time</th> <th>words_emphasis</th> <th>syllables_id</th> <th>syllables_label</th> <th>syllables_start_time</th> <th>syllables_stop_time</th> <th>id</th> <th>start_time</th> <th>stop_time</th> <th>label</th> <th>max_pitch</th> </tr> </thead> <tbody> <tr> <th>0</th> <td>0</td> <td>A-L</td> <td>0.0</td> <td>12.0</td> <td>0</td> <td>A-F</td> <td>0.0</td> <td>6.0</td> <td>False</td> <td>0</td> <td>abc</td> <td>0.0</td> <td>3.0</td> <td>0</td> <td>0.0</td> <td>1.0</td> <td>a</td> <td>0</td> </tr> <tr> <th>1</th> <td>0</td> <td>A-L</td> <td>0.0</td> <td>12.0</td> <td>0</td> <td>A-F</td> <td>0.0</td> <td>6.0</td> <td>False</td> <td>0</td> <td>abc</td> <td>0.0</td> <td>3.0</td> <td>1</td> <td>1.0</td> <td>2.0</td> <td>b</td> <td>1</td> </tr> <tr> <th>2</th> <td>0</td> <td>A-L</td> <td>0.0</td> <td>12.0</td> <td>0</td> <td>A-F</td> <td>0.0</td> <td>6.0</td> <td>False</td> <td>0</td> <td>abc</td> <td>0.0</td> <td>3.0</td> <td>2</td> <td>2.0</td> <td>3.0</td> <td>c</td> <td>4</td> </tr> <tr> <th>3</th> <td>0</td> <td>A-L</td> <td>0.0</td> <td>12.0</td> <td>0</td> <td>A-F</td> <td>0.0</td> <td>6.0</td> <td>False</td> <td>1</td> <td>def</td> <td>3.0</td> <td>6.0</td> <td>3</td> <td>3.0</td> <td>4.0</td> <td>d</td> <td>9</td> </tr> <tr> <th>4</th> <td>0</td> <td>A-L</td> <td>0.0</td> <td>12.0</td> <td>0</td> <td>A-F</td> <td>0.0</td> <td>6.0</td> <td>False</td> <td>1</td> <td>def</td> <td>3.0</td> <td>6.0</td> <td>4</td> <td>4.0</td> <td>5.0</td> <td>e</td> <td>16</td> </tr> <tr> <th>5</th> <td>0</td> <td>A-L</td> <td>0.0</td> <td>12.0</td> <td>0</td> <td>A-F</td> <td>0.0</td> <td>6.0</td> <td>False</td> <td>1</td> <td>def</td> <td>3.0</td> <td>6.0</td> <td>5</td> <td>5.0</td> <td>6.0</td> <td>f</td> <td>25</td> </tr> <tr> <th>6</th> <td>0</td> <td>A-L</td> <td>0.0</td> <td>12.0</td> <td>1</td> <td>G-L</td> <td>6.0</td> <td>12.0</td> <td>True</td> <td>2</td> <td>ghi</td> <td>6.0</td> <td>9.0</td> <td>6</td> <td>6.0</td> <td>7.0</td> <td>g</td> <td>36</td> </tr> <tr> <th>7</th> <td>0</td> <td>A-L</td> <td>0.0</td> <td>12.0</td> <td>1</td> <td>G-L</td> <td>6.0</td> <td>12.0</td> <td>True</td> <td>2</td> <td>ghi</td> <td>6.0</td> <td>9.0</td> <td>7</td> <td>7.0</td> <td>8.0</td> <td>h</td> <td>49</td> </tr> <tr> <th>8</th> <td>0</td> <td>A-L</td> <td>0.0</td> <td>12.0</td> <td>1</td> <td>G-L</td> <td>6.0</td> <td>12.0</td> <td>True</td> <td>2</td> <td>ghi</td> <td>6.0</td> <td>9.0</td> <td>8</td> <td>8.0</td> <td>9.0</td> <td>i</td> <td>64</td> </tr> <tr> <th>9</th> <td>0</td> <td>A-L</td> <td>0.0</td> <td>12.0</td> <td>1</td> <td>G-L</td> <td>6.0</td> <td>12.0</td> <td>True</td> <td>3</td> <td>jkl</td> <td>9.0</td> <td>12.0</td> <td>9</td> <td>9.0</td> <td>10.0</td> <td>j</td> <td>81</td> </tr> <tr> <th>10</th> <td>0</td> <td>A-L</td> <td>0.0</td> <td>12.0</td> <td>1</td> <td>G-L</td> <td>6.0</td> <td>12.0</td> <td>True</td> <td>3</td> <td>jkl</td> <td>9.0</td> <td>12.0</td> <td>10</td> <td>10.0</td> <td>11.0</td> <td>k</td> <td>100</td> </tr> <tr> <th>11</th> <td>0</td> <td>A-L</td> <td>0.0</td> <td>12.0</td> <td>1</td> <td>G-L</td> <td>6.0</td> <td>12.0</td> <td>True</td> <td>3</td> <td>jkl</td> <td>9.0</td> <td>12.0</td> <td>11</td> <td>11.0</td> <td>12.0</td> <td>l</td> <td>121</td> </tr> </tbody> </table></html>



This extension was created using [ndx-template](https://github.com/nwb-extensions/ndx-template).
