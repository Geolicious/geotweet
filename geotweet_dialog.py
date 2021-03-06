# -*- coding: utf-8 -*-
"""
/***************************************************************************
 geotweetDialog
                                 A QGIS plugin
 collects tweets by area or keywords
                             -------------------
        begin                : 2015-05-11
        git sha              : $Format:%H$
        copyright            : (C) 2015 by Riccardo Klinger, Geolicious
        email                : riccardo.klinger@geolicious.de
 ***************************************************************************/

/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation; either version 2 of the License, or     *
 *   (at your option) any later version.                                   *
 *                                                                         *
 ***************************************************************************/
"""

import os

from PyQt4 import QtGui, uic
from qgis.core import *
import qgis.utils
import tempfile
import urllib
import zipfile


FORM_CLASS, _ = uic.loadUiType(os.path.join(
    os.path.dirname(__file__), 'geotweet_dialog_base.ui'))


class geotweetDialog(QtGui.QDialog, FORM_CLASS):
    def __init__(self, parent=None):
        """Constructor."""
        super(geotweetDialog, self).__init__(parent)
        # Set up the user interface from Designer.
        # After setupUI you can access any designer object by doing
        # self.<objectname>, and you can use autoconnect slots - see
        # http://qt-project.org/doc/qt-4.8/designer-using-a-ui-file.html
        # #widgets-and-dialogs-with-auto-connect
        self.setupUi(self)
        try:
            import tweepy
            print "module tweepy found"
            #QtGui.QMessageBox.about(self, "tweepy found", "Your tweepy installation was found. cool!")
        except ImportError:
            QtGui.QMessageBox.about(self, "must install tweepy!", "we will download tweepy to your temp folder but you must install it by yourself")
            print "module tweepy not found but will be downloaded and installe"
            tempfolder = tempfile.gettempdir()
            urllib.urlretrieve('https://github.com/tweepy/tweepy/archive/master.zip', tempfolder + os.sep + 'master.zip')
            print "tweepy was downloaded to your temp folder"
            with zipfile.ZipFile(tempfolder + os.sep + 'master.zip', "r") as z:
                z.extractall(tempfolder + os.sep)
            print "tweepy was unzipped to ~Temp/tweepy-master/"
        #for i in allLayers:
        #    self.layer_extent.addItem(i.name())
        #nr_tweets = self.nr_tweets.valueChanged.connect(self.get_tweets)
        #return nr_tweets




