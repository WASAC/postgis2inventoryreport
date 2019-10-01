from lib.report_base.assets_base.assets_base import AssetsBase


class PumpingStations(AssetsBase):
    class PumpingStation(object):
        def __init__(self, params):
            self.id = params[0]
            self.x = params[1]
            self.y = params[2]
            self.z = params[3]
            self.head_pump = params[4]
            self.power_pump = params[5]
            self.discharge_pump = params[6]
            self.pump_type = params[7]
            self.power_source = params[8]
            self.no_pump = params[9]
            self.kva = params[10]
            self.no_generator = params[11]
            self.construction_year = params[12]
            self.status = params[13]
            self.observation = params[14]
            self.has_water_meter = params[15]
            self.meter_installation_date = params[16]
            self.installation_antihummer = params[17]
            self.capacity_antihummber = params[18]
            self.has_clorination = params[19]
            self.sector = params[20]
            self.cell = params[21]
            self.village = params[22]

    def __init__(self, wss_id):
        super().__init__(wss_id, "Pumping Stations")

    def get_assets_info(self, db):
        query = " SELECT "
        query += "    a.pumpingstation_id, "
        query += "    round(cast(st_x(a.geom) as numeric),6) as x, "
        query += "    round(cast(st_y(a.geom) as numeric),6) as y,  "
        query += "    cast(ST_Value(e.rast, 1, a.geom) as integer) as z,  "
        query += "    a.head_pump,  "
        query += "    a.power_pump,"
        query += "    a.discharge_pump,"
        query += "    a.pump_type,"
        query += "    a.power_source,"
        query += "    a.no_pump,"
        query += "    a.kva,"
        query += "    a.no_generator,"
        query += "    COALESCE(a.rehabilitation_year," \
                 "cast(a.construction_year as character varying)) as construction_year,  "
        query += "    b.status,  "
        query += "    a.observation,  "
        query += "    CASE WHEN a.water_meter = true THEN 'YES' ELSE 'NO' END as has_water_meter,"
        query += "    a.meter_installation_date,"
        query += "    CASE WHEN a.installation_antihummer = true THEN 'YES' ELSE 'NO' END as installation_antihummer,  "
        query += "    a.capacity_antihummber,"
        query += "    CASE WHEN a.chlorination_unit = true THEN 'YES' ELSE 'NO' END as has_clorination, "
        query += "    h.sector, "
        query += "    g.cell, "
        query += "    f.village "
        query += "  FROM pumping_station a "
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
            self.assetsList.append(PumpingStations.PumpingStation(data))
        return self.assetsList

    def create_column_list(self):
        return [AssetsBase.Column('ID', 'id', ''),
                AssetsBase.Column('X', 'x', ''),
                AssetsBase.Column('Y', 'y', ''),
                AssetsBase.Column('Z', 'z', ''),
                AssetsBase.Column('Construction', 'construction_year', ''),
                AssetsBase.Column('Status', 'status', ''),
                AssetsBase.Column('Head', 'head_pump', ''),
                AssetsBase.Column('Power', 'power_pump', ''),
                AssetsBase.Column('Discharge', 'discharge_pump', ''),
                AssetsBase.Column('Type', 'pump_type', '')
                ]

    def create_vertical_column_list(self):
        return [AssetsBase.Column('ID', 'id', ''),
                AssetsBase.Column('X', 'x', ''),
                AssetsBase.Column('Y', 'y', ''),
                AssetsBase.Column('Z', 'z', ''),
                AssetsBase.Column('Sector', 'sector', ''),
                AssetsBase.Column('Cell', 'cell', ''),
                AssetsBase.Column('Village', 'village', ''),
                AssetsBase.Column('Construction', 'construction_year', ''),
                AssetsBase.Column('Status', 'status', ''),
                AssetsBase.Column('Head', 'head_pump', ''),
                AssetsBase.Column('Power', 'power_pump', ''),
                AssetsBase.Column('Discharge', 'discharge_pump', ''),
                AssetsBase.Column('Type', 'pump_type', ''),
                AssetsBase.Column('Source', 'power_source', ''),
                AssetsBase.Column('No of Pumps', 'no_pump', ''),
                AssetsBase.Column('KVA', 'kva', ''),
                AssetsBase.Column('No of Generators', 'no_generator', ''),
                AssetsBase.Column('Water Meter', 'has_water_meter', 'NO'),
                AssetsBase.Column('Meter Installation', 'meter_installation_date', ''),
                AssetsBase.Column('Antihummer Installation', 'installation_antihummer', 'NO'),
                AssetsBase.Column('Antihummer Capacity', 'capacity_antihummber', ''),
                AssetsBase.Column('Chlorination Unit', 'has_clorination', 'NO'),
                AssetsBase.Column('Observation', 'observation', '')]

    def add_table(self, doc):
        super().add_table(doc)
        if len(self.assetsList) == 0:
            doc.add_paragraph('No item')
        self.add_table_vertical(doc)
