$(document).ready(function() {
    $('.alert').fadeOut(4000);

    $('button[type="submit"').attr('disabled', 'disabled');

    $('#id_data_file').on('change', function() {
        if ($('#id_file_type').val() != "") {
            $('button[type="submit"]').removeAttr('disabled');
        }
    });

    $('#id_file_type').on('change', function() {
        if ($('#id_data_file').val() != "") {
            $('button[type="submit"]').removeAttr('disabled');
        }
    });

});


