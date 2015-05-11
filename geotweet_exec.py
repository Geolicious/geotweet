# -*- coding: utf-8 -*-
"""
/***************************************************************************
 geotweeter
								 A QGIS plugin
 Twitter collector for qgis
							 -------------------
		begin				: 2015-05-12
		copyright			: (C) 2015 by Riccardo Klinger
		email				: riccardo.klinger@geolicious.com
 ***************************************************************************/

/***************************************************************************
 *																		 *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation; either version 3 of the License, or	 *
 *   (at your option) any later version.								   *
 *																		 *
 ***************************************************************************/
"""

from PyQt4.QtCore import QFileInfo
import osgeo.ogr, osgeo.osr #we will need some packages
from osgeo import ogr
from osgeo import gdal
import processing
import shutil
from qgis.core import *
import qgis.utils
import os #for file writing/folder actions
import shutil #for reverse removing directories
import urllib # to get files from the web
from urlparse import parse_qs
import time
import tempfile
import re
import fileinput
import webbrowser #to open the made map directly in your browser
import sys #to use another print command without annoying newline characters 
from xml.etree import ElementTree as et
import zipfile

def geotweet_exec():
	canvas = qgis.utils.iface.mapCanvas()
	allLayers = canvas.layers()
	for i in allLayers:
		#first for vector files:
		print i.name()