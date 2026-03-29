# main.py
# Punto de entrada del sistema de monitoreo eléctrico

import os
import time
import inputs
from config import SECTORES, POTENCIA_DEFAULT, POTENCIA_MIN
from sensors import leer_voltaje, aplicar_simulacion_voltaje, leer_corriente, aplicar_simulacion_corriente
from simulator import (
    inicializar_simulador,
    actualizar_simulacion,
    clasificar_estado,
    estimar_tiempo_restauracion,
    mostrar_estado,
    mostrar_fin_simulacion,
)
import simulator
from reports import registrar_reporte, graficar_sesion


MODO_DEMO = True  # bool - False activa eventos con probabilidad aleatoria


# ─── Bucle principal ──────────────────────────────────────────────────────────

def main():
    os.system("cls" if os.name == "nt" else "clear")
    print("╔══════════════════════════════════╗")
    print("║  ⚡ MONITOR DE RED ELÉCTRICA     ║")
    print("╚══════════════════════════════════╝")

    sector, v_nominal = inputs.solicitar_sector()
    potencia_nominal  = inputs.solicitar_potencia()
    i_nominal = potencia_nominal/v_nominal

    os.system("cls" if os.name == "nt" else "clear")

    while True:
        inicializar_simulador(v_nominal, potencia_nominal)

        # Historial para la gráfica final
        hist_t         = []  # lista de int
        hist_voltaje   = []  # lista de float
        hist_corriente = []  # lista de float

        # Ciclo de muestreo
        while True:
            # 1. Decidir si hay un evento activo este ciclo
            actualizar_simulacion(MODO_DEMO)

            # 2. Leer señales base del sensor
            voltaje   = leer_voltaje(v_nominal, simulator.t)
            voltaje   = aplicar_simulacion_voltaje(voltaje, simulator.simulacion, v_nominal)
            corriente = leer_corriente(potencia_nominal, voltaje)
            corriente = aplicar_simulacion_corriente(corriente, simulator.simulacion, i_nominal)

            # 3. Clasificar el estado del sistema
            estado, tipo_falla = clasificar_estado(voltaje, corriente)
            
            simulator.estado = estado

            # 4. Calcular tiempo de restauración si acaba de cambiar de estado
            tiempo_restauracion = None
            if estado != simulator.ultimo_estado and estado != "normal":
                tiempo_restauracion = estimar_tiempo_restauracion(tipo_falla)
            simulator.ultimo_estado = estado

            # 5. Guardar en historial
            hist_t.append(simulator.t)
            hist_voltaje.append(voltaje)
            hist_corriente.append(corriente)

            # 6. Manejo de estado crítico
            if estado == "critico":
                mostrar_fin_simulacion(tipo_falla, voltaje, corriente, tiempo_restauracion)

                registrar_reporte(
                    sector,
                    estado,
                    tipo_falla,
                    voltaje,
                    corriente,
                    tiempo_restauracion or 0,
                )

                graficar_sesion(hist_t,
                                hist_voltaje,
                                hist_corriente,
                                v_nominal,
                                i_nominal, 
                                sector,
                                simulator.umbrales)

                if inputs.preguntar_continuar():
                    os.system("cls" if os.name == "nt" else "clear")
                    break       # vuelve al while externo → reinicia simulador
                else:
                    print("\n  👋 Simulación terminada. ¡Hasta pronto!\n")
                    return

            # 7. Mostrar estado normal / advertencia
            mostrar_estado(
                voltaje,
                corriente,
                tipo_falla,
                estado,
                simulator.simulacion)

            simulator.t += 1
            time.sleep(1)
            os.system("cls" if os.name == "nt" else "clear")


if __name__ == "__main__":
    main()
