# PostGIS2InventoryReport

## postgis2inventoryreport.py

A simple tool for exporting from a PostGIS table to Zipped QField datasets. Assumes [Python 3.6+](http://www.python.org/download/), 
[psycopg2](http://initd.org/psycopg/download/), [python-docx](https://python-docx.readthedocs.io), [lxml](https://lxml.de/) are already installed and in your ````PATH````.

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
Before installing geopandas, you can download whl file of GDAL, Fiona and Shapely as following webiste. You can chose the file depends on your platform(32bit or 64bit, Python version, etc).
````
https://www.lfd.uci.edu/~gohlke/pythonlibs/
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

But this script will not create the explanation for each district and wss, and also not create maps for each system. After creating the inventory report, you can make maps and explanation by yourself and insert them into the report.

Before running the script, kindly check the database settings at command line parameters.
````
python postgis2inventoryreport.py -d yourdatabase -H localhost - p 5432 -u user -w securePassword
````

If you want to filter only specific dictricts, use ````-l```` parameter to list ID of district by comma(,)

````
python postgis2inventoryreport.py -l 51,52,53
````

This script was developed by ````Jin IGARASHI, JICA Expert```` from ````The Project for Strengthening Operation and Maintenance of Rural Water Supply Systems in Rwanda- RWASOM````.