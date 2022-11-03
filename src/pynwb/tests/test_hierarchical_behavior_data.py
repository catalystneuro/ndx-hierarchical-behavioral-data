import shutil
from datetime import datetime
from pathlib import Path
from tempfile import mkdtemp

import numpy as np
from dateutil import tz
from hdmf.testing import TestCase
from pynwb import NWBFile, NWBHDF5IO
from pynwb.epoch import TimeIntervals

from ndx_hierarchical_behavioral_data import HierarchicalBehavioralTable


class TestHierarchicalBehavioralTable(TestCase):
    def setUp(self):
        self.test_dir = Path(mkdtemp())

        self.nwbfile = NWBFile(
            session_description="session_description",
            identifier="identifier",
            session_start_time=datetime.now().astimezone(tz=tz.gettz("US/Pacific")),
        )
        self.nwbfile_path = self.test_dir / "test.nwb"

        self.lower_tier_table = TimeIntervals(
            name="Words",
            description="The intervals for the lowest hierarchy.",
        )

        self.lower_tier_table.add_column(
            name="label", description="The label for this table."
        )

        self.lower_tier_table.add_row(start_time=0.3, stop_time=0.5, label="The")
        self.lower_tier_table.add_row(start_time=0.7, stop_time=0.9, label="First")
        self.lower_tier_table.add_row(start_time=1.3, stop_time=3.0, label="Sentence")
        self.lower_tier_table.add_row(start_time=4.0, stop_time=5.0, label="And")
        self.lower_tier_table.add_row(start_time=6.0, stop_time=7.0, label="Another")

    def tearDown(self):
        shutil.rmtree(self.test_dir)

    def test_roundtrip(self):
        sentences_table = HierarchicalBehavioralTable(
            name="Sentences",
            description="The behavioral table.",
            lower_tier_table=self.lower_tier_table,
        )
        sentences_table.add_interval(
            label="Sentence1",
            next_tier=[0, 1, 2],
        )
        sentences_table.add_interval(
            label="Sentence2",
            next_tier=[3, 4],
        )

        self.nwbfile.add_time_intervals(self.lower_tier_table)
        self.nwbfile.add_time_intervals(sentences_table)

        with NWBHDF5IO(self.nwbfile_path, mode="w") as io:
            io.write(self.nwbfile)

        with NWBHDF5IO(self.nwbfile_path, mode="r", load_namespaces=True) as io:
            read_nwbfile = io.read()

            for column_name in self.lower_tier_table.colnames:
                np.testing.assert_array_equal(
                    self.lower_tier_table[column_name][:],
                    read_nwbfile.intervals["Words"][column_name][:],
                )

            for column_name in [
                column for column in sentences_table.colnames if column != "next_tier"
            ]:
                np.testing.assert_array_equal(
                    sentences_table[column_name][:],
                    read_nwbfile.intervals["Sentences"][column_name][:],
                )
