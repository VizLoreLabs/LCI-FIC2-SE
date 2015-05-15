/**
 * Created by dimitrije on 6.4.15..
 */

var algorithm = 'svm';
var feature_set = 'standard';
var uuid = '2';
var acceleration = [];
var gyroscope = [];
var min_timestamp;
var max_timestamp;
var query_number;
var start_ts;
var end_ts;

function set_algorithm(value) {
    algorithm = value;
}

function set_feature_set(value) {
    feature_set = value;
}

function handleAccelerationFileSelect(evt) {
    evt.stopPropagation();
    evt.preventDefault();

    var files;

    if (evt.dataTransfer != undefined)
        files = evt.dataTransfer.files;
    else
        files = evt.target.files;

    for (var i = 0, f; f = files[i]; i++) {
        var reader = new FileReader();
        reader.onload = function (progressEvent) {

            var lines = this.result.split('\n');
            var acc = [];

            for (var line = 0; line < lines.length - 1; line++) {
                var values = lines[line].split(',');
                acc.push({
                    timestamp: parseFloat(values[0]) / 1000000,
                    x: parseFloat(values[1]),
                    y: parseFloat(values[2]),
                    z: parseFloat(values[3])
                });
            }

            acceleration = acc;
        };
        document.getElementById('drop_zone_acc').innerHTML = files[i].name;
        reader.readAsText(f);
    }
}

function handleGyroscopeFileSelect(evt) {
    evt.stopPropagation();
    evt.preventDefault();

    var files;

    if (evt.dataTransfer != undefined)
        files = evt.dataTransfer.files;
    else
        files = evt.target.files;

    for (var i = 0, f; f = files[i]; i++) {
        var reader = new FileReader();
        reader.onload = function (progressEvent) {

            var lines = this.result.split('\n');
            var gyo = [];

            for (var line = 0; line < lines.length - 1; line++) {
                var values = lines[line].split(',');
                gyo.push({
                    timestamp: parseFloat(values[0]) / 1000000,
                    x: parseFloat(values[1]),
                    y: parseFloat(values[2]),
                    z: parseFloat(values[3])
                });
            }

            gyroscope = gyo;
        };
        document.getElementById('drop_zone_gyo').innerHTML = files[i].name;
        reader.readAsText(f);
    }
}

function get_next_acceleration_frame(index) {
    var frame = [];

    for (var i = index; i < acceleration.length; i++) {

        if (acceleration[i].timestamp - acceleration[index].timestamp < 2560) {
            frame.push(acceleration[i])
        }
        else {
            frame.push(acceleration[i]);
            break;
        }
    }

    return frame;
}

function get_next_gyroscope_frame(index) {
    var frame = [];

    for (var i = index; i < gyroscope.length; i++) {

        if (gyroscope[i].timestamp - gyroscope[index].timestamp < 2560) {
            frame.push(gyroscope[i])
        }
        else {
            frame.push(gyroscope[i]);
            break;
        }
    }

    return frame;
}

function process_data() {
    var acceleration_frames = [];
    var i = 0;
    var frame;

    query_number = 0;

    while (i < acceleration.length) {
        frame = get_next_acceleration_frame(i);
        i += frame.length;
        acceleration_frames.push(frame);
    }

    var gyroscope_frames = [];
    i = 0;

    while (i < gyroscope.length) {
        frame = get_next_gyroscope_frame(i);
        i += frame.length;
        gyroscope_frames.push(frame);
    }

    if (gyroscope_frames.length > 0) {
        var max_size = Math.min(acceleration_frames.length, gyroscope_frames.length);

        for (i = 0; i < max_size; i++) {
            do_post(acceleration_frames[i], gyroscope_frames[i]);
            document.getElementById('output').innerHTML = ((query_number * 100) / max_size).toString() + "% complete";
        }

        min_timestamp = Math.max(acceleration[0].timestamp, gyroscope[0].timestamp);
        max_timestamp = Math.min(acceleration[acceleration.length - 1].timestamp,
            gyroscope[acceleration.length - 1].timestamp);
    }
    else {
        for (i = 0; i < acceleration_frames.length; i++) {
            do_post(acceleration_frames[i], []);
            document.getElementById('output').innerHTML =
                ((query_number * 100) / acceleration_frames.length).toString() + "% complete";
        }

        min_timestamp = acceleration[0].timestamp;
        max_timestamp = acceleration[acceleration.length - 1].timestamp;
    }

    $("#slider-range").slider({
        range: true,
        min: min_timestamp,
        max: max_timestamp,
        values: [min_timestamp, max_timestamp],
        slide: function (event, ui) {
            start_ts = Math.round(ui.values[0]);
            end_ts = Math.round(ui.values[1]);
            $("#start_ts").val(Math.round(ui.values[0]));
            $("#end_ts").val(Math.round(ui.values[1]));
        }
    });

    $("#start_ts").val(Math.round(min_timestamp));
    $("#end_ts").val(Math.round(max_timestamp));

    document.getElementById('output').innerHTML = "Uploaded the data to the server for user: " + uuid +
    " Starting timestamp : " + min_timestamp.toString() + "ms" +
    " Ending timestamp : " + max_timestamp.toString() + "ms";
}

