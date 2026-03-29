# simulador.py
# Lógica de detección de fallos, clasificación de estados y salida por consola

import random
from config import (
    FACTOR_CRITICO_ARRIBA,
    FACTOR_CRITICO_ABAJO,
    UMBRAL_MUESTRAS_CRITICO,
    INTERVALO_EVENTO_DEMO,
    DURACION_EVENTO_MIN,
    DURACION_EVENTO_MAX,
    PROB_EVENTO_REALISTA,
)

SIMULACIONES_POSIBLES = ["subtension", "sobretension", "sobrecarga", "subcarga"]

ICONOS = {"normal": "🟢", "advertencia": "🟡", "critico": "🔴"}

# ─── Variables del simulador ──────────────────────────────────────────────────
# Guardan el estado interno entre ciclos del bucle principal

umbral_voltaje_alto: float
umbral_voltaje_bajo: float
umbral_corriente_alto: float
umbral_corriente_bajo: float

t: int               # muestra actual
t_generar: int       # muestra en la que se generará la proxima simulacion (modo demo)
duracion_simulacion: int

contador_bajo_voltaje: int   # muestras consecutivas por debajo del umbral
contador_alto_voltaje: int   # muestras consecutivas por encima del umbral

contador_bajo_corriente: int   # muestras consecutivas por debajo del umbral
contador_alto_corriente: int   

estado: str
ultimo_estado: str
simulacion: str
umbrales = {}


def inicializar_simulador(v_nominal, potencia_nominal):
    # Inicializa (o reinicia) todas las variables globales del simulador
    global umbral_voltaje_alto, umbral_voltaje_bajo
    global umbral_corriente_alto, umbral_corriente_bajo
    global t, t_generar, duracion_simulacion
    global contador_bajo_voltaje, contador_alto_voltaje
    global contador_bajo_corriente, contador_alto_corriente
    global simulacion, estado, ultimo_estado, umbrales

    umbral_voltaje_alto = FACTOR_CRITICO_ARRIBA * v_nominal
    umbral_voltaje_bajo = FACTOR_CRITICO_ABAJO  * v_nominal

    # Corriente esperada en condiciones normales: I = P / V
    corriente_esperada    = potencia_nominal / v_nominal
    umbral_corriente_alto = FACTOR_CRITICO_ARRIBA * corriente_esperada
    umbral_corriente_bajo = FACTOR_CRITICO_ABAJO  * corriente_esperada

    t               = 0
    t_generar       = INTERVALO_EVENTO_DEMO
    duracion_simulacion = 0

    contador_bajo_voltaje   = 0
    contador_alto_voltaje   = 0

    contador_bajo_corriente   = 0
    contador_alto_corriente   = 0

    estado        = "normal"
    ultimo_estado = "normal"
    simulacion    = "normal"
    umbrales = {
        "umbral_voltaje_alto": umbral_voltaje_alto,
        "umbral_voltaje_bajo": umbral_voltaje_bajo,
        "umbral_corriente_alto":umbral_corriente_alto,
        "umbral_corriente_bajo":umbral_corriente_bajo
        }


# ─── Generación de simulaciones ────────────────────────────────────────────────────

def generar_simulacion():
    # Devuelve un simulacion eléctrico aleatorio (str)
    return random.choice(SIMULACIONES_POSIBLES)


def actualizar_simulacion(modo_demo):
    # Decide si se genera o mantiene un simulacion en este ciclo
    # Modifica las variables globales: simulacion, duracion_simulacion, t_generar
    global simulacion, duracion_simulacion, t_generar

    if duracion_simulacion > 0:
        duracion_simulacion -= 1
        return  # la simulacion actual continúa

    simulacion = "normal"

    if modo_demo:
        if t == t_generar:
            simulacion          = generar_simulacion()
            
            t_generar          += 20
            duracion_simulacion = random.randint(DURACION_EVENTO_MIN, DURACION_EVENTO_MAX)
    else:
        if random.random() < PROB_EVENTO_REALISTA:
            simulacion          = generar_simulacion()
            duracion_simulacion = random.randint(DURACION_EVENTO_MIN, DURACION_EVENTO_MAX)


