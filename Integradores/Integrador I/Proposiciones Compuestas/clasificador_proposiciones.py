# Clasificador de Proposiciones Compuestas
# Trabajo Integrador - Matemática y Programación I - UTN 2026
#
# Genera la tabla de verdad de una proposición lógica y la clasifica
# como TAUTOLOGÍA, CONTRADICCIÓN o CONTINGENCIA.

from itertools import product


# ── 1. SEPARAR LA PROPOSICIÓN EN SÍMBOLOS ─────────────────────────────
# Recorre el texto y arma una lista con cada parte por separado.
# Ejemplo: "p -> ~q"  →  ['p', '->', '~', 'q']

def separar_simbolos(proposicion):
    simbolos = []
    i = 0
    while i < len(proposicion):
        if proposicion[i] == ' ':
            i += 1
        elif proposicion[i:i+3] == '<->':        # bicondicional (3 caracteres)
            simbolos.append('<->'); i += 3
        elif proposicion[i:i+2] == '->':         # condicional (2 caracteres)
            simbolos.append('->'); i += 2
        elif proposicion[i] in '~&|()':
            simbolos.append(proposicion[i]); i += 1
        elif proposicion[i].isalpha():
            simbolos.append(proposicion[i].lower()); i += 1
        else:
            raise ValueError(f"Símbolo no reconocido: '{proposicion[i]}'")
    return simbolos


# ── 2. EVALUAR LA PROPOSICIÓN ──────────────────────────────────────────
# Calcula el resultado respetando la precedencia matemática de operadores:
#
#   <->  <  ->  <  |  <  &  <  ~     (de menor a mayor precedencia)
#
# Cada función maneja un operador y llama a la del siguiente nivel.
# La variable 'pos' indica qué símbolo de la lista se está leyendo.

def eval_bicondicional(simbolos, pos, valores):
    izq, pos = eval_condicional(simbolos, pos, valores)
    while pos < len(simbolos) and simbolos[pos] == '<->':
        pos += 1
        der, pos = eval_condicional(simbolos, pos, valores)
        izq = (izq == der)          # p <-> q: verdadero cuando ambos tienen el mismo valor
    return izq, pos

def eval_condicional(simbolos, pos, valores):
    izq, pos = eval_disyuncion(simbolos, pos, valores)
    while pos < len(simbolos) and simbolos[pos] == '->':
        pos += 1
        der, pos = eval_disyuncion(simbolos, pos, valores)
        izq = (not izq) or der      # p -> q equivale a ~p | q (falso solo si p=V y q=F)
    return izq, pos

def eval_disyuncion(simbolos, pos, valores):
    izq, pos = eval_conjuncion(simbolos, pos, valores)
    while pos < len(simbolos) and simbolos[pos] == '|':
        pos += 1
        der, pos = eval_conjuncion(simbolos, pos, valores)
        izq = izq or der
    return izq, pos

def eval_conjuncion(simbolos, pos, valores):
    izq, pos = eval_negacion(simbolos, pos, valores)
    while pos < len(simbolos) and simbolos[pos] == '&':
        pos += 1
        der, pos = eval_negacion(simbolos, pos, valores)
        izq = izq and der
    return izq, pos

def eval_negacion(simbolos, pos, valores):
    if pos < len(simbolos) and simbolos[pos] == '~':
        pos += 1
        resultado, pos = eval_negacion(simbolos, pos, valores)  # permite ~~p
        return not resultado, pos
    return eval_variable(simbolos, pos, valores)

def eval_variable(simbolos, pos, valores):
    if pos >= len(simbolos):
        raise ValueError("Proposición incompleta.")
    if simbolos[pos] == '(':                    # expresión entre paréntesis
        pos += 1
        resultado, pos = eval_bicondicional(simbolos, pos, valores)
        if pos >= len(simbolos) or simbolos[pos] != ')':
            raise ValueError("Falta cerrar paréntesis.")
        return resultado, pos + 1
    if simbolos[pos] in valores:                # variable con su valor asignado
        return valores[simbolos[pos]], pos + 1
    raise ValueError(f"Variable no reconocida: '{simbolos[pos]}'")

def evaluar(proposicion, valores):
    simbolos = separar_simbolos(proposicion)
    resultado, _ = eval_bicondicional(simbolos, 0, valores)
    return resultado


