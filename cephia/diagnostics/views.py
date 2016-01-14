from django.shortcuts import render

# Create your views here.



@csrf_exempt
@login_required
def eddi_report(request, template="diagnostics/eddi_report.html"):
    context = {}

    if visit_ids and subject_ids:
        specimens = Specimen.objects.filter(Q(visit__id__in=visit_ids) | Q(subject__id__in=subject_ids))
    elif subject_ids and not visit_ids:
        specimens = Specimen.objects.filter(subject__id__in=subject_ids)
    elif visit_ids and not subject_ids:
        specimens = Specimen.objects.filter(visit__id__in=visit_ids)
    else:
        specimens = None

        Subject ref
        EDDIMin
        EDDIMax
        EDDIMidPointEstimate
        Completeness (one of [ PosAndNeg, OnlyPos, OnlyNeg ] )

    context['specimens'] = specimens
    response = render_to_response(template, context, context_instance=RequestContext(request))
    return response
