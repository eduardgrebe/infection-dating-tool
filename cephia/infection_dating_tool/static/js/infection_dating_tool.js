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
