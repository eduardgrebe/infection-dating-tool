$(document).ready(function() {
    //remove alerts after certain amount of time
    $('.alert').fadeOut(10000);
    $( ".datepicker" ).datepicker({ dateFormat: 'yy-mm-dd' });
    $('div.upload-assay').hide();
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
    //COMMENT MOODAL CALL
    $('.btn-comment-modal').on('click', function(event) {
        event.preventDefault();
        var rowId = $(this).parent().data('row-id');
        var fileId = $(this).parent().data('file-id');
        var fileType = $(this).parent().data('file-type');
        var url = "/row_comment/" + fileType + '/' + String(fileId) + '/' + String(rowId);

        $.get(url, function(data, status) {
            var response = JSON.parse(data);
            if (status == "success") {
                $(".comment-modal").html(response.response);
                $( ".datepicker" ).datepicker({ dateFormat: 'yy-mm-dd' });
                $("#myModal").modal();
            }
        })
    });
    //
    //RESULT FILE MODAL CALL
    $('.btn-result-file-modal').on('click', function(event) {
        event.preventDefault();
        var panelId = $(this).parent().data('panel-id');
        var url = "/assay/result_file_upload/" + String(panelId);

        $.get(url, function(data, status) {
            var response = JSON.parse(data);
            if (status == "success") {
                $(".result-modal").html(response.response);
                $("#resultModal").modal();
            }
        })
    });


    //MEMBERSHIP FILE MODAL CALL
    $('.btn-membership-file-modal').on('click', function(event) {
        event.preventDefault();
        var panelId = $(this).parent().data('panel-id');
        var url = "/assay/membership_file_upload/" + String(panelId);

        $.get(url, function(data, status) {
            var response = JSON.parse(data);
            if (status == "success") {
                $(".membership-modal").html(response.response);
                $("#membershipModal").modal();
            }
        })
    });
    //SHIPMENT FILE MODAL CALL
    $('.btn-shipment-file-modal').on('click', function(event) {
        event.preventDefault();
        var panelId = $(this).parent().data('panel-id');
        var url = "/assay/shipment_file_upload/" + String(panelId);

        $.get(url, function(data, status) {
            var response = JSON.parse(data);
            if (status == "success") {
                $(".shipment-modal").html(response.response);
                $("#shipmentModal").modal();
            }
        })
    });
    //MAKE CURRENT NAV TAB ACTIVE
    $('.navtab').on('click', function(event) {
        $(this).addClass('active');
    });

    $('input[name="visit"]').on('click', function(event) {
        var artificialButton = $(this).parents().eq(9).find('input[name="artificial"]');
        var confirmButton = $(this).parents().eq(9).find('input[name="confirm"]');
        var provisionalButton = $(this).parents().eq(9).find('input[name="provisional"]');
        var selectedSpecimen = $('input[name="specimen"].selected');

        $('input[name="visit"].selected').removeClass('selected');
        $(this).addClass('selected');

        if (selectedSpecimen.length > 0) {
            provisionalButton.show();
        }
    });

    $('input[name="specimen"]').on('click', function(event) {
        var artificialButton = $(this).parents().eq(9).find('input[name="artificial"]');
        var confirmButton = $(this).parents().eq(9).find('input[name="confirm"]');
        var provisionalButton = $(this).parents().eq(9).find('input[name="provisional"]');
        var selectedVisit = $('input[name="visit"].selected');
        
        $('input[name="specimen"].selected').removeClass('selected');
        $(this).addClass('selected');
        artificialButton.show();

        if (selectedVisit.length > 0) {
            provisionalButton.show();
        }
    });
    //AJAX CALL TO SHOW SPECIMEN DETAIL ON REPORT
    $('a.show-specimen').on('click', function(event) {
        event.preventDefault();

        var url = "/reports/visit_specimen_report/";
        var post_data = $('#specimen-form').serializeArray();

        $.post(url, post_data, function(data, status) {
            var response = JSON.parse(data);

            if (status == "success") {
                $(".specimens-modal").html(response.response);
                $("#specimenModal").modal();
            }
        });
    });

    $('a.view-specific-results').on('click', function(event) {
        getSpecificAssayResults();
    });

    //SHOW AND HIDE ASSAY TYPE DROPDOWN ON FILE UPLOAD
    $('div.upload-file-type select').on('change', function(event) {
        var fileType = $('div.upload-file-type select option:selected').val();

        if (fileType == 'assay') {
            $('div.upload-assay').show();
        } else {
            $('div.upload-assay').hide();
        }
    });
    //

    $('a.show-eddi-detail').on('click', function(event) {
        event.preventDefault();
        var subjectId = $(this).parent().parent().data('subject-id');
        var url = "/diagnostics/eddi_report_detail/" + String(subjectId);
        
        $.get(url, function(data, status) {
            var response = JSON.parse(data);

            if (status == "success") {
                $(".eddi-modal-container").html(response.response);
                $('.status-message').hide();
                $("#eddiModal").modal();
                $('a.eddi-status-update').on('click', function(event) {
                    event.preventDefault();
                    var $form = $('#eddi-status-form');
                    var subjectId = $form.data('subject-id');
                    var url = "/diagnostics/eddi_report_detail/" + String(subjectId) + "/";
                    var post_data = $form.serializeArray();
                    
                    $.post(url, post_data, function(data, status) {
                        if (status == "success") {
                            $('.status-message').show();
                            $('.status-message').text("Status successfully changed");
                            $('.status-message').fadeOut(2000);
                        }
                    });
                });
            }
        });
    });
});
//
function submitFilterFormCSV() {
    $('<input />').attr('type', 'hidden')
        .attr('name', "csv")
        .attr('value', "1")
        .appendTo('.filter-form');
    $(".filter-form").submit();
    return true;
};

function getSpecificAssayResults() {
    debugger;
    event.preventDefault();
    var resultId = $(this).parent().data('result-id');
    var url = "/assay/specific_results/" + String(resultId);

    $.get(url, function(data, status) {
        var response = JSON.parse(data);
        if (status == "success") {
            $(".result-modal-container").html(response.response);
            $("#resultModal").modal();
        }
    });
};
//
// function confirmResultFileUpload() {
//     var $resultFileModal = $(event.target).closest(".modal");
//     var file = $resultFileModal.find("input[type='file']").val();
//     var assay = $($resultFileModal.find("select option:selected")[0]).text()
//     var lab = $($resultFileModal.find("select option:selected")[1]).text()
//     $resultFileModal.modal('hide');
//     debugger;
//     //$("#confirmModal").modal();
// };
//
