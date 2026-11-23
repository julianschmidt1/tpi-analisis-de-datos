# TPI · Análisis de bajas de clientes de Telco

[![Open in Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/julianschmidt1/tpi-analisis-de-datos/blob/main/notebooks/TPI_Analisis_de_Datos.ipynb)

**Introducción al Análisis de Datos · UTN Facultad Regional Avellaneda**
**División 343**
**Integrantes:** Matías, Julián y Emmanuel.

Este trabajo analiza el abandono de clientes (*churn*) en **Telco Customer Churn**, un dataset obtenido de Kaggle con 7.043 clientes y 21 variables originales. Busca comprender cómo se relacionan el contrato, la antigüedad, los servicios y los cargos con las bajas registradas, para orientar el estudio de acciones de retención.

Cada fila representa un cliente; la variable objetivo `Churn` indica baja (`Yes`) o permanencia (`No`). El trabajo incluye limpieza, análisis exploratorio, visualización, preprocesamiento, regresión lineal simple (`TotalCharges ~ tenure`) y clasificación mediante Regresión Logística.

## Entregables

| Recurso | Contenido |
|---|---|
| [Notebook integrado](notebooks/TPI_Analisis_de_Datos.ipynb) | Pipeline completo con explicaciones, gráficos y evaluación. Disponible en local y Colab. |
| [Informe ejecutivo](docs/INFORME_EJECUTIVO.pdf) | PDF de 19 páginas con ambas partes, modelos y conclusiones. |

## División de tareas

| Tarea | Descripción | Realizó |
|---|---|---|
| 1 | Creación del repositorio | Julián |
| 2 | Estructura inicial del repositorio y dataset original | Emmanuel |
| 3 | Plantilla de notebook con Colab y dataset provisorio | Matías |
| 4 | Problema de negocio e hipótesis analíticas | Matías |
| 5 | Relevamiento de variables: tipo teórico frente al `dtype` de Pandas | Emmanuel |
| 6 | Inspección y limpieza de `TotalCharges` | Julián |
| 7 | Tipos de datos, columnas calculadas y renombrado de columnas | Matías |
| 8 | Detección de valores atípicos con IQR | Julián |
| 9 | Revisión de calidad y dataset limpio final | Emmanuel |
| 10 | Estadística descriptiva de antigüedad y cargos | Julián |
| 11 | Correlaciones de Pearson y Spearman | Julián |
| 12 | Análisis categórico de la baja de clientes | Julián |
| 13 | Filtrado avanzado de clientes | Julián |
| 14 | Segmentación de clientes con `groupby` | Julián |
| 15 | Hallazgos del análisis exploratorio | Julián |
| 16 | Estilo común y exportación de gráficos | Matías |
| 17 | Histogramas con KDE de antigüedad y cargo mensual | Emmanuel |
| 18 | Mapa de calor de la correlación de Pearson | Julián |
| 19 | Tasa de baja por contrato y método de pago | Julián |
| 20 | Unificación y revisión de los gráficos | Julián |
| 21 | Partición de datos y codificación del objetivo | Matías |
| 22 | Codificación de variables categóricas | Matías |
| 23 | Escalado e integración del preprocesamiento | Matías |
| 24 | Verificación de ausencia de fuga de datos | Matías |
| 25 | Regresión lineal del cargo acumulado y su diagnóstico | Julián y Emmanuel |
| 26 | Modelo de clasificación: regresión logística | Emmanuel |
| 27 | Evaluación de la clasificación | Matías |
| 28 | Interpretación de los coeficientes del modelo | Emmanuel |
| 29 | Integración del notebook completo | Julián |
| 30 | Informe ejecutivo, parte 1 | Matías |
| 31 | Informe ejecutivo, parte 2 y PDF final | Emmanuel |
| 32 | README | Matías |
| 33 | Revisión final del repositorio | Julián |

## Ejecutar en Google Colab

1. Abrir el botón **Open in Colab** del encabezado: apunta al notebook integrado en `main`.
2. Conectar el entorno y elegir **Entorno de ejecución → Reiniciar sesión y ejecutar todas**.
3. Leer los resultados en orden. El notebook descarga el CSV original desde GitHub y genera los archivos intermedios durante la ejecución; requiere conexión a internet.
4. Descargar las salidas que se quieran conservar desde el panel **Archivos**. Los datos generados quedan en `data/processed/` y las figuras en `reports/figures/`. Los archivos de la sesión de Colab son temporales.

## Ejecutar en local

Se necesita Python 3 con `pip`. Clonar el repositorio y crear un entorno virtual:

```bash
git clone https://github.com/julianschmidt1/tpi-analisis-de-datos.git
cd tpi-analisis-de-datos
python -m venv .venv
```

Activar el entorno con el comando correspondiente:

| Terminal | Comando |
|---|---|
| Windows · PowerShell | `.venv\Scripts\Activate.ps1` |
| Windows · Git Bash | `source .venv/Scripts/activate` |
| Linux/macOS · Bash | `source .venv/bin/activate` |

Instalar las dependencias e iniciar Jupyter desde la raíz del repositorio:

```bash
python -m pip install -r requirements.txt
jupyter lab
```

Abrir `notebooks/TPI_Analisis_de_Datos.ipynb`, reiniciar el kernel y ejecutar todas las celdas en orden. El notebook utiliza el CSV original incluido en el repositorio y regenera las salidas. Las rutas se resuelven desde el directorio de ejecución o sus padres; las exportaciones pueden sobrescribir archivos generados de ejecuciones anteriores.

Los notebooks de `notebooks/trabajo/` contienen el desarrollo de cada tarea. Para reproducir el flujo completo, usar el notebook integrado.

## Stack

| Herramienta | Uso |
|---|---|
| Python | Lenguaje del análisis. |
| Pandas y NumPy | Carga, limpieza, transformación y cálculo numérico. |
| Matplotlib y Seaborn | Visualización y exportación de figuras. |
| SciPy | Cálculos estadísticos y soporte para correlaciones por rangos. |
| Scikit-learn | Partición, codificación, escalado, modelos y métricas. |
| JupyterLab / Google Colab | Ejecución y lectura de notebooks. |

Las dependencias están en [requirements.txt](requirements.txt). No se fijan versiones; los resultados numéricos pueden presentar pequeñas variaciones entre entornos.

## Estructura del repositorio

```text
├── data/
│   ├── raw/                       # CSV original, sin modificar
│   └── processed/                 # Datos limpios y matrices para modelado
│       ├── particion/             # Train/test sin transformar (tarea 21)
│       └── codificacion/          # Matrices codificadas sin escalar (tarea 22)
├── notebooks/
│   ├── TPI_Analisis_de_Datos.ipynb # Notebook integrado
│   └── trabajo/                   # Desarrollo individual por tarea
├── docs/                          # Informe, textos fuente y scripts para regenerarlo
│   ├── 30_informe_ejecutivo_parte1.md
│   ├── 31_informe_ejecutivo_parte2.md
│   ├── 31_resumen_ejecutivo.md
│   ├── 30_reproducir_eda.py        # Regenera evidencia de la parte 1
│   ├── 31_ensamblar_informe.py     # Genera el PDF final
│   └── INFORME_EJECUTIVO.pdf      # Informe ejecutivo completo
├── reports/
│   ├── figures/                   # Gráficos exportados en PNG
│   └── tables/                    # Tablas del informe en CSV
├── README.md
└── requirements.txt
```

El [CSV original](data/raw/WA_Fn-UseC_-Telco-Customer-Churn.csv) se conserva sin modificar. La limpieza genera [telco_clean.csv](data/processed/telco_clean.csv), con 7.043 clientes y 22 columnas: se elimina `customerID` y se agregan `ingreso_estimado` y `diferencia_facturacion`. `Churn` permanece como `Yes/No` en esta etapa y se codifica como `No=0`, `Yes=1` para clasificación.

La clasificación utiliza una partición 80/20 estratificada con `random_state=42`. Los codificadores y escaladores se ajustan solo con train. Las matrices finales `X_train.csv`, `X_test.csv`, `y_train.csv` e `y_test.csv` se exportan directamente en `data/processed/` y se leen con `index_col='fila_origen'`: el índice identifica clientes y no es un predictor. La regresión lineal tiene su propia partición.

Para regenerar únicamente las tablas y figuras de la primera parte del informe, ejecutar desde la raíz:

```bash
python docs/30_reproducir_eda.py
```

Para regenerar el informe en PDF (requiere `markdown`, incluido en `requirements.txt`, y Google Chrome o Microsoft Edge):

```bash
python docs/31_ensamblar_informe.py
```
