from ndx_hierarchical_behavioral_data.definitions.transcription import phonemes, syllables, words, sentences

for i, p in enumerate('abcdefghijkl'):
    phonemes.add_interval(label=p, start_time=float(i), stop_time=float(i+1))

syllables.add_interval(label='abc', next_tier=[0, 1, 2])
syllables.add_interval(label='def', next_tier=[3, 4, 5])
syllables.add_interval(label='ghi', next_tier=[6, 7, 8])
syllables.add_interval(label='jkl', next_tier=[9, 10, 11])

words.add_interval(label='A-F', next_tier=[0, 1])
words.add_interval(label='G-L', next_tier=[2, 3])

print(words.to_denormalized_dataframe())
print(words.to_hierarchical_dataframe())
