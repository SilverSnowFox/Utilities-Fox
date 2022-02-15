from chemlib import Compound


MOLARMASS_LIMIT = 10000


def molarmass_limit_check(compound: Compound) -> bool:
    """Checks that the compound is smaller than a fixed amount"""
    amounts = [int(x) for x in compound.occurences.values()]
    return sum(amounts) <= MOLARMASS_LIMIT
