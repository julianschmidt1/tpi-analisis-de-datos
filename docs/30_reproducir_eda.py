"""Regenera las tablas y figuras de la parte 1: python docs/30_reproducir_eda.py."""
from pathlib import Path
import json

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.ticker import PercentFormatter
import pandas as pd

RAIZ = Path(__file__).resolve().parents[1]
df = pd.read_csv(RAIZ / 'data/processed/telco_clean.csv')
assert df.shape == (7043, 22) and not df.isna().any().any()
assert df.Churn.isin(['Yes', 'No']).all()
numericas = df[['tenure', 'MonthlyCharges', 'TotalCharges']]
resumen = pd.DataFrame({
    'media': numericas.mean(), 'mediana': numericas.median(),
    'modas': [s.mode().tolist() for _, s in numericas.items()],
    'desvio_muestral': numericas.std(), 'minimo': numericas.min(),
    'maximo': numericas.max(), 'rango': numericas.max() - numericas.min(),
    'q1': numericas.quantile(.25), 'q3': numericas.quantile(.75),
    'iqr': numericas.quantile(.75) - numericas.quantile(.25),
    'asimetria': numericas.skew(), 'exceso_curtosis': numericas.kurt(),
})
y = df.Churn.eq('Yes')
mediana = df.MonthlyCharges.median()
def segmentar(grupo):
    return pd.DataFrame({'clientes': y.groupby(grupo).size(),
                         'bajas': y.groupby(grupo).sum(),
                         'tasa_porcentaje': 100 * y.groupby(grupo).mean()})

tablas = {'estadisticas': resumen,
          'pearson': numericas.corr(), 'spearman': numericas.corr(method='spearman'),
          'contrato': segmentar(df.Contract), 'internet': segmentar(df.InternetService),
          'pago': segmentar(df.PaymentMethod),
          'antiguedad': segmentar(df.tenure.le(12).map({True: 'Hasta 12 meses', False: 'Mas de 12 meses'})),
          'cargo': segmentar(df.MonthlyCharges.gt(mediana).map({True: 'Superior a mediana', False: 'Hasta mediana'}))}
salida = RAIZ / 'reports/tables'
salida.mkdir(parents=True, exist_ok=True)
for nombre, tabla in tablas.items():
    tabla.to_csv(salida / f'30_{nombre}.csv', encoding='utf-8', index_label='variable_o_segmento')

# Copiar la configuración canónica de la tarea 16 sin ejecutar sus ejemplos.
plantilla = json.loads((RAIZ / 'notebooks/trabajo/16_estilo_graficos.ipynb').read_text(encoding='utf-8'))
fuente = next(''.join(c['source']) for c in plantilla['cells']
              if c['cell_type'] == 'code' and 'def aplicar_estilo' in ''.join(c['source']))
import seaborn as sns
exec(fuente[fuente.index('TAMANO_FIGURA ='):])

fig, axes = plt.subplots(1, 3, figsize=(12, 4.5), layout='constrained')
for ax, columna, titulo, unidad in zip(axes, numericas.columns,
        ['Antigüedad', 'Cargo mensual', 'Cargo acumulado'],
        ['Meses', 'Unidades monetarias', 'Unidades monetarias']):
    ax.hist(df[columna], bins=20, color='#0072B2', edgecolor='white')
    ax.axvline(df[columna].median(), color='#D55E00', label='Mediana')
    ax.set(title=titulo, xlabel=unidad, ylabel='Clientes')
    ax.legend()
fig.suptitle('Distribuciones de antigüedad y cargos · 7.043 clientes')
guardar_figura(fig, '30_distribuciones')
plt.close(fig)

fig, ax = plt.subplots(layout='constrained')
contratos = tablas['contrato'].reindex(['Month-to-month', 'One year', 'Two year'])
barras = ax.bar(['Mensual', 'Un año', 'Dos años'], contratos.tasa_porcentaje / 100,
                color=['#D55E00', '#0072B2', '#009E73'])
ax.bar_label(barras, labels=[f'{v:.2f} %' for v in contratos.tasa_porcentaje], padding=5)
ax.set(title='Tasa de abandono según contrato', xlabel='Modalidad de contrato',
       ylabel='Porcentaje de bajas dentro del segmento', ylim=(0, .55))
ax.yaxis.set_major_formatter(PercentFormatter(1))
ax.xaxis.grid(False)
fig.supxlabel('Fuente: telco_clean.csv · 7.043 clientes', fontsize=9)
guardar_figura(fig, '30_churn_contrato')
plt.close(fig)
print(f'Tablas: reports/tables/30_*.csv; figuras: reports/figures/30_*.png')
print(f'Clientes: {len(df)}; bajas: {y.sum()}; tasa: {y.mean():.4%}; mediana mensual: {mediana}')
