import locale

def rupiah_format(angka, with_prefix=True, desimal=0):
    # locale.setlocale(locale.LC_NUMERIC, '')
    # rupiah = locale.format("%.*f", (desimal, angka), True)
    rupiah = int(angka)
    if with_prefix:
        return 'Rp. {0:,}'.format(rupiah)
    return rupiah