# Plan de tareas – TPI Introducción al Análisis de Datos (Div. 343)

**Dataset:** Telco Customer Churn (Kaggle) · **Entrega y defensa:** martes 24/11/2026 (Clase 15; la consigna y el aula dicen 23/11 20:30, confirmar la hora límite en el campus) · **Recuperatorio:** 1/12
**Integrantes (3, aprobado por el docente):** Matías (**M**) · Julián (**J**) · Emmanuel (**E**)

> Cómo leer este documento: el TPI se divide en **piezas** (Setup, Fundamentos y limpieza, EDA, Visualización, Preprocesamiento, Modelado, Integración e informe, Defensa). Cada pieza es independiente de las demás gracias a **contratos de datos** (sección 2). Dentro de cada pieza, las tareas están repartidas entre los tres, y quien lleva la parte más pesada rota de pieza en pieza. Así los tres tocan todo el pipeline, que es lo que exige la defensa individual.

---

## 1. Reglas de trabajo (leer antes de empezar)

**Git**
- Cada uno configura su identidad antes del primer commit: `git config user.name "..."` y `git config user.email "..."` (el mismo correo que usa en GitHub, para que los commits cuenten como suyos).
- `main` solo se actualiza por Pull Request (PR). Nadie hace push directo a `main`.
- Una rama por tarea: `feat/<id-tarea>-<tema>`, por ejemplo `feat/6-totalcharges`.
- Mensajes de commit descriptivos, en español, en imperativo y con el id de la tarea: `6: convierte TotalCharges a numérico y trata 11 nulos`. Nada de "cambios" ni "update".
- **Revisión cruzada obligatoria:** M revisa los PR de J, J revisa los de E, E revisa los de M. Quien revisa también tiene que poder explicar el código en la defensa.
- Commits chicos y frecuentes. El historial de `git log` es parte de la nota (rúbrica: Colab, Repositorio Git e Informe, 20%).

