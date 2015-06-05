$(document).ready(function(){
    $('[data-toggle="tooltip"]').tooltip();

    if ($('#messages').text().trim() != '') {
	$('#messageModal').modal('show');
    }
});
