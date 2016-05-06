def do_curtis_alg2016(luminex_result):
    try:
        needed_fields = {'gp120_MFIn':4.2,
                         'gp160_MFIn':3.1,
                         'gp120_AI':24.9,
                         'gp160_AI':31.8,
                         'gp41_AI':31.8}

        for field in needed_fields:
            field_value = getattr(luminex_result, field)
            if field_value:
                float(field_value)
            else:
                raise ValueError

        criteria_met = [ field if getattr(luminex_result, field) < cut_off else None for field, cut_off in needed_fields.iteritems() ]

        if criteria_met == len(needed_fields):
            luminex_result.recent_curtis_2016_alg = True
        else:
            luminex_result.recent_curtis_2016_alg = False

        luminex_result.save()
    except ValueError:
        pass

def do_curtis_alg2013(luminex_result):
    try:
        needed_fields = {'gp160_MFIn':5.0,
                         'gp120_MFIn':7.0,
                         'gp120_AI':20.0,
                         'gp160_AI':25.0,
                         'gp41_AI':35.0}

        criteria_met = [ field if getattr(luminex_result, field) < cut_off\
                         else None for field, cut_off in needed_fields.iteritems() ]

        if len(criteria_met) >= 3:
            luminex_result.recent_curtis_2013_alg35 = True
        else:
            luminex_result.recent_curtis_2013_alg35 = False
        luminex_result.save()
    except ValueError:
        pass
