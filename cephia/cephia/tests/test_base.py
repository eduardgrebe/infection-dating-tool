 # -*- coding: utf-8 -*-
from django.test import TestCase
import logging
from cephia.models import *
from cephia.file_handlers.file_handler_register import *
from django.core.files import File

logger = logging.getLogger(__name__)

class TestHelper(object):
    """ Put helper functions that all tests can use in this class """

    def __init__(self, *args, **kwargs):
        super(TestHelper, self).__init__(*args, **kwargs)

    def get_file(self, file_name, case_name):
        return File(open(settings.TEST_FILES_ROOT + case_name + '/' + file_name))
    
    def create_fileinfo(self, file_name, case_name):
        file_info = self.get_file(file_name, case_name)
        return FileInfo.objects.create(data_file=file_info,
                                       file_type=file_name.split('.')[0],
                                       state='pending')

    def create_admin_user(self, username="admin", password="password"):
        user = CephiaUser.objects.get_or_create(username=username, first_name='adminfirst', last_name='adminlast', is_superuser=True)[0]
        user.set_password(password)
        user.save()
        return user


    def create_ethnicities(self):
        Ethnicity.objects.get_or_create(name='Hispanic/Latino')
        Ethnicity.objects.get_or_create(name='Black African')
        Ethnicity.objects.get_or_create(name='Brazilian')
        Ethnicity.objects.get_or_create(name='Multiethnic')
        Ethnicity.objects.get_or_create(name='African American')
        Ethnicity.objects.get_or_create(name='White')
        Ethnicity.objects.get_or_create(name='Other')
        Ethnicity.objects.get_or_create(name='Unknown')
        Ethnicity.objects.get_or_create(name='Asian')

    def create_countries(self):
        region = Region.objects.get_or_create(name='default')
        Country.objects.get_or_create(code='WF', name="Wallis and Futuna", region_id=1)
        Country.objects.get_or_create(code="JP", name="Japan", region_id=1)
        Country.objects.get_or_create(code="JM", name="Jamaica", region_id=1)
        Country.objects.get_or_create(code="JO", name="Jordan", region_id=1)
        Country.objects.get_or_create(code="WS", name="Samoa", region_id=1)
        Country.objects.get_or_create(code="JE", name="Jersey", region_id=1)
        Country.objects.get_or_create(code="GW", name="Guinea", region_id=1)
        Country.objects.get_or_create(code="GU", name="Guam", region_id=1)
        Country.objects.get_or_create(code="GT", name="Guatemala", region_id=1)
        Country.objects.get_or_create(code="GS", name="South", region_id=1)
        Country.objects.get_or_create(code="GR", name="Greece", region_id=1)
        Country.objects.get_or_create(code="GQ", name="Equatorial", region_id=1)
        Country.objects.get_or_create(code="GP", name="Guadeloupe", region_id=1)
        Country.objects.get_or_create(code="GY", name="Guyana", region_id=1)
        Country.objects.get_or_create(code="GG", name="Guernsey", region_id=1)
        Country.objects.get_or_create(code="GF", name="French", region_id=1)
        Country.objects.get_or_create(code="GE", name="Georgia", region_id=1)
        Country.objects.get_or_create(code="GD", name="Grenada", region_id=1)
        Country.objects.get_or_create(code="GB", name="United", region_id=1)
        Country.objects.get_or_create(code="GA", name="Gabon", region_id=1)
        Country.objects.get_or_create(code="GN", name="Guinea", region_id=1)
        Country.objects.get_or_create(code="GM", name="Gambia", region_id=1)
        Country.objects.get_or_create(code="GL", name="Greenland", region_id=1)
        Country.objects.get_or_create(code="GI", name="Gibraltar", region_id=1)
        Country.objects.get_or_create(code="GH", name="Ghana", region_id=1)
        Country.objects.get_or_create(code="PR", name="Puerto", region_id=1)
        Country.objects.get_or_create(code="PS", name="Palestine", region_id=1)
        Country.objects.get_or_create(code="PW", name="Palau", region_id=1)
        Country.objects.get_or_create(code="PT", name="Portugal", region_id=1)
        Country.objects.get_or_create(code="PY", name="Paraguay", region_id=1)
        Country.objects.get_or_create(code="PA", name="Panama", region_id=1)
        Country.objects.get_or_create(code="PF", name="French", region_id=1)
        Country.objects.get_or_create(code="PG", name="Papua", region_id=1)
        Country.objects.get_or_create(code="PE", name="Peru", region_id=1)
        Country.objects.get_or_create(code="PK", name="Pakistan", region_id=1)
        Country.objects.get_or_create(code="PH", name="Philippines", region_id=1)
        Country.objects.get_or_create(code="PN", name="Pitcairn", region_id=1)
        Country.objects.get_or_create(code="PL", name="Poland", region_id=1)
        Country.objects.get_or_create(code="PM", name="Saint", region_id=1)
        Country.objects.get_or_create(code="ZM", name="Zambia", region_id=1)
        Country.objects.get_or_create(code="ZA", name="South", region_id=1)
        Country.objects.get_or_create(code="ZW", name="Zimbabwe", region_id=1)
        Country.objects.get_or_create(code="ME", name="Montenegro", region_id=1)
        Country.objects.get_or_create(code="MD", name="Moldova", region_id=1)
        Country.objects.get_or_create(code="MG", name="Madagascar", region_id=1)
        Country.objects.get_or_create(code="MF", name="Saint", region_id=1)
        Country.objects.get_or_create(code="MA", name="Morocco", region_id=1)
        Country.objects.get_or_create(code="MC", name="Monaco", region_id=1)
        Country.objects.get_or_create(code="MM", name="Myanmar", region_id=1)
        Country.objects.get_or_create(code="ML", name="Mali", region_id=1)
        Country.objects.get_or_create(code="MO", name="Macao", region_id=1)
        Country.objects.get_or_create(code="MN", name="Mongolia", region_id=1)
        Country.objects.get_or_create(code="MH", name="Marshall", region_id=1)
        Country.objects.get_or_create(code="MK", name="Macedonia", region_id=1)
        Country.objects.get_or_create(code="MU", name="Mauritius", region_id=1)
        Country.objects.get_or_create(code="MT", name="Malta", region_id=1)
        Country.objects.get_or_create(code="MW", name="Malawi", region_id=1)
        Country.objects.get_or_create(code="MV", name="Maldives", region_id=1)
        Country.objects.get_or_create(code="MQ", name="Martinique", region_id=1)
        Country.objects.get_or_create(code="MP", name="Northern", region_id=1)
        Country.objects.get_or_create(code="MS", name="Montserrat", region_id=1)
        Country.objects.get_or_create(code="MR", name="Mauritania", region_id=1)
        Country.objects.get_or_create(code="MY", name="Malaysia", region_id=1)
        Country.objects.get_or_create(code="MX", name="Mexico", region_id=1)
        Country.objects.get_or_create(code="MZ", name="Mozambique", region_id=1)
        Country.objects.get_or_create(code="FR", name="France", region_id=1)
        Country.objects.get_or_create(code="FI", name="Finland", region_id=1)
        Country.objects.get_or_create(code="FJ", name="Fiji", region_id=1)
        Country.objects.get_or_create(code="FK", name="Falkland", region_id=1)
        Country.objects.get_or_create(code="FM", name="Micronesia", region_id=1)
        Country.objects.get_or_create(code="FO", name="Faroe", region_id=1)
        Country.objects.get_or_create(code="CK", name="Cook", region_id=1)
        Country.objects.get_or_create(code="CI", name="Côte", region_id=1)
        Country.objects.get_or_create(code="CH", name="Switzerland", region_id=1)
        Country.objects.get_or_create(code="CO", name="Colombia", region_id=1)
        Country.objects.get_or_create(code="CN", name="China", region_id=1)
        Country.objects.get_or_create(code="CM", name="Cameroon", region_id=1)
        Country.objects.get_or_create(code="CL", name="Chile", region_id=1)
        Country.objects.get_or_create(code="CC", name="Cocos", region_id=1)
        Country.objects.get_or_create(code="CA", name="Canada", region_id=1)
        Country.objects.get_or_create(code="CG", name="Congo", region_id=1)
        Country.objects.get_or_create(code="CF", name="Central", region_id=1)
        Country.objects.get_or_create(code="CD", name="Congo", region_id=1)
        Country.objects.get_or_create(code="CZ", name="Czech", region_id=1)
        Country.objects.get_or_create(code="CY", name="Cyprus", region_id=1)
        Country.objects.get_or_create(code="CX", name="Christmas", region_id=1)
        Country.objects.get_or_create(code="CR", name="Costa", region_id=1)
        Country.objects.get_or_create(code="CW", name="Curaçao", region_id=1)
        Country.objects.get_or_create(code="CV", name="Cabo", region_id=1)
        Country.objects.get_or_create(code="CU", name="Cuba", region_id=1)
        Country.objects.get_or_create(code="SZ", name="Swaziland", region_id=1)
        Country.objects.get_or_create(code="SY", name="Syrian", region_id=1)
        Country.objects.get_or_create(code="SX", name="Sint", region_id=1)
        Country.objects.get_or_create(code="SS", name="South", region_id=1)
        Country.objects.get_or_create(code="SR", name="Suriname", region_id=1)
        Country.objects.get_or_create(code="SV", name="El", region_id=1)
        Country.objects.get_or_create(code="ST", name="Sao", region_id=1)
        Country.objects.get_or_create(code="SK", name="Slovakia", region_id=1)
        Country.objects.get_or_create(code="SJ", name="Svalbard", region_id=1)
        Country.objects.get_or_create(code="SI", name="Slovenia", region_id=1)
        Country.objects.get_or_create(code="SH", name="Saint", region_id=1)
        Country.objects.get_or_create(code="SO", name="Somalia", region_id=1)
        Country.objects.get_or_create(code="SN", name="Senegal", region_id=1)
        Country.objects.get_or_create(code="SM", name="San", region_id=1)
        Country.objects.get_or_create(code="SL", name="Sierra", region_id=1)
        Country.objects.get_or_create(code="SC", name="Seychelles", region_id=1)
        Country.objects.get_or_create(code="SB", name="Solomon", region_id=1)
        Country.objects.get_or_create(code="SA", name="Saudi", region_id=1)
        Country.objects.get_or_create(code="SG", name="Singapore", region_id=1)
        Country.objects.get_or_create(code="SE", name="Sweden", region_id=1)
        Country.objects.get_or_create(code="SD", name="Sudan", region_id=1)
        Country.objects.get_or_create(code="YE", name="Yemen", region_id=1)
        Country.objects.get_or_create(code="YT", name="Mayotte", region_id=1)
        Country.objects.get_or_create(code="LB", name="Lebanon", region_id=1)
        Country.objects.get_or_create(code="LC", name="Saint", region_id=1)
        Country.objects.get_or_create(code="LA", name="Lao", region_id=1)
        Country.objects.get_or_create(code="LK", name="Sri", region_id=1)
        Country.objects.get_or_create(code="LI", name="Liechtenstein", region_id=1)
        Country.objects.get_or_create(code="LV", name="Latvia", region_id=1)
        Country.objects.get_or_create(code="LT", name="Lithuania", region_id=1)
        Country.objects.get_or_create(code="LU", name="Luxembourg", region_id=1)
        Country.objects.get_or_create(code="LR", name="Liberia", region_id=1)
        Country.objects.get_or_create(code="LS", name="Lesotho", region_id=1)
        Country.objects.get_or_create(code="LY", name="Libya", region_id=1)
        Country.objects.get_or_create(code="VA", name="Holy", region_id=1)
        Country.objects.get_or_create(code="VC", name="Saint", region_id=1)
        Country.objects.get_or_create(code="VE", name="Venezuela", region_id=1)
        Country.objects.get_or_create(code="VG", name="Virgin", region_id=1)
        Country.objects.get_or_create(code="IQ", name="Iraq", region_id=1)
        Country.objects.get_or_create(code="VI", name="Virgin", region_id=1)
        Country.objects.get_or_create(code="IS", name="Iceland", region_id=1)
        Country.objects.get_or_create(code="IR", name="Iran", region_id=1)
        Country.objects.get_or_create(code="IT", name="Italy", region_id=1)
        Country.objects.get_or_create(code="VN", name="Viet", region_id=1)
        Country.objects.get_or_create(code="IM", name="Isle", region_id=1)
        Country.objects.get_or_create(code="IL", name="Israel", region_id=1)
        Country.objects.get_or_create(code="IO", name="British", region_id=1)
        Country.objects.get_or_create(code="IN", name="India", region_id=1)
        Country.objects.get_or_create(code="IE", name="Ireland", region_id=1)
        Country.objects.get_or_create(code="ID", name="Indonesia", region_id=1)
        Country.objects.get_or_create(code="BD", name="Bangladesh", region_id=1)
        Country.objects.get_or_create(code="BE", name="Belgium", region_id=1)
        Country.objects.get_or_create(code="BF", name="Burkina", region_id=1)
        Country.objects.get_or_create(code="BG", name="Bulgaria", region_id=1)
        Country.objects.get_or_create(code="BA", name="Bosnia", region_id=1)
        Country.objects.get_or_create(code="BB", name="Barbados", region_id=1)
        Country.objects.get_or_create(code="BL", name="Saint", region_id=1)
        Country.objects.get_or_create(code="BM", name="Bermuda", region_id=1)
        Country.objects.get_or_create(code="BN", name="Brunei", region_id=1)
        Country.objects.get_or_create(code="BO", name="Bolivia", region_id=1)
        Country.objects.get_or_create(code="BH", name="Bahrain", region_id=1)
        Country.objects.get_or_create(code="BI", name="Burundi", region_id=1)
        Country.objects.get_or_create(code="BJ", name="Benin", region_id=1)
        Country.objects.get_or_create(code="BT", name="Bhutan", region_id=1)
        Country.objects.get_or_create(code="BV", name="Bouvet", region_id=1)
        Country.objects.get_or_create(code="BW", name="Botswana", region_id=1)
        Country.objects.get_or_create(code="BQ", name="Bonaire", region_id=1)
        Country.objects.get_or_create(code="BR", name="Brazil", region_id=1)
        Country.objects.get_or_create(code="BS", name="Bahamas", region_id=1)
        Country.objects.get_or_create(code="BY", name="Belarus", region_id=1)
        Country.objects.get_or_create(code="BZ", name="Belize", region_id=1)
        Country.objects.get_or_create(code="RU", name="Russian", region_id=1)
        Country.objects.get_or_create(code="RW", name="Rwanda", region_id=1)
        Country.objects.get_or_create(code="RS", name="Serbia", region_id=1)
        Country.objects.get_or_create(code="RE", name="Réunion", region_id=1)
        Country.objects.get_or_create(code="RO", name="Romania", region_id=1)
        Country.objects.get_or_create(code="OM", name="Oman", region_id=1)
        Country.objects.get_or_create(code="HR", name="Croatia", region_id=1)
        Country.objects.get_or_create(code="HT", name="Haiti", region_id=1)
        Country.objects.get_or_create(code="HU", name="Hungary", region_id=1)
        Country.objects.get_or_create(code="HK", name="Hong", region_id=1)
        Country.objects.get_or_create(code="HN", name="Honduras", region_id=1)
        Country.objects.get_or_create(code="HM", name="Heard", region_id=1)
        Country.objects.get_or_create(code="EH", name="Western", region_id=1)
        Country.objects.get_or_create(code="EE", name="Estonia", region_id=1)
        Country.objects.get_or_create(code="EG", name="Egypt", region_id=1)
        Country.objects.get_or_create(code="EC", name="Ecuador", region_id=1)
        Country.objects.get_or_create(code="ET", name="Ethiopia", region_id=1)
        Country.objects.get_or_create(code="ES", name="Spain", region_id=1)
        Country.objects.get_or_create(code="ER", name="Eritrea", region_id=1)
        Country.objects.get_or_create(code="UY", name="Uruguay", region_id=1)
        Country.objects.get_or_create(code="UZ", name="Uzbekistan", region_id=1)
        Country.objects.get_or_create(code="US", name="United", region_id=1)
        Country.objects.get_or_create(code="UM", name="United", region_id=1)
        Country.objects.get_or_create(code="UG", name="Uganda", region_id=1)
        Country.objects.get_or_create(code="UA", name="Ukraine", region_id=1)
        Country.objects.get_or_create(code="VU", name="Vanuatu", region_id=1)
        Country.objects.get_or_create(code="NI", name="Nicaragua", region_id=1)
        Country.objects.get_or_create(code="NL", name="Netherlands", region_id=1)
        Country.objects.get_or_create(code="NO", name="Norway", region_id=1)
        Country.objects.get_or_create(code="NA", name="Namibia", region_id=1)
        Country.objects.get_or_create(code="NC", name="New", region_id=1)
        Country.objects.get_or_create(code="NE", name="Niger", region_id=1)
        Country.objects.get_or_create(code="NF", name="Norfolk", region_id=1)
        Country.objects.get_or_create(code="NG", name="Nigeria", region_id=1)
        Country.objects.get_or_create(code="NZ", name="New", region_id=1)
        Country.objects.get_or_create(code="NP", name="Nepal", region_id=1)
        Country.objects.get_or_create(code="NR", name="Nauru", region_id=1)
        Country.objects.get_or_create(code="NU", name="Niue", region_id=1)
        Country.objects.get_or_create(code="KG", name="Kyrgyzstan", region_id=1)
        Country.objects.get_or_create(code="KE", name="Kenya", region_id=1)
        Country.objects.get_or_create(code="KI", name="Kiribati", region_id=1)
        Country.objects.get_or_create(code="KH", name="Cambodia", region_id=1)
        Country.objects.get_or_create(code="KN", name="Saint", region_id=1)
        Country.objects.get_or_create(code="KM", name="Comoros", region_id=1)
        Country.objects.get_or_create(code="KR", name="Korea", region_id=1)
        Country.objects.get_or_create(code="KP", name="Korea", region_id=1)
        Country.objects.get_or_create(code="KW", name="Kuwait", region_id=1)
        Country.objects.get_or_create(code="KZ", name="Kazakhstan", region_id=1)
        Country.objects.get_or_create(code="KY", name="Cayman", region_id=1)
        Country.objects.get_or_create(code="DO", name="Dominican", region_id=1)
        Country.objects.get_or_create(code="DM", name="Dominica", region_id=1)
        Country.objects.get_or_create(code="DJ", name="Djibouti", region_id=1)
        Country.objects.get_or_create(code="DK", name="Denmark", region_id=1)
        Country.objects.get_or_create(code="DE", name="Germany", region_id=1)
        Country.objects.get_or_create(code="DZ", name="Algeria", region_id=1)
        Country.objects.get_or_create(code="TZ", name="Tanzania", region_id=1)
        Country.objects.get_or_create(code="TV", name="Tuvalu", region_id=1)
        Country.objects.get_or_create(code="TW", name="Taiwan", region_id=1)
        Country.objects.get_or_create(code="TT", name="Trinidad", region_id=1)
        Country.objects.get_or_create(code="TR", name="Turkey", region_id=1)
        Country.objects.get_or_create(code="TN", name="Tunisia", region_id=1)
        Country.objects.get_or_create(code="TO", name="Tonga", region_id=1)
        Country.objects.get_or_create(code="TL", name="Timor", region_id=1)
        Country.objects.get_or_create(code="TM", name="Turkmenistan", region_id=1)
        Country.objects.get_or_create(code="TJ", name="Tajikistan", region_id=1)
        Country.objects.get_or_create(code="TK", name="Tokelau", region_id=1)
        Country.objects.get_or_create(code="TH", name="Thailand", region_id=1)
        Country.objects.get_or_create(code="TF", name="French", region_id=1)
        Country.objects.get_or_create(code="TG", name="Togo", region_id=1)
        Country.objects.get_or_create(code="TD", name="Chad", region_id=1)
        Country.objects.get_or_create(code="TC", name="Turks", region_id=1)
        Country.objects.get_or_create(code="AE", name="United", region_id=1)
        Country.objects.get_or_create(code="AD", name="Andorra", region_id=1)
        Country.objects.get_or_create(code="AG", name="Antigua", region_id=1)
        Country.objects.get_or_create(code="AF", name="Afghanistan", region_id=1)
        Country.objects.get_or_create(code="AI", name="Anguilla", region_id=1)
        Country.objects.get_or_create(code="AM", name="Armenia", region_id=1)
        Country.objects.get_or_create(code="AL", name="Albania", region_id=1)
        Country.objects.get_or_create(code="AO", name="Angola", region_id=1)
        Country.objects.get_or_create(code="AQ", name="Antarctica", region_id=1)
        Country.objects.get_or_create(code="AS", name="American", region_id=1)
        Country.objects.get_or_create(code="AR", name="Argentina", region_id=1)
        Country.objects.get_or_create(code="AU", name="Australia", region_id=1)
        Country.objects.get_or_create(code="AT", name="Austria", region_id=1)
        Country.objects.get_or_create(code="AW", name="Aruba", region_id=1)
        Country.objects.get_or_create(code="AX", name="Åland", region_id=1)
        Country.objects.get_or_create(code="AZ", name="Azerbaijan", region_id=1)
        Country.objects.get_or_create(code="QA", name="Qatar", region_id=1)
        Country.objects.get_or_create(code="BO", name="Bolivia", region_id=1)
        Country.objects.get_or_create(code="VE", name="Venezuela", region_id=1)
        Country.objects.get_or_create(code="RU", name="Russia", region_id=1)
        Country.objects.get_or_create(code="BN", name="Brunei", region_id=1)
        Country.objects.get_or_create(code="IR", name="Iran", region_id=1)
        Country.objects.get_or_create(code="VN", name="Vietnam", region_id=1)
        Country.objects.get_or_create(code="MD", name="Moldovia", region_id=1)
        Country.objects.get_or_create(code="SY", name="Syria", region_id=1)
        Country.objects.get_or_create(code="TZ", name="Tanzania", region_id=1)
        Country.objects.get_or_create(code="LA", name="Laos", region_id=1)
        Country.objects.get_or_create(code="TW", name="Taiwan", region_id=1)
        Country.objects.get_or_create(code="MK", name="Macedonia", region_id=1)
        Country.objects.get_or_create(code="KR", name="South", region_id=1)
        Country.objects.get_or_create(code="KP", name="North", region_id=1)

    def create_source_study(self):
        Study.objects.get_or_create(name='IAVI', description='IAVI study - from core lab in London')
        Study.objects.get_or_create(name='UCSD', description='UCSD study, San Diego, CA')
        Study.objects.get_or_create(name='SCOPE', description='SCOPE study, San Francisco, CA')
        Study.objects.get_or_create(name='AMPLIAR', description='AMPLIAR study, Brazil')
        Study.objects.get_or_create(name='SFMHS', description='San Francisco Men’s Health Study')
        Study.objects.get_or_create(name='CTS', description='Blood bank - Blood Systems Testing Lab (Description to be updated')
        Study.objects.get_or_create(name='BRAZIL', description='Blood bank - Brazil')
        Study.objects.get_or_create(name='SANBS', description='Blood bank - SANBS')
        Study.objects.get_or_create(name='CAPRISA', description='CAPRISA study - South Africa')
        Study.objects.get_or_create(name='FPSHSP', description='Fundação Pro-Sangue-Hemocentro de São Paulo, Brazil')
        Study.objects.get_or_create(name='GAMA', description='CRESIB malaria cohort')
        Study.objects.get_or_create(name='IMPACTA', description='Asociación Civil Impacta Saludy Educación')
        Study.objects.get_or_create(name='ARC', description='Blood bank - American Red Cross')
        Study.objects.get_or_create(name='OPTIONS', description='Options study')
        Study.objects.get_or_create(name='SERACARE', description='')

    def create_specimen_type(self):
        SpecimenType.objects.get_or_create(name='Whole Blood', spec_type=1, spec_group=1)
        SpecimenType.objects.get_or_create(name='DBS', spec_type=2, spec_group=2)
        SpecimenType.objects.get_or_create(name='Serum', spec_type=3, spec_group=3)
        SpecimenType.objects.get_or_create(name='Urine / Nothing', spec_type=4.1, spec_group=4)
        SpecimenType.objects.get_or_create(name='Urine / Azide', spec_type=4.2, spec_group=4)
        SpecimenType.objects.get_or_create(name='Stool / Nothing', spec_type=5.1, spec_group=5)
        SpecimenType.objects.get_or_create(name='Stool / RNAlater', spec_type=5.2, spec_group=5)
        SpecimenType.objects.get_or_create(name='Saliva', spec_type=6.1, spec_group=6)
        SpecimenType.objects.get_or_create(name='PBMC', spec_type=7, spec_group=7)
        SpecimenType.objects.get_or_create(name='Plasma', spec_type=8, spec_group=8)
        SpecimenType.objects.get_or_create(name='Hair', spec_type=9, spec_group=9)
        SpecimenType.objects.get_or_create(name='Buccal swab / Nothing', spec_type=10.1, spec_group=10)
        SpecimenType.objects.get_or_create(name='Buccal swab / Buffer', spec_type=10.2, spec_group=10)
        SpecimenType.objects.get_or_create(name='Saliva / Pellets', spec_type=6.2, spec_group=6)
        SpecimenType.objects.get_or_create(name='Urine / Unknown', spec_type=4.9, spec_group=4)
        SpecimenType.objects.get_or_create(name='Stool / Unknown', spec_type=5.9, spec_group=5)

class TestBase(TestCase, TestHelper):
    """ All tests should extend from this class """
    pass
