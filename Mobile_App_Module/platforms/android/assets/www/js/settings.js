/*global $*/

var settings = {
    // Settings widgets
    settings_popup: null,
    confirm_button: null,
    restore_button: null,
    
    acr_textbox: null,
    rmp_textbox: null,
    sending_toggle: null,
    
    // Settings default values
    acr_url_default: "http://89.216.30.67:8089",
    rmp_url_default: "http://89.216.30.67:4545",
    sending_default: "on",
    
    // Settings values
    acr_url: null,
    rmp_url: null,
    sending: null,
    
    init: function () {
        "use strict";
        this.settings_popup = $("#settings_popup");
        this.confirm_button = $("#confirm");
        this.restore_button = $("#restore");

        this.acr_textbox = $("#acr_url");
        this.rmp_textbox = $("#rmp_url");
        this.sending_toggle = $("#sending_data");
        
        this.acr_url = window.localStorage.getItem("acr_url") || settings.acr_url_default;
        this.rmp_url = window.localStorage.getItem("rmp_url") || settings.rmp_url_default;
        this.sending = window.localStorage.getItem("sending") || settings.sending_default;

        this.settings_popup.on("popupafteropen", function () {
            settings.refreshForm();
        });
        
        this.confirm_button.click(function () {
            settings.commitChanges();
            settings.settings_popup.popup("close");
        });
        
        this.restore_button.click(function () {
            settings.acr_textbox.val(settings.acr_url_default);
            settings.rmp_textbox.val(settings.rmp_url_default);
            settings.sending_toggle.val(settings.sending_default).flipswitch("refresh");
            settings.commitChanges();
        });
        
    },
    
    refreshForm: function () {
        "use strict";
        this.acr_textbox.val(settings.acr_url);
        this.rmp_textbox.val(settings.rmp_url);
        this.sending_toggle.val(settings.sending).flipswitch("refresh");
    },
    
    commitChanges: function () {
        "use strict";
        this.acr_url = this.acr_textbox.val();
        this.rmp_url = this.rmp_textbox.val();
        this.sending = this.sending_toggle.val();

        window.localStorage.setItem("acr_url", this.acr_url);
        window.localStorage.setItem("rmp_url", this.rmp_url);
        window.localStorage.setItem("sending", this.sending);
    }
};