**Notebooks** (los `.ipynb` generan conflictos de merge feos)
- Cada tarea tiene **su propio notebook** en `notebooks/trabajo/<n>_<tema>.ipynb` (por ejemplo `6_totalcharges.ipynb`, donde `<n>` es el número de tarea). Nunca dos personas editan el mismo `.ipynb`.
- Usar el [formato común de los notebooks](#formato-común-de-los-notebooks) al empezar una tarea.
- El notebook final `notebooks/TPI_Analisis_de_Datos.ipynb` lo arma **una sola persona (J, tarea 29)** copiando las celdas de los notebooks de trabajo en orden.
- Cada celda de código lleva un comentario o markdown arriba que explique **qué** hace y **por qué**, y cada gráfico o tabla lleva su interpretación orientada al negocio (lo pide la consigna).
- Nunca rutas absolutas del tipo `F:\...`. Todo con rutas relativas al repo, para que funcione en Colab.

#### Formato común de los notebooks

Usar [el notebook del punto 3](notebooks/trabajo/3_plantilla.ipynb) como plantilla y adaptar estas partes a la tarea:

1. **Encabezado.** Título con el formato `Tarea <n> · <tema>`, botón **Open in Colab**, datos del TPI, integrantes, responsable y un párrafo con el objetivo y los archivos de entrada y salida, si corresponde.
2. **Cómo ejecutarlo.** Indicar los pasos para correr todas las celdas en local y en Colab. El botón debe abrir el notebook en la rama publicada durante la revisión y apuntar a `main` para la versión integrada.
3. **Secciones numeradas.** Organizar el trabajo en secciones como `## 1. Carga de datos`. Antes de cada celda de código, explicar en Markdown qué hace y por qué. Después de cada tabla o gráfico, explicar qué muestra y qué significa para el problema de negocio.
4. **Carga y exportación.** Si la tarea usa datos del repo, seguir la celda de carga de la plantilla. En local, buscar el archivo desde el directorio de ejecución o sus padres. En Colab, leer desde GitHub cuando el archivo ya esté publicado, o indicar cómo obtenerlo si se genera en una tarea previa. Guardar las salidas en las rutas relativas acordadas en los contratos de datos y aclarar dónde encontrarlas.
5. **Verificación.** Antes de abrir el PR, reiniciar el entorno y ejecutar todas las celdas en orden. Comprobar el criterio de terminado de la tarea y verificar que el botón de Colab abre el notebook publicado.

**Calidad**
- `random_state=42` en todo lo que lo admita.
- El notebook final tiene que correr en Colab con *Runtime → Reiniciar y ejecutar todo* sin errores.
- Un PR no se mergea sin su revisor y sin que la tarea cumpla su criterio de "terminado".

**Tamaños:** S ≈ 1 h · M ≈ 2 h · L ≈ 3 h o más.

---

## 2. Contratos de datos (acordar antes de repartirse a trabajar)

Estos acuerdos permiten que las piezas avancen en paralelo sin esperarse.

| Archivo / objeto | Lo produce | Contenido |
|---|---|---|
| `data/raw/WA_Fn-UseC_-Telco-Customer-Churn.csv` | 2 | Dataset original. **No se modifica nunca.** |
| `data/processed/telco_provisorio.csv` | 3 | Versión rápida: solo `TotalCharges` convertido a numérico, nulos sin tratar. Sirve para desbloquear a los demás el día 1. |
| `data/processed/telco_step1.csv` | 6 | `TotalCharges` numérico y nulos tratados. |
| `data/processed/telco_step2.csv` | 7 | Tipos corregidos, columnas renombradas o eliminadas, columnas calculadas. |
| **`data/processed/telco_clean.csv`** | 9 | **Dataset limpio final.** Es el dato de entrada de las piezas de EDA, visualización, preprocesamiento y modelado. |
| `data/processed/X_train.csv`, `X_test.csv`, `y_train.csv`, `y_test.csv` | Preprocesamiento | Datos ya transformados y particionados. Los usa el modelado. |

**Reglas del esquema limpio** (`telco_clean.csv`):
- Se mantienen los nombres originales `tenure`, `MonthlyCharges`, `TotalCharges` y `Churn`, porque la consigna los nombra.
- `Churn` queda como texto `Yes/No` en el dataset limpio. La codificación a 0/1 se hace en la pieza de preprocesamiento.
- `TotalCharges` es `float64`, sin nulos.
- Se elimina `customerID` (no aporta al análisis) y se agregan las columnas calculadas definidas en 7.
- Las columnas categóricas quedan como `category`.

**Nombres que usan todos:** `df` (dataset limpio), `X_train`, `X_test`, `y_train`, `y_test`, `preprocessor` (el `ColumnTransformer`).

---

## 3. Decisiones abiertas (resolver entre los tres, anotar el resultado en el informe)

1. **¿Qué hacer con las filas de `TotalCharges` vacío?** En la versión pública del dataset son pocas (alrededor de 11, de clientes con `tenure = 0`; verificar al cargarlo). Opciones: imputar con 0 o eliminarlas. Decide quien hace 6 y lo justifica por escrito.
2. **`PaymentMethod`**: One-Hot completo, o agrupar por tasa de churn (automático vs manual). La Clase 7 pide justificarlo en el informe.
3. **`Contract`**: Ordinal Encoding (`Month-to-month` < `One year` < `Two year`), con su fundamento teórico en el informe.
4. **Modelo de clasificación único**: la consigna pide uno. Propuesta: Regresión Logística, por ser interpretable y por tener ya un ejemplo en Clase 7.
5. **Variable de la regresión lineal**: la consigna sugiere `TotalCharges`. Propuesta: `TotalCharges ~ tenure` (simple, un solo predictor).
6. **Notebooks de trabajo**: la consigna pide una estructura "estricta". Preguntarle al docente si se tolera `notebooks/trabajo/` en el repo final. Si no, se borra al terminar 29.
7. **Hora límite exacta de la entrega** en el campus.

---

## 4. Calendario sugerido

| Hito | Fecha límite | Piezas |
|---|---|---|
| H1 | vie 6/11 | Setup (tareas 1 a 3) y Fundamentos y limpieza (4 a 9) |
| H2 | vie 13/11 | EDA (10 a 15), Visualización (16 a 20) y Preprocesamiento (21 a 24) |
| H3 | mié 18/11 | 5 (modelos) y 29 (notebook integrado y corriendo en Colab) |
| H4 | dom 22/11 | 30 y 31 (informe PDF y README) y 7 (defensa) |
| Colchón | lun 23/11 | Revisión final, ensayo de la exposición |
| **Entrega** | **mar 24/11** | |

Las clases 10 a 14 todavía no se dictaron. Si traen contenido de modelos (regresión, clasificación, métricas), hay que contrastarlo con la pieza de modelado antes de cerrarla.

---

## 5. Piezas y tareas

Cada tarea indica: **responsable**, **tamaño**, **depende de**, **entrada → salida** y **criterio de terminado**. Marcar con `[x]` al mergear el PR.

### Pieza «Setup» – Setup del repositorio  *(consigna: D, Reproducibilidad)*

- [ ] **1 · Julián · S** · Crear el repositorio público en GitHub, `main` protegido, invitar a Matías y Emmanuel como colaboradores. Agregar este plan al repo.
  *Terminado:* los tres pueden hacer push de ramas y abrir PR.
- [ ] **2 · Emmanuel · S** · Crear la estructura de carpetas (`data/raw`, `data/processed`, `notebooks`, `notebooks/trabajo`, `docs`, `reports/figures`), `.gitignore`, `requirements.txt` y subir el CSV a `data/raw/`. Depende de: 1.
  *Terminado:* la estructura coincide con la consigna y el dataset se puede leer con `pd.read_csv`.
- [ ] **3 · Matías · S** · Crear la plantilla de notebook con el badge "Open in Colab", la celda de carga de datos que funciona tanto en Colab (URL raw de GitHub) como en local, y generar `telco_provisorio.csv`. Depende de: 2.
  *Terminado:* el badge abre el notebook en Colab y la celda de carga funciona.

### Pieza «Fundamentos y limpieza» – Fundamentos y limpieza  *(consigna: A · notebooks `<n>_…`)*

- [ ] **4 · Matías · M** · Definir el problema de negocio, redactar al menos 3 hipótesis analíticas, identificar la variable objetivo y justificar que el dataset es **estructurado**.
  *Entrada:* ninguna. *Salida:* sección de texto en markdown. *Terminado:* hipótesis comprobables con los datos.
- [ ] **5 · Emmanuel · M** · Tabla de relevamiento de las 21 variables: tipo teórico (cualitativa nominal/ordinal, cuantitativa discreta/continua) frente al `dtype` que asigna Pandas, con las discrepancias señaladas.
  *Entrada:* `data/raw`. *Salida:* tabla en markdown. *Terminado:* ninguna variable sin clasificar y cada discrepancia comentada.
- [ ] **6 · Julián · L** · **Tarea crítica.** Carga, inspección (`shape`, `info`, `describe`, duplicados) y tratamiento de `TotalCharges` (espacios `" "` → NaN → `to_numeric`). Decidir y justificar el tratamiento de los nulos (decisión abierta 1). Depende de: 2.
  *Entrada:* `data/raw`. *Salida:* `telco_step1.csv`. *Terminado:* `TotalCharges` es `float64`, sin nulos, y hay una justificación escrita.
- [ ] **7 · Matías · M** · Adecuación de `dtypes` (`category`, `SeniorCitizen` 0/1 → Yes/No si se decide), renombrado de columnas, eliminar `customerID`, crear columnas calculadas por aritmética directa (propuesta: `ingreso_estimado = MonthlyCharges * tenure` y `diferencia_facturacion = TotalCharges - ingreso_estimado`). Depende de: 6.
  *Entrada:* `telco_step1.csv`. *Salida:* `telco_step2.csv`. *Terminado:* `df.info()` muestra solo los tipos esperados.
- [ ] **8 · Julián · M** · Detección de outliers con IQR y boxplot en `tenure`, `MonthlyCharges` y `TotalCharges`. Decidir y justificar si se conservan o se tratan. Depende de: 6.
  *Entrada:* `telco_step1.csv`. *Salida:* análisis más decisión escrita (no modifica el dataset). *Terminado:* cantidad de outliers por variable y decisión fundamentada.
- [ ] **9 · Emmanuel · M** · Aplicar la decisión de 8 si corresponde, chequeo de calidad de datos (completitud, validez, unicidad, consistencia, como en Clase 1) y exportar `telco_clean.csv`. Depende de: 7 y 8.
  *Entrada:* `telco_step2.csv`. *Salida:* **`telco_clean.csv`**. *Terminado:* cumple todas las reglas del esquema limpio de la sección 2.

### Pieza «EDA» – Manipulación y estadística exploratoria  *(consigna: A Pandas y B EDA · notebooks `<n>_…`)*

*Empieza con `telco_provisorio.csv` y pasa a `telco_clean.csv` cuando 9 esté mergeado.*

- [ ] **10 · Julián · M** · Tendencia central (media, mediana, moda) y dispersión (desvío, rango, IQR, asimetría y curtosis) de `tenure`, `MonthlyCharges` y `TotalCharges`, con interpretación.
  *Terminado:* tabla resumen más una interpretación por variable.
- [ ] **11 · Matías · M** · Correlación lineal Pearson y Spearman entre las tres variables numéricas, con interpretación de la relación.
  *Terminado:* ambas matrices calculadas y comentadas, incluida la diferencia entre las dos.
- [ ] **12 · Emmanuel · M** · Análisis categórico: frecuencias absolutas y relativas y tablas de contingencia (`crosstab` normalizado) de las variables sociodemográficas y de contratación frente a `Churn`.
  *Terminado:* tablas para las variables relevantes y 3 hallazgos redactados.
- [ ] **13 · Matías · S** · Filtrado avanzado con múltiples condiciones (`&` y `|`): al menos 3 consultas con sentido de negocio (por ejemplo, clientes con contrato mensual, fibra óptica y alto cargo mensual).
  *Terminado:* consultas con paréntesis correctos y el resultado explicado.
- [ ] **14 · Julián · M** · `groupby` con múltiples agregaciones (promedio, conteo, suma) para segmentar el negocio por contrato, servicio de internet y método de pago.
  *Terminado:* al menos 2 segmentaciones con `.agg(...)` y su interpretación.
- [ ] **15 · Emmanuel · S** · Resumen de hallazgos del EDA: lista de los 5 a 7 hallazgos más importantes de 10 a 14, para reutilizar en el informe y la defensa. Depende de: 10 a 14.
  *Terminado:* lista redactada en `docs/` o en el notebook.

### Pieza «Visualización» – Visualización  *(consigna: B Visualización · notebooks `<n>_…`)*

- [ ] **16 · Matías · S** · Estilo común de gráficos (paleta, tamaño, fuentes) y función para exportar figuras a `reports/figures/`. **Hacerla primero**, para que los demás la usen.
  *Terminado:* la función existe y está documentada en una celda que los demás pueden copiar.
- [ ] **17 · Emmanuel · M** · Histogramas con KDE de `tenure` y `MonthlyCharges`, con interpretación orientada al negocio. Depende de: 16.
  *Terminado:* dos gráficos con título, ejes rotulados e interpretación.
- [ ] **18 · Matías · S** · Heatmap de la matriz de correlación con anotaciones, con su interpretación. Depende de: 16.
  *Terminado:* gráfico legible y comentado.
- [ ] **19 · Julián · M** · Diagramas de barras de la tasa de churn por tipo de contrato y por método de pago, con interpretación. Depende de: 16.
  *Terminado:* dos gráficos que muestran la **tasa** (no el conteo) y la lectura de negocio.
- [ ] **20 · Julián · S** · Revisión transversal de coherencia visual de todos los gráficos de la pieza antes de mergear. Depende de: 17 a 19.
  *Terminado:* mismo estilo en todos y ninguna figura sin interpretación.

### Pieza «Preprocesamiento» – Preprocesamiento  *(consigna: C Preprocesamiento · notebooks `<n>_…` · tiene orden estricto)*

> Orden interno obligatorio por riesgo de *data leakage*: primero partir, después ajustar (`fit`) **solo con train**, y recién después transformar test.

- [ ] **21 · Matías · M** · **Primero.** Separar `X` e `y`, codificar el target (`Churn` → 0/1 con `LabelEncoder`) y hacer `train_test_split` 80/20 **estratificado** con `random_state=42`.
  *Entrada:* `telco_clean.csv`. *Terminado:* proporciones de churn casi idénticas en train y test.
- [ ] **22 · Emmanuel · L** · Codificación: One-Hot para las nominales (decisión abierta 2), `OrdinalEncoder` para `Contract` (decisión 3), con `fit` solo en train. Depende de: 21.
  *Terminado:* sin columnas de texto, y el orden ordinal verificado.
- [ ] **23 · Julián · L** · Escalado de `tenure`, `MonthlyCharges` y `TotalCharges` (`StandardScaler`, y probar `MinMaxScaler` para comparar), y armado del `ColumnTransformer` integrando la codificación de la tarea 22. Exportar `X_train`, `X_test`, `y_train` e `y_test`. Depende de: 21 (puede arrancar en paralelo con 22 y luego integrar).
  *Terminado:* media ≈ 0 y desvío ≈ 1 en train, archivos exportados.
- [ ] **24 · Matías · S** · Verificación anti-leakage: comprobar que ningún `fit` vio el test, y documentar el orden de las operaciones. Revisa 22 y 23. Depende de: 22 y 23.
  *Terminado:* lista de comprobaciones marcadas en el notebook.

### Pieza «Modelado» – Modelado y evaluación  *(consigna: C Modelos · notebooks `<n>_…`)*

> Estas clases todavía no se dictaron. Antes de cerrar, contrastar con lo que enseñe el docente.

- [ ] **25 · Julián · M** · Regresión lineal simple (`TotalCharges ~ tenure`, decisión 5): ajuste, **R²** y **MAE** sobre test, e interpretación del coeficiente.
  *Entrada:* `telco_clean.csv`, con su propia partición 80/20. *Terminado:* métricas calculadas y comentadas.
- [ ] **26 · Emmanuel · M** · Modelo de clasificación único (Regresión Logística, decisión 4) entrenado con los datos de la pieza de preprocesamiento, con justificación de la elección. Depende de: 23.
  *Entrada:* `X_train`, `y_train`. *Terminado:* modelo entrenado, sin `fit` sobre test.
- [ ] **27 · Matías · M** · Evaluación: **matriz de confusión**, **exactitud (accuracy)** e interpretación de errores de negocio (falsos negativos frente a falsos positivos), comparada con una línea base (predecir siempre la clase mayoritaria). Depende de: 26.
  *Terminado:* matriz graficada e interpretada, línea base calculada.
- [ ] **28 · Emmanuel · S** · Interpretación de los coeficientes del modelo (qué variables empujan al churn) para las conclusiones del informe. Depende de: 26.
  *Terminado:* 3 a 5 variables destacadas con su lectura de negocio.

### Pieza «Integración, informe y README» – Integración, informe y README  *(consigna: entregables, 20% de la nota)*

- [ ] **29 · Julián · L** · Integrar las celdas de los notebooks de trabajo en `TPI_Analisis_de_Datos.ipynb`, en orden, con el badge de Colab. Probar *Reiniciar y ejecutar todo* en Colab y arreglar rutas. Depende de: todas las piezas anteriores (limpieza a modelado).
  *Terminado:* corre completo en Colab de forma limpia y secuencial, sin errores.
- [ ] **30 · Matías · L** · Informe ejecutivo, parte 1: **carátula** (materia, título, integrantes, fecha), resumen ejecutivo, problema de negocio, metodología, limpieza y EDA estadístico. Depende de: las piezas de limpieza y EDA.
  *Terminado:* secciones redactadas con tablas y gráficos incluidos.
- [ ] **31 · Emmanuel · L** · Informe ejecutivo, parte 2: visualización, preprocesamiento, justificación de modelos, métricas, **conclusiones estratégicas** y ensamblado a `docs/INFORME_EJECUTIVO.pdf`. Depende de: las piezas de visualización a modelado y de 30.
  *Terminado:* PDF único, con carátula y numeración.
- [ ] **32 · Matías · S** · README final: título, descripción, integrantes y división, badge de Colab, stack (Python, Pandas, NumPy, Scikit-Learn, Seaborn…) y guía de la estructura. Depende de: 29.
  *Terminado:* los cinco puntos que pide la consigna están presentes.
- [ ] **33 · Julián · S** · Revisión final del repo: estructura contra la consigna, que no haya archivos sobrantes, historial de commits de los tres, enlace publicado y entregado en el campus. Depende de: 29 a 32.
  *Terminado:* lista de chequeo de la consigna completa y enlace entregado.

### Pieza «Defensa» – Defensa oral  *(consigna: 5 Evaluación, 15% de la nota)*

- [ ] **34 · Matías · M** · Presentación de 12 a 15 min: portada, problema, hipótesis, limpieza y EDA (la parte de Matías, unos 4 min). Armar la estructura de diapositivas para los tres.
- [ ] **35 · Julián · M** · Su parte: visualización y hallazgos del EDA (unos 4 min), más el banco de preguntas de defensa sobre las piezas de limpieza, EDA y visualización.
- [ ] **36 · Emmanuel · M** · Su parte: preprocesamiento, modelos, métricas y conclusiones (unos 5 min), más el banco de preguntas sobre las piezas de preprocesamiento y modelado.
- [ ] **37 · Los tres · M** · **Ensayo cruzado:** cada uno le hace preguntas a los otros sobre piezas que **no** desarrolló. Cronometrar la exposición.
  *Terminado:* cada uno puede explicar cualquier celda del notebook y justificar cada decisión metodológica.

---

## 6. Carga por persona (aproximada)

| | Tareas | Perfil de carga |
|---|---|---|
| **Matías** | 3, 4, 7, 11, 13, 16, 18, 21, 24, 27, 30, 32, 34 (+37) | Más tareas, pero chicas |
| **Julián** | 1, 6, 8, 10, 14, 19, 20, 23, 25, 29, 33, 35 (+37) | Integración técnica en Colab |
| **Emmanuel** | 2, 5, 9, 12, 15, 17, 22, 26, 28, 31, 36 (+37) | Datos críticos y cierre del informe |

La carga se reajusta si alguna tarea resulta más pesada de lo previsto: quien termine antes toma tareas de otro. Registrar el cambio en este archivo.

---

## 7. Mapa de dependencias

```
1 ─► 2 ─► 3 ──► (telco_provisorio.csv libera a EDA, visualización y preprocesamiento desde el día 1)
        │
        └─► 6 ─► 7 ─┐
              └─► 8 ─┴─► 9 ─► telco_clean.csv ─┬─► 10-15
                                                  ├─► 16 ─► 17,18,19 ─► 20
                                                  ├─► 21 ─► 22,23 ─► 24
                                                  └─► 25
                                      23 ─► 26 ─► 27, 28
 limpieza a modelado ─► 29 ─► 32 ─► 33        10-15 ─► 30 ─► 31        todo ─► 34-37
```
