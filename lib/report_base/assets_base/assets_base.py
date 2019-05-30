from abc import abstractmethod
from lib.report_base.report_base import ReportBase


class AssetsBase(ReportBase):
    def __init__(self, wss_id, type_name):
        self.assets_type = type_name
        self.wss_id = wss_id
        self.assetsList = []

    def add_main_title(self, doc):
        doc.add_heading('List of {0}'.format(self.assets_type), level=3)

    @abstractmethod
    def get_assets_info(self, db):
        raise NotImplementedError()

    @abstractmethod
    def create_column_list(self, db):
        raise NotImplementedError()

    def add_table(self, doc):
        if len(self.assetsList) == 0:
            doc.add_paragraph('No item')
            return

        keyval = self.create_column_list()
        table = doc.add_table(rows=1, cols=len(keyval), style='Table Grid')
        hdr_cells = table.rows[0].cells
        for val in keyval:
            hdr_cells[keyval.index(val)].text = val[0]

        self.set_repeat_table_header(table.rows[0])

        for data in self.assetsList:
            row_cells = table.add_row().cells
            for val2 in keyval:
                _default = val2[2]
                if type(data.__dict__[val2[1]]) is str:
                    _value = data.__dict__[val2[1]] or _default
                else:
                    _value = data.__dict__[val2[1]] or _default
                row_cells[keyval.index(val2)].text = str(_value)

    def create(self, db, doc):
        self.get_assets_info(db)
        if len(self.assetsList) > 0:
            self.add_main_title(doc)
            self.add_table(doc)
            self.add_break(doc)
        return self.assetsList

