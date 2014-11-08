__author__ = 'scott'

"""
The standard CSVItemExporter class does not pass the kwargs through to the
CSV writer, resulting in EXPORT_FIELDS and EXPORT_ENCODING being ignored
(EXPORT_EMPTY is not used by CSV).
"""

from scrapy.conf import settings
from scrapy.contrib.exporter import CsvItemExporter
import csv

class CSVkwItemExporter(CsvItemExporter):

    def __init__(self, *args, **kwargs):
        kwargs['fields_to_export'] = settings.getlist('EXPORT_FIELDS') or None
        kwargs['encoding'] = settings.get('EXPORT_ENCODING', 'utf-8')
        self.list_of_items = []

        super(CSVkwItemExporter, self).__init__(*args, **kwargs)

    def export_item(self, item):
        if self._headers_not_written:
            self._headers_not_written = False
            self._write_headers_and_set_fields_to_export(item)

        fields = self._get_serialized_fields(item, default_value='',\
            include_empty=True)
        values = [x[1] for x in fields]
        self.list_of_items.append(values)

    def finish_exporting(self):
        def cast_float(data):
            try:
                return float(data)
            except ValueError:
                return 100000000000000.0
        self.list_of_items.sort(key=lambda x:cast_float(x[self.fields_to_export.index('Prime_Price')]))
        self.list_of_items.sort(key=lambda x:x[self.fields_to_export.index('Cheapest')])
        for values in self.list_of_items:
            self.csv_writer.writerow(values)
