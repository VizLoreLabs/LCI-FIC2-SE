/*
 * POIs.js
 */

/*global $*/
/*global alert*/
/*global sensors*/
/*global device*/
/*global map*/
/*global settings*/

var POIs = {
    
    init: function () {
        "use strict";
        this.initRecommend();
    },
    
    // Init recommend button
    initRecommend: function () {
        "use strict";
        $('#recommend').click(function () {
            map.removePopups();
            POIs.getPOIs();
        });
    },
    
    // Show markers on the map
    showMarkers: function (data) {
        "use strict";
        var poi, id, html = "", position, fw_core;
        for (poi in data.POIS) {
            if (data.POIS.hasOwnProperty(poi)) {
                for (id in data.POIS[poi]) {
                    if (data.POIS[poi].hasOwnProperty(id)) {
                        fw_core = data.POIS[poi][id].fw_core;
                        html = '<h2>' + fw_core.name[''] + '</h2>' +
                            '<h3>' + fw_core.label[''] + '</h3>' +
                            '<div style="text-align: center;">' +
                            '<button type="button" onclick="POIs.accept(\'' + id + '\')" style="display" inline-block;">Accept</button>' +
                            '<button type="button" onclick="POIs.ignore(\'' + id + '\')" style="display: inline-block;">Ignore</button></div>';
                        position = {lat: fw_core.location.wgs84.latitude, lon: fw_core.location.wgs84.longitude};
                        map.addPopup(position, html);
                    }
                }
            }
        }
        $("#activity").text(data.activity);
    },
    
    // Ignore poi
    ignore: function (id) {
        "use strict";
        map.removePopups();
        POIs.getPOIs(id);
    },
    
    accept: function (id) {
        "use strict";
    },
    
    // Get POIs from recommender
    getPOIs: function (ignore_id) {
        "use strict";
        
        var position = sensors.getCachedPosition(),
            data = {
                uuid: device.uuid,
                lat: position.coords.latitude,
                lon: position.coords.longitude,
                /*lat: 41.402486,
                lon: 2.188002,*/
                ts: (new Date()).getTime(),
                ac: 1
            };
        
        if (ignore_id) {
            $.extend(data, {ignore: ignore_id});
        }

        $.ajax({
            type: 'GET',
            data: data,
            contentType: "application/json; charset=utf-8",
            dataType: "json",
            url: settings.rmp_url + "/recommend",
            success: function (data) {
                POIs.showMarkers(data);
            },
            error: function (error) {
                alert('There was an error with getting data from server!\n' + JSON.stringify(error));
            }
        });
    }
                
};