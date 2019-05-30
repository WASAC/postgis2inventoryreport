import os
import shutil
from docx import Document
from lib.report_base.report_base import ReportBase
from lib.report_base.assets_base.wss import WssList
from lib.report_base.assets_base.summary import Summary
from lib.report_base.assets_base.chamber import Chambers
from lib.report_base.assets_base.reservoir import Reservoirs
from lib.report_base.assets_base.pumping_station import PumpingStations
from lib.report_base.assets_base.watersource import WaterSources
from lib.report_base.assets_base.waterconnection import WaterConnections


class InventoryReport(ReportBase):
    def __init__(self, db, district, tmp_file_path, current_date):
        self.db = db
        self.district = district
        self.tmp_file_path = tmp_file_path
        self.main_directory = current_date.strftime('%Y%m%d_%H%M%S') + "_RWSS_Inventory_Reports"
        self.month_year = current_date.strftime('%B %Y')

    def create(self):
        if not os.path.exists(self.main_directory):
            os.makedirs(self.main_directory, exist_ok=True)

        new_file_path = "/".join(
            [self.main_directory, "{0}_Inventory Data for {1} District.docx".format(self.district.dist_id, self.district.district)])
        shutil.copy2(self.tmp_file_path, new_file_path)

        doc = Document(new_file_path)

        values = {"%district%": self.district.district.upper(), "%monthyear%": self.month_year}
        self.docx_replace(doc, values)

        wss_list_obj = WssList(self.district.dist_id)
        wss_list = wss_list_obj.create(self.db, doc)
        for wss_data in wss_list:
            doc.add_heading('{0} {1} WSS'.format(wss_data.wss_id, wss_data.wss_name), level=1)
            doc.add_heading('About Situation of {0} WSS'.format(wss_data.wss_name), level=2)
            doc.add_paragraph('Please describe the WSS here. ')
            doc.add_heading('Map of the WSS', level=2)
            self.add_temp_image(doc)
            doc.add_page_break()
            doc.add_heading('Assets Data', level=2)

            for assets_obj in [Summary(wss_data.wss_id), Chambers(wss_data.wss_id),
                               Reservoirs(wss_data.wss_id), PumpingStations(wss_data.wss_id),
                               WaterSources(wss_data.wss_id), WaterConnections(wss_data.wss_id)]:
                assets_obj.create(self.db, doc)
                doc.save(new_file_path)

            doc.add_page_break()
            doc.save(new_file_path)

        doc.save(new_file_path)
        del doc
        print("It created Inventory Report of {0} at folder: {1}".format(self.district.district, new_file_path))
