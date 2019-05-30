from lib.report_base.assets_base.assets_base import AssetsBase


class Chambers(AssetsBase):
    class Chamber(object):
        def __init__(self, params):
            self.id = params[0]
            self.x = params[1]
            self.y = params[2]
            self.z = params[3]
            self.chamber_size = params[4]
            self.material = params[5]
            self.construction_year = params[6]
            self.status = params[7]
            self.observation = params[8]
            self.for_breakpressure = params[9]
            self.has_clorination = params[10]

    def __init__(self, wss_id):
        super().__init__(wss_id, "Chambers")
        self.chamber_type = ''

    def get_assets_info(self, db):
        """
                Get the list of WSS by targeted district from PostGIS

                Parameters
                ----------
                db : Database object
                """
        query = "   SELECT "
        query += "     a.chamber_id, "
        query += "     round(cast(st_x(a.geom) as numeric),6) as x, "
        query += "     round(cast(st_y(a.geom) as numeric),6) as y,  "
        query += "     cast(ST_Value(e.rast, 1, a.geom) as integer) as z,  "
        query += "     a.chamber_size,  "
        query += "     a.material,  "
        query += "    COALESCE(a.rehabilitation_year," \
                 "cast(a.construction_year as character varying)) as construction_year,  "
        query += "     b.status,  "
        query += "     a.observation,  "
        query += "     CASE WHEN a.is_breakpressure = 1 THEN 'YES' ELSE 'NO' END as for_breakpressure,  "
        query += "     CASE WHEN a.chlorination_unit = 1 THEN 'YES' ELSE 'NO' END as has_clorination "
        query += "   FROM chamber a "
        query += "   INNER JOIN status b "
        query += "   ON a.status = b.code "
        query += "   INNER JOIN rwanda_dem_10m e "
        query += "   ON ST_Intersects(e.rast, a.geom) "
        query += "   WHERE a.chamber_type = '{0}' ".format(self.chamber_type)
        query += "   AND a.wss_id = {0}".format(self.wss_id)
        result = db.execute(query)
        self.assetsList = []
        for data in result:
            self.assetsList.append(Chambers.Chamber(data))
        return self.assetsList

    def add_title(self, doc):
        doc.add_heading('List of {0}'.format(self.chamber_type), level=4)

    def create_column_list(self):
        return [['ID', 'id', ''], ['X', 'x', ''], ['Y', 'y', ''], ['Z', 'z', ''],
                ['Construction', 'construction_year', ''], ['Status', 'status', ''],
                ['Size', 'chamber_size', ''], ['Material', 'material', ''],
                ['for Break pressure', 'for_breakpressure', 'NO'],
                ['has Chlorination Unit', 'has_clorination', 'NO'],
                ['Observation', 'observation', '']]

    def create(self, db, doc):
        chamber_type_list = ["Valve chamber", "Air release chamber", "Washout chamber",
                             "Break Pressure chamber", "PRV chamber",
                             "Starting chamber", "Collection chamber"]
        for chamber_type in chamber_type_list:
            self.chamber_type = chamber_type
            if chamber_type_list.index(chamber_type) == 0:
                self.add_main_title(doc)
            self.get_assets_info(db)
            if len(self.assetsList) > 0:
                self.add_title(doc)
                self.add_table(doc)
                self.add_break(doc)