# ─── Clasificación del estado eléctrico ──────────────────────────────────────

def clasificar_estado(voltaje, corriente):
    # Evalúa voltaje y corriente y devuelve (estado, tipo_falla)
    # estado     → str: "normal" | "advertencia" | "critico"
    # tipo_falla → str o None

    global contador_bajo_voltaje, contador_alto_voltaje, contador_bajo_corriente, contador_alto_corriente

#Verificacion de voltaje por encima del umbral 3 veces seguidas
    if voltaje > umbral_voltaje_alto:
        contador_alto_voltaje += 1

        if contador_alto_voltaje >= UMBRAL_MUESTRAS_CRITICO:
            return "critico", "sobretension"
        else:
            return "advertencia", "sobretension"

    
    else: 
        contador_alto_voltaje = 0
        
#Verificacion de la corriente por encima del umbral 3 veces seguidas.
#Sino devuelve advertencia
    if corriente > umbral_corriente_alto:
        
        contador_alto_corriente += 1

        if contador_alto_corriente >= UMBRAL_MUESTRAS_CRITICO:
            return "critico", "sobrecarga"
        else:
            return "advertencia", "sobrecarga"
    else: 
        contador_alto_corriente = 0
    

#Verificacion de voltaje por debajo del umbral 3 veces seguidas
    if voltaje < umbral_voltaje_bajo:
        contador_bajo_voltaje += 1

        if contador_bajo_voltaje >= UMBRAL_MUESTRAS_CRITICO:
            return "critico", "subtension"
        else:
            return "advertencia", "subtension"

    else: contador_bajo_voltaje = 0

#Verificacion de la corriente por debajo del umbral 3 veces seguidas
    if corriente < umbral_corriente_bajo:
        contador_bajo_corriente += 1

        if contador_bajo_corriente >= UMBRAL_MUESTRAS_CRITICO:
            return "critico", "subcarga"
        else:
            return "advertencia", "subcarga"

    else: contador_bajo_corriente = 0

#Si ninguna condicion se cumple el estado es normal y el tipo_falla es None
    return "normal", "ninguna"

def estimar_tiempo_restauracion(tipo_falla):
    # Devuelve un tiempo estimado de restauración en minutos (int)
    tiempos = {
        "subtension":   (5, 20),
        "sobretension": (5, 15),
        "sobrecarga":   (10, 40),
        "subcarga":     (10, 40),
    }
    rango = tiempos.get(tipo_falla, (5, 10))

    return random.randint(*rango)


# ─── Salida por consola ───────────────────────────────────────────────────────

def mostrar_estado(voltaje, corriente, tipo_falla, estado, simulacion):
    # Imprime el panel de monitoreo en tiempo real
    icono = ICONOS.get(estado, "⚪")
    
    print("\n----------------------------")
    print("⚡ SISTEMA ELÉCTRICO")
    print("----------------------------")
    print(f"Voltaje:            {round(voltaje, 2)} V")
    print(f"Corriente:          {round(corriente, 2)} A")
    print(f"Tipo de falla:      {tipo_falla.capitalize()}")
    print(f"Estado:             {icono} {estado.upper()}")
    print(f"Evento simulado:    {simulacion.capitalize()}")



def mostrar_fin_simulacion(tipo_falla, voltaje, corriente, tiempo_restauracion):
    # Imprime el resumen final cuando el sistema alcanza estado crítico
    icono = ICONOS.get(estado, "⚪")
    print("\n╔═══════════════════════════╗")
    print("║ ⚡ SIMULACIÓN FINALIZADA  ║")
    print("╚═══════════════════════════╝")
    print(f"  Falla detectada : {tipo_falla.upper()}")
    print(f"  Voltaje final   : {round(voltaje, 2)} V")
    print(f"  Corriente final : {round(corriente, 2)} A")
    print(f"  Estado          : {icono} {estado.upper()}")

    if tiempo_restauracion is not None:
        print(f"  Tiempo estimado de restauración: {tiempo_restauracion} min")

    print("─" * 30)
