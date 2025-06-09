import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# Cargar datos
df = pd.read_csv('benchmark_resultados2.csv')

# Extraer nombres de funciones más legibles
df['test_function'] = df['name'].str.extract(r'::([^:]+)$')[0]
function_names = {
    'test_read_password_entries': 'Leer',
    'test_create_password_entry': 'Crear', 
    'test_update_password_entry': 'Actualizar',
    'test_encrypt_password': 'Encriptar',
    'test_decrypt_password_benchmark': 'Desencriptar'
}
df['test_function'] = df['test_function'].map(function_names)

# Calcular promedios por función
summary = df.groupby('test_function').agg({
    'mean': 'mean',
    'ops': 'mean'
}).reset_index()

# Crear la gráfica
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))
fig.suptitle('Benchmark - Sistema de Contraseñas', fontsize=16, fontweight='bold')

# Gráfica 1: Tiempo promedio (en milisegundos)
colors = ['#FF6B6B', '#4ECDC4', '#45B7D1', '#96CEB4', '#FFEAA7']
bars1 = ax1.bar(summary['test_function'], summary['mean'] * 1000, 
                color=colors, alpha=0.8, edgecolor='black', linewidth=0.5)

ax1.set_title('Tiempo Promedio por Operación')
ax1.set_ylabel('Tiempo (ms)')
ax1.set_xlabel('Función')

# Añadir valores en las barras
for bar, value in zip(bars1, summary['mean'] * 1000):
    ax1.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.05,
             f'{value:.2f}', ha='center', va='bottom', fontweight='bold')

# Gráfica 2: Operaciones por segundo
bars2 = ax2.bar(summary['test_function'], summary['ops'], 
                color=colors, alpha=0.8, edgecolor='black', linewidth=0.5)

ax2.set_title('Operaciones por Segundo')
ax2.set_ylabel('Ops/seg')
ax2.set_xlabel('Función')

# Añadir valores en las barras
for bar, value in zip(bars2, summary['ops']):
    ax2.text(bar.get_x() + bar.get_width()/2, bar.get_height() + max(summary['ops'])*0.02,
             f'{value:,.0f}', ha='center', va='bottom', fontweight='bold')

# Ajustar diseño
plt.tight_layout()
plt.grid(True, alpha=0.3)

# Mostrar información resumida
print("RESUMEN DE BENCHMARKS:")
print("-" * 30)
for _, row in summary.iterrows():
    print(f"{row['test_function']:12} | {row['mean']*1000:6.2f} ms | {row['ops']:8,.0f} ops/seg")

# Mostrar y guardar
plt.savefig('benchmark_grafica.png', dpi=300, bbox_inches='tight')
plt.show()