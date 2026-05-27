import pandas as pd
import numpy as np
import time
import multiprocessing as mp
import os
import math
import matplotlib.pyplot as plt

# ==========================================
# 1. GENERACIÓN DEL DATASET SIMULADO
# ==========================================
def generar_dataset(filas=600000, archivo="telemetria_samp.csv"):
    if not os.path.exists(archivo):
        print(f"Generando dataset de {filas} registros de telemetría...")
        np.random.seed(42) 
        
        datos = {
            "player_id": np.random.randint(1, 5000, filas),
            "player_score": np.random.randint(0, 15000, filas), 
            "ping_ms": np.random.normal(60, 30, filas).clip(5, 500), 
            "packet_loss": np.random.uniform(0, 10, filas), 
            "playtime_min": np.random.randint(1, 120, filas) 
        }
        
        df = pd.DataFrame(datos)
        df.to_csv(archivo, index=False)
        print("Dataset generado con éxito.\n")
        
    return pd.read_csv(archivo)

# ==========================================
# 2. TAREA COMPUTACIONAL EXTREMADAMENTE PESADA
# ==========================================
def calcular_calidad_conexion(df_chunk):
    """
    Simula una carga de procesamiento brutal obligando a la CPU a realizar 
    100 cálculos trigonométricos por cada fila de forma nativa.
    """
    def procesamiento_pesado(row):
        val = 0.0
        ping = row['ping_ms']
        score = row['player_score']
        for i in range(100):
            val += math.sin(ping + i) * math.cos(score - i)
        return val

    df_chunk['network_quality_index'] = df_chunk.apply(procesamiento_pesado, axis=1)
    return df_chunk

# ==========================================
# 3. PROCESAMIENTO SECUENCIAL (1 NÚCLEO)
# ==========================================
def procesamiento_secuencial(df):
    print("Iniciando procesamiento Secuencial (1 proceso)... Esto tomará varios segundos.")
    inicio = time.time()
    
    resultado = calcular_calidad_conexion(df.copy())
    
    tiempo_total = time.time() - inicio
    print(f"Tiempo Secuencial: {tiempo_total:.4f} segundos\n")
    return tiempo_total

# ==========================================
# 4. PROCESAMIENTO PARALELO (MÚLTIPLES NÚCLEOS)
# ==========================================
def procesamiento_paralelo(df, num_procesos):
    print(f"Iniciando procesamiento Paralelo con {num_procesos} procesos...")
    inicio = time.time()
    
    # Particionar usando índices nativos para no romper Pandas
    indices = np.array_split(df.index, num_procesos)
    chunks = [df.loc[idx].copy() for idx in indices]
    
    with mp.Pool(processes=num_procesos) as pool:
        resultados = pool.map(calcular_calidad_conexion, chunks)
        
    df_final = pd.concat(resultados)
    
    tiempo_total = time.time() - inicio
    print(f"Tiempo Paralelo ({num_procesos} proc): {tiempo_total:.4f} segundos\n")
    return tiempo_total

# ==========================================
# 5. EJECUCIÓN PRINCIPAL, REPORTE Y GRÁFICOS
# ==========================================
if __name__ == '__main__':
    df_telemetria = generar_dataset(600000)
    
    t1 = procesamiento_secuencial(df_telemetria)
    t2 = procesamiento_paralelo(df_telemetria, 2)
    t4 = procesamiento_paralelo(df_telemetria, 4)
    
    speedup_2 = t1 / t2
    eficiencia_2 = speedup_2 / 2
    
    speedup_4 = t1 / t4
    eficiencia_4 = speedup_4 / 4
    
    reporte = (
        "-" * 55 + "\n"
        "RESUMEN DE MÉTRICAS EXPERIMENTALES\n"
        "-" * 55 + "\n"
        f"Procesos | Tiempo (s) | Speedup (S_p) | Eficiencia (E_p)\n"
        f"   1     |  {t1:>8.4f}  |      1.0000   |     1.0000\n"
        f"   2     |  {t2:>8.4f}  |      {speedup_2:.4f}   |     {eficiencia_2:.4f}\n"
        f"   4     |  {t4:>8.4f}  |      {speedup_4:.4f}   |     {eficiencia_4:.4f}\n"
        "-" * 55 + "\n"
    )
    
    print(reporte)
    with open("resultados_benchmark.txt", "w", encoding="utf-8") as archivo_txt:
        archivo_txt.write(reporte)
    print(">> Tabla guardada en 'resultados_benchmark.txt'")

    # --- Creación de la imagen con AMBOS gráficos ---
    procesos = [1, 2, 4]
    tiempos = [t1, t2, t4]
    speedups = [1.0, speedup_2, speedup_4]

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))

    # Gráfico izquierdo: Tiempo
    ax1.plot(procesos, tiempos, marker='o', color='red', linestyle='-', linewidth=2)
    ax1.set_title('Tiempo vs Número de Procesos')
    ax1.set_xlabel('Número de Procesos (p)')
    ax1.set_ylabel('Tiempo (segundos)')
    ax1.set_xticks(procesos)
    ax1.grid(True, linestyle=':', alpha=0.7)

    # Gráfico derecho: Speedup
    ax2.plot(procesos, speedups, marker='o', color='blue', label='S_p Experimental', linewidth=2)
    ax2.plot(procesos, procesos, linestyle='--', color='gray', label='S_p Ideal (Lineal)')
    ax2.set_title('Speedup vs Número de Procesos')
    ax2.set_xlabel('Número de Procesos (p)')
    ax2.set_ylabel('Speedup ($S_p$)')
    ax2.set_xticks(procesos)
    ax2.legend()
    ax2.grid(True, linestyle=':', alpha=0.7)

    plt.tight_layout()
    plt.savefig('graficos_rendimiento.png', dpi=300, bbox_inches='tight')
    print(">> Imagen con ambos gráficos guardada en 'graficos_rendimiento.png'")