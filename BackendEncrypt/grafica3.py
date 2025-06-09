import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import psutil
import time
import threading
from concurrent.futures import ThreadPoolExecutor
import gc
import random
import string

class MemoryMonitor:
    """Monitor de uso de memoria en tiempo real"""
    def __init__(self):
        self.memory_usage = []
        self.timestamps = []
        self.monitoring = False
        self.process = psutil.Process()
    
    def start_monitoring(self):
        self.monitoring = True
        self.memory_usage = []
        self.timestamps = []
        
        def monitor():
            start_time = time.time()
            while self.monitoring:
                memory_mb = self.process.memory_info().rss / 1024 / 1024
                self.memory_usage.append(memory_mb)
                self.timestamps.append(time.time() - start_time)
                time.sleep(0.1)  # Muestrear cada 100ms
        
        self.thread = threading.Thread(target=monitor)
        self.thread.daemon = True
        self.thread.start()
    
    def stop_monitoring(self):
        self.monitoring = False
        if hasattr(self, 'thread'):
            self.thread.join()

def simulate_crud_operations(num_operations=1000):
    """Simular operaciones CRUD con medición de rendimiento"""
    
    # Simulación de datos
    passwords_db = {}
    
    def generate_password():
        return ''.join(random.choices(string.ascii_letters + string.digits, k=12))
    
    def create_entry():
        id = len(passwords_db) + 1
        passwords_db[id] = {
            'username': f'user_{id}',
            'password': generate_password(),
            'url': f'https://site{id}.com'
        }
        return id
    
    def read_entry(id):
        return passwords_db.get(id)
    
    def update_entry(id):
        if id in passwords_db:
            passwords_db[id]['password'] = generate_password()
            return True
        return False
    
    def delete_entry(id):
        if id in passwords_db:
            del passwords_db[id]
            return True
        return False
    
    # Medición de operaciones CRUD
    results = {
        'CREATE': {'times': [], 'memory': []},
        'READ': {'times': [], 'memory': []},
        'UPDATE': {'times': [], 'memory': []},
        'DELETE': {'times': [], 'memory': []}
    }
    
    monitor = MemoryMonitor()
    
    print("Ejecutando simulación de operaciones CRUD...")
    
    # CREATE
    monitor.start_monitoring()
    start_time = time.time()
    
    for i in range(num_operations):
        op_start = time.time()
        create_entry()
        op_time = time.time() - op_start
        results['CREATE']['times'].append(op_time * 1000)  # convertir a ms
    
    monitor.stop_monitoring()
    results['CREATE']['memory'] = monitor.memory_usage.copy()
    
    # READ
    monitor.start_monitoring()
    ids = list(passwords_db.keys())
    
    for i in range(min(num_operations, len(ids))):
        op_start = time.time()
        read_entry(random.choice(ids))
        op_time = time.time() - op_start
        results['READ']['times'].append(op_time * 1000)
    
    monitor.stop_monitoring()
    results['READ']['memory'] = monitor.memory_usage.copy()
    
    # UPDATE
    monitor.start_monitoring()
    
    for i in range(min(num_operations//2, len(ids))):
        op_start = time.time()
        update_entry(random.choice(ids))
        op_time = time.time() - op_start
        results['UPDATE']['times'].append(op_time * 1000)
    
    monitor.stop_monitoring()
    results['UPDATE']['memory'] = monitor.memory_usage.copy()
    
    # DELETE
    monitor.start_monitoring()
    delete_ids = random.sample(ids, min(num_operations//4, len(ids)))
    
    for id in delete_ids:
        op_start = time.time()
        delete_entry(id)
        op_time = time.time() - op_start
        results['DELETE']['times'].append(op_time * 1000)
    
    monitor.stop_monitoring()
    results['DELETE']['memory'] = monitor.memory_usage.copy()
    
    return results

def simulate_load_test(concurrent_users=10, operations_per_user=100):
    """Simular carga con múltiples usuarios concurrentes"""
    passwords_db = {}
    lock = threading.Lock()
    
    def user_operations():
        times = []
        for _ in range(operations_per_user):
            # Operación aleatoria
            operation = random.choice(['CREATE', 'READ', 'UPDATE'])
            
            start_time = time.time()
            
            if operation == 'CREATE':
                with lock:
                    id = len(passwords_db) + 1
                    passwords_db[id] = {'user': f'user_{id}', 'pass': 'secret123'}
            
            elif operation == 'READ' and passwords_db:
                with lock:
                    random.choice(list(passwords_db.values()))
            
            elif operation == 'UPDATE' and passwords_db:
                with lock:
                    id = random.choice(list(passwords_db.keys()))
                    passwords_db[id]['pass'] = 'updated_pass'
            
            op_time = (time.time() - start_time) * 1000
            times.append(op_time)
        
        return times
    
    # Monitor de memoria durante la carga
    monitor = MemoryMonitor()
    monitor.start_monitoring()
    
    print(f"Ejecutando prueba de carga: {concurrent_users} usuarios concurrentes...")
    
    start_time = time.time()
    
    with ThreadPoolExecutor(max_workers=concurrent_users) as executor:
        futures = [executor.submit(user_operations) for _ in range(concurrent_users)]
        all_times = []
        for future in futures:
            all_times.extend(future.result())
    
    total_time = time.time() - start_time
    monitor.stop_monitoring()
    
    return {
        'response_times': all_times,
        'memory_usage': monitor.memory_usage,
        'memory_timestamps': monitor.timestamps,
        'total_time': total_time,
        'throughput': len(all_times) / total_time
    }

def analyze_csv_data():
    """Analizar datos del archivo CSV existente"""
    try:
        df = pd.read_csv('benchmark_resultados.csv')
        
        # Extraer nombres de funciones
        df['test_function'] = df['name'].str.extract(r'::([^:]+)$')[0]
        function_mapping = {
            'test_read_password_entries': 'READ',
            'test_create_password_entry': 'CREATE',
            'test_update_password_entry': 'UPDATE',
            'test_encrypt_password': 'ENCRYPT',
            'test_decrypt_password_benchmark': 'DECRYPT'
        }
        df['operation'] = df['test_function'].map(function_mapping)
        
        return df
    except FileNotFoundError:
        print("Archivo CSV no encontrado. Usando solo simulación.")
        return None

def create_comprehensive_analysis():
    """Crear análisis completo"""
    
    # Analizar datos CSV existentes
    csv_data = analyze_csv_data()
    
    # Ejecutar simulaciones
    crud_results = simulate_crud_operations(500)
    load_test_results = simulate_load_test(5, 50)
    
    # Crear visualización
    fig = plt.figure(figsize=(16, 12))
    fig.suptitle('Análisis Completo: Velocidad de Respuesta y Uso de Memoria', fontsize=16, fontweight='bold')
    
    # 1. Datos del CSV - Velocidad de respuesta
    if csv_data is not None:
        ax1 = plt.subplot(2, 3, 1)
        csv_summary = csv_data.groupby('operation')['mean'].mean() * 1000
        bars = ax1.bar(csv_summary.index, csv_summary.values, 
                      color=['#FF6B6B', '#4ECDC4', '#45B7D1', '#96CEB4', '#FFEAA7'], alpha=0.8)
        ax1.set_title('Tiempos CSV (Datos Reales)')
        ax1.set_ylabel('Tiempo (ms)')
        ax1.tick_params(axis='x', rotation=45)
        
        # Añadir valores
        for bar, value in zip(bars, csv_summary.values):
            ax1.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.01,
                    f'{value:.3f}', ha='center', va='bottom', fontsize=8)
    
    # 2. Simulación CRUD - Velocidad
    ax2 = plt.subplot(2, 3, 2)
    crud_times = {op: np.mean(data['times']) for op, data in crud_results.items()}
    bars2 = ax2.bar(crud_times.keys(), crud_times.values(), 
                   color=['#FF6B6B', '#4ECDC4', '#45B7D1', '#96CEB4'], alpha=0.8)
    ax2.set_title('Simulación CRUD - Velocidad')
    ax2.set_ylabel('Tiempo Promedio (ms)')
    
    for bar, value in zip(bars2, crud_times.values()):
        ax2.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.001,
                f'{value:.3f}', ha='center', va='bottom', fontsize=8)
    
    # 3. Uso de memoria por operación CRUD
    ax3 = plt.subplot(2, 3, 3)
    memory_usage = {op: np.mean(data['memory']) if data['memory'] else 0 
                   for op, data in crud_results.items()}
    bars3 = ax3.bar(memory_usage.keys(), memory_usage.values(), 
                   color=['#FFA07A', '#98D8C8', '#87CEEB', '#F0E68C'], alpha=0.8)
    ax3.set_title('Uso de Memoria por Operación')
    ax3.set_ylabel('Memoria (MB)')
    
    for bar, value in zip(bars3, memory_usage.values()):
        if value > 0:
            ax3.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 1,
                    f'{value:.1f}', ha='center', va='bottom', fontsize=8)
    
    # 4. Distribución de tiempos de respuesta bajo carga
    ax4 = plt.subplot(2, 3, 4)
    ax4.hist(load_test_results['response_times'], bins=30, alpha=0.7, color='skyblue', edgecolor='black')
    ax4.set_title('Distribución Tiempos - Carga Simulada')
    ax4.set_xlabel('Tiempo de Respuesta (ms)')
    ax4.set_ylabel('Frecuencia')
    
    # 5. Memoria durante prueba de carga
    ax5 = plt.subplot(2, 3, 5)
    if load_test_results['memory_usage']:
        ax5.plot(load_test_results['memory_timestamps'], load_test_results['memory_usage'], 
                color='red', linewidth=2)
        ax5.set_title('Uso de Memoria - Prueba de Carga')
        ax5.set_xlabel('Tiempo (s)')
        ax5.set_ylabel('Memoria (MB)')
        ax5.grid(True, alpha=0.3)
    
    # 6. Resumen de rendimiento
    ax6 = plt.subplot(2, 3, 6)
    ax6.axis('off')
    
    # Estadísticas de resumen
    stats_text = f"""RESUMEN DE RENDIMIENTO
    
Simulación CRUD:
• CREATE: {np.mean(crud_results['CREATE']['times']):.3f} ms
• READ: {np.mean(crud_results['READ']['times']):.3f} ms  
• UPDATE: {np.mean(crud_results['UPDATE']['times']):.3f} ms
• DELETE: {np.mean(crud_results['DELETE']['times']):.3f} ms

Prueba de Carga:
• Throughput: {load_test_results['throughput']:.0f} ops/seg
• Tiempo promedio: {np.mean(load_test_results['response_times']):.3f} ms
• Memoria máxima: {max(load_test_results['memory_usage']) if load_test_results['memory_usage'] else 0:.1f} MB

Datos CSV:
• Total pruebas: {len(csv_data) if csv_data is not None else 0}
• Operación más rápida: {csv_summary.idxmin() if csv_data is not None else 'N/A'}
"""
    
    ax6.text(0.1, 0.9, stats_text, transform=ax6.transAxes, fontsize=10,
             verticalalignment='top', fontfamily='monospace',
             bbox=dict(boxstyle='round', facecolor='lightgray', alpha=0.8))
    
    plt.tight_layout()
    plt.savefig('analisis_completo_crud_memoria.png', dpi=300, bbox_inches='tight')
    plt.show()
    
    # Imprimir resumen en consola
    print("\n" + "="*60)
    print("ANÁLISIS COMPLETO - VELOCIDAD Y MEMORIA")
    print("="*60)
    print(f"Throughput bajo carga: {load_test_results['throughput']:.2f} operaciones/segundo")
    print(f"Tiempo promedio bajo carga: {np.mean(load_test_results['response_times']):.3f} ms")
    print(f"Memoria máxima utilizada: {max(load_test_results['memory_usage']) if load_test_results['memory_usage'] else 0:.1f} MB")
    print("="*60)

if __name__ == "__main__":
    create_comprehensive_analysis()