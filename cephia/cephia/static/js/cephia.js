$(document).ready(function(){

    toggleUploadButton: function(ev) {
	if ($('#id_data_file').val() != "" && $('#id_file_type').val() != "") {
	    $('.upload-btn').disable(false);
	}
    }
    
    $('#id_data_file').change(function() {
	debugger;
	toggleUploadButton();
    });

    $('#id_file_type').change(function() {
	debugger;
	toggleUploadButton();
    });
});
