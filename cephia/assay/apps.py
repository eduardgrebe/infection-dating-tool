from django.apps import AppConfig


class AssayConfig(AppConfig):
    name = 'assay'
    verbose_name = "Assay"

    def ready(self):
        from assay_result_factory import *
        from models import *

        register_result(ArchitectAvidityResult, 'ArchitectAvidity')
        register_result(ArchitectUnmodifiedResult, 'ArchitectUnmodified')
        register_result(BEDResult, 'BED')
        register_result(BioRadAvidityCDCResult, 'BioRadAvidity-CDC')
        register_result(BioRadAvidityGlasgowResult, 'BioRadAvidity-Glasgow')
        register_result(BioRadAvidityJHUResult, 'BioRadAvidity-JHU')
        register_result(GeeniusResult, 'Geenius')
        register_result(IDEV3Result, 'IDE-V3')
        register_result(LagMaximResult, 'LAg-Maxim')
        register_result(LagSediaResult, 'LAg-Sedia')
        register_result(LSVitrosDiluentResult, 'LSVitros-Diluent')
        register_result(LSVitrosPlasmaResult, 'LSVitros-Plasma')
        register_result(LuminexCDCResult, 'BioPlex-CDC')
        register_result(VitrosAvidityResult, 'Vitros')
