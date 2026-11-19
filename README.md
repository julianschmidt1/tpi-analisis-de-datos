# TPI – Introducción al Análisis de Datos (Predicción de Churn en Telco)

> Esqueleto provisorio. La versión final (tarea 6D del plan) incluirá la descripción del problema, el badge de Colab y la guía completa.

- **Materia:** Introducción al Análisis de Datos – UTN FRA, División 343, 2.º cuatrimestre 2026
- **Integrantes:** Matías, Julián y Emmanuel
- **Dataset:** Telco Customer Churn (Kaggle)

## Estructura del repositorio
```
├── data/
│   ├── raw/          # Dataset original (no se modifica)
│   └── processed/    # Datasets depurados y transformados
├── notebooks/
│   ├── trabajo/      # Notebooks de trabajo por tarea
│   └── TPI_Analisis_de_Datos.ipynb   # Notebook final (pendiente)
├── docs/
│   └── INFORME_EJECUTIVO.pdf         # Informe final (pendiente)
├── reports/figures/  # Gráficos exportados
├── PLAN_TAREAS.md    # Reparto de tareas y reglas de trabajo
└── requirements.txt
```

Las reglas de trabajo (ramas, commits, revisión cruzada) están en [PLAN_TAREAS.md](PLAN_TAREAS.md).

## Plantilla y datos provisorios (tarea 3)

[![Open in Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/julianschmidt1/tpi-analisis-de-datos/blob/main/notebooks/trabajo/3_plantilla.ipynb)

La [plantilla de notebook](notebooks/trabajo/3_plantilla.ipynb) carga el CSV original desde GitHub en Colab o desde `data/raw/` en local. Al ejecutar todas sus celdas, genera `data/processed/telco_provisorio.csv`: solo convierte `TotalCharges` a numérico y conserva los nulos para la limpieza posterior.

Para ejecutarla en local, instalar las dependencias con `pip install -r requirements.txt` e iniciar `jupyter lab` desde el repositorio. El badge estará disponible cuando el notebook se integre en `main`.

## Problema de negocio e hipótesis (tarea 4)

El [notebook de fundamentos](notebooks/trabajo/4_problema_hipotesis.ipynb) define el problema de negocio, la variable objetivo `Churn` y tres hipótesis sobre contrato, antigüedad y cargo mensual. También explica por qué el dataset es estructurado y cómo se evaluarán las hipótesis durante el EDA. Contiene únicamente texto en Markdown y no requiere ejecutar código.

## Tipos y columnas calculadas (tarea 7)

El [notebook de transformación](notebooks/trabajo/7_tipos_columnas.ipynb) carga `data/processed/telco_step1.csv`, elimina `customerID`, convierte `SeniorCitizen` a `No/Yes` y las variables categóricas a `category`. Agrega `ingreso_estimado` y `diferencia_facturacion` y exporta `data/processed/telco_step2.csv`, con 7.043 clientes y 22 columnas.

Se ejecuta completo en local o en Colab; en Colab la entrada se obtiene desde GitHub y la salida queda en el panel Archivos. Como CSV no conserva los tipos categóricos, el notebook incluye el esquema `tipos_esperados` y verifica su recuperación con `pd.read_csv(ruta, dtype=tipos_esperados)`.

## Partición para preprocesamiento (tarea 21)

El [notebook de partición](notebooks/trabajo/21_particion_datos.ipynb) separa `Churn` de los predictores, codifica `No=0` y `Yes=1` y divide el dataset limpio en entrenamiento y prueba (80/20), con estratificación y `random_state=42`.

Exporta los cuatro conjuntos sin transformar a `data/processed/particion/`. Para continuar en las tareas 22 y 23, leer los CSV con `index_col='fila_origen'` y ajustar codificadores y escaladores solo con entrenamiento. El índice identifica filas y no debe usarse como predictor.

## Codificación de variables (tarea 22)

El [notebook de codificación](notebooks/trabajo/22_codificacion.ipynb) utiliza la partición de la tarea 21. Aplica One-Hot completo a las nominales, incluido `PaymentMethod`, y codifica `Contract` como mensual=0, un año=1 y dos años=2. Los codificadores se ajustan solo con entrenamiento; test se transforma con las categorías aprendidas.

Exporta 46 predictores numéricos sin escalar a `data/processed/codificacion/`. El notebook incluye el esquema para integrarlo con el escalado en la tarea 23 y verifica el orden contractual, la alineación de etiquetas y la conservación de las variables numéricas. En Colab requiere cargar los cuatro CSV de la tarea 21 en `data/processed/particion/`.

## Estilo común de gráficos (tarea 16)

El [notebook de estilo y exportación](notebooks/trabajo/16_estilo_graficos.ipynb) contiene una celda lista para copiar a los notebooks de visualización. Define paleta, fuentes y tamaños, los colores de `Churn` (`No` azul, `Yes` naranja) y `guardar_figura(fig, nombre)`, que exporta PNG a 300 dpi en `reports/figures/`.

Incluye un ejemplo de proporciones de churn exportado a `reports/figures/16_ejemplo_churn.png`. En local y Colab utiliza `telco_clean.csv` si está disponible y, mientras tanto, `telco_provisorio.csv`, identificando la fuente en el gráfico. En Colab se puede descargar la imagen desde el panel Archivos.

## Escalado y preprocesamiento integrado (tarea 23)

El [notebook de escalado](notebooks/trabajo/23_escalado.ipynb) lee la partición original de la tarea 21 e integra en `preprocessor` la codificación de la tarea 22 y `StandardScaler` para las cinco variables numéricas, incluidas las calculadas. Compara las escalas de entrenamiento con `MinMaxScaler`; ambos se ajustan exclusivamente con train. La salida final utiliza StandardScaler.

Exporta `X_train.csv`, `X_test.csv`, `y_train.csv` e `y_test.csv` directamente en `data/processed/`: 5.634 filas de entrenamiento, 1.409 de prueba y 46 predictores. Para modelado, leer con `pd.read_csv(ruta, index_col='fila_origen')`; en las etiquetas seleccionar `Churn`. No incluir el índice como predictor ni volver a escalar estas matrices. El notebook verifica media cercana a cero y desvío poblacional cercano a uno en train, alineación de etiquetas y lectura de las exportaciones.

En local requiere los cuatro CSV de `data/processed/particion/`. En Colab, cargar esos archivos conservando la estructura de carpetas. El objeto ajustado `preprocessor` queda en memoria; los CSV no lo serializan. La revisión transversal del flujo corresponde a la tarea 24.
