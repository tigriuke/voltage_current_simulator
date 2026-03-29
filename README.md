# ⚡ Simulador de red eléctrica

Sistema de simulación y monitoreo en tiempo real del comportamiento eléctrico de sectores residenciales e industriales. Detecta fallas de voltaje y corriente, clasifica estados del sistema y genera reportes persistentes con gráficas por sesión.

---

## Tabla de contenidos

- [Características](#características)
- [Arquitectura](#arquitectura)
- [Requisitos](#requisitos)
- [Instalación](#instalación)
- [Ejecución](#ejecución)
- [Configuración](#configuración)
- [Tipos de falla](#tipos-de-falla)
- [Estructura de reportes](#estructura-de-reportes)

---

## Características

- Simulación de señal eléctrica con variación senoidal y ruido gaussiano escalados al voltaje nominal
- Detección de fallas sostenidas: subtensión, sobretensión, sobrecarga y subcarga
- Clasificación de estados: `normal`, `advertencia` y `crítico`
- Persistencia de reportes en `reportes.json` con historial acumulativo por sector
- Generación automática de gráficas de voltaje y corriente por sesión
- Modo **demo** (eventos periódicos predecibles) y modo **realista** (eventos con probabilidad aleatoria)

---

## Arquitectura

```
voltage_current_simulator/
│
├── main.py          # Punto de entrada — bucle principal de muestreo
├── simulator.py     # Detección de fallas, clasificación de estados, salida por consola
├── sensors.py       # Generación de señales de voltaje y corriente
├── reports.py       # Persistencia JSON y generación de gráficas matplotlib
├── inputs.py        # Utilidades de entrada de usuario con validación
├── config.py        # Configuración central de todos los parámetros
│
├── reportes.json    # Generado automáticamente al registrar la primera falla
└── grafica_<sector>_<timestamp>.png   # Generada al finalizar cada sesión
```

### Flujo de datos por ciclo

```
actualizar_simulacion()
        │
        ▼
leer_voltaje()  ──►  aplicar_simulacion_voltaje()
        │
        ▼
leer_corriente()  ──►  aplicar_simulacion_corriente()
        │
        ▼
clasificar_estado()
        │
     ┌──┴──────────┐
     ▼             ▼
  normal /      crítico
 advertencia       │
     │         registrar_reporte()
     ▼         graficar_sesion()
mostrar_estado()
```

### Responsabilidad de cada módulo

| Módulo | Responsabilidad |
|---|---|
| `main.py` | Orquesta el bucle, conecta todos los módulos |
| `simulator.py` | Estado interno del simulador, contadores, umbrales, salida por consola |
| `sensors.py` | Modela la física de la señal eléctrica con ruido y perturbaciones |
| `reports.py` | Lee/escribe `reportes.json` y genera gráficas matplotlib |
| `inputs.py` | Solicita y valida entradas del usuario (sector, potencia, modo) |
| `config.py` | Fuente única de verdad para todos los parámetros del sistema |

---

## Requisitos

- Python 3.10 o superior (requerido por `match/case`)
- pip

### Dependencias Python

```
matplotlib
```

> La librería estándar (`math`, `random`, `json`, `os`, `time`, `datetime`) no requiere instalación adicional.

---

## Instalación

### 1. Clonar el repositorio

```bash
git clone https://github.com/tigriuke/voltage_current_simulator.git
cd voltage_current_simulator
```

### 2. Crear entorno virtual (recomendado)

```bash
python -m venv venv
```

Activar el entorno:

```bash
# Linux / macOS
source venv/bin/activate

# Windows
venv\Scripts\activate
```

### 3. Instalar dependencias

```bash
pip install matplotlib
```

---

## Ejecución

### Desarrollo

En desarrollo se recomienda activar el **modo demo**, que genera eventos eléctricos en intervalos fijos y predecibles, ideal para observar el comportamiento del sistema sin esperar eventos aleatorios.

En `main.py`, asegúrate de tener:

```python
MODO_DEMO = True
```

Luego ejecuta:

```bash
python main.py
```

El programa pedirá:

1. **Sector** — elige entre los disponibles o ingresa uno personalizado con su voltaje nominal
2. **Potencia nominal** — usa el valor por defecto (1200 W) o ingresa uno personalizado

### Producción

En producción se usa el **modo realista**, donde los eventos ocurren con una probabilidad baja por muestra (`PROB_EVENTO_REALISTA = 0.02`), simulando condiciones de red reales.

En `main.py`, cambia:

```python
MODO_DEMO = False
```

Luego ejecuta:

```bash
python main.py
```

Para ejecutarlo en segundo plano en un servidor Linux:

```bash
nohup python main.py > monitor.log 2>&1 &
```

Para detenerlo:

```bash
kill $(pgrep -f main.py)
```

---

## Configuración

Todos los parámetros se gestionan desde `config.py`. No es necesario modificar otros archivos para ajustar el comportamiento del sistema.

### Sectores y voltajes nominales

```python
SECTORES = {
    "melendez":   120.0,   
    "caney":      130.0,
    "industrial": 110.0,
}
```

Agrega nuevos sectores con su voltaje nominal correspondiente.

### Parámetros de potencia

```python
POTENCIA_DEFAULT   = 1200.0  # W — hogar colombiano promedio
POTENCIA_RUIDO_STD = 0.08    # 8% del nominal como desviación estándar del ruido
POTENCIA_MIN       = 0.01    # 1% del nominal como mínimo físicamente válido
```

### Parámetros de la señal base

```python
AMPLITUD_VARIACION  = 0.015  # 1.5% del voltaje nominal — amplitud senoidal
FRECUENCIA_SENOIDAL = 0.05   # rad/muestra — frecuencia de oscilación
RUIDO_VOLTAJE_STD   = 0.004  # 0.4% del voltaje nominal — ruido gaussiano
```

### Umbrales de detección

```python
FACTOR_CRITICO_ARRIBA = 1.2  # 120% del nominal → umbral alto
FACTOR_CRITICO_ABAJO  = 0.8  # 80%  del nominal → umbral bajo
UMBRAL_MUESTRAS_CRITICO = 3  # muestras consecutivas para declarar fallo crítico
```

### Magnitud de perturbaciones por falla

Basados en estándares **IEEE 1159** e **IEC 61000-4-30**:

```python
# Subtensión / Sobretensión (voltage sag / swell)
FALLA_VOLTAJE_MIN = 0.10   # 10% del nominal
FALLA_VOLTAJE_MAX = 0.30   # 30% del nominal

# Sobrecarga / Subcarga
FALLA_CORRIENTE_MIN = 0.10  # 10% de la corriente nominal
FALLA_CORRIENTE_MAX = 0.30  # 30% de la corriente nominal
```

### Temporización de eventos

```python
INTERVALO_EVENTO_DEMO = 10   # muestras entre eventos en modo demo
DURACION_EVENTO_MIN   = 5    # duración mínima de un evento (muestras)
DURACION_EVENTO_MAX   = 15   # duración máxima de un evento (muestras)
PROB_EVENTO_REALISTA  = 0.02 # probabilidad de evento por muestra en modo realista
```

---

## Tipos de falla

| Tipo | Descripción | Efecto en voltaje | Efecto en corriente |
|---|---|---|---|
| `subtension` | Caída de tensión en la red | −10% a −30% del nominal | Sin cambio directo |
| `sobretension` | Subida de tensión en la red | +10% a +30% del nominal | Sin cambio directo |
| `sobrecarga` | Exceso de consumo | −3% a −8% (caída resistiva) | +10% a +30% del nominal |
| `subcarga` | Consumo muy bajo | +1% a +4% | −10% a −30% del nominal |

### Estados del sistema

| Estado | Condición | Icono |
|---|---|---|
| `normal` | Voltaje y corriente dentro de umbrales | 🟢 |
| `advertencia` | 1–2 muestras consecutivas fuera de umbral | 🟡 |
| `critico` | 3+ muestras consecutivas fuera de umbral | 🔴 |

Al alcanzar estado **crítico**, el sistema detiene la simulación, registra el reporte y genera la gráfica de la sesión.

---

## Estructura de reportes

Los reportes se guardan en `reportes.json` con una lista de registros por sector:

```json
{
  "melendez": [
    {
      "estado": "critico",
      "tipo_falla": "sobrecarga",
      "voltaje": 118.43,
      "corriente": 15.21,
      "reportes": 1,
      "tiempo_estimado": 25,
      "ultima_actualizacion": "2026-03-28T17:02:01"
    },
    {
      "estado": "critico",
      "tipo_falla": "subtension",
      "voltaje": 94.10,
      "corriente": 9.87,
      "reportes": 2,
      "ultima_actualizacion": "2026-03-28T18:15:44"
    }
  ],
  "industrial": [
    {
      "estado": "critico",
      "tipo_falla": "sobretension",
      "voltaje": 134.56,
      "corriente": 11.20,
      "reportes": 1,
      "ultima_actualizacion": "2026-03-28T19:00:10"
    }
  ]
}
```

Cada vez que el sistema alcanza estado crítico se agrega un nuevo registro a la lista del sector correspondiente. El campo `reportes` indica el número de incidentes acumulados para ese sector.
