var idt = idt || {};

idt.specify_select = function() {
    var params = { form : 'specify' };
    var url = document.getElementById('specify').dataset.url;
    $.ajax({
        type: "GET",
        url: url,
        data: params
    }).done(function(response) {
        $('#form-panel').html(response);
    });
};

idt.calculate_select = function() {
    var params = { form : 'calculate' };
    var url = document.getElementById('calculate').dataset.url;
    $.ajax({
        type: "GET",
        url: url,
        data: params
    }).done(function(response) {
        $('#form-panel').html(response);
    });
};
