/*
 * sensors.js
 */

/*global alert*/
/*global confirm*/
/*global $*/
/*global map*/

var sensors = {
    
    sendingInterval: 3000,
    accelerometerInterval: 20,
    geolocationInterval: 15000,
    gyroscopeInterval: 20,
    wifiInterval: 15000,
    
    init: function () {
        "use strict";
        this.initAccelerometer();
        this.initGeolocation();
        this.initWifiWatch();
        this.initGyroscope();
        setInterval(this.sendData, this.sendingInterval);
    },
    
    // Packet
    packet: {uuid: null, acceleration: [], location: [], wifi: [], gyroscope: []},
    sendData: function () {
        "use strict";
        sensors.packet.uuid = window.device.uuid;
        sensors.packet.gyroscope = [];

        $.ajax({
            type: 'POST',
            data: JSON.stringify(sensors.packet),
            contentType: "application/json; charset=utf-8",
            dataType: "json",
            url: 'http://89.216.30.67:55555/ac/',
            success: function (data) {
                //alert("Data from server: " + JSON.stringify(data));
            },
            error: function () {
                //alert('There was an error with getting data from server!');
            }
        });
        
        sensors.packet = {uuid: null, acceleration: [], location: [], wifi: [], gyroscope: []};
    },
    
    // Accelerometer
    accelerometerWatch: null,
    initAccelerometer: function () {
        "use strict";
        var onSuccess = function (acceleration) {
            sensors.packet.acceleration.push(acceleration);
        },
            onError = function () {
                alert('Accelerometer: onError!');
            },
            options = {
                frequency: sensors.accelerometerInterval
            };
        
        this.accelerometerWatch = navigator.accelerometer.watchAcceleration(onSuccess, onError, options);
    },
    
    // Geolocation
    geoloactionWatch: null,
    lastPositionTimestamp: 0,
    cachedPosition: null,
    initGeolocation: function () {
        "use strict";
        var onSuccess = function (position) {
                var curTimestamp = Math.round((new Date()).getTime());
                sensors.cachedPosition = position;
                if (curTimestamp - sensors.lastPositionTimestamp > sensors.geolocationInterval) {
                    sensors.packet.location.push(position);
                    sensors.lastPositionTimestamp = curTimestamp;
                    map.setView(position.coords.latitude, position.coords.longitude);
                    map.setLocationMarker(position.coords.latitude, position.coords.longitude);
                }
            },
            onError = function (error) {
                if (confirm("Turn on GPS and click OK!") !== true) {
                    navigator.app.exitApp();
                }
            },
            options = {
                enableHighAccuracy: true
            };
        
        this.gelocationWatch = navigator.geolocation.watchPosition(onSuccess, onError, options);
    },
    
    getCachedPosition: function () {
        "use strict";
        return sensors.cachedPosition;
    },
    
    // Wifi Watch
    wifiWatch: null,
    initWifiWatch: function () {
        "use strict";
        var wifiCallback = function () {
            var net = window.wifi.networks,
                SSIDs = [],
                networks,
                network,
                timestamp,
                i;
            
			for (i in net) {
                if (net.hasOwnProperty(i)) {
                    network = net[i];
                    SSIDs.push(network.SSID);
                }
			}
            
            timestamp = (new Date()).getTime();
            networks = { ssids: SSIDs, timestamp:  timestamp};
            sensors.packet.wifi.push(networks);
        };
        
        this.wifiWatch = setInterval(wifiCallback, sensors.wifiInterval);
    },
    
    // Gyroscope
    gyroscopeWatch: null,
    initGyroscope: function () {
        "use strict";
        var onSuccess = function (speed) {
            sensors.packet.gyroscope.push(speed);
        },
            onError = function (error) {
                alert("Gyroscope: onError - " + JSON.stringify(error));
            },
            options = {
                frequency: sensors.gyroscopeInterval
            };
        
        this.gyroscopeWatch = navigator.gyroscope.watchAngularSpeed(onSuccess, onError, options);
    }
    
};