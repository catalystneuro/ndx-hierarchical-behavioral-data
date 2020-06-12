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
    lower_tier_table=phonemes
)

words = HierarchicalBehavioralTable(
    name='words',
    description='desc',
    lower_tier_table=syllables
)

sentences = HierarchicalBehavioralTable(
    name='sentences',
    description='desc',
    lower_tier_table=words
)
