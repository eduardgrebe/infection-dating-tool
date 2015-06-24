from django.http import HttpResponse
import csv

def _response_for_data_download(request, data, filename, mimetype=None):
    if mimetype is None:
        mimetype = 'application/octet-stream'
    if data is None:
        response = HttpResponse(content_type=mimetype)
    else:
        response = HttpResponse(data, content_type=mimetype)
        content_disposition = 'attachment; filename=%s' % (filename)
        response['Content-Disposition'] = content_disposition

    return response

def get_csv_response(filename_to_show_in_download_box):
    response = _response_for_data_download(request=None, data=None,
                                           filename=filename_to_show_in_download_box, mimetype='text/csv')
    return response, csv.writer(response)
