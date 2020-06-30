from lib.report_base.assets_base.assets_base import AssetsBase


class WssList(AssetsBase):

    class Wss(object):
        def __init__(self, params):
            self.wss_id = params[0]
            self.wss_name = params[1]
            self.wss_type = params[2]
            self.status = params[3]
            self.po_name = params[4]
            self.po_type = params[5]
            self.lon = params[6]
            self.lat = params[7]
            self.description = params[8]
            self.length = params[9]

    def __init__(self, dist_id):
        super().__init__(None, "Water Supply Systems")
        self.dist_id = dist_id
        self.assetsList = []

    def add_main_title(self, doc):
        doc.add_heading('List of {0}'.format(self.assets_type), level=2)

    def get_assets_info(self, db):
        """
        Get the list of WSS by targeted district from PostGIS

        Parameters
        ----------
        db : Database object
        """
        query = " SELECT "
        query += "   a.wss_id,  "
        query += "   a.wss_name,  "
        query += "   a.wss_type,  "
        query += "   a.status,  "
        query += "   c.po_name, "
        query += "   c.po_type, "
        query += "   st_x(st_centroid(a.geom)) as lon,  "
        query += "   st_y(st_centroid(a.geom)) as lat, "
        query += "   a.description, "
        query += "   round(cast(d.length as numeric),2) as length "
        query += " FROM wss a "
        query += " LEFT JOIN management b "
        query += " ON a.wss_id = b.wss_id "
        query += " LEFT JOIN private_operator c "
        query += " ON b.po_id = c.po_id "
        query += " LEFT JOIN (SELECT wss_id, sum(st_length(st_transform(geom,32637))) as length " \
                 " FROM pipeline GROUP BY wss_id) d "
        query += " ON a.wss_id = d.wss_id "
        query += " WHERE a.dist_id = " + str(self.dist_id)
        query += " ORDER BY a.wss_id "
        result = db.execute(query)
        self.assetsList = []
        for data in result:
            self.assetsList.append(WssList.Wss(data))
        return self.assetsList

    def create_column_list(self):
        return [AssetsBase.Column('WSS ID', 'wss_id', ''),
                AssetsBase.Column('Name', 'wss_name', '0'),
                AssetsBase.Column('Length(m)', 'length', '0.0'),
                AssetsBase.Column('Type', 'wss_type', '0'),
                AssetsBase.Column('Status', 'status', ''),
                AssetsBase.Column('Management', 'po_name', ''),
                AssetsBase.Column('Category of Management', 'po_type', '')]

    def create(self, db, doc):
        self.add_main_title(doc)
        self.get_assets_info(db)
        self.add_table(doc)
        doc.add_page_break()
        return self.assetsList
