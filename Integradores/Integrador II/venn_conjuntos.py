# ============================================================
# INTEGRADOR 2 - Matematica y Programacion en Python
# Teoria de Conjuntos: Diagrama de Venn con tres conjuntos
# Franco Kaddour
# ============================================================

import sys
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import Circle

sys.stdout.reconfigure(encoding="utf-8")


# ------------------------------------------------------------
# INGRESO DE DATOS
# ------------------------------------------------------------

def pedir_numero(mensaje):
    """Pide un numero entero positivo y repite hasta que sea valido."""
    while True:
        try:
            valor = int(input(mensaje))
            if valor >= 0:
                return valor
            print("  El valor no puede ser negativo. Intente nuevamente.")
        except ValueError:
            print("  Ingrese un numero entero valido.")


def ingresar_datos():
    """
    Guia al usuario para ingresar todos los datos del problema:
    universo, nombres y cardinalidades de los conjuntos e intersecciones.
    Devuelve un diccionario con todos los valores.
    """
    print("\n" + "=" * 55)
    print("  INTEGRADOR 2 - Matematica y Programacion en Python")
    print("  Diagrama de Venn con tres conjuntos")
    print("=" * 55 + "\n")

    desc_u  = input("Descripcion del universo U: ")
    total_u = pedir_numero("Cantidad total de elementos |U|: ")

    print()
    nombre_a = input("Descripcion del conjunto A: ")
    nombre_b = input("Descripcion del conjunto B: ")
    nombre_c = input("Descripcion del conjunto C: ")

    print()
    card_a  = pedir_numero("Cantidad de elementos en A  |A|: ")
    card_b  = pedir_numero("Cantidad de elementos en B  |B|: ")
    card_c  = pedir_numero("Cantidad de elementos en C  |C|: ")

    print()
    card_ab  = pedir_numero("Elementos en A y B         |A n B|: ")
    card_ac  = pedir_numero("Elementos en A y C         |A n C|: ")
    card_bc  = pedir_numero("Elementos en B y C         |B n C|: ")

    print()
    card_abc = pedir_numero("Elementos en A, B y C  |A n B n C|: ")

    return {
        "desc_u":   desc_u,   "total_u":  total_u,
        "nombre_a": nombre_a, "nombre_b": nombre_b, "nombre_c": nombre_c,
        "card_a":   card_a,   "card_b":   card_b,   "card_c":   card_c,
        "card_ab":  card_ab,  "card_ac":  card_ac,  "card_bc":  card_bc,
        "card_abc": card_abc,
    }


# ------------------------------------------------------------
# CALCULOS
# ------------------------------------------------------------

def calcular_regiones(datos):
    """
    Calcula las 8 regiones del diagrama de Venn usando la formula
    de descomposicion por regiones exclusivas:

      Solo A   = |A| - (|AnB| - |AnBnC|) - (|AnC| - |AnBnC|) - |AnBnC|
      Solo B   = |B| - (|AnB| - |AnBnC|) - (|BnC| - |AnBnC|) - |AnBnC|
      Solo C   = |C| - (|AnC| - |AnBnC|) - (|BnC| - |AnBnC|) - |AnBnC|
      Solo AnB = |AnB| - |AnBnC|   (idem para AnC y BnC)

    Devuelve un diccionario con los resultados.
    """
    a, b, c = datos["card_a"], datos["card_b"], datos["card_c"]
    ab, ac, bc, abc = datos["card_ab"], datos["card_ac"], datos["card_bc"], datos["card_abc"]

    solo_a  = a - (ab - abc) - (ac - abc) - abc
    solo_b  = b - (ab - abc) - (bc - abc) - abc
    solo_c  = c - (ac - abc) - (bc - abc) - abc
    solo_ab = ab - abc
    solo_ac = ac - abc
    solo_bc = bc - abc
    triple  = abc

    total_union = solo_a + solo_b + solo_c + solo_ab + solo_ac + solo_bc + triple
    fuera       = datos["total_u"] - total_union

    return {
        "solo_a": solo_a, "solo_b": solo_b, "solo_c": solo_c,
        "solo_ab": solo_ab, "solo_ac": solo_ac, "solo_bc": solo_bc,
        "triple": triple, "total_union": total_union, "fuera": fuera,
    }


