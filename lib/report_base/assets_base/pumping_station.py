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
        query += "    CASE WHEN a.chlorination_unit = true THEN 'YES' ELSE 'NO' END as has_clorination "
        query += "  FROM pumping_station a "
        query += "  INNER JOIN status b "
        query += "  ON a.status = b.code "
        query += "  INNER JOIN rwanda_dem_10m e "
        query += "  ON ST_Intersects(e.rast, a.geom) "
        query += "  WHERE "
        query += "   a.wss_id = {0}".format(self.wss_id)
        result = db.execute(query)
        self.assetsList = []
        for data in result:
            self.assetsList.append(PumpingStations.PumpingStation(data))
        return self.assetsList

    def create_column_list(self):
        return [['ID', 'id', ''], ['X', 'x', ''], ['Y', 'y', ''], ['Z', 'z', ''],
                  ['Construction', 'construction_year', ''], ['Status', 'status', ''],
                  ['Head', 'head_pump', ''], ['Power', 'power_pump', ''], ['Discharge', 'discharge_pump', ''],
                  ['Type', 'pump_type', ''], ['Source', 'power_source', ''], ['No of Pumps', 'no_pump', ''],
                  ['KVA', 'kva', ''], ['No of Generators', 'no_generator', ''], ['has Water Meter', 'has_water_meter', 'NO'],
                  ['Meter Installation', 'meter_installation_date', ''],
                  ['Antihummer Installation', 'installation_antihummer', 'NO'],
                  ['Antihummer Capacity', 'capacity_antihummber', ''],
                  ['has Chlorination Unit', 'has_clorination', 'NO'],
                  ['Observation', 'observation', '']]

    def add_table(self, doc):
        if len(self.assetsList) == 0:
            doc.add_paragraph('No item')
            return

        keyval = self.create_column_list()
        max_col_table = 10
        table = doc.add_table(rows=1, cols=max_col_table, style='Table Grid')
        hdr_cells = table.rows[0].cells
        for val in keyval:
            if keyval.index(val) < max_col_table:
                hdr_cells[keyval.index(val)].text = val[0]

        self.set_repeat_table_header(table.rows[0])

        for data in self.assetsList:
            row_cells = table.add_row().cells
            for val2 in keyval:
                if keyval.index(val2) < max_col_table:
                    row_cells[keyval.index(val2)].text = str(data.__dict__[val2[1]]) or val2[2]
        self.add_break(doc)

        for data in self.assetsList:
            doc.add_heading('Pumping Station #{0}'.format(str(data.id)), level=5)
            table2 = doc.add_table(rows=1, cols=2, style='Table Grid')
            hdr_cells2 = table2.rows[0].cells
            hdr_cells2[0].text = 'Item'
            hdr_cells2[1].text = 'Desription'
            self.set_repeat_table_header(table2.rows[0])
            for val3 in keyval:
                row_cells2 = table2.add_row().cells
                row_cells2[0].text = val3[0]
                row_cells2[1].text = str(data.__dict__[val3[1]]) or val3[2]
            self.add_break(doc)
