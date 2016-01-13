(function() {

var showChannels = function(data, textStatus, jqXHR) {
    var table = $('#dataTable');
    console.log(data);
};

var showError = function(jqXHR, textStatus, errorThrown) {

};

var sendGET = function(channel) {
    var requestURL = "/channels";
    if (channel) {
        requestURL += "/" + channel;
    }

    $.GET({
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
    $('#btnRefreshAll').click(sendGET);
};

init();

})();
