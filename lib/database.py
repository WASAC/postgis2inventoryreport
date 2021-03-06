import psycopg2
import geopandas as gpd


class Database(object):
    def __init__(self, params):
        """
        Constructor

        Parameters
        ----------
        params : object
            List of arguments from command line
        """
        self.host = params.host
        self.port = params.port
        self.user = params.user
        self.password = params.password
        self.database = params.database
        self.conn = None
        self.create_connection()

    def create_connection(self):
        """
        Create the database connection
        """
        try:
            self.conn = psycopg2.connect(host=self.host, port=self.port, database=self.database, user=self.user, password=self.password)
        except:
            print("Unable to connect to the database. Please check your options and try again.")
            exit()

    def execute(self, query):
        """
        Execute SQL on PostGIS

        Parameters
        ----------
        query : str
            SQL for running
        """
        with self.conn.cursor() as cur:
            # Execute the query
            try:
                cur.execute(query)
            except Exception as exc:
                print("Unable to execute query. Error was {0}".format(str(exc)))
                exit()
            rows = cur.fetchall()
            return rows

    def get_geodataframe_from_postgis(self, sql):
        return gpd.GeoDataFrame.from_postgis(sql, self.conn, geom_col='geom')