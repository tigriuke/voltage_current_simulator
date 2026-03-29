# reportes.py
# Persistencia de reportes en JSON y generación de gráficas

import json
import os
from datetime import datetime

import matplotlib.pyplot as plt
import matplotlib.ticker as ticker

from config import RUTA_REPORTES


# ─── Archivado JSON ───────────────────────────────────────────────────────────

def cargar_reportes():
    # Lee el archivo de reportes existente y devuelve un dict
    # Si no existe o está corrupto, devuelve un dict vacío
    if not os.path.exists(RUTA_REPORTES):
        return {}
    with open(RUTA_REPORTES, "r", encoding="utf-8") as f:
        try:
            return json.load(f)
        except json.JSONDecodeError:
            return {}


def guardar_reportes(datos):
    # Escribe el diccionario de reportes en disco
    with open(RUTA_REPORTES, "w", encoding="utf-8") as f:
        json.dump(datos, f, indent=2, ensure_ascii=False)


def registrar_reporte(sector, estado, tipo_falla, voltaje, corriente, tiempo_estimado):
    # Actualiza el reporte acumulativo del sector en reportes.json
    # Si el sector ya existe, incrementa el contador de reportes
    # Estructura guardada por sector:
    #   estado, tipo_falla, voltaje, corriente, reportes, tiempo_estimado, ultima_actualizacion
    datos = cargar_reportes()

    #entrada_anterior = datos.get(sector, {})
    #reportes_previos = entrada_anterior.get("reportes", 0)

    # Si el sector no existe, inicializarlo con una lista vacía
    if sector not in datos:
        datos[sector] = []

    # Contar los reportes previos según cuántos registros hay en la lista
    reportes_previos = len(datos[sector])

    datos[sector].append({
        "estado":               estado,
        "tipo_falla":           tipo_falla,
        "voltaje":              round(voltaje, 2),
        "corriente":            round(corriente, 2),
        "reportes":             reportes_previos + 1,
        "tiempo_estimado":      round(tiempo_estimado, 0),
        "ultima_actualizacion": datetime.now().isoformat(timespec="seconds"),
    })

    guardar_reportes(datos)
    print(f"\n📁 Reporte guardado en '{RUTA_REPORTES}' para el sector '{sector}'.")


# ─── Gráfica de voltaje y corriente vs tiempo ─────────────────────────────────

def graficar_sesion(historial_t, historial_voltaje, historial_corriente, v_nominal, i_nominal, sector, umbrales):
    # Genera y guarda una gráfica de voltaje y corriente vs tiempo
    # Incluye líneas de referencia para los umbrales críticos de voltaje
    if not historial_t:
        print("⚠ Sin datos para graficar.")
        return

    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 6), sharex=True)
    fig.suptitle(
        f"Sesión de monitoreo — Sector: {sector.capitalize()}",
        fontsize=13, fontweight="bold"
    )

    # Subgráfica de voltaje
    ax1.plot(historial_t, historial_voltaje, color="#2196F3", linewidth=1.5, label="Voltaje (V)")
    ax1.axhline(v_nominal,   color="green",  linestyle="--", linewidth=1, label=f"Nominal ({v_nominal} V)")
    ax1.axhline(umbrales["umbral_voltaje_alto"], color="orange", linestyle=":",  linewidth=1, label=f"Umbral alto ({umbrales["umbral_voltaje_alto"]:.0f} V)")
    ax1.axhline(umbrales["umbral_voltaje_bajo"], color="red",    linestyle=":",  linewidth=1, label=f"Umbral bajo ({umbrales["umbral_voltaje_bajo"]:.0f} V)")
    ax1.set_ylabel("Voltaje (V)")
    ax1.legend(fontsize=8, loc="upper right")
    ax1.yaxis.set_minor_locator(ticker.AutoMinorLocator())
    ax1.grid(True, which="major", linestyle="--", alpha=0.4)
    ax1.grid(True, which="minor", linestyle=":",  alpha=0.2)

    # Subgráfica de corriente
    ax2.plot(historial_t, historial_corriente, color="#E91E63", linewidth=1.5, label="Corriente (A)")
    ax2.axhline(i_nominal,   color="green",  linestyle="--", linewidth=1, label=f"Nominal ({i_nominal} i)")
    ax2.axhline(umbrales["umbral_corriente_alto"], color="orange", linestyle=":",  linewidth=1, label=f"Umbral alto ({umbrales["umbral_corriente_alto"]:.0f} V)")
    ax2.axhline(umbrales["umbral_corriente_bajo"], color="red",    linestyle=":",  linewidth=1, label=f"Umbral bajo ({umbrales["umbral_corriente_bajo"]:.0f} V)")
    ax2.grid(True, which="major", linestyle="--", alpha=0.4)
    ax2.set_ylabel("Corriente (A)")
    ax2.set_xlabel("Tiempo (muestras)")
    ax2.legend(fontsize=8, loc="upper right")
    ax2.yaxis.set_minor_locator(ticker.AutoMinorLocator())
    ax2.grid(True, which="minor", linestyle=":",  alpha=0.2)

    plt.tight_layout()

    nombre_archivo = f"grafica_{sector}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
    plt.savefig(nombre_archivo, dpi=150, bbox_inches="tight")
    print(f"📊 Gráfica guardada como '{nombre_archivo}'.")

    plt.show()
