from lib.report_base.assets_base.assets_base import AssetsBase
from lib.report_base.assets_base.pipeline import PipelineList


class Summary(AssetsBase):

    class Table(object):
        def __init__(self, params):
            self.no = params[0]
            self.item = params[1]
            self.no_unknown = params[2]
            self.no_fully = params[3]
            self.no_partially = params[4]
            self.no_abandoned = params[5]
            self.no_not = params[6]
            self.no_total = params[7]

    def __init__(self, wss_id):
        super().__init__(wss_id, "Assets")

    def add_main_title(self, doc):
        doc.add_heading('Summary of {0}'.format(self.assets_type), level=3)

    def get_assets_info(self, db):
        query = " SELECT * FROM("
        #Water Connection Summary
        query += " SELECT "
        query += "   1 as no,"
        query += "   a.connection_type,"
        query += "   COUNT(CASE WHEN a.status = 0 THEN a.status END) as no_unknown,"
        query += "   COUNT(CASE WHEN a.status = 1 THEN a.status END) as no_fully,"
        query += "   COUNT(CASE WHEN a.status = 2 THEN a.status END) as no_partially,"
        query += "   COUNT(CASE WHEN a.status = 3 THEN a.status END) as no_abandoned,"
        query += "   COUNT(CASE WHEN a.status = 4 THEN a.status END) as no_not,"
        query += "   COUNT(*) as no_total"
        query += " FROM water_connection a"
        query += " WHERE a.connection_type = 'Household'"
        query += " AND a.wss_id = {0} "
        query += " GROUP BY no, a.connection_type"
        query += " UNION"
        query += " SELECT "
        query += "   2 as no,"
        query += "   a.connection_type,"
        query += "   COUNT(CASE WHEN a.status = 0 THEN a.status END) as no_unknown,"
        query += "   COUNT(CASE WHEN a.status = 1 THEN a.status END) as no_fully,"
        query += "   COUNT(CASE WHEN a.status = 2 THEN a.status END) as no_partially,"
        query += "   COUNT(CASE WHEN a.status = 3 THEN a.status END) as no_abandoned,"
        query += "   COUNT(CASE WHEN a.status = 4 THEN a.status END) as no_not,"
        query += "   COUNT(*) as no_total"
        query += " FROM water_connection a"
        query += " WHERE a.connection_type = 'Public Tap'"
        query += " AND a.wss_id = {0} "
        query += " GROUP BY no, a.connection_type"
        query += " UNION"
        query += " SELECT "
        query += "   3 as no,"
        query += "   a.connection_type,"
        query += "   COUNT(CASE WHEN a.status = 0 THEN a.status END) as no_unknown,"
        query += "   COUNT(CASE WHEN a.status = 1 THEN a.status END) as no_fully,"
        query += "   COUNT(CASE WHEN a.status = 2 THEN a.status END) as no_partially,"
        query += "   COUNT(CASE WHEN a.status = 3 THEN a.status END) as no_abandoned,"
        query += "   COUNT(CASE WHEN a.status = 4 THEN a.status END) as no_not,"
        query += "   COUNT(*) as no_total"
        query += " FROM water_connection a"
        query += " WHERE a.connection_type = 'Water Kiosk'"
        query += " AND a.wss_id = {0} "
        query += " GROUP BY no, a.connection_type"
        query += " UNION"
        query += " SELECT "
        query += "   4 as no,"
        query += "   a.connection_type,"
        query += "   COUNT(CASE WHEN a.status = 0 THEN a.status END) as no_unknown,"
        query += "   COUNT(CASE WHEN a.status = 1 THEN a.status END) as no_fully,"
        query += "   COUNT(CASE WHEN a.status = 2 THEN a.status END) as no_partially,"
        query += "   COUNT(CASE WHEN a.status = 3 THEN a.status END) as no_abandoned,"
        query += "   COUNT(CASE WHEN a.status = 4 THEN a.status END) as no_not,"
        query += "   COUNT(*) as no_total"
        query += " FROM water_connection a"
        query += " WHERE a.connection_type = 'Industrial'"
        query += " AND a.wss_id = {0} "
        query += " GROUP BY no, a.connection_type"
        query += " UNION"
        query += " SELECT "
        query += "   5 as no,"
        query += "   a.connection_type,"
        query += "   COUNT(CASE WHEN a.status = 0 THEN a.status END) as no_unknown,"
        query += "   COUNT(CASE WHEN a.status = 1 THEN a.status END) as no_fully,"
        query += "   COUNT(CASE WHEN a.status = 2 THEN a.status END) as no_partially,"
        query += "   COUNT(CASE WHEN a.status = 3 THEN a.status END) as no_abandoned,"
        query += "   COUNT(CASE WHEN a.status = 4 THEN a.status END) as no_not,"
        query += "   COUNT(*) as no_total"
        query += " FROM water_connection a"
        query += " WHERE a.connection_type NOT IN ('Household', 'Public Tap', 'Water Kiosk', 'Industrial')"
        query += " AND a.wss_id = {0} "
        query += " GROUP BY no, a.connection_type"
        query += " UNION"
        #Chamber Summary
        query += " SELECT "
        query += "   6 as no,"
        query += "   a.chamber_type,"
        query += "   COUNT(CASE WHEN a.status = 0 THEN a.status END) as no_unknown,"
        query += "   COUNT(CASE WHEN a.status = 1 THEN a.status END) as no_fully,"
        query += "   COUNT(CASE WHEN a.status = 2 THEN a.status END) as no_partially,"
        query += "   COUNT(CASE WHEN a.status = 3 THEN a.status END) as no_abandoned,"
        query += "   COUNT(CASE WHEN a.status = 4 THEN a.status END) as no_not,"
        query += "   COUNT(*) as no_total"
        query += " FROM chamber a"
        query += " WHERE a.chamber_type = 'Valve chamber'"
        query += " AND a.wss_id = {0} "
        query += " GROUP BY no, a.chamber_type"
        query += " UNION"
        query += " SELECT "
        query += "   7 as no,"
        query += "   a.chamber_type,"
        query += "   COUNT(CASE WHEN a.status = 0 THEN a.status END) as no_unknown,"
        query += "   COUNT(CASE WHEN a.status = 1 THEN a.status END) as no_fully,"
        query += "   COUNT(CASE WHEN a.status = 2 THEN a.status END) as no_partially,"
        query += "   COUNT(CASE WHEN a.status = 3 THEN a.status END) as no_abandoned,"
        query += "   COUNT(CASE WHEN a.status = 4 THEN a.status END) as no_not,"
        query += "   COUNT(*) as no_total"
        query += " FROM chamber a"
        query += " WHERE a.chamber_type = 'Air release chamber'"
        query += " AND a.wss_id = {0} "
        query += " GROUP BY no, a.chamber_type"
        query += " UNION"
        query += " SELECT "
        query += "   8 as no,"
        query += "   a.chamber_type,"
        query += "   COUNT(CASE WHEN a.status = 0 THEN a.status END) as no_unknown,"
        query += "   COUNT(CASE WHEN a.status = 1 THEN a.status END) as no_fully,"
        query += "   COUNT(CASE WHEN a.status = 2 THEN a.status END) as no_partially,"
        query += "   COUNT(CASE WHEN a.status = 3 THEN a.status END) as no_abandoned,"
        query += "   COUNT(CASE WHEN a.status = 4 THEN a.status END) as no_not,"
        query += "   COUNT(*) as no_total"
        query += " FROM chamber a"
        query += " WHERE a.chamber_type = 'Washout chamber'"
        query += " AND a.wss_id = {0} "
        query += " GROUP BY no, a.chamber_type"
        query += " UNION"
        query += " SELECT "
        query += "   9 as no,"
        query += "   a.chamber_type,"
        query += "   COUNT(CASE WHEN a.status = 0 THEN a.status END) as no_unknown,"
        query += "   COUNT(CASE WHEN a.status = 1 THEN a.status END) as no_fully,"
        query += "   COUNT(CASE WHEN a.status = 2 THEN a.status END) as no_partially,"
        query += "   COUNT(CASE WHEN a.status = 3 THEN a.status END) as no_abandoned,"
        query += "   COUNT(CASE WHEN a.status = 4 THEN a.status END) as no_not,"
        query += "   COUNT(*) as no_total"
        query += " FROM chamber a"
        query += " WHERE a.chamber_type = 'Break Pressure chamber'"
        query += " AND a.wss_id = {0} "
        query += " GROUP BY no, a.chamber_type"
        query += " UNION"
        query += " SELECT "
        query += "   10 as no,"
        query += "   a.chamber_type,"
        query += "   COUNT(CASE WHEN a.status = 0 THEN a.status END) as no_unknown,"
        query += "   COUNT(CASE WHEN a.status = 1 THEN a.status END) as no_fully,"
        query += "   COUNT(CASE WHEN a.status = 2 THEN a.status END) as no_partially,"
        query += "   COUNT(CASE WHEN a.status = 3 THEN a.status END) as no_abandoned,"
        query += "   COUNT(CASE WHEN a.status = 4 THEN a.status END) as no_not,"
        query += "   COUNT(*) as no_total"
        query += " FROM chamber a"
        query += " WHERE a.chamber_type = 'PRV chamber'"
        query += " AND a.wss_id = {0} "
        query += " GROUP BY no, a.chamber_type"
        query += " UNION"
        query += " SELECT "
        query += "   11 as no,"
        query += "   a.chamber_type,"
        query += "   COUNT(CASE WHEN a.status = 0 THEN a.status END) as no_unknown,"
        query += "   COUNT(CASE WHEN a.status = 1 THEN a.status END) as no_fully,"
        query += "   COUNT(CASE WHEN a.status = 2 THEN a.status END) as no_partially,"
        query += "   COUNT(CASE WHEN a.status = 3 THEN a.status END) as no_abandoned,"
        query += "   COUNT(CASE WHEN a.status = 4 THEN a.status END) as no_not,"
        query += "   COUNT(*) as no_total"
        query += " FROM chamber a"
        query += " WHERE a.chamber_type = 'Starting chamber'"
        query += " AND a.wss_id = {0} "
        query += " GROUP BY no, a.chamber_type"
        query += " UNION"
        query += " SELECT "
        query += "   12 as no,"
        query += "   a.chamber_type,"
        query += "   COUNT(CASE WHEN a.status = 0 THEN a.status END) as no_unknown,"
        query += "   COUNT(CASE WHEN a.status = 1 THEN a.status END) as no_fully,"
        query += "   COUNT(CASE WHEN a.status = 2 THEN a.status END) as no_partially,"
        query += "   COUNT(CASE WHEN a.status = 3 THEN a.status END) as no_abandoned,"
        query += "   COUNT(CASE WHEN a.status = 4 THEN a.status END) as no_not,"
        query += "   COUNT(*) as no_total"
        query += " FROM chamber a"
        query += " WHERE a.chamber_type = 'Collection chamber'"
        query += " AND a.wss_id = {0} "
        query += " GROUP BY no, a.chamber_type"
        query += " UNION"
        query += " SELECT "
        query += "   13 as no,"
        query += "   'Pumping Station' as item,"
        query += "   COUNT(CASE WHEN a.status = 0 THEN a.status END) as no_unknown,"
        query += "   COUNT(CASE WHEN a.status = 1 THEN a.status END) as no_fully,"
        query += "   COUNT(CASE WHEN a.status = 2 THEN a.status END) as no_partially,"
        query += "   COUNT(CASE WHEN a.status = 3 THEN a.status END) as no_abandoned,"
        query += "   COUNT(CASE WHEN a.status = 4 THEN a.status END) as no_not,"
        query += "   COUNT(*) as no_total"
        query += " FROM pumping_station a"
        query += " WHERE a.wss_id = {0} "
        query += " GROUP BY no, item"
        query += " UNION"
        query += " SELECT "
        query += "   14 as no,"
        query += "   'Reservoir' as item,"
        query += "   COUNT(CASE WHEN a.status = 0 THEN a.status END) as no_unknown,"
        query += "   COUNT(CASE WHEN a.status = 1 THEN a.status END) as no_fully,"
        query += "   COUNT(CASE WHEN a.status = 2 THEN a.status END) as no_partially,"
        query += "   COUNT(CASE WHEN a.status = 3 THEN a.status END) as no_abandoned,"
        query += "   COUNT(CASE WHEN a.status = 4 THEN a.status END) as no_not,"
        query += "   COUNT(*) as no_total"
        query += " FROM reservoir a"
        query += " WHERE a.wss_id = {0} "
        query += " GROUP BY no, item"
        query += " UNION"
        query += " SELECT "
        query += "   15 as no,"
        query += "   'Water Source' as item,"
        query += "   COUNT(CASE WHEN a.status = 0 THEN a.status END) as no_unknown,"
        query += "   COUNT(CASE WHEN a.status = 1 THEN a.status END) as no_fully,"
        query += "   COUNT(CASE WHEN a.status = 2 THEN a.status END) as no_partially,"
        query += "   COUNT(CASE WHEN a.status = 3 THEN a.status END) as no_abandoned,"
        query += "   COUNT(CASE WHEN a.status = 4 THEN a.status END) as no_not,"
        query += "   COUNT(*) as no_total"
        query += " FROM watersource a "
        query += " WHERE a.wss_id = {0} "
        query += " GROUP BY no, item"
        query += " ) x"
        query += " ORDER BY x.no"
        query = query.format(self.wss_id)
        result = db.execute(query)
        self.assetsList = []
        for data in result:
            self.assetsList.append(Summary.Table(data))
        return self.assetsList

    def create_column_list(self):
        return [AssetsBase.Column('Assets', 'item', ''),
                AssetsBase.Column('Unknown', 'no_unknown', '0'),
                AssetsBase.Column('Fully Functional', 'no_fully', '0'),
                AssetsBase.Column('Partially Functional', 'no_partially', '0'),
                AssetsBase.Column('Abandoned', 'no_abandoned', '0'),
                AssetsBase.Column('Non Functional', 'no_not', '0'),
                AssetsBase.Column('Total', 'no_total', '0')]

    def create(self, db, doc):
        self.add_main_title(doc)

        pipe_list_obj = PipelineList(self.wss_id, None)
        pipe_list_obj.get_assets_info(db)
        pipe_list_obj.add_table(doc)
        self.add_break(doc)
        self.get_assets_info(db)
        self.add_table(doc)
        self.add_break(doc)
