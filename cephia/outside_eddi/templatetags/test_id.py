# from django.template import Library
# from outside_eddi.models import OutsideEddiDiagnosticTest

# register = Library()

# @register.simple_tag
# def test_id(test_name):
#     if test_name:
#         test = OutsideEddiDiagnosticTest.objects.filter(name=test_name).first()
#         test_id = test.pk
#     else:
#         test_id = 0
#     return test_id
