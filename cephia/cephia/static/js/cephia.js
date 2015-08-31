$(document).ready(function() {
    //remove alerts after certain amount of time
    $('.alert').fadeOut(4000);

    //initially disable upload file button
    //$('.upload-btn').attr('disabled', 'disabled');

    //enable and disable the upload file button
    $('#id_data_file').on('change', function() {
        if ($('#id_file_type').val() != "") {
            $('.upload-btn').removeAttr('disabled');
        }
    });

    $('#id_file_type').on('change', function() {
        if ($('#id_data_file').val() != "") {
            $('.upload-btn').removeAttr('disabled');
        }
    });
    //

    $('.btn-comment-modal').on('click', function(event) {
        var targetData = $(event.target).parent().data();
        var rowId = targetData.rowId;
        var fileId = targetData.fileId;
        var fileType = targetData.fileType;
        var url = "/row_comment/" + fileType + '/' + String(fileId) + '/' + String(rowId);

        $.get(url, function(data, status) {
            console.log("in get callback");
            debugger;
        })
    });
    //
    $( ".datepicker" ).datepicker();
});


