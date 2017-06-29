var idt = idt || {};

idt.specify_select = function() {
    var url = document.getElementById('specify').dataset.url;
    $.ajax({
        type: "GET",
        url: url
    }).done(function(response) {
        $('#form-panel').html(response);
    });
};

idt.calculate_select = function() {
    var url = document.getElementById('calculate').dataset.url;
    $.ajax({
        type: "GET",
        url: url
    }).done(function(response) {
        $('#form-panel').html(response);
    });
};

idt.calculate_window = function() {
    var test = $("#id_test").val();
    if (test) {
        var params = { test_id : test };
        var url = document.getElementById('test_window').dataset.url;

        $.ajax({
            type: "GET",
            url: url,
            data: params
        }).done(function(response) {
            $("#window").removeClass("hidden");
            $('#window_value').text(response.window);
        });
    }
    else {
        $("#window").addClass("hidden");
    }
};
