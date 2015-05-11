# -*- coding: utf-8 -*-
"""
/***************************************************************************
 geotweet
                                 A QGIS plugin
 collects tweets by area or keywords
                             -------------------
        begin                : 2015-05-11
        copyright            : (C) 2015 by Riccardo Klinger, Geolicious
        email                : riccardo.klinger@geolicious.de
        git sha              : $Format:%H$
 ***************************************************************************/

/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation; either version 2 of the License, or     *
 *   (at your option) any later version.                                   *
 *                                                                         *
 ***************************************************************************/
 This script initializes the plugin, making it known to QGIS.
"""


# noinspection PyPep8Naming
def classFactory(iface):  # pylint: disable=invalid-name
    """Load geotweet class from file geotweet.

    :param iface: A QGIS interface instance.
    :type iface: QgsInterface
    """
    #
    from .geotweet import geotweet
    return geotweet(iface)
