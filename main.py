from enum import Enum

class Flag(Enum):
    NoValue = -1
    Linked = 0
    HasValue = 1

class Term:
    def __init__(self, name, value='', flag=Flag.NoValue):
        self.name = name
        self.value = value
        self.flag = flag

    def __str__(self) -> str:
        if self.flag == Flag.NoValue:
            return self.name
        
        return self.value

class Atom:
    def __init__(self, name, sign, terms):
        self.name = name
        self.sign = sign
        self.terms = terms

    def can_be_unified(self, other):
        if self.name != other.name:
            return False
        
        if self.sign == other.sign:
            return False
        
        if len(self.terms) != len(other.terms):
            return False
        
        for l, r in zip(self.terms, other.terms):
            if l.flag == Flag.HasValue and r.flag == Flag.HasValue:
                if l.value != r.value:
                    return False
                
        return True
    
    def __str__(self) -> str:
        return f'{"!" if not self.sign else ""}{self.name}({", ".join(str(i) for i in self.terms)})'

class Disjunct:
    def __init__(self, atoms):
        self.atoms = atoms

    def __str__(self) -> str:
        return f'{" v ".join(str(i) for i in self.atoms)}'
    

def find_disjuncts_to_unify(disjuncts):
    for disjunct in disjuncts:
        for atom in disjunct.atoms:
            if any([i.flag != Flag.HasValue for i in atom.terms]):
                continue

            for target_disjunct in disjuncts:
                if target_disjunct == disjunct:
                    continue

                for target_atom in target_disjunct.atoms:
                    if atom.can_be_unified(target_atom):
                        return disjunct, atom, target_disjunct, target_atom

    return None

def unify(disjuncts, main_disjunct, main_atom, target_disjunct, target_atom):
    disjuncts.remove(main_disjunct)

    target_disjunct.atoms.remove(target_atom)

    substitution = {}

    for main_term, target_term in zip(main_atom.terms, target_atom.terms):
        if target_term.flag == Flag.NoValue:
            substitution[target_term.name] = main_term.name

    print(f'Замены: {substitution}')

    for atom in target_disjunct.atoms:
        for term in atom.terms:
            if term.name in substitution.keys():
                term.name = substitution[term.name]
                term.value = term.name
                term.flag = Flag.Linked


def resolve(disjuncts):
    while True:
        result = find_disjuncts_to_unify(disjuncts)

        if result is None:
            print(f'Нечего унифицировать: {" & ".join(str(i) for i in disjuncts)}')
            break

        (disjunct, atom, target_disjunct, target_atom) = result

        print(f'Дизъюнкты: {" & ".join(str(i) for i in disjuncts)}')
        print(f'Унифицируемые дизъюнкты: {disjunct}, {target_disjunct}')
        print(f'Унифицируемые атомы: {atom}, {target_atom}')

        unify(disjuncts, disjunct, atom, target_disjunct, target_atom)

        print('-----------------------------------------------------------')


def example_1():
    resolve(
        [
            Disjunct([
                Atom("P1", True, [Term("BT", "BT", Flag.HasValue)])
            ]),
            Disjunct([
                Atom("P2", False, [Term("DT", "DT", Flag.HasValue), Term("BT", "BT", Flag.HasValue)])
            ]),
            Disjunct([
                Atom("P1", False, [Term("y")]),
                Atom("P2", True, [Term("x"), Term("y")]),
                Atom("l", False, [Term("x"), Term("y")])
            ])
        ]
    )

example_1()
