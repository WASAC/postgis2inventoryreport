from abc import abstractmethod
from lib.report_base.report_base import ReportBase


class AssetsBase(ReportBase):
    class Column(object):
        def __init__(self, label, field, default):
            self.label = label
            self.field = field
            self.default = default

    def __init__(self, wss_id, type_name):
        self.assets_type = type_name
        self.wss_id = wss_id
        self.assetsList = []
        self.columnList = []

    def add_main_title(self, doc):
        doc.add_heading('List of {0}'.format(self.assets_type), level=3)

    @abstractmethod
    def get_assets_info(self, db):
        raise NotImplementedError()

    @abstractmethod
    def create_column_list(self, db):
        raise NotImplementedError()

    def add_table(self, doc, max_col=None):
        if len(self.assetsList) == 0:
            doc.add_paragraph('No item')

        self.columnList = self.create_column_list()
        if not max_col:
            max_col = len(self.columnList)
        table = doc.add_table(rows=1, cols=max_col, style='Table Grid')
        hdr_cells = table.rows[0].cells
        for col in self.columnList:
            if self.columnList.index(col) < max_col:
                hdr_cells[self.columnList.index(col)].text = col.label

        self.set_repeat_table_header(table.rows[0])

        for data in self.assetsList:
            row_cells = table.add_row().cells
            for col2 in self.columnList:
                if self.columnList.index(col2) < max_col:
                    _default = col2.default
                    if type(data.__dict__[col2.field]) is str:
                        _value = data.__dict__[col2.field] or _default
                    else:
                        _value = data.__dict__[col2.field] or _default
                    row_cells[self.columnList.index(col2)].text = str(_value)

    def add_table_vertical(self, doc):
        for data in self.assetsList:
            doc.add_heading('{0} #{1}'.format( self.assets_type, str(data.id)), level=5)
            table2 = doc.add_table(rows=1, cols=2, style='Table Grid')
            hdr_cells2 = table2.rows[0].cells
            hdr_cells2[0].text = 'Item'
            hdr_cells2[1].text = 'Desription'
            self.set_repeat_table_header(table2.rows[0])
            for col in self.columnList:
                row_cells2 = table2.add_row().cells
                row_cells2[0].text = col.label
                row_cells2[1].text = str(data.__dict__[col.field]) or col.default
            self.add_break(doc)

    def create(self, db, doc):
        self.get_assets_info(db)
        if len(self.assetsList) > 0:
            self.add_main_title(doc)
            self.add_table(doc)
            self.add_break(doc)
        return self.assetsList

