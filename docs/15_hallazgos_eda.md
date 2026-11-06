# Tarea 15 · Hallazgos del análisis exploratorio

**Responsable según el plan** — Emmanuel

Los puntos 10 a 14 se ejecutaron con `data/processed/telco_provisorio.csv`. La cartera tiene 7.043 clientes, de los cuales 1.869 figuran como bajas (26,54 %). Las tasas por segmento se calculan sobre los clientes de cada grupo. Para el informe final, repetir los cálculos con `telco_clean.csv`.

1. **El contrato mensual concentra las bajas (puntos 12 y 14).** Se dieron de baja 1.655 de los 3.875 clientes con contrato mensual (42,71 %). La tasa baja al 11,27 % en contratos de un año y al 2,83 % en los de dos años. El contrato mensual reúne cerca del 89 % de todas las bajas observadas.
2. **Entre los clientes recientes, el filtro de contrato mensual o cheque electrónico identifica un grupo con más bajas (punto 13).** Entre los clientes con hasta seis meses de antigüedad que tenían contrato mensual o pagaban con cheque electrónico, se dieron de baja 781 de 1.419 (55,04 %). Esa tasa supera la de la cartera en 28,50 puntos porcentuales.
3. **Fibra óptica combina cargos mensuales altos y una proporción alta de bajas (puntos 12 y 14).** Los 3.096 clientes de fibra pagaban en promedio 91,50 al mes y registraron una tasa de baja del 41,89 %. En DSL, el promedio fue de 58,10 y la tasa de baja, del 18,96 %.
4. **El cheque electrónico registra la mayor tasa de baja entre los métodos de pago (puntos 12 y 14).** Se dieron de baja 1.071 de 2.365 clientes de ese grupo (45,29 %), frente al 16,71 % con transferencia bancaria automática y al 15,24 % con tarjeta de crédito automática.
5. **El promedio del cargo acumulado supera a la mediana (punto 10).** La media de 2.283,30 supera a la mediana de 1.397,48. La asimetría positiva (0,96) muestra que los cargos altos elevan el promedio. La mediana describe mejor el centro de la distribución en este caso. El cálculo usa 7.032 clientes con cargo acumulado registrado.
6. **El cargo acumulado está más asociado con la antigüedad que con el cargo mensual (punto 11).** Para antigüedad y cargo acumulado, Pearson da 0,826 y Spearman da 0,889. Para cargo mensual y acumulado, los valores son 0,651 y 0,638. En estos datos, los clientes con más meses de servicio tienden a estar más arriba en el orden de cargos acumulados.

Los segmentos pueden compartir clientes. Las diferencias entre grupos describen asociaciones observadas. Para evaluar si se sostienen, se pueden comparar clientes con condiciones similares de contrato, servicio y antigüedad.
