from pynwb.epoch import TimeIntervals

from ..hierarchical_behavioral_data import HierarchicalBehavioralTable

phonemes = TimeIntervals(
    name='phonemes',
    description='desc'
)

phonemes.add_column('label', 'label of phoneme')

syllables = HierarchicalBehavioralTable(
    name='syllables',
    description='desc',
    next_tier=phonemes
)

words = HierarchicalBehavioralTable(
    name='words',
    description='desc',
    next_tier=syllables
)

sentences = HierarchicalBehavioralTable(
    name='sentences',
    description='desc',
    next_tier=words
)
