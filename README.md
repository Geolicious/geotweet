# geotweet
collects tweets for qgis by area or keywords.
## Prerequisites
+ install tweepy
+ get API keys wit your twitter account
******
Prior usage you need to install [tweepy](http://tweepy.readthedocs.org/en/v3.2.0/#)!!!

After insallation of tweepy:
```
cd .qgis2/python/plugins
git clone https://github.com/Geolicious/geotweet.git
```
You can also download and install it from the plugin-toolbar in QGIS.
Furthermore you will need 4 keys from Twitter by [creating an app in your Twitter account](https://apps.twitter.com/app/new)


##Usage
The plugin allows either selecting by location (defined by a shapefile) or with keywords. A combined search is not possible. 
You can also define the number of geo_enabled tweets you would like to have.
Twitter offers two location parameters: place and location. The first one can be defined by the user by selecting a place for his tweet. This can be a whole country (e.g. Canada) or a city (e.g. Edmonton). The user can be at a total different location. If you select "user location" you only collect tweets with a "correct" user location as defined by the current device. Be warned: only 1% of all tweets seem to be "true" geo-enabled.

The whole collection of tweets freezes the QGIS application at the moment when the search for geo_enabled tweets takes to long! But it is still collecting and checking for geo coordinates.

You can also select to store the gathered stream. This txt file will be stored in your temp folder by default.

## Version_changes
*2015/05/17 0.8c added some more information about prerequisites, add messagebar for blank tokens
*2015/05/17 0.8 first release

## License

```
/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation; either version 2 of the License, or     *
 *   (at your option) any later version.                                   *
 *                                                                         *
 ***************************************************************************/
```