# ------------------------------------------------------------
# MOSTRAR RESULTADOS
# ------------------------------------------------------------

def mostrar_resultados(datos, r):
    """Muestra los resultados en una tabla y verifica que el total coincida con |U|."""
    print("\n" + "=" * 55)
    print("             RESULTADOS")
    print("=" * 55)
    print(f"\n  Universo: {datos['desc_u']}  (|U| = {datos['total_u']})")
    print(f"  A = {datos['nombre_a']}")
    print(f"  B = {datos['nombre_b']}")
    print(f"  C = {datos['nombre_c']}\n")
    print(f"  {'Region':<30} | Cantidad")
    print("-" * 45)
    print(f"  {'Solo A':<30} |   {r['solo_a']}")
    print(f"  {'Solo B':<30} |   {r['solo_b']}")
    print(f"  {'Solo C':<30} |   {r['solo_c']}")
    print(f"  {'Solo A y B (sin C)':<30} |   {r['solo_ab']}")
    print(f"  {'Solo A y C (sin B)':<30} |   {r['solo_ac']}")
    print(f"  {'Solo B y C (sin A)':<30} |   {r['solo_bc']}")
    print(f"  {'A, B y C (los tres)':<30} |   {r['triple']}")
    print("-" * 45)
    print(f"  {'En al menos un conjunto':<30} |   {r['total_union']}")
    print(f"  {'Fuera de A, B y C':<30} |   {r['fuera']}")
    print("=" * 55)

    total = r["total_union"] + r["fuera"]
    if total == datos["total_u"]:
        print(f"  OK: {r['total_union']} + {r['fuera']} = {total} = |U|  (verificacion correcta)\n")
    else:
        print(f"  ERROR: el total ({total}) no coincide con |U| = {datos['total_u']}\n")


# ------------------------------------------------------------
# DIAGRAMA DE VENN
# ------------------------------------------------------------

