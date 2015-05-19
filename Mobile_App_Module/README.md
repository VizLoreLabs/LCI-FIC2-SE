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


## Instalation guide:
- This application is based on a Cordova 4.2.0 framework: https://cordova.apache.org/docs/en/4.0.0/guide_platforms_android_index.md.html#Android%20Platform%20Guide
- The .apk file can be installed on any Android mobile device: https://github.com/VizLoreLabs/LCI-FIC2-SE/blob/master/Mobile_App_Module/FIC2.apk
- The following Cordova plugins are used:
  - org.apache.cordova.device 0.2.10 “Device” (used for generating UUIDs)
  - org.apache.cordova.device-motion 0.2.12-dev “Device Motion” (used for gathering data from accelerometer)
  - org.apache.cordova.geolocation 0.3.8 “Geolocation” (used for getting current location)
  - org.apache.cordova.wifiinfo 0.1.1 “Wifi Network Information” (used for gathering nearby SSIDs)
  - org.dartlang.phonegap.gyroscope 0.0.2 “Device Gyroscope” (used for gathering data from gyroscope)
- The following JavaScript libraries are used:
  - leaflet.js (used for displaying map)
  - jquery-1.10.2.min.js (used for DOM manipulations)
  - jquery.mobile-1.4.2.min.js (used for app design)
- Within the application you can use the settings button in the GUI to:
  - Specify base URL for the Activity and Context Recognition module
  - Specify base URL for the Recommendation Matrix Preparation module
  - Toggle on/off sensory data stream
  - Enter recommendation matrix code for your custom recommendation matrix defined through the web interface of the Recommendation Matrix Preparation module available here: http://89.216.30.67:8080/recommend/

