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
