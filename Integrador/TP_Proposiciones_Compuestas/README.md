# Clasificador de Proposiciones Compuestas

**Trabajo Integrador N°1 — Matemática y Programación I**  
UTN · Comisión N°11 · Regional Venado Tuerto · Cohorte Marzo 2026

---

## Descripción

Programa en Python que recibe una proposición lógica compuesta, genera su tabla de verdad completa y la clasifica automáticamente como **tautología**, **contradicción** o **contingencia**.

Integra conceptos de álgebra de Boole y lógica proposicional aplicados mediante estructuras de programación: funciones, ciclos, listas y diccionarios.

---

## Operadores soportados

| Símbolo | Operador | Ejemplo |
|---|---|---|
| `~p` | Negación | `~p` |
| `p & q` | Conjunción (AND) | `p & q` |
| `p \| q` | Disyunción (OR) | `p \| q` |
| `p -> q` | Condicional | `p -> q` |
| `p <-> q` | Bicondicional | `p <-> q` |

Variables: cualquier letra minúscula (`p`, `q`, `r`, `s`, ...)

---

## Cómo ejecutar

```bash
python clasificador_proposiciones.py
```

Requiere Python 3.7 o superior. No necesita librerías externas.

---

## Ejemplos incluidos

| Proposición | Clasificación |
|---|---|
| `p & ~p` | Contradicción |
| `p \| ~p` | Tautología |
| `p -> q` | Contingencia |
| `(p -> q) <-> (~q -> ~p)` | Tautología (Ley de la Contrarrecíproca) |
| `(p & q) \| ~r` | Contingencia |

---

## Estructura del proyecto

```
TP_Proposiciones_Compuestas/
├── clasificador_proposiciones.py   # Código fuente
├── PDF1_Descripcion_y_Ejercicio.txt
├── PDF3_Iteraciones_IA.txt
└── README.md
```

---

## Conceptos matemáticos aplicados

- Proposiciones simples y compuestas
- Tabla de verdad: con `n` variables se generan `2ⁿ` combinaciones
- Precedencia de operadores lógicos
- Equivalencia lógica: `p → q` ≡ `¬p ∨ q`
- Clasificación: tautología, contradicción, contingencia

---

## Uso de Inteligencia Artificial

El proyecto fue desarrollado con apoyo de tres herramientas de IA con roles diferenciados:

- **Gemini** — generación de ideas y diseño del proyecto
- **ChatGPT** — comprensión y profundización de conceptos matemáticos  
- **Claude** — desarrollo y revisión del código

Cada sugerencia fue validada y adaptada al nivel del curso antes de ser implementada.