def graficar_venn(datos, r):
    """
    Genera y guarda el diagrama de Venn como 'diagrama_venn.png'.
    Usa tres circulos en disposicion triangular:
      A = izquierda, B = derecha, C = abajo centro.
    """
    fig, ax = plt.subplots(figsize=(10, 8))
    ax.set_xlim(0, 10); ax.set_ylim(0, 9)
    ax.set_aspect("equal"); ax.axis("off")
    fig.patch.set_facecolor("#F8F9FA")

    # Universo U (rectangulo de fondo)
    ax.add_patch(mpatches.FancyBboxPatch(
        (0.2, 0.3), 9.6, 8.3, boxstyle="round,pad=0.1",
        linewidth=2, edgecolor="#333333", facecolor="#FFFDE7"))
    ax.text(0.55, 8.35, "U", fontsize=16, fontweight="bold")

    # Centros y radio de los tres circulos
    cx_a, cy_a = 3.9, 5.4
    cx_b, cy_b = 6.1, 5.4
    cx_c, cy_c = 5.0, 3.4
    radio = 2.1

    # Dibujar circulos (relleno semitransparente + borde)
    for cx, cy, color, borde in [
        (cx_a, cy_a, "#2196F3", "#1565C0"),
        (cx_b, cy_b, "#F44336", "#B71C1C"),
        (cx_c, cy_c, "#4CAF50", "#1B5E20"),
    ]:
        ax.add_patch(Circle((cx, cy), radio, color=color, alpha=0.3, zorder=2))
        ax.add_patch(Circle((cx, cy), radio, fill=False, edgecolor=borde, linewidth=2, zorder=3))

    # Etiquetas de los conjuntos
    ax.text(cx_a - 2.4, cy_a + 1.9, f"A\n{datos['nombre_a'][:18]}",
            fontsize=9, fontweight="bold", ha="center", va="center", color="#1565C0",
            bbox=dict(boxstyle="round,pad=0.3", facecolor="#E3F2FD", alpha=0.85))
    ax.text(cx_b + 2.4, cy_b + 1.9, f"B\n{datos['nombre_b'][:18]}",
            fontsize=9, fontweight="bold", ha="center", va="center", color="#B71C1C",
            bbox=dict(boxstyle="round,pad=0.3", facecolor="#FFEBEE", alpha=0.85))
    ax.text(cx_c, cy_c - 2.5, f"C\n{datos['nombre_c'][:18]}",
            fontsize=9, fontweight="bold", ha="center", va="center", color="#1B5E20",
            bbox=dict(boxstyle="round,pad=0.3", facecolor="#E8F5E9", alpha=0.85))

    # Valores en cada region
    n = dict(fontsize=13, ha="center", va="center", fontweight="bold", zorder=5)
    ax.text(cx_a - 1.2,              cy_a + 0.4,              str(r["solo_a"]),  color="#1565C0", **n)
    ax.text(cx_b + 1.2,              cy_b + 0.4,              str(r["solo_b"]),  color="#B71C1C", **n)
    ax.text(cx_c,                    cy_c - 1.2,              str(r["solo_c"]),  color="#1B5E20", **n)
    ax.text((cx_a+cx_b)/2,           cy_a + 0.8,              str(r["solo_ab"]), color="#6A1B9A", **n)
    ax.text((cx_a+cx_c)/2 - 0.4,    (cy_a+cy_c)/2 - 0.1,    str(r["solo_ac"]), color="#E65100", **n)
    ax.text((cx_b+cx_c)/2 + 0.4,    (cy_b+cy_c)/2 - 0.1,    str(r["solo_bc"]), color="#004D40", **n)
    ax.text((cx_a+cx_b+cx_c)/3,     (cy_a+cy_b+cy_c)/3,      str(r["triple"]),  color="#880E4F", **n)
    ax.text(0.8, 1.1, str(r["fuera"]), color="#546E7A", fontsize=12,
            ha="center", va="center", fontweight="bold", zorder=5)

    # Titulo y leyenda inferior
    ax.set_title(f"Diagrama de Venn\n{datos['desc_u']}", fontsize=11, fontweight="bold", pad=12)
    ax.text(5.0, 0.1,
            f"|U|={datos['total_u']}  |  En al menos un conjunto: {r['total_union']}  |  Fuera: {r['fuera']}",
            fontsize=8, ha="center", color="#546E7A", style="italic")

    plt.tight_layout()
    plt.savefig("diagrama_venn.png", dpi=200, bbox_inches="tight", facecolor="#F8F9FA")
    print("  Diagrama guardado como 'diagrama_venn.png'")
    plt.show()


# ------------------------------------------------------------
# PROGRAMA PRINCIPAL
# ------------------------------------------------------------

def main():
    # 1. Ingresar datos
    datos = ingresar_datos()

    # 2. Calcular regiones
    regiones = calcular_regiones(datos)

    # 3. Verificar que ningun resultado sea negativo (datos inconsistentes)
    valores_negativos = [k for k, v in regiones.items() if v < 0]
    if valores_negativos:
        print(f"\n  ERROR: valores negativos en {valores_negativos}.")
        print("  Los datos ingresados son inconsistentes. Revise e intente nuevamente.")
        return

    # 4. Mostrar resultados
    mostrar_resultados(datos, regiones)

    # 5. Generar diagrama
    respuesta = input("  ¿Desea ver el diagrama de Venn? (s/n): ").strip().lower()
    if respuesta == "s":
        graficar_venn(datos, regiones)

    print("  Programa finalizado.\n")


if __name__ == "__main__":
    main()
