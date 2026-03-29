# sensores.py
# Simulación de lecturas de sensores eléctricos

import math
import random
from config import (
    AMPLITUD_VARIACION,
    FRECUENCIA_SENOIDAL,
    POTENCIA_MIN,
    RUIDO_VOLTAJE_STD,
    POTENCIA_RUIDO_STD,
    FALLA_VOLTAJE_MIN,
    FALLA_VOLTAJE_MAX,
    FALLA_CORRIENTE_MIN,
    FALLA_CORRIENTE_MAX,
)


def leer_voltaje(v_nominal, t):
    # Genera una lectura de voltaje simulada (float)
    # Modela la señal como: V(t) = V_nominal + variación_senoidal(t) + ruido_gaussiano
    amplitud = AMPLITUD_VARIACION * v_nominal         
    ruido_std = RUIDO_VOLTAJE_STD * v_nominal
    
    variacion = amplitud * math.sin(FRECUENCIA_SENOIDAL * t)
    ruido     = random.gauss(0, ruido_std)
    voltaje   = v_nominal + variacion + ruido
    return max(voltaje, 0.0)


def aplicar_simulacion_voltaje(voltaje, simulacion, v_nominal):
    # Perturba el voltaje según el tipo de simulacion activa (str)
    # Devuelve el voltaje perturbado (float), siempre positivo

    # Perturbación escalada al nominal
    delta_min = FALLA_VOLTAJE_MIN * v_nominal          
    delta_max = FALLA_VOLTAJE_MAX * v_nominal          

    match simulacion:
        case "subtension":
            voltaje -= random.uniform(delta_min, delta_max)
        case "sobretension":
            voltaje += random.uniform(delta_min, delta_max)
        case "sobrecarga":
            voltaje -= 0.3 * random.uniform(delta_min, delta_max)
        case "subcarga":
            voltaje += 0.02 * v_nominal                # +2% fijo
    return max(voltaje, 0.0)

def leer_corriente(potencia_nominal, voltaje):
    # Estima la corriente usando P = V * I (float)
    # La potencia varía ligeramente en cada muestra para simular cambios en la carga
    if voltaje <= 0:
        return 0.0
    
    ruido_std = POTENCIA_RUIDO_STD * potencia_nominal   
    potencia_min = POTENCIA_MIN * potencia_nominal 

    potencia_instantanea = potencia_nominal + random.gauss(0, ruido_std)
    potencia_instantanea = max(potencia_instantanea, potencia_min) #evita una potencia negativa, y que la potencia baje del minimo, 1% de potencia nominal
    return potencia_instantanea / voltaje


def aplicar_simulacion_corriente(corriente, simulacion, i_nominal):
    # Perturba la corriente según el tipo de simulacion activa (str)
    # Devuelve la corriente perturbada (float), siempre >= 0

    delta_min = FALLA_CORRIENTE_MIN * i_nominal
    delta_max = FALLA_CORRIENTE_MAX * i_nominal

    match simulacion:
        case "sobrecarga":
            corriente += random.uniform(delta_min, delta_max)
        case "subcarga":
            corriente -= random.uniform(delta_min, delta_max)
    return max(corriente, 0.0)
