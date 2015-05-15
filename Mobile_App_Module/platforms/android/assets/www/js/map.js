/*global $*/
/*global L*/
/*global HeatmapOverlay*/
/*jslint plusplus: true */

var map = {
    emulatedLat: 41.402486,
    emulatedLon: 2.188002,
    mapElement: null,
    mapquestUrl: 'http://otile{s}.mqcdn.com/tiles/1.0.0/osm/{z}/{x}/{y}.png',
    
    init: function () {
        "use strict";
        this.fixHeight();
        this.initDivElement();
        this.initMap();
    },
    
    fixHeight: function () {
        "use strict";
        var height = $(window).height() - 50;
        $("#menu_side_panel").css("overflow-y", "auto").css("height", height);
    },
    
    initDivElement: function () {
        "use strict";
        var header = $('#header'),
            footer = $('#footer'),
            body = $('html');
        
        this.mapElement = $('#map');
        this.mapElement.css('height', body.height() - header.outerHeight() - footer.outerHeight());
        this.mapElement.css('width', body.width());
    },
    
    map: null,
    baseLayer: null,
    initMap: function () {
        "use strict";
        this.baseLayer = new L.TileLayer(this.mapquestUrl, {
            maxZoom: 18,
            subdomains: ['1', '2', '3', '4']
        });
        
        this.map = new L.Map('map', {
            center: new L.LatLng(this.emulatedLat, this.emulatedLon),
            zoom: 17,
            layers: [this.baseLayer]
        });
    },
    
    setView: function (lat, lon) {
        "use strict";
        this.map.panTo(new L.LatLng(lat, lon));
    },
    
    popups: [],
    addPopup: function (position, html) {
        "use strict";
        var icon = L.icon({
            iconUrl: 'img/marker_blue.png',
            iconSize: [25, 38],
            iconAnchor: [12, 38]
        }),
            marker = L.marker([position.lat, position.lon], {icon: icon}).addTo(this.map);
        
        marker.bindPopup(html);
        this.popups.push(marker);
    },
    
    removePopups: function () {
        "use strict";
        var i;
        for (i = 0; i < this.popups.length; i++) {
            this.map.removeLayer(this.popups[i]);
        }
        this.popups = [];
    },
    
    locationMarker: null,
    setLocationMarker: function (lat, lon) {
        "use strict";
        alert('aa');
        var icon = L.icon({
            iconUrl: 'img/marker_red.png',
            iconSize: [25, 38],
            iconAnchor: [12, 38]
        });
        
        if (map.locationMarker) {
            map.map.removeLayer(this.locationMarker);
        }
        map.locationMarker = L.marker([lat, lon], {icon: icon}).addTo(this.map);
    }
    
    
};