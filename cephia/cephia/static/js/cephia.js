$(document).ready(function(){
    if ($('#messages').text().trim() != '') {
	$('#messageModal').modal('show');
    }
});
