from chemlib import Reaction, Compound


def react():
    r = Reaction([Compound(" N2O5       "), Compound("   H2O")], [Compound("HNO3")])
    print(r.formula)
    print(r.is_balanced)

    r.balance()
    print(r.formula)
    print(r.is_balanced)


react()

print([Compound('H2O'), Compound("NO3")])
