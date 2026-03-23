var idt = idt || {};

idt.specify_select = function() {
    var url = document.getElementById('specify').dataset.url;
    $.ajax({
        type: "GET",
        url: url
    }).done(function(response) {
        $('#form-estimates-panel').html(response);
    });
};

idt.calculate_select = function() {
    var url = document.getElementById('calculate').dataset.url;
    $.ajax({
        type: "GET",
        url: url
    }).done(function(response) {
        $('#form-estimates-panel').html(response);
    });
};

idt.estimates_select = function() {
    var url = document.getElementById('estimates').dataset.url;
    $.ajax({
        type: "GET",
        url: url
    }).done(function(response) {
        $('#form-panel').html(response);
    });
};

idt.data_select = function() {
    var url = document.getElementById('data').dataset.url;
    $.ajax({
        type: "GET",
        url: url
    }).done(function(response) {
        $('#form-panel').html(response);
    });
};

idt.supply_select = function() {
    var url = document.getElementById('supply').dataset.url;
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
            $('#window_value').text(response.window + ' days');
        });
    }
    else {
        $("#window").addClass("hidden");
    }
};

idt.update_form = function(category) {
     if (category === 'viral_load') {
         $("input[id$='diagnostic_delay']").attr('readonly', true);
         $("input[id$='diagnostic_delay']").hide();
         $("input[id$='detection_threshold']").attr('readonly', false);
         $("div[id$='_vl_dd']").show();
     } else if (category === '') {
         $("input[id$='diagnostic_delay']").attr('readonly', true);
         $("input[id$='diagnostic_delay']").show();
         $("input[id$='detection_threshold']").attr('readonly', true);
         $("div[id$='_vl_dd']").hide();
     } else {
         $("input[id$='diagnostic_delay']").attr('readonly', false);
         $("input[id$='diagnostic_delay']").show();
         $("input[id$='detection_threshold']").attr('readonly', true);
         $("div[id$='_vl_dd']").hide();
     }
};

idt.check_category = function() {
    var category = $('#id_category').val();
    idt.update_form(category);
};

idt.calculate_nums = function(growth_rate) {
    var inputs = document.querySelectorAll("input[id$='detection_threshold']");
    for (var i = 0, len = inputs.length; i < len; i++) {
        var name = inputs[i].name;
        var value = inputs[i].value;
        if (value) {
            var log10_value = log10(value);
            function log10(val) {
                return Math.log(val) / Math.LN10;
            }
            var vl_dd = log10_value / growth_rate;
            var vl_dd_name = '#' + name + '_vl_dd';
            $(vl_dd_name).text("(" + vl_dd.toFixed(2) + ")");
        }
    }
};

idt.GetElementInsideContainer = function(containerID, childID) {
    var elm = document.getElementById(childID);
    var parent = elm ? elm.parentNode : {};
    return (parent.id && parent.id === containerID) ? elm : {};
};


idt.update_form = function(category) {
    if (category === 'viral_load') {
        $("input[id$='diagnostic_delay']").attr('readonly', true);
        $("input[id$='diagnostic_delay']").hide();
        $("input[id$='detection_threshold']").attr('readonly', false);
        $("div[id$='_vl_dd']").show();
    } else if (category === '') {
        $("input[id$='diagnostic_delay']").attr('readonly', true);
        $("input[id$='diagnostic_delay']").show();
        $("input[id$='detection_threshold']").attr('readonly', true);
        $("div[id$='_vl_dd']").hide();
    } else {
        $("input[id$='diagnostic_delay']").attr('readonly', false);
        $("input[id$='diagnostic_delay']").show();
        $("input[id$='detection_threshold']").attr('readonly', true);
        $("div[id$='_vl_dd']").hide();
    }
};

idt.check_category = function() {
    var category = $('#id_category').val();
    idt.update_form(category);
};


idt.calculate_nums = function(growth_rate) {
    var inputs = document.querySelectorAll("input[id$='detection_threshold']");
    for (var i = 0, len = inputs.length; i < len; i++) {
        var name = inputs[i].name;
        var value = inputs[i].value;
        if (value) {
            idt.calculate_num(name, value, growth_rate);
        }
    }
};

idt.calculate_num = function(name, value, growth_rate) {
    var log10_value = log10(value);
    function log10(val) {
        return Math.log(val) / Math.LN10;
    }
    var vl_dd = log10_value / growth_rate;
    var vl_dd_name = '#' + name + '_vl_dd';
    $(vl_dd_name).text("(" + vl_dd.toFixed(2) + ")");
};
