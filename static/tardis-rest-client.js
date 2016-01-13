(function() {

var showChannels = function(data, textStatus, jqXHR) {
    var table = $('#dataTable');
    table.text('');
    for (var channel in data) {
        var row = $('<tr><td>'+channel+'</td></tr>');

        if (channel == 'obstacles') {
            row.append(
                '<td>Position :<br>' +
                'x = ' + data[channel][0] + '<br>' +
                'y = ' + data[channel][1] + '</td>'
            );
        }
        else if (channel == 'new_pos') {
            row.append(
                '<td>Position :<br>' +
                'x = ' + data[channel][0] + '<br>' +
                'y = ' + data[channel][1] + '<br>' +
                'Angle : ' + data[channel][2] + '</td>'
            );
        }
        else if (channel == 'mesured_pos') {
            row.append(
                '<td>Position :<br>' +
                'x = ' + data[channel][0] + '<br>' +
                'y = ' + data[channel][1] + '<br>' +
                'Angle : ' + data[channel][2] + '</td>'
            );
        }
        table.append(row);
    }
};

var showError = function(jqXHR, textStatus, errorThrown) {

};

var sendGET = function(channel) {
    var requestURL = "/channels";
    if (channel !== undefined) {
        requestURL += "/" + channel;
    }

    $.ajax({
        type: 'GET',
        url: requestURL,
        dataType: "json",
        success: showChannels,
        error: showError
    });
};

var init = function() {
    // Activating Bootstrap tooltips
    $('[data-toggle="tooltip"]').tooltip();

    // Refresh button
    $('#btnRefreshAll').click(function(event) {
        event.preventDefault();
        sendGET();
    });

    // Loads the initial data
    sendGET();
};

init();

})();
