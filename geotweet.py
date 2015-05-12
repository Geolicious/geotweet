# -*- coding: utf-8 -*-
"""
/***************************************************************************
 geotweet
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
from PyQt4.QtCore import QSettings, QTranslator, qVersion, QCoreApplication, QVariant
from PyQt4.QtGui import QAction, QIcon
from PyQt4 import QtGui
#from PyQt4.QtCore import QVariant
# Initialize Qt resources from file resources.py
import resources_rc
# Import the code for the dialog
from geotweet_dialog import geotweetDialog
from geotweet_exec import geotweet_exec 
import os.path
from qgis.core import *
import qgis.utils
import urllib
import tempfile
import sys, re
from subprocess import call
import datetime
#datetime.datetime.utcfromtimestamp()

class geotweet:
    """QGIS Plugin Implementation."""

    def __init__(self, iface):
        """Constructor.

        :param iface: An interface instance that will be passed to this class
            which provides the hook by which you can manipulate the QGIS
            application at run time.
        :type iface: QgsInterface
        """
        # Save reference to the QGIS interface
        self.iface = iface
        # initialize plugin directory
        self.plugin_dir = os.path.dirname(__file__)
        # initialize locale
        locale = QSettings().value('locale/userLocale')[0:2]
        locale_path = os.path.join(
            self.plugin_dir,
            'i18n',
            'geotweet_{}.qm'.format(locale))

        if os.path.exists(locale_path):
            self.translator = QTranslator()
            self.translator.load(locale_path)

            if qVersion() > '4.3.3':
                QCoreApplication.installTranslator(self.translator)

        # Create the dialog (after translation) and keep reference
        self.dlg = geotweetDialog()

        # Declare instance attributes
        self.actions = []
        self.menu = self.tr(u'&twitter2qgis')
        # TODO: We are going to let the user set this up in a future iteration
        self.toolbar = self.iface.addToolBar(u'geotweet')
        self.toolbar.setObjectName(u'geotweet')

    # noinspection PyMethodMayBeStatic
    def tr(self, message):
        """Get the translation for a string using Qt translation API.

        We implement this ourselves since we do not inherit QObject.

        :param message: String for translation.
        :type message: str, QString

        :returns: Translated version of message.
        :rtype: QString
        """
        # noinspection PyTypeChecker,PyArgumentList,PyCallByClass
        return QCoreApplication.translate('geotweet', message)


    def add_action(
        self,
        icon_path,
        text,
        callback,
        enabled_flag=True,
        add_to_menu=True,
        add_to_toolbar=True,
        status_tip=None,
        whats_this=None,
        parent=None):
        """Add a toolbar icon to the toolbar.

        :param icon_path: Path to the icon for this action. Can be a resource
            path (e.g. ':/plugins/foo/bar.png') or a normal file system path.
        :type icon_path: str

        :param text: Text that should be shown in menu items for this action.
        :type text: str

        :param callback: Function to be called when the action is triggered.
        :type callback: function

        :param enabled_flag: A flag indicating if the action should be enabled
            by default. Defaults to True.
        :type enabled_flag: bool

        :param add_to_menu: Flag indicating whether the action should also
            be added to the menu. Defaults to True.
        :type add_to_menu: bool

        :param add_to_toolbar: Flag indicating whether the action should also
            be added to the toolbar. Defaults to True.
        :type add_to_toolbar: bool

        :param status_tip: Optional text to show in a popup when mouse pointer
            hovers over the action.
        :type status_tip: str

        :param parent: Parent widget for the new action. Defaults None.
        :type parent: QWidget

        :param whats_this: Optional text to show in the status bar when the
            mouse pointer hovers over the action.

        :returns: The action that was created. Note that the action is also
            added to self.actions list.
        :rtype: QAction
        """

        icon = QIcon(icon_path)
        action = QAction(icon, text, parent)
        action.triggered.connect(callback)
        action.setEnabled(enabled_flag)

        if status_tip is not None:
            action.setStatusTip(status_tip)

        if whats_this is not None:
            action.setWhatsThis(whats_this)

        if add_to_toolbar:
            self.toolbar.addAction(action)

        if add_to_menu:
            self.iface.addPluginToWebMenu(
                self.menu,
                action)

        self.actions.append(action)

        return action

    def initGui(self):
        """Create the menu entries and toolbar icons inside the QGIS GUI."""

        icon_path = ':/plugins/geotweet/icon.png'
        self.add_action(
            icon_path,
            text=self.tr(u'collects tweets'),
            callback=self.run,
            parent=self.iface.mainWindow())


    def unload(self):
        """Removes the plugin menu item and icon from QGIS GUI."""
        for action in self.actions:
            self.iface.removePluginWebMenu(
                self.tr(u'&twitter2qgis'),
                action)
            self.iface.removeToolBarIcon(action)
        # remove the toolbar
        del self.toolbar


    def run(self):
        """Run method that performs all the real work"""
        # show the dialog
        # read the current project
        canvas = qgis.utils.iface.mapCanvas()
        allLayers = canvas.layers()
        #clear layer list prior calling the dialog
        self.dlg.layer_extent.clear()
        #adding current layers to the dlg
        index = 0
        for i in allLayers: 
            if i.type() == 0 or i.type() == 1: 
                self.dlg.layer_extent.addItem(i.name())      
                self.dlg.layer_extent.setItemData(index,i.id())
                self.dlg.layer_extent.setItemText(index,i.name())
                index = index +1

        self.dlg.show
        # Run the dialog event loop
        result = self.dlg.exec_()
        # See if OK was pressed
        if result:
            # Do something useful here - delete the line containing pass and
            # substitute with your code.
            #get nr of tweets
            tweets = self.dlg.nr_tweets.value()
            keywords = self.dlg.keywords.text()
            print str(tweets) + " : # of tweets"
            print "keywords: " + keywords
            layerid = self.dlg.layer_extent.itemData(self.dlg.layer_extent.currentIndex())
            #layer = self.dlg.layer_extent.currentText()[1]
            print "using extent of layer " + str(layerid) + " as bounding box"
            try:
                import tweepy
                print "module tweepy found"
                
            #QtGui.QMessageBox.about(self, "tweepy found", "Your tweepy installation was found. cool!")
            except ImportError:
                raise Exception("Tweepy module not installed correctly")
            #create keys for tweepy:
            if self.dlg.consumer_key.text() == '':
                access_token = "xxx"
                access_token_secret = "xxx"
                consumer_key = "xxx"
                consumer_secret = "xxx"
                key = tweepy.OAuthHandler(consumer_key, consumer_secret)
                key.set_access_token(access_token, access_token_secret)
                m = self.dlg.nr_tweets.value()
                print "used predefined key"
            else:
                key = tweepy.OAuthHandler(self.dlg.consumer_key.text(), self.dlg.consumer_key_secret.text())
                key.set_access_token(self.dlg.access_token.text(), self.dlg.access_token_secret.text())
            class stream2lib(tweepy.StreamListener):
                output = {}
                def __init__(self, api=None):
                    api = tweepy.API(key)
                    self.api = api or API()
                    self.n = 0
                    self.m = m
                def on_status(self, status):
                    self.output[status.id] = {
                        'tweet':status.text.encode('utf8'),
                        'user':status.user.screen_name,
                        'geo':status.geo,
                        'place':status.place,
                        'localization':status.user.location,
                        'time_zone':status.user.time_zone,
                        'time':status.timestamp_ms}
                    self.n = self.n+1
                    if self.n < self.m: 
                        return True
                    else:
                        print 'tweets = '+str(self.n)
                        return False

            GEOBOX_WORLD = [-180,-90,180,90]
            #getting the extent:
            for i in allLayers:
                if i.id() == layerid:
                    extent = i.extent()
            
            crsSrc = i.crs()
            crsDest = QgsCoordinateReferenceSystem(4326)
            xform = QgsCoordinateTransform(crsSrc, crsDest)
            extentn = xform.transform(extent)
            print extentn.xMinimum()
            GEOBOX_SPECIFIC = [extentn.xMinimum(), extentn.yMinimum(), extentn.xMaximum(), extentn.yMaximum()]
            #GEOBOX_SPECIFIC = [5.0770, 47.2982, 15.0403, 54.9039]
            tweepy.streaming.Stream(key, stream2lib())
            stream = tweepy.streaming.Stream(key, stream2lib())
            stream.filter(locations=GEOBOX_SPECIFIC)
            tweetdic = stream2lib().output
            print tweetdic

            vl = QgsVectorLayer("Point", "temporary_twitter_results", "memory")
            pr = vl.dataProvider()

            # changes are only possible when editing the layer
            vl.startEditing()
            # add fields
            pr.addAttributes([QgsField("user_name", QVariant.String),QgsField("localization", QVariant.String),QgsField("place", QVariant.String), QgsField("tweet", QVariant.String), QgsField("time", QVariant.String)])
            # add a feature
            for tweet in tweetdic:
                
                fet = QgsFeature()
                fet.setGeometry(QgsGeometry.fromPoint(QgsPoint(tweetdic[tweet]['place'].bounding_box.coordinates[0][1][0],tweetdic[tweet]['place'].bounding_box.coordinates[0][1][1] )))
                tweettime = datetime.datetime.utcfromtimestamp(float(tweetdic[tweet]['time'][:-3] + "." + tweetdic[tweet]['time'][11:13])).strftime('%Y-%m-%d %H:%M:%S:%f')
                #print tweettime
                #print tweetdic[tweet][str(datetime.datetime.utcfromtimestamp(float(tweetdic[tweet]['time'][:-3] + "." + tweetdic[tweet]['time'][11:13])).strftime('%Y-%m-%d %H:%M:%S'))]
                fet.setAttributes([tweetdic[tweet]['user'],tweetdic[tweet]['localization'],tweetdic[tweet]['place'].full_name + ", "+ tweetdic[tweet]['place'].country,tweetdic[tweet]['tweet'],tweettime])
                #fet.setAttributes([tweetdic[tweet]['user'],tweetdic[tweet]['localization'],tweetdic[tweet]['place'].full_name + ", "+ tweetdic[tweet]['place'].country,tweetdic[tweet]['tweet'],'test'])

                pr.addFeatures([fet])
            # commit to stop editing the layer
            vl.commitChanges()
            # update layer's extent when new features have been added
            # because change of extent in provider is not propagated to the layer
            vl.updateExtents()

            # add layer to the legend
            QgsMapLayerRegistry.instance().addMapLayer(vl)
                #call("python " + tempfolder + os.sep + "tweepy-master" + os.sep + "setup.py install" )
            #sys_modules = sys.modules.keys()
            #regex=re.compile(".*(tweepy).*")
            #tweepy_modules=[m.group(0) for l in sys_modules for m in [regex.search(l)] if m]
            #if len(tweepy_modules) == 0:
                #tempfolder = tempfile.gettempdir()
                #urllib.urlretrieve('https://github.com/tweepy/tweepy/archive/master.zip', tempfolder + os.sep + 'master.zip')
                #print "tweepy was downloaded" + str(len(tweepy_modules))
                #print test