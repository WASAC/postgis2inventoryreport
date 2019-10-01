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
            self.sector = params[12]
            self.cell = params[13]
            self.village = params[14]

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
        query += "    CASE WHEN a.source_protected = true THEN 'YES' ELSE 'NO' END as source_protected, "
        query += "    h.sector, "
        query += "    g.cell, "
        query += "    f.village "
        query += "  FROM watersource a "
        query += "  INNER JOIN status b "
        query += "  ON a.status = b.code "
        query += "  INNER JOIN rwanda_dem_10m e "
        query += "  ON ST_Intersects(e.rast, a.geom) "
        query += "  INNER JOIN village f ON ST_Intersects(f.geom, a.geom) "
        query += "  INNER JOIN cell g ON f.cell_id = g.cell_id "
        query += "  INNER JOIN sector h ON f.sect_id = h.sect_id "
        query += "  WHERE "
        query += "   a.wss_id = {0}".format(self.wss_id)
        result = db.execute(query)
        self.assetsList = []
        for data in result:
            self.assetsList.append(WaterSources.WaterSource(data))
        return self.assetsList

    def create_column_list(self):
        return [#AssetsBase.Column('ID', 'id', ''),
                AssetsBase.Column('X', 'x', ''),
                AssetsBase.Column('Y', 'y', ''),
                AssetsBase.Column('Z', 'z', ''),
                AssetsBase.Column('Sector', 'sector', ''),
                AssetsBase.Column('Cell', 'cell', ''),
                AssetsBase.Column('Village', 'village', ''),
                AssetsBase.Column('Construction', 'construction_year', ''),
                AssetsBase.Column('Status', 'status', ''),
                AssetsBase.Column('Type', 'source_type', ''),
                AssetsBase.Column('Discharge(l/s)', 'discharge', ''),
                AssetsBase.Column('Water Meter', 'has_water_meter', 'NO'),
                AssetsBase.Column('Chlorination Unit', 'has_clorination', 'NO'),
                AssetsBase.Column('Observation', 'observation', '')]
