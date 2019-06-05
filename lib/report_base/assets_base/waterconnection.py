from lib.report_base.assets_base.assets_base import AssetsBase


class WaterConnections(AssetsBase):
    class WaterConnection(object):
        def __init__(self, params):
            self.id = params[0]
            self.x = params[1]
            self.y = params[2]
            self.z = params[3]
            self.connection_type = params[4]
            self.construction_year = params[5]
            self.status = params[6]
            self.no_user = params[7]
            self.customer_name = params[8]
            self.national_id = params[9]
            self.phone_number = params[10]
            self.meter_serialno = params[11]
            self.water_meter = params[12]
            self.meter_installation_date = params[13]
            self.disconnection_date = params[14]
            self.observation = params[15]

    def __init__(self, wss_id):
        super().__init__(wss_id, "Water Connections")
        self.connection_type = ''

    def get_assets_info(self, db):
        query = " SELECT "
        query += "    a.connection_id, "
        query += "    round(cast(st_x(a.geom) as numeric),6) as x, "
        query += "    round(cast(st_y(a.geom) as numeric),6) as y,  "
        query += "    cast(ST_Value(e.rast, 1, a.geom) as integer) as z,  "
        query += "    a.connection_type, "
        query += "    COALESCE(a.rehabilitation_year," \
                 "cast(a.construction_year as character varying)) as construction_year, "
        query += "    b.status,  "
        query += "    a.no_user,"
        query += "    a.customer_name,"
        query += "    a.national_id,"
        query += "    a.phone_number,"
        query += "    a.meter_serialno,"
        query += "    CASE WHEN a.water_meter = true THEN 'YES' ELSE 'NO' END as water_meter,  "
        query += "    a.meter_installation_date,"
        query += "    a.disconnection_date,"
        query += "    a.observation"
        query += "  FROM water_connection a "
        query += "  INNER JOIN status b "
        query += "  ON a.status = b.code "
        query += "  INNER JOIN rwanda_dem_10m e "
        query += "  ON ST_Intersects(e.rast, a.geom) "
        if self.connection_type == "Others":
            query += "   WHERE a.connection_type IS NULL "
        else:
            query += "   WHERE a.connection_type = '{0}' ".format(self.connection_type)
        query += "   AND a.wss_id = {0}".format(self.wss_id)
        result = db.execute(query)
        self.assetsList = []
        for data in result:
            self.assetsList.append(WaterConnections.WaterConnection(data))
        return self.assetsList

    def add_title(self, doc):
        doc.add_heading('List of {0}'.format(self.connection_type), level=4)

    def create_column_list(self):
        return [['ID', 'id', ''], ['X', 'x', ''], ['Y', 'y', ''], ['Z', 'z', ''],
                ['Type', 'connection_type', ''],
                ['Construction', 'construction_year', ''], ['Status', 'status', ''],
                ['No of Users', 'no_user', ''], ['Customer', 'customer_name', ''],
                ['Water Meter', 'water_meter', 'NO'],
                ['Meter Installation date', 'meter_installation_date', ''],
                ['Disconnection  date', 'disconnection_date', ''],
                ['Observation', 'observation', '']]

    def create(self, db, doc):
        connection_type_list = ["Public Tap",
                                "Water Kiosk",
                                "Household",
                                "Industrial",
                                "Others"]
        for connection_type in connection_type_list:
            self.connection_type = connection_type
            if connection_type_list.index(connection_type) == 0:
                self.add_main_title(doc)
            self.get_assets_info(db)
            if len(self.assetsList) > 0:
                self.add_title(doc)
                self.add_table(doc)
                self.add_break(doc)
