from process.ded_complex.serpentis_narcotic_warehouses import SerpentisNarcoticWarehouses

COMPLEX_MAP = {
    'Serpentis Narcotic Warehouses': SerpentisNarcoticWarehouses
}


def create_complex(name):
    if name in COMPLEX_MAP:
        return COMPLEX_MAP[name]()