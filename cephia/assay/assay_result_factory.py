from assay.models import *

class AssayResultFactory(object):

    def __init__(self, assay_result_id):
        if assay_result.assay.name == 'LAg-Sedia':
            self.results = LagSediaResult.objects.filter(assay_result__pk=assay_result_id)
        elif assay_result.assay.name == 'LAg-Maxim':
            self.results = LagMaximResult.objects.filter(assay_result__pk=assay_result_id)
        elif assay_result.assay.name == 'ArchitectUnmodified':
            self.results = ArchitectUnmodifiedResult.objects.filter(assay_result__pk=assay_result_id)
        elif assay_result.assay.name == 'ArchitectAvidity':
            self.results = ArchitectAvidityResult.objects.filter(assay_result__pk=assay_result_id)
        elif assay_result.assay.name == 'BioRadAvidity-CDC':
            self.results = BioRadAvidityCDCResult.objects.filter(assay_result__pk=assay_result_id)
        elif assay_result.assay.name == 'BioRadAvidity-JHjU':
            self.results = BioRadAvidityJHUResult.objects.filter(assay_result__pk=assay_result_id)
        elif assay_result.assay.name == 'LSVitros-Diluent':
            self.results = LSVitrosDiluentResult.objects.filter(assay_result__pk=assay_result_id)
        elif assay_result.assay.name == 'LSVitros-Plasma':
            self.results = LSVitrosPlasmaResult.objects.filter(assay_result__pk=assay_result_id)
        elif assay_result.assay.name == 'Geenius':
            self.results = GeeniusResult.objects.filter(assay_result__pk=assay_result_id)
        elif assay_result.assay.name == 'BED':
            self.results = BEDResult.objects.filter(assay_result__pk=assay_result_id)
        elif assay_result.assay.name == 'BioRadAvidity-Glasgow':
            self.results = BioRadAvidityGlasgowResult.objects.filter(assay_result__pk=assay_result_id)
        elif assay_result.assay.name == 'BioPlex-CDC':
            self.results = BioPlexCDCResult.objects.filter(assay_result__pk=assay_result_id)
        elif assay_result.assay.name == 'IDE-iV3':
            self.results = IDEV3Result.objects.filter(assay_result__pk=assay_result_id)
        elif assay_result.assay.name == 'BioPlex-Duke':
            self.results = BioPlexDukeResult.objects.filter(assay_result__pk=assay_result_id)

    def get_results(self):
        return self.results

    def get_headers(self):
        import pdb; pdb.set_trace()
