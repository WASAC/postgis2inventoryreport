# PostGIS2InventoryReport

## postgis2inventoryreport.py

A simple tool for exporting from a PostGIS table to Inventory Data Reports in Rwanda. Assumes 
[Python 3.6+](http://www.python.org/download/), 
[psycopg2](http://initd.org/psycopg/download/), 
[python-docx](https://python-docx.readthedocs.io), 
[matplotlib](https://matplotlib.org/), 
[geopandas](http://geopandas.org/), 
[GDAL](https://gdal.org/),
[Fiona](https://github.com/Toblerity/Fiona), 
[Shapely](https://github.com/Toblerity/Shapely), 
[descartes](https://bitbucket.org/sgillies/descartes/src/default/) 
are already installed and in your ````PATH````.

The following is example of installation procedures by pip installation.
````
pip install psycopg2
pip install python-docx
pip install matplotlib
pip install GDAL-2.4.1-cp37-cp37m-win_amd64.whl
pip install Fiona-1.8.6-cp37-cp37m-win_amd64.whl
pip install Shapely-1.6.4.post1-cp37-cp37m-win_amd64.whl
pip install geopandas
pip install descartes
````
Before installing geopandas, you can download whl file of GDAL, Fiona and Shapely from [here](https://www.lfd.uci.edu/~gohlke/pythonlibs/). You can chose the file depends on your platform(32bit or 64bit, Python version, etc).

If you failed to install geopandas by pip or wheel file, you can install from Git directly as below.
````
git clone https://github.com/geopandas/geopandas.git
cd geopandas
pip install .
````

The tool was designed for RWSS department of WASAC in Rwanda.

####Example usage:

To export the following information of ````water pipeline network````from database ````rwss_assets```` as user ````user```` to word document(.docx) for each districts:

* List of Water Supply Systems
* (repeat) WSS Information
    * Summary of Assets
    * List of Chambers
    * List of Reservoirs
    * List of Water Sources
    * List of Water Connections (Houlsehold, Public Tap, Water Kiosk and Industry)

But this script will not create the explanation for each district and wss. After creating the inventory report, you can make explanation by yourself and insert them into the report.

Before running the script, kindly check the database settings at command line parameters.
````
python postgis2inventoryreport.py -d yourdatabase -H localhost - p 5432 -u user -w securePassword
````

If you want to filter only specific dictricts, use ````-l```` parameter to list ID of district by comma(,)

````
python postgis2inventoryreport.py -l 51,52,53
````

This script was developed by ````Jin IGARASHI, JICA Expert```` from ````The Project for Strengthening Operation and Maintenance of Rural Water Supply Systems in Rwanda- RWASOM````.