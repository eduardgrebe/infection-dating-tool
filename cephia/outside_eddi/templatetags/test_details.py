# from django.template import Library
# from outside_eddi.models import OutsideEddiDiagnosticTest

# register = Library()

# @register.simple_tag
# def test_details(test_id):
#     details = ''
#     if test_id:
#         test = OutsideEddiDiagnosticTest.objects.filter(id = test_id).first()
#         details = test.description
#     return details

