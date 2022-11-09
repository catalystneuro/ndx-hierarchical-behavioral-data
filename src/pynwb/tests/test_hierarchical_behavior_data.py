from datetime import datetime
from pathlib import Path
from tempfile import mkdtemp

from dateutil import tz
from hdmf.testing import TestCase
from numpy.testing import assert_array_equal
from pandas.testing import assert_frame_equal
from pynwb import NWBFile, NWBHDF5IO
from pynwb.epoch import TimeIntervals
from pynwb.testing import remove_test_file

from ndx_hierarchical_behavioral_data import HierarchicalBehavioralTable


def create_time_intervals():
    words_table = TimeIntervals(
        name="Words",
        description="The intervals for the lowest hierarchy.",
    )
    words_table.add_column(
        name="label", description="The label for this table."
    )

    words_table.add_row(start_time=0.3, stop_time=0.5, label="The")
    words_table.add_row(start_time=0.7, stop_time=0.9, label="First")
    words_table.add_row(start_time=1.3, stop_time=3.0, label="Sentence")
    words_table.add_row(start_time=4.0, stop_time=5.0, label="And")
    words_table.add_row(start_time=6.0, stop_time=7.0, label="Another")

    return words_table


class TestHierarchicalBehavioralTable(TestCase):
    def setUp(self):
        self.words_table = create_time_intervals()

        self.sentences_table = HierarchicalBehavioralTable(
            name="Sentences",
            description="The behavioral table.",
            lower_tier_table=self.words_table,
        )
        self.sentences_table.add_column(
            name="is_practice", description="Whether or not this sentence were shown as practice."
        )
        self.sentences_table.add_interval(
            label="Sentence1",
            next_tier=[0, 1, 2],
            is_practice=True,
        )
        self.sentences_table.add_interval(
            label="Sentence2",
            next_tier=[3, 4],
            is_practice=False,
        )

        self.nwbfile = NWBFile(
            session_description="session_description",
            identifier="identifier",
            session_start_time=datetime.now().astimezone(tz=tz.gettz("US/Pacific")),
        )
        self.nwbfile_path = Path(mkdtemp()) / "test_hierarchical_behavior_data.nwb"

    def tearDown(self):
        remove_test_file(self.nwbfile_path)

    def test_roundtrip(self):
        self.nwbfile.add_time_intervals(self.words_table)
        self.nwbfile.add_time_intervals(self.sentences_table)

        with NWBHDF5IO(self.nwbfile_path, mode="w") as io:
            io.write(self.nwbfile)

        with NWBHDF5IO(self.nwbfile_path, mode="r", load_namespaces=True) as io:
            read_nwbfile = io.read()

            self.assertEqual(len(read_nwbfile.intervals), 2)

            self.assertIn("Words", read_nwbfile.intervals)
            self.assertIn("Sentences", read_nwbfile.intervals)

            self.assertIsInstance(
                read_nwbfile.intervals["Sentences"], HierarchicalBehavioralTable,
            )

            for column_name in self.words_table.colnames:
                assert_array_equal(
                    self.words_table[column_name][:],
                    read_nwbfile.intervals["Words"][column_name][:]
                )

            for column_name in [c for c in self.sentences_table.colnames if c != 'next_tier']:
                assert_array_equal(
                    self.sentences_table[column_name][:],
                    read_nwbfile.intervals["Sentences"][column_name][:],
                )

    def test_hierarchical_dataframes(self):
        paragraphs_table = HierarchicalBehavioralTable(
            name="Paragraphs",
            description="The table representing the highest hierarchy.",
            lower_tier_table=self.sentences_table,
        )
        paragraphs_table.add_interval(
            label="Paragraph",
            next_tier=[0, 1],
        )

        self.nwbfile.add_time_intervals(self.words_table)
        self.nwbfile.add_time_intervals(self.sentences_table)
        self.nwbfile.add_time_intervals(paragraphs_table)

        with NWBHDF5IO(self.nwbfile_path, mode="w") as io:
            io.write(self.nwbfile)

        with NWBHDF5IO(self.nwbfile_path, mode="r", load_namespaces=True) as io:
            read_nwbfile = io.read()

            assert_frame_equal(
                self.words_table.to_dataframe(),
                read_nwbfile.intervals["Words"].to_dataframe(),
            )

            assert_frame_equal(
                self.sentences_table.to_hierarchical_dataframe(),
                read_nwbfile.intervals["Sentences"].to_hierarchical_dataframe(),
            )

            assert_frame_equal(
                paragraphs_table.to_hierarchical_dataframe(),
                read_nwbfile.intervals["Paragraphs"].to_hierarchical_dataframe(),
            )
