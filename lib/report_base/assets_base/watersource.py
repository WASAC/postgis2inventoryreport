from lib.report_base.assets_base.assets_base import AssetsBase


class WaterSources(AssetsBase):
    class WaterSource(object):
        def __init__(self, params):
            self.id = params[0]
            self.x = params[1]
            self.y = params[2]
            self.z = params[3]
            self.source_type = params[4]
            self.discharge = params[5]
            self.construction_year = params[6]
            self.status = params[7]
            self.observation = params[8]
            self.has_water_meter = params[9]
            self.has_clorination = params[10]
            self.source_protected = params[11]

    def __init__(self, wss_id):
        super().__init__(wss_id, "Water Sources")

    def get_assets_info(self, db):
        query = " SELECT "
        query += "    a.watersource_id, "
        query += "    round(cast(st_x(a.geom) as numeric),6) as x, "
        query += "    round(cast(st_y(a.geom) as numeric),6) as y,  "
        query += "    cast(ST_Value(e.rast, 1, a.geom) as integer) as z,  "
        query += "    a.source_type,  "
        query += "    a.discharge,"
        query += "    COALESCE(a.rehabilitation_year," \
                 "cast(a.construction_year as character varying)) as construction_year,  "
        query += "    b.status,  "
        query += "    a.observation,  "
        query += "    CASE WHEN a.water_meter = true THEN 'YES' ELSE 'NO' END as has_water_meter,"
        query += "    CASE WHEN a.chlorination_unit = true THEN 'YES' ELSE 'NO' END as has_clorination, "
        query += "    CASE WHEN a.source_protected = true THEN 'YES' ELSE 'NO' END as source_protected "
        query += "  FROM watersource a "
        query += "  INNER JOIN status b "
        query += "  ON a.status = b.code "
        query += "  INNER JOIN rwanda_dem_10m e "
        query += "  ON ST_Intersects(e.rast, a.geom) "
        query += "  WHERE "
        query += "   a.wss_id = {0}".format(self.wss_id)
        result = db.execute(query)
        self.assetsList = []
        for data in result:
            self.assetsList.append(WaterSources.WaterSource(data))
        return self.assetsList

    def create_column_list(self):
        return [['ID', 'id', ''], ['X', 'x', ''], ['Y', 'y', ''], ['Z', 'z', ''],
                  ['Construction', 'construction_year', ''], ['Status', 'status', ''],
                  ['Type', 'source_type', ''], ['Discharge', 'discharge', ''],
                  ['has Water Meter', 'has_water_meter', 'NO'],
                  ['has Chlorination Unit', 'has_clorination', 'NO'],
                  ['Observation', 'observation', '']]


