# config.py
# Configuración central del sistema de monitoreo eléctrico

# ─── Sectores y voltajes nominales ───────────────────────────────────────────
SECTORES = {
    "melendez":   120.0,
    "caney":      130.0,
    "industrial": 110.0,
}

# ─── Potencia por defecto ─────────────────────────────────────────────────────
POTENCIA_DEFAULT  = 1200.0  # float - Watts, representa un hogar colombiano promedio
POTENCIA_RUIDO_STD = 0.08    # float - 8% de la potencia nominal como ruido gaussiano
POTENCIA_MIN = 0.01    # float - 1% del nominal como mínimo físicamente válido

# ─── Umbrales de detección (fracción del valor nominal) ──────────────────────
# Se aplican tanto al voltaje como a la corriente esperada
FACTOR_CRITICO_ARRIBA = 1.2  # float
FACTOR_CRITICO_ABAJO  = 0.8  # float

# ─── Parámetros de la señal base ──────────────────────────────────────────────

AMPLITUD_VARIACION  = 0.015  # float - 1.5% del voltaje nominal
FRECUENCIA_SENOIDAL = 0.05   # float - Frecuencia angular (rad/muestra) — esta sí es absoluta
RUIDO_VOLTAJE_STD   = 0.004  # float - 0.4% del voltaje nominal

# ─── Perturbaciones de voltaje y corriente (fracción del nominal) ─────────────────────
FALLA_VOLTAJE_MIN   = 0.10   # float - 6% del nominal  → perturbación mínima
FALLA_VOLTAJE_MAX   = 0.30  # float - 12% del nominal → perturbación máxima
FALLA_CORRIENTE_MIN = 0.10   # float
FALLA_CORRIENTE_MAX = 0.30   # float

# ─── Detección de fallos sostenidos ──────────────────────────────────────────
UMBRAL_MUESTRAS_CRITICO = 3  # int - Muestras consecutivas para declarar fallo

# ─── Temporización de eventos (modo demo) ────────────────────────────────────
INTERVALO_EVENTO_DEMO = 10  # int - Muestras entre eventos en modo demo
DURACION_EVENTO_MIN   = 5   # int
DURACION_EVENTO_MAX   = 15  # int

# ─── Probabilidad de evento en modo realista ─────────────────────────────────
PROB_EVENTO_REALISTA = 0.02  # float

# ─── Archivo de reportes ──────────────────────────────────────────────────────
RUTA_REPORTES = "reportes.json"  # str
