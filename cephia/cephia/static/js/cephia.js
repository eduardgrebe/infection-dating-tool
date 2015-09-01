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
    event.preventDefault();
    var rowId = $(this).parent().data('row-id');
    var fileId = $(this).parent().data('file-id');
    var fileType = $(this).parent().data('file-type');
    var url = "/row_comment/" + fileType + '/' + String(fileId) + '/' + String(rowId);

    $.get(url, function(data, status) {
      var response = JSON.parse(data);
      if (status == "success") {
        $(".comment-modal").html(response.response);
        $( ".datepicker" ).datepicker();
        $("#myModal").modal();
      }
    })
  });
  //

  $( ".datepicker" ).datepicker();
});


