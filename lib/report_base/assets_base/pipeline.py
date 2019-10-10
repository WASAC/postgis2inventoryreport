from lib.report_base.assets_base.assets_base import AssetsBase


class PipelineList(AssetsBase):
    class Pipeline(object):
        def __init__(self, params):
            self.material = params[0]
            self.pipe_size = params[1]
            self.unknown = params[2]
            self.three_year = params[3]
            self.five_years = params[4]
            self.ten_years = params[5]
            self.twenty_years = params[6]
            self.more_than_twenty_years = params[7]
            self.total_length_each_material = params[8]

    def __init__(self, wss_id):
        super().__init__(wss_id, "Pipeline")

    def get_assets_info(self, db):
        query = "  SELECT "
        query += "    y.material, "
        query += "    y.pipe_size, "
        query += "    SUM(CASE WHEN y.diff_const_year IS NULL THEN round(pipe_length,2) END) as unknown, "
        query += "    SUM(CASE WHEN y.diff_const_year BETWEEN 0 AND 3 THEN round(pipe_length,2) END) as three_year, "
        query += "    SUM(CASE WHEN y.diff_const_year BETWEEN 4 AND 5 THEN round(pipe_length,2) END) as five_years, "
        query += "    SUM(CASE WHEN y.diff_const_year BETWEEN 6 AND 10 THEN round(pipe_length,2) END) as ten_years,	 "
        query += "    SUM(CASE WHEN y.diff_const_year BETWEEN 11 AND 20 THEN round(pipe_length,2) END) as twenty_years, "
        query += "    SUM(CASE WHEN y.diff_const_year > 20 THEN round(pipe_length,2) END) as more_than_twenty_years, "
        query += "    round(SUM(pipe_length), 2) as total_length_each_material "
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
        query += "      cast(to_char(current_timestamp, 'YYYY') as integer) - COALESCE(rehabilitation_year, construction_year) as diff_const_year, "
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

        table = doc.add_table(rows=2, cols=9, style='Table Grid')
        hdr_cells = table.rows[0].cells
        hdr_cells[0].text = 'Material'
        hdr_cells[1].text = 'Diameter'
        hdr_cells[2].text = 'Length(m)'
        hdr_cells_2 = table.rows[1].cells
        hdr_cells_2[2].text = 'Unknown'
        hdr_cells_2[3].text = '<= 3 years'
        hdr_cells_2[4].text = '<= 5 years'
        hdr_cells_2[5].text = '<= 10 years'
        hdr_cells_2[6].text = '<= 20 years'
        hdr_cells_2[7].text = '> 20 years'
        hdr_cells_2[8].text = 'Total'
        hdr_cells[0].merge(hdr_cells_2[0])
        hdr_cells[1].merge(hdr_cells_2[1])
        hdr_cells[2].merge(hdr_cells[8])

        self.set_repeat_table_header(table.rows[0])
        self.set_repeat_table_header(table.rows[1])

        sum_unknown = 0.0
        sum_three = 0.0
        sum_five = 0.0
        sum_ten = 0.0
        sum_twenty = 0.0
        sum_more_twenty = 0.0
        sum_total = 0.0

        for data in self.assetsList:
            row_cells = table.add_row().cells
            row_cells[0].text = data.material or 'Unknown'
            row_cells[1].text = str(data.pipe_size).replace('None', 'Unknown') or 'Unknown'
            row_cells[2].text = str(data.unknown).replace('None', '') or '0.00'
            row_cells[3].text = str(data.three_year).replace('None', '')or '0.00'
            row_cells[4].text = str(data.five_years).replace('None', '') or '0.00'
            row_cells[5].text = str(data.ten_years).replace('None', '') or '0.00'
            row_cells[6].text = str(data.twenty_years).replace('None', '') or '0.00'
            row_cells[7].text = str(data.more_than_twenty_years).replace('None', '000') or '0.00'
            row_cells[8].text = str(data.total_length_each_material).replace('None', '000') or '0.00'

            sum_unknown += float(row_cells[2].text)
            sum_three += float(row_cells[3].text)
            sum_five += float(row_cells[4].text)
            sum_ten += float(row_cells[5].text)
            sum_twenty += float(row_cells[6].text)
            sum_more_twenty += float(row_cells[7].text)
            sum_total += float(row_cells[8].text)

        row_cells = table.add_row().cells
        row_cells[0].text = 'Total Length'
        row_cells[0].merge(row_cells[1])
        row_cells[2].text = str(round(sum_unknown, 2)) or '0.00'
        row_cells[3].text = str(round(sum_three, 2)) or '0.00'
        row_cells[4].text = str(round(sum_five, 2)) or '0.00'
        row_cells[5].text = str(round(sum_ten, 2)) or '0.00'
        row_cells[6].text = str(round(sum_twenty, 2)) or '0.00'
        row_cells[7].text = str(round(sum_more_twenty, 2)) or '0.00'
        row_cells[8].text = str(round(sum_total, 2)) or '0.00'
