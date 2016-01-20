(function() {

// Updates the data table that shows the channels and their value
var showChannels = function(data) {
    for (var c in data) {
        var valuesCell = $('#' + c + ' > td').last();
        channels[c].showValues(valuesCell, data[c]);
    }
};

// Shows an error message
var showError = function() {
    $('#channelTable').before(
        '<div class="alert alert-danger alert-dismissible fade in" role="alert">' +
            '<button class="close" aria-label="Fermer" data-dismiss="alert" type="button">' +
                '<span aria-hidden="true">x</span>' +
            '</button>' +
            '<p>Une erreur est survenue ...</p>' +
        '</div>'
    );
};

// Send the AJAX GET request to get the channels data
var sendGET = function(channel) {
    var requestURL = '/channels';
    if (channel !== undefined) {
        requestURL += '/' + channel;
    }

    $.ajax({
        type: 'GET',
        url: requestURL,
        dataType: 'json',
        success: showChannels,
        error: showError
    });
};

// Send the AJAX POST request to upload data to a channel
var sendPOST = function(channel, values) {
    console.log(channel);
    console.log(values);

    var requestURL = '/channels/' + channel;
    $.ajax({
        type : 'POST',
        url : requestURL,
        dataType : 'json',
        data : JSON.stringify(values),
        contentType: "application/json; charset=utf-8",
        error : showError
    });
};

// Collection of channels handled by the application
var channels = {
    avoid_direction : {
        name : 'Vecteur d\'évitement',
        valuesForm :'<label>x : </label>' +
                    '<input type="text" name="x">' +
                    '<br>' +
                    '<label>y : </label>' +
                    '<input type="text" name="y">',
        valuesToObject : function(valuesContainer) {
            return {
                avoid_direction : [
                    parseInt(valuesContainer.find('input[name="x"]').val()) || 0,
                    parseInt(valuesContainer.find('input[name="y"]').val()) || 0
                ]
            };
        },
        showValues : function(valuesContainer, values) {
            valuesContainer.find('input[name="x"]').val(values[0]);
            valuesContainer.find('input[name="y"]').val(values[1]);
        }
    },

    ultrasonic : {
        name : 'Ultrasons',
        valuesForm :'<input type="text" name="0">' +
                    '<input type="text" name="1">' +
                    '<input type="text" name="2">' +
                    '<input type="text" name="3">' +
                    '<input type="text" name="4">' +
                    '<input type="text" name="5">' +
                    '<input type="text" name="6">' +
                    '<input type="text" name="7">' +
                    '<input type="text" name="8">' +
                    '<input type="text" name="9">' +
                    '<input type="text" name="10">' +
                    '<input type="text" name="11">',
        valuesToObject : function(valuesContainer) {
            return {
                ultrasonic: [
                    parseInt(valuesContainer.find('input[name="0"]').val()) || 0,
                    parseInt(valuesContainer.find('input[name="1"]').val()) || 0,
                    parseInt(valuesContainer.find('input[name="2"]').val()) || 0,
                    parseInt(valuesContainer.find('input[name="3"]').val()) || 0,
                    parseInt(valuesContainer.find('input[name="4"]').val()) || 0,
                    parseInt(valuesContainer.find('input[name="5"]').val()) || 0,
                    parseInt(valuesContainer.find('input[name="6"]').val()) || 0,
                    parseInt(valuesContainer.find('input[name="7"]').val()) || 0,
                    parseInt(valuesContainer.find('input[name="8"]').val()) || 0,
                    parseInt(valuesContainer.find('input[name="9"]').val()) || 0,
                    parseInt(valuesContainer.find('input[name="10"]').val()) || 0,
                    parseInt(valuesContainer.find('input[name="11"]').val()) || 0
                ]
            };
        },
        showValues : function(valuesContainer, values) {
            for (var i = 0; i < 12; i++) {
                valuesContainer.find('input[name="'+i+'"]').val(values[i]);
            }
        }
    },

    mesured_pos : {
        name : 'Position mesurée',
        valuesForm :'<label>x : </label>' +
                    '<input type="text" name="x">' +
                    '<br>' +
                    '<label>y : </label>' +
                    '<input type="text" name="y">' +
                    '<br>' +
                    '<label>Angle : </label>' +
                    '<input type="text" name="theta">',
        valuesToObject : function(valuesContainer) {
            return {
                mesured_pos : [
                    parseInt(valuesContainer.find('input[name="x"]').val()) || 0,
                    parseInt(valuesContainer.find('input[name="y"]').val()) || 0,
                    parseInt(valuesContainer.find('input[name="theta"]').val()) || 0
                ]
            };
        },
        showValues : function(valuesContainer, values) {
            valuesContainer.find('input[name="x"]').val(values[0]);
            valuesContainer.find('input[name="y"]').val(values[1]);
            valuesContainer.find('input[name="theta"]').val(values[2]);
        }
    },

    new_pos : {
        name : 'Nouvelle position',
        valuesForm :'<label>x : </label>' +
                    '<input type="text" name="x">' +
                    '<br>' +
                    '<label>y : </label>' +
                    '<input type="text" name="y">' +
                    '<br>' +
                    '<label>Angle : </label>' +
                    '<input type="text" name="theta">',
        valuesToObject : function(valuesContainer) {
            return {
                new_pos : [
                    parseInt(valuesContainer.find('input[name="x"]').val()) || 0,
                    parseInt(valuesContainer.find('input[name="y"]').val()) || 0,
                    parseInt(valuesContainer.find('input[name="theta"]').val()) || 0
                ]
            };
        },
        showValues : function(valuesContainer, values) {
            valuesContainer.find('input[name="x"]').val(values[0]);
            valuesContainer.find('input[name="y"]').val(values[1]);
            valuesContainer.find('input[name="theta"]').val(values[2]);
        }
    }
};

// Creates the rows of the channel table based on the channel collection
var initChannelTable = function() {
    var table = $('#channelTable > tbody');
    for (channel in channels) {
        (function(c) { // Closure

            var row = $('<tr id="' + c + '"><td>' + channels[c].name + '</td></tr>');
            var valuesCell = $('<td></td>');
            var uploadButton = $('<button class="btn btn-default btn-lg pull-right"><span class="glyphicon glyphicon-upload"></span></button>');
            uploadButton.click(function() {
                sendPOST(c, channels[c].valuesToObject($(this).parent()));
            });
            valuesCell.append(uploadButton);
            valuesCell.append(channels[c].valuesForm);
            row.append(valuesCell);
            table.append(row);

        })(channel);
    }
};

// Initialize the application
var init = function() {
    // Activating Bootstrap tooltips
    $('[data-toggle="tooltip"]').tooltip();

    // Refresh button
    $('#btnRefreshAll').click(function(event) {
        event.preventDefault();
        sendGET();
    });

    // Initialize the channel table
    initChannelTable();

    // Loads the initial data
    sendGET();
};

init();

})();
