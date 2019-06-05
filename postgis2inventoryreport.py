import datetime
import argparse
from lib.database import Database
from lib.district import Districts
from lib.report_base.inventory_report import InventoryReport
from lib.mapcreator import MapCreator


def create_argument_parser():
    """
     Create the parameters for the script
    """
    parser = argparse.ArgumentParser(
        description="Create a QField datasets from PostGIS database.",
        epilog="Example usage: python postgis2qfield.py -d yourdatabase -H localhost - p 5432 "
               "-u user -w securePassword -l list_of_distID(seperated by comma)"
    )
    parser.add_argument("-d", "--database", dest="database",
                        type=str, required=True,
                        help="The database to connect to")

    # Python doesn't let you use -h as an option for some reason
    parser.add_argument("-H", "--host", dest="host",
                        default="localhost", type=str,
                        help="Database host. Defaults to 'localhost'")

    parser.add_argument("-p", "--port", dest="port",
                        default="5432", type=str,
                        help="Password for the database user")

    parser.add_argument("-u", "--user", dest="user",
                        default="postgres", type=str,
                        help="Database user. Defaults to 'postgres'")

    parser.add_argument("-w", "--password", dest="password",
                        type=str, required=True,
                        help="Password for the database user")

    parser.add_argument("-l", "--dist_id", dest="dist_id",
                        default="", type=str,
                        help="List of district ID which you want to export. For example, '51,52,53'")

    return parser.parse_args()


def create_reports(args):
    db = Database(args)

    temp_file_path = "./template/template_inventory_report.docx"
    current_date = datetime.datetime.now()
    main_directory = current_date.strftime('%Y%m%d_%H%M%S') + "_RWSS_Inventory_Reports"

    districts_obj = Districts(params.dist_id)
    districts = districts_obj.get_wss_list_each_district(db)
    for dist in districts:
        creator = MapCreator(db, dist, main_directory)
        creator.create()
    for dist in districts:
        inventory = InventoryReport(db, dist, temp_file_path, main_directory)
        inventory.create()


if __name__ == "__main__":
    params = create_argument_parser()
    create_reports(params)
