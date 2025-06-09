import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

# Configurar el estilo de los gráficos
plt.style.use('seaborn-v0_8')
sns.set_palette("husl")

# Cargar los datos
# df = pd.read_csv('benchmark_resultados.csv')
df = pd.read_csv('benchmark_resultados2.csv')

# Limpiar y procesar los datos
# Extraer el nombre del test de la columna 'name'
df['test_name'] = df['name'].str.extract(r'::(\w+)$')
df['test_category'] = df['test_name'].str.replace('test_', '').str.replace('_benchmark', '')

# Convertir tiempos a milisegundos para mejor legibilidad
time_columns = ['min', 'max', 'mean', 'stddev', 'median', 'iqr']
for col in time_columns:
    df[f'{col}_ms'] = df[col] * 1000

# Crear figura con subplots
fig, axes = plt.subplots(2, 2, figsize=(15, 12))
fig.suptitle('Análisis de Rendimiento - Benchmarks de Password Entry', fontsize=16, fontweight='bold')

# 1. Comparación de tiempos promedio por operación
ax1 = axes[0, 0]
operation_stats = df.groupby('test_category').agg({
    'mean_ms': 'mean',
    'stddev_ms': 'mean'
}).reset_index()

bars = ax1.bar(operation_stats['test_category'], operation_stats['mean_ms'], 
               yerr=operation_stats['stddev_ms'], capsize=5, alpha=0.7)
ax1.set_title('Tiempo Promedio por Operación')
ax1.set_ylabel('Tiempo (ms)')
ax1.set_xlabel('Tipo de Operación')
ax1.tick_params(axis='x', rotation=45)

# Agregar valores en las barras
for bar, value in zip(bars, operation_stats['mean_ms']):
    ax1.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.1, 
             f'{value:.3f}ms', ha='center', va='bottom', fontsize=9)

# 2. Boxplot de distribución de tiempos
ax2 = axes[0, 1]
# Crear datos para boxplot
boxplot_data = []
labels = []
for category in df['test_category'].unique():
    if pd.notna(category):
        category_data = df[df['test_category'] == category]['mean_ms']
        boxplot_data.append(category_data)
        labels.append(category)

ax2.boxplot(boxplot_data, labels=labels)
ax2.set_title('Distribución de Tiempos por Operación')
ax2.set_ylabel('Tiempo (ms)')
ax2.tick_params(axis='x', rotation=45)

# 3. Operaciones por segundo (OPS)
ax3 = axes[1, 0]
ops_stats = df.groupby('test_category')['ops'].mean().reset_index()
bars = ax3.bar(ops_stats['test_category'], ops_stats['ops'], alpha=0.7, color='green')
ax3.set_title('Operaciones por Segundo (OPS)')
ax3.set_ylabel('Operaciones/segundo')
ax3.set_xlabel('Tipo de Operación')
ax3.tick_params(axis='x', rotation=45)

# Agregar valores en las barras
for bar, value in zip(bars, ops_stats['ops']):
    ax3.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 50, 
             f'{value:.0f}', ha='center', va='bottom', fontsize=9)

# 4. Análisis de variabilidad (min vs max)
ax4 = axes[1, 1]
variability_stats = df.groupby('test_category').agg({
    'min_ms': 'mean',
    'max_ms': 'mean'
}).reset_index()

x = np.arange(len(variability_stats))
width = 0.35

bars1 = ax4.bar(x - width/2, variability_stats['min_ms'], width, 
                label='Tiempo Mínimo', alpha=0.7)
bars2 = ax4.bar(x + width/2, variability_stats['max_ms'], width, 
                label='Tiempo Máximo', alpha=0.7)

ax4.set_title('Variabilidad de Tiempos (Min vs Max)')
ax4.set_ylabel('Tiempo (ms)')
ax4.set_xlabel('Tipo de Operación')
ax4.set_xticks(x)
ax4.set_xticklabels(variability_stats['test_category'], rotation=45)
ax4.legend()

plt.tight_layout()
plt.show()

# Crear un gráfico adicional más detallado
plt.figure(figsize=(12, 8))

# Gráfico de líneas mostrando la evolución temporal de los benchmarks
test_categories = df['test_category'].unique()
test_categories = [cat for cat in test_categories if pd.notna(cat)]

for i, category in enumerate(test_categories):
    category_data = df[df['test_category'] == category]
    plt.subplot(2, 2, i+1)
    
    # Crear un índice de ejecución (asumiendo orden cronológico)
    execution_index = range(len(category_data))
    
    plt.plot(execution_index, category_data['mean_ms'], 'o-', alpha=0.7, linewidth=2)
    plt.fill_between(execution_index, 
                     category_data['mean_ms'] - category_data['stddev_ms'],
                     category_data['mean_ms'] + category_data['stddev_ms'],
                     alpha=0.3)
    
    plt.title(f'{category.replace("_", " ").title()} - Evolución')
    plt.xlabel('Ejecución #')
    plt.ylabel('Tiempo (ms)')
    plt.grid(True, alpha=0.3)

plt.suptitle('Evolución Temporal de los Benchmarks', fontsize=16, fontweight='bold')
plt.tight_layout()
plt.show()

# Imprimir estadísticas resumidas
print("=== RESUMEN DE BENCHMARKS ===")
print("\nTiempos promedio por operación:")
summary_stats = df.groupby('test_category').agg({
    'mean_ms': ['mean', 'std'],
    'ops': 'mean',
    'rounds': 'mean'
}).round(4)

for category in df['test_category'].unique():
    if pd.notna(category):
        cat_data = df[df['test_category'] == category]
        avg_time = cat_data['mean_ms'].mean()
        avg_ops = cat_data['ops'].mean()
        total_rounds = cat_data['rounds'].sum()
        
        print(f"\n{category.replace('_', ' ').title()}:")
        print(f"  - Tiempo promedio: {avg_time:.3f} ms")
        print(f"  - Operaciones/seg: {avg_ops:.0f}")
        print(f"  - Total de rondas: {total_rounds}")

print(f"\nOperación más rápida: {df.loc[df['mean_ms'].idxmin(), 'test_category']}")
print(f"Operación más lenta: {df.loc[df['mean_ms'].idxmax(), 'test_category']}")