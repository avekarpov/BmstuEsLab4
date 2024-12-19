import logging

logging.basicConfig(level=logging.DEBUG, format='%(message)s')

def compare_atoms(atom1, atom2):
    return (atom1[0] == atom2[0] and
            atom1[1] == atom2[1] and
            sorted(atom1[2]) == sorted(atom2[2]))

def unify_variable(var, value, substitutions):
    if var in substitutions.keys():
        return unify_term(substitutions[var], value, substitutions)

    if value in substitutions.keys():
        return unify_term(var, substitutions[value], substitutions)

    substitutions[var] = value
    logging.info(f"Унификация переменной {var} -> {value}")


    return substitutions

def unify_term(l, r, substitutions):
    if l == r:
        return substitutions
    
    if l.islower():
        return unify_variable(l, r, substitutions)
    
    if r.islower():
        return unify_variable(r,l, substitutions)

    return None

def unify_atom(l_terms, r_terms, substitutions):
    for l, r in zip(l_terms, r_terms):
        substitutions = unify_term(l, r, substitutions)
        if substitutions is None:
            return None

    return substitutions

def apply_substitutions(clause, substitutions):
    def substitute_term(term):
        while term in substitutions:
            term = substitutions[term]

        return term

    def substitute_atom(atom):
        sign, name, terms = atom
        return (sign, name, [substitute_term(term) for term in terms])

    substituted_clause = [substitute_atom(atom) for atom in clause]
    logging.info(f"Применение замен: {substitutions} -> {substituted_clause}")
    return substituted_clause

def resolve(l_clause, r_clause):
    substitutions = {}

    logging.info(f"Резолюция между {l_clause} и {r_clause}")

    for l in l_clause:
        l_sign, l_name, l_terms = l
        for r in r_clause:
            r_sign, r_name, r_terms = r

            logging.debug(f"Попытка унификации {l} и {r}")

            if l_name != r_name:
                logging.debug("Неудача, разные имена")
                continue

            if l_sign == r_sign:
                logging.debug("Неудача, один знак")
                continue

            if len(l_terms) != len(r_terms):
                logging.debug("Неудача, разное количество термов")
                continue

            substitutions = unify_atom(l_terms, r_terms, substitutions) 

            if substitutions is not None:
                new_clause = (
                    [i for i in l_clause if i != l] +
                    [i for i in r_clause if i != r]
                )
                logging.info(f"Резолюция между {l_clause} и {r_clause}, результат: {new_clause}")
                return apply_substitutions(new_clause, substitutions)

    return None

def resolution(clauses):
    while True:
        new_clauses = []

        for l in range(0, len(clauses)):
            for r in range(l + 1, len(clauses)):
                resolvent = resolve(clauses[l], clauses[r])

                if resolvent is None:
                    continue

                if len(resolvent) == 0:
                    return True
                
                for i in resolvent:
                    if i not in new_clauses:
                        new_clauses.append(i)

        if len(new_clauses) == 0:
            return False
        
        for i in new_clauses:
            if i not in clauses:
                logging.debug(f'Добавляем кляузу {i}')
                clauses.append([i])

def example_1():
    logging.info("--- Пример 1: логический вывод R(b) ---")
    clauses = [
        [(True, "P", ["x"]), (True, "Q", ["x"])],
        [(False, "P", ["a"]), (True, "R", ["b"])],
        [(False, "Q", ["a"])]
    ]
    result = resolution(clauses)
    logging.info("Результат: Доказано противоречие" if result else "Результат: Доказательство не найдено\n")

def example_2():
    logging.info("--- Пример 2: теорема о дружбе ---")
    clauses = [
        [(False, "Friends", ["Alice", "Bob"]), (True, "Friends", ["Bob", "Alice"])],
        [(True, "Friends", ["Alice", "Bob"])],
        [(False, "Friends", ["Bob", "Alice"])]
    ]
    result = resolution(clauses)
    logging.info("Результат: Доказано противоречие" if result else "Результат: Доказательство не найдено\n")

def example_3():
    logging.info("--- Пример 3: дедукция ---")
    clauses = [
        [(False, "Rain", []), (True, "WetStreet", [])],
        [(True, "Rain", [])],
        [(False, "WetStreet", [])]
    ]
    result = resolution(clauses)
    logging.info("Результат: Доказано противоречие" if result else "Результат: Доказательство не найдено\n")

if __name__ == "__main__":
    example_1()
    # example_2()
    # example_3()