# ── 3. TABLA DE VERDAD Y CLASIFICACIÓN ────────────────────────────────

def generar_tabla(proposicion):
    # Extrae las variables únicas y genera las 2^n combinaciones posibles
    variables = sorted(set(c for c in proposicion.lower() if c.isalpha()))
    if not variables:
        raise ValueError("La proposición no contiene variables.")
    filas = []
    for combinacion in product([False, True], repeat=len(variables)):
        valores = dict(zip(variables, combinacion))
        filas.append({'valores': valores, 'resultado': evaluar(proposicion, valores)})
    return variables, filas

def clasificar(filas):
    resultados = [f['resultado'] for f in filas]
    if all(resultados):       return "TAUTOLOGÍA"
    if not any(resultados):   return "CONTRADICCIÓN"
    return "CONTINGENCIA"


# ── 4. MOSTRAR RESULTADOS ──────────────────────────────────────────────

def mostrar_tabla(proposicion, variables, filas, clasificacion):
    encabezado = "  " + " | ".join(f" {v} " for v in variables) + " | Resultado"
    separador  = "  " + "-" * (len(encabezado) - 2)

    print(f"\n{'='*55}")
    print(f"  Proposición: {proposicion}")
    print(f"{'='*55}")
    print(encabezado)
    print(separador)
    for fila in filas:
        celdas = " | ".join(f" {'V' if fila['valores'][v] else 'F'} " for v in variables)
        res    = 'V' if fila['resultado'] else 'F'
        print(f"  {celdas} |     {res}")
    print(separador)

    print(f"\n  >>> {clasificacion} <<<\n")
    if clasificacion == "TAUTOLOGÍA":
        print("  Verdadera en TODOS los casos.")
        print("  El resultado no depende de los valores de las variables.")
    elif clasificacion == "CONTRADICCIÓN":
        print("  Falsa en TODOS los casos.")
        print("  El resultado no depende de los valores de las variables.")
    else:
        verdaderas = sum(1 for f in filas if f['resultado'])
        print(f"  Verdadera en {verdaderas} de {len(filas)} casos.")
        print("  El resultado depende de los valores de las variables.")
    print("=" * 55)


# ── 5. MENÚ ────────────────────────────────────────────────────────────

EJEMPLOS = [
    ("p & ~p",                  "Contradicción clásica"),
    ("p | ~p",                  "Tautología (Tercio Excluso)"),
    ("p -> q",                  "Condicional simple"),
    ("(p -> q) <-> (~q -> ~p)", "Ley de la Contrarrecíproca"),
    ("(p & q) | ~r",            "Proposición con 3 variables"),
]

def menu():
    print("\n" + "=" * 55)
    print("   CLASIFICADOR DE PROPOSICIONES COMPUESTAS")
    print("   Matemática y Programación I  —  UTN 2026")
    print("=" * 55)
    print("  Operadores:  ~p   p & q   p | q   p -> q   p <-> q")
    print("  Variables:   cualquier letra  (p, q, r, s, ...)")
    print("=" * 55)

    while True:
        print()
        print("  1. Analizar una proposicion propia")
        print("  2. Ver ejemplos predefinidos")
        print("  3. Salir")
        opcion = input("\n  Opción (1-3): ").strip()

        if opcion == "1":
            proposicion = input("\n  Ingresar proposición: ").strip()
            if not proposicion:
                print("  La proposición no puede estar vacía.")
                continue
            try:
                variables, filas = generar_tabla(proposicion)
                mostrar_tabla(proposicion, variables, filas, clasificar(filas))
            except ValueError as e:
                print(f"\n  Error: {e}\n")

        elif opcion == "2":
            print()
            for i, (prop, desc) in enumerate(EJEMPLOS, 1):
                print(f"  {i}. {prop:<38}  ({desc})")
            try:
                sel = int(input("\n  Seleccionar número: ").strip())
                if 1 <= sel <= len(EJEMPLOS):
                    proposicion = EJEMPLOS[sel - 1][0]
                    variables, filas = generar_tabla(proposicion)
                    mostrar_tabla(proposicion, variables, filas, clasificar(filas))
                else:
                    print("  Número fuera de rango.")
            except ValueError:
                print("  Ingresá un número válido.")

        elif opcion == "3":
            print("\n  ¡Hasta luego!\n")
            break
        else:
            print("  Opción no válida.")


if __name__ == "__main__":
    menu()
