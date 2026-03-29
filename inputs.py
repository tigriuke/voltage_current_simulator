#inputs.py
# ─── Utilidades de entrada ────────────────────────────────────────────────────

from config import POTENCIA_DEFAULT, POTENCIA_MIN, SECTORES


def leer_float(prompt, minimo=0.0):
    # Solicita un número decimal al usuario con validación
    # Rechaza valores no numéricos y menores a minimo
    # Devuelve un float válido
    while True:
        entrada = input(prompt).strip()
        try:
            valor = float(entrada)
            if valor < minimo:
                print(f"  ⚠ El valor debe ser mayor o igual a {minimo}. Intenta de nuevo.")
            else:
                return valor
        except ValueError:
            print("  ⚠ Ingresa un número válido (usa punto como separador decimal).")


def solicitar_sector():
    # Pide el sector al usuario
    # Devuelve (sector, v_nominal) → (str, float)
    sectores_disponibles = ", ".join(SECTORES.keys())
    print(f"\n  Sectores disponibles: {sectores_disponibles}")
    sector = input("  Ingrese el sector: ").strip().lower()

    if sector in SECTORES:
        v_nominal = SECTORES[sector]
        print(f"  ✔ Voltaje nominal para '{sector}': {v_nominal} V")
    else:
        print(f"  Sector '{sector}' no reconocido.")
        v_nominal = leer_float("  Ingrese el voltaje nominal de su sector (V): ", minimo=1.0)

    return sector, v_nominal


def solicitar_potencia():
    # Pregunta si usar la potencia por defecto o ingresar una personalizada
    # Devuelve la potencia nominal en Watts (float)
    print(f"\n  Potencia por defecto: {POTENCIA_DEFAULT} W (hogar promedio)")
    
    while True:
        usar_default = input("  ¿Desea usar la potencia por defecto? (S/N): ").strip().upper()

        if usar_default == "S" or usar_default == "N":
            break
        print("  ⚠ Ingrese S para Sí o N para No.")

    if usar_default == "S":
        print(f"  ✔ Usando potencia por defecto: {POTENCIA_DEFAULT} W")
        return POTENCIA_DEFAULT
    else:
        return leer_float(
            f"  Ingrese la potencia nominal de su hogar (W, mínimo {POTENCIA_MIN}): ",
            minimo=POTENCIA_MIN,
        )


def preguntar_continuar():
    # Pregunta si se desea reiniciar la simulación
    # Devuelve True para continuar, False para salir
    while True:
        resp = input("\n  ¿Desea continuar la simulación? (S/N): ").strip().upper()
        if resp == "S":
            return True
        if resp == "N":
            return False
        print("  ⚠ Ingrese S para Sí o N para No.")

