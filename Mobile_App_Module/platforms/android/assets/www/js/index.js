/*
 * Licensed to the Apache Software Foundation (ASF) under one
 * or more contributor license agreements.  See the NOTICE file
 * distributed with this work for additional information
 * regarding copyright ownership.  The ASF licenses this file
 * to you under the Apache License, Version 2.0 (the
 * "License"); you may not use this file except in compliance
 * with the License.  You may obtain a copy of the License at
 *
 * http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing,
 * software distributed under the License is distributed on an
 * "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
 * KIND, either express or implied.  See the License for the
 * specific language governing permissions and limitations
 * under the License.
 */

/*global settings*/
/*global sensors*/
/*global map*/
/*global POIs*/
/*global console*/
/*global $*/
/*global alert*/

var app = {
    // Application Constructor
    initialize: function () {
        "use strict";
        this.bindEvents();
    },
    
    // Bind Event Listeners
    bindEvents: function () {
        "use strict";
        document.addEventListener('deviceready', this.onDeviceReady, false);
    },
    
    // deviceready Event Handler
    onDeviceReady: function () {
        "use strict";
        app.receivedEvent('deviceready');

        //navigator.splashscreen.show();
        settings.init();
        sensors.init();
        map.init();
        POIs.init();
    },
    
    // Log on a Received Event
    receivedEvent: function (id) {
        "use strict";
        console.log('Received Event: ' + id);
    }
};
