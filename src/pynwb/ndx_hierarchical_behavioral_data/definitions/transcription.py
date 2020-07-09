from pynwb.epoch import TimeIntervals
from ..hierarchical_behavioral_data import HierarchicalBehavioralTable


class TIPhonemes(TimeIntervals):
    """Phonemes level"""
    def __init__(self, name='phonemes', description='desc'):
        super().__init__(name=name, description=description)
        self.add_column('label', 'label of phoneme')


class HBTSyllables(HierarchicalBehavioralTable):
    """Syllables level"""
    def __init__(self, lower_tier_table, name='syllables', description='desc'):
        super().__init__(name=name, description=description, lower_tier_table=lower_tier_table)


class HBTWords(HierarchicalBehavioralTable):
    """Words level"""
    def __init__(self, lower_tier_table, name='words', description='desc'):
        super().__init__(name=name, description=description, lower_tier_table=lower_tier_table)


class HBTSentences(HierarchicalBehavioralTable):
    """Sentences level"""
    def __init__(self, lower_tier_table, name='sentences', description='desc'):
        super().__init__(name=name, description=description, lower_tier_table=lower_tier_table)


# phonemes = TimeIntervals(
#     name='phonemes',
#     description='desc'
# )
# phonemes.add_column('label', 'label of phoneme')

# syllables = HierarchicalBehavioralTable(
#     name='syllables',
#     description='desc',
#     lower_tier_table=phonemes
# )

# words = HierarchicalBehavioralTable(
#     name='words',
#     description='desc',
#     lower_tier_table=syllables
# )

# sentences = HierarchicalBehavioralTable(
#     name='sentences',
#     description='desc',
#     lower_tier_table=words
# )
