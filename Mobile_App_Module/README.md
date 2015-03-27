Mobile Application Module
====================
The module is implemented as a demo Android application.
This application is based on a Cordova 4.2.0 framework. 
If you want to choose another recommender you should change the getPOIs() function inside POIs.js file. For choosing another activity recognition module you should change the sendData() function inside sensors.js file.

Used Cordova plugins:

  - org.apache.cordova.device 0.2.10 "Device" (used for generating UUIDs)
  - org.apache.cordova.device-motion 0.2.12-dev "Device Motion" (used for gathering data from accelerometer)
  - org.apache.cordova.geolocation 0.3.8 "Geolocation" (used for getting current location)
  - org.apache.cordova.wifiinfo 0.1.1 "Wifi Network Information" (used for gathering nearby SSIDs)
  - org.dartlang.phonegap.gyroscope 0.0.2 "Device Gyroscope" (used for gathering data from gyroscope)

Used JavaScript libraries:

  - leaflet.js (used for displaying map)
  - jquery-1.10.2.min.js (used for DOM manipulations)
  - jquery.mobile-1.4.2.min.js (used for app design)
