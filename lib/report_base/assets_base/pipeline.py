from lib.report_base.assets_base.assets_base import AssetsBase


class PipelineList(AssetsBase):
    class Pipeline(object):
        def __init__(self, params):
            self.material = params[0]
            self.pipe_size = params[1]
            self.unknown = params[2]
            self.one_year = params[3]
            self.three_years = params[4]
            self.five_years = params[5]
            self.ten_years = params[6]
            self.more_than_ten_years = params[7]

    def __init__(self, wss_id):
        super().__init__(wss_id, "Pipeline")

    def get_assets_info(self, db):
        """
                Get the list of WSS by targeted district from PostGIS

                Parameters
                ----------
                db : Database object
                """
        query = "  SELECT "
        query += "    y.material, "
        query += "    y.pipe_size, "
        query += "    SUM(CASE WHEN y.diff_const_year IS NULL THEN round(pipe_length,2) END) as unknown, "
        query += "    SUM(CASE WHEN y.diff_const_year BETWEEN 0 AND 1 THEN round(pipe_length,2) END) as one_year, "
        query += "    SUM(CASE WHEN y.diff_const_year BETWEEN 2 AND 3 THEN round(pipe_length,2) END) as three_years, "
        query += "    SUM(CASE WHEN y.diff_const_year BETWEEN 4 AND 5 THEN round(pipe_length,2) END) as five_years,	 "
        query += "    SUM(CASE WHEN y.diff_const_year BETWEEN 6 AND 10 THEN round(pipe_length,2) END) as ten_years, "
        query += "    SUM(CASE WHEN y.diff_const_year > 10 THEN round(pipe_length,2) END) as more_than_ten_years "
        query += "  FROM ( "
        query += "  SELECT "
        query += "    x.material, "
        query += "    x.pipe_size, "
        query += "    x.diff_const_year, "
        query += "    sum(x.pipe_length) as pipe_length "
        query += "  FROM ( "
        query += "    SELECT  "
        query += "      material,  "
        query += "      cast(pipe_size as integer) as pipe_size,  "
        query += "      cast(to_char(current_timestamp, 'YYYY') as integer) - cast(COALESCE( "
        query += "       CASE WHEN (rehabilitation_year ~ '^[0-9]{4}$') = false THEN NULL ELSE rehabilitation_year END,"
        query += "       CASE WHEN (construction_year ~ '^[0-9]{4}$') = false  THEN NULL ELSE construction_year END,"
        query += "       NULL) as integer) as diff_const_year, "
        query += "      cast(ST_LENGTH(ST_TRANSFORM(geom, 32736)) as numeric) as pipe_length "
        query += "    FROM pipeline "
        query += "    WHERE wss_id = {0} ".format(str(self.wss_id))
        query += "  ) x "
        query += "  GROUP BY "
        query += "    x.material, "
        query += "    x.pipe_size, "
        query += "    x.diff_const_year) y "
        query += "  GROUP BY "
        query += "    y.material, "
        query += "    y.pipe_size "
        query += "  ORDER BY  "
        query += "    y.material, "
        query += "    y.pipe_size "
        result = db.execute(query)
        self.assetsList = []
        for data in result:
            self.assetsList.append(PipelineList.Pipeline(data))
        return self.assetsList

    def add_table(self, doc):
        if len(self.assetsList) == 0:
            doc.add_paragraph('No item')
            return

        table = doc.add_table(rows=2, cols=8, style='Table Grid')
        hdr_cells = table.rows[0].cells
        hdr_cells[0].text = 'Material'
        hdr_cells[1].text = 'Diameter'
        hdr_cells[2].text = 'Length(m)'
        hdr_cells_2 = table.rows[1].cells
        hdr_cells_2[2].text = 'Unknown'
        hdr_cells_2[3].text = '<= 1 year'
        hdr_cells_2[4].text = '<= 3 years'
        hdr_cells_2[5].text = '<= 5 years'
        hdr_cells_2[6].text = '<= 10 years'
        hdr_cells_2[7].text = '> 10 years'
        hdr_cells[0].merge(hdr_cells_2[0])
        hdr_cells[1].merge(hdr_cells_2[1])
        hdr_cells[2].merge(hdr_cells[7])

        self.set_repeat_table_header(table.rows[0])
        self.set_repeat_table_header(table.rows[1])

        for data in self.assetsList:
            row_cells = table.add_row().cells
            row_cells[0].text = data.material or ''
            row_cells[1].text = str(data.pipe_size).replace('None', '') or ''
            row_cells[2].text = str(data.unknown).replace('None', '') or '0.00'
            row_cells[3].text = str(data.one_year).replace('None', '')or '0.00'
            row_cells[4].text = str(data.three_years).replace('None', '') or '0.00'
            row_cells[5].text = str(data.five_years).replace('None', '') or '0.00'
            row_cells[6].text = str(data.ten_years).replace('None', '') or '0.00'
            row_cells[7].text = str(data.more_than_ten_years).replace('None', '000') or '0.00'
