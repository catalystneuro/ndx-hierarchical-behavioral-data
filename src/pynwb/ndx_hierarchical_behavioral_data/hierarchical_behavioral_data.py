from hdmf.common import DynamicTable, DynamicTableRegion
from pynwb.epoch import TimeIntervals
from pynwb import register_class, TimeSeries
from hdmf.utils import docval, get_docval, popargs


@register_class('HierarchicalBehavioralTable', 'ndx-hierarchical-behavioral-data')
class HierarchicalBehavioralTable(TimeIntervals, DynamicTable):
    """
    A table for storing hierarchical behavioral data.
    """
    __columns__ = tuple(list(TimeIntervals.__columns__) + [
        {'name': 'label',
         'description': 'Column for each label.',
         'required': True},
        {'name': 'next_tier',
         'description': 'References to the next tier.',
         'required': True,
         'table': True,
         'index': True}
    ])

    @docval({'name': 'name', 'type': str, 'doc': 'name of table.'},
            {'name': 'description', 'type': str, 'doc': 'description of table.'},
            {'name': 'lower_tier_table',
             'type': 'DynamicTable',
             'doc': 'The next tier that this table references',
             'default': None},
            *get_docval(TimeIntervals.__init__, 'id', 'columns', 'colnames'))
    def __init__(self, **kwargs):
        lower_tier_table = popargs('lower_tier_table', kwargs)
        self.lower_tier_table = lower_tier_table
        super().__init__(**kwargs)

        if self['next_tier'].target.table is None:
            if lower_tier_table is not None:
                self['next_tier'].target.table = lower_tier_table
            else:
                raise ValueError('lower_tier_table constructor argument required')

    @docval({'name': 'start_time', 'type': 'float', 'doc': 'Start time of epoch, in seconds', 'default': None},
            {'name': 'stop_time', 'type': 'float', 'doc': 'Stop time of epoch, in seconds', 'default': None},
            {'name': 'tags', 'type': (str, list, tuple), 'doc': 'user-defined tags used throughout time intervals',
             'default': None},
            {'name': 'timeseries', 'type': (list, tuple, TimeSeries), 'doc': 'the TimeSeries this epoch applies to',
             'default': None},
            allow_extra=True)
    def add_interval(self, **kwargs):
        # automatically populate the time with the start time of the first element of the next tier
        if kwargs.get('start_time', None) is None:
            kwargs.update(start_time=self['next_tier'].target.table['start_time'][kwargs['next_tier'][0]])

        if kwargs.get('stop_time', None) is None:
            kwargs.update(stop_time=self['next_tier'].target.table['stop_time'][kwargs['next_tier'][-1]])

        super().add_interval(**kwargs)
