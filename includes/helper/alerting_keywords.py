__author__ = 'LenardZill'

def convert(keyword):
    gsa = ''
    ew = ''
    eg = ''

    if 'FEU AUS' in keyword:
        gsa = 'Feuer, aus'
    elif 'FEU K' in keyword:
        gsa = 'Feuer, klein'
    elif 'FEU G' in keyword:
        gsa = 'Feuer, groß'
    elif 'FEU 2' in keyword:
        gsa = 'Feuer, 2 Löschzüge'
    elif 'FEU 3' in keyword:
        gsa = 'Feuer, 3 Löschzüge'
    elif 'FEU 4' in keyword:
        gsa = 'Feuer, 4 Löschzüge'
    elif 'FEU 5' in keyword:
        gsa = 'Feuer, 5 Löschzüge'
    elif 'FEU 6' in keyword:
        gsa = 'Feuer, 6 Löschzüge'
    elif 'FEU 7' in keyword:
        gsa = 'Feuer, 7 Löschzüge'

    return keyword