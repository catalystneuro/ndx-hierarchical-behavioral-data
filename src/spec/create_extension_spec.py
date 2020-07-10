# -*- coding: utf-8 -*-

import os.path
from hdmf.spec import RefSpec, NamespaceBuilder, export_spec

from pynwb.spec import NWBGroupSpec


def main():
    ns_builder = NamespaceBuilder(
        doc="""HDMF extensions for storing hierarchical behavioral data""",
        name="""ndx-hierarchical-behavioral-data""",
        version="""0.1.1""",
        author=list(map(str.strip, """Ben Dichter""".split(','))),
        contact=list(map(str.strip, """ben.dichter@catalystneuro.com""".split(',')))
    )

    # TODO: specify the neurodata_types that are used by the extension as well
    # as in which namespace they are found
    # this is similar to specifying the Python modules that need to be imported
    # to use your new data types
    # as of HDMF 1.6.1, the full ancestry of the neurodata_types that are used by
    # the extension should be included, i.e., the neurodata_type and its parent
    # type and its parent type and so on. this will be addressed in a future
    # release of HDMF.
    ns_builder.include_type('TimeIntervals', namespace='core')
    ns_builder.include_type('DynamicTableRegion', namespace='core')
    ns_builder.include_type('VectorData', namespace='core')

    behav_table = NWBGroupSpec(
        neurodata_type_def='HierarchicalBehavioralTable',
        neurodata_type_inc='TimeIntervals',
        doc='DynamicTable that holds hierarchical behavioral information.')

    behav_table.add_dataset(
        name='label',
        neurodata_type_inc='VectorData',
        doc='The label associated with each item',
        dtype='text'
    )

    next_tier = behav_table.add_dataset(
        name='next_tier',
        neurodata_type_inc='DynamicTableRegion',
        doc='reference to the next tier',
    )
    next_tier.add_attribute(
        name='table',
        dtype=RefSpec(target_type='TimeIntervals',
                      reftype='object'),
        doc='reference to the next level'
    )
    behav_table.add_dataset(
        name='next_tier_index',
        neurodata_type_inc='VectorIndex',
        doc='Index dataset for next tier.',
    )

    new_data_types = [behav_table]

    # export the spec to yaml files in the spec folder
    output_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'spec'))
    export_spec(ns_builder, new_data_types, output_dir)


if __name__ == "__main__":
    # usage: python create_extension_spec.py
    main()
