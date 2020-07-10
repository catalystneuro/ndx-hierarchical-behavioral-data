from ndx_hierarchical_behavioral_data.definitions.transcription import TIPhonemes, HBTSyllables, HBTWords, HBTSentences
from pynwb import NWBHDF5IO, NWBFile
from pynwb.testing import TestCase, remove_test_file
import numpy as np
import datetime


class TestTranscription(TestCase):
    """Simple roundtrip test for TetrodeSeries."""

    def setUp(self):
        self.nwbfile = NWBFile(
            session_description='session_description',
            identifier='identifier',
            session_start_time=datetime.datetime.now(datetime.timezone.utc))
        self.path = 'test.nwb'

    def tearDown(self):
        remove_test_file(self.path)

    def test_roundtrip(self):
        """
        Add a transcription to an NWBFile, write it to file, read the file, and test that the sentences table from the
        file matches the original sentences table.
        """

        phonemes = TIPhonemes()
        phonemes.add_column('max_pitch', 'maximum pitch for this phoneme. NaN for unvoiced')

        for i, p in enumerate('abcdefghijkl'):
            phonemes.add_interval(label=p, start_time=float(i), stop_time=float(i + 1), max_pitch=i ** 2)

        syllables = HBTSyllables(lower_tier_table=phonemes)
        syllables.add_interval(label='abc', next_tier=[0, 1, 2])
        syllables.add_interval(label='def', next_tier=[3, 4, 5])
        syllables.add_interval(label='ghi', next_tier=[6, 7, 8])
        syllables.add_interval(label='jkl', next_tier=[9, 10, 11])

        words = HBTWords(lower_tier_table=syllables)
        words.add_column('emphasis', 'boolean indicating whether this word was emphasized')
        words.add_interval(label='A-F', next_tier=[0, 1], emphasis=False)
        words.add_interval(label='G-L', next_tier=[2, 3], emphasis=True)

        sentences = HBTSentences(lower_tier_table=words)
        sentences.add_interval(label='A-L', next_tier=[0, 1])

        mod = self.nwbfile.create_processing_module('test_mod', 'test_mod')

        mod.add(phonemes)
        mod.add(syllables)
        mod.add(words)
        mod.add(sentences)

        with NWBHDF5IO(self.path, mode='w') as io:
            io.write(self.nwbfile)

        with NWBHDF5IO(self.path, mode='r', load_namespaces=True) as io:
            read_nwbfile = io.read()

            for col in phonemes.colnames:
                np.testing.assert_equal(phonemes[col][:], read_nwbfile.processing['test_mod']['phonemes'][col][:])

            for col in [c for c in syllables.colnames if c != 'next_tier']:
                np.testing.assert_equal(syllables[col][:], read_nwbfile.processing['test_mod']['syllables'][col][:])

            for col in [c for c in words.colnames if c != 'next_tier']:
                np.testing.assert_equal(words[col][:], read_nwbfile.processing['test_mod']['words'][col][:])