function recognise_activity() {
    var curr_act = document.getElementById("current_activity");

    if (start_ts == "" || end_ts == "") {
        start_ts = min_timestamp / 1000;
        end_ts = max_timestamp / 1000;
    }

    $.ajax({
        url: 'hac/',
        type: 'GET',
        data: 'uuid=' + uuid +
        '&alg=' + algorithm +
        '&fs=' + feature_set +
        '&curr_act=' + curr_act.checked +
        '&start_ts=' + start_ts +
        '&end_ts=' + end_ts,
        async: false,
        complete: function (result) {
            if (result.status == 0) {
                alert('0 status - browser could be on offline mode');
            } else if (result.status == 404) {
                alert('404 - not found');
            } else {
                document.getElementById('list').innerHTML += '<ul>' + result.responseText + '</ul>';
            }
        }
    });
}

function do_post(acceleration, gyroscope) {

    var location = [
        {timestamp: 423611596321, coords: {latitude: 44.802416, longitude: 20.465601}},
        {timestamp: 423611595214, coords: {latitude: 44.802416, longitude: 20.465601}}
    ];

    var wifi = [
        {ssids: ["Ninja", "Turtle"], timestamp: 423611596321},
        {ssids: ["Ninja2", "Turtle"], timestamp: 423611595214}
    ];

    var data = {uuid: uuid, acceleration: acceleration, gyroscope: gyroscope, location: location, wifi: wifi};
    $.ajax(
        {
            url: 'hac/',
            type: 'POST',
            processData: false,
            contentType: 'application/json; charset=utf-8',
            data: JSON.stringify(data),
            dataType: 'json',
            async: false,
            complete: function (result) {
                if (result.status == 0) {
                    alert('0 status - browser could be on offline mode');
                } else if (result.status == 404) {
                    alert('404 - not found');
                } else {
                    query_number += 1;
                }
            }
        });
}

function handleDragOver(evt) {
    evt.stopPropagation();
    evt.preventDefault();
    evt.dataTransfer.dropEffect = 'copy'; // Explicitly show this is a copy.
}


function displayAccelerationFileSelect() {
    document.getElementById('file_acc').click();
}

function displayGyroscopeFileSelect() {
    document.getElementById('file_gyo').click();
}

var dropZoneAcc = document.getElementById('drop_zone_acc');
dropZoneAcc.addEventListener('dragover', handleDragOver, false);
dropZoneAcc.addEventListener('drop', handleAccelerationFileSelect, false);
dropZoneAcc.addEventListener('click', displayAccelerationFileSelect);

var dropZoneGyo = document.getElementById('drop_zone_gyo');
dropZoneGyo.addEventListener('dragover', handleDragOver, false);
dropZoneGyo.addEventListener('drop', handleGyroscopeFileSelect, false);
dropZoneGyo.addEventListener('click', displayGyroscopeFileSelect);

document.getElementById('file_acc').addEventListener('change', handleAccelerationFileSelect, false);
document.getElementById('file_gyo').addEventListener('change', handleGyroscopeFileSelect, false);

var submitButton = document.getElementById('submit_button');
submitButton.addEventListener("click", process_data);

var activityButton = document.getElementById('activity_button');
activityButton.addEventListener("click", recognise_activity);