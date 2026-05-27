import os
import json
import time
from datetime import datetime
import pandas as pd
import numpy as np
import duckdb
import matplotlib.pyplot as plt

# ==========================================
# 1. CONFIGURACIÓN DE RUTAS
# ==========================================
ZONAS = ["bronze", "silver", "gold", "metadata", "metrics"]
for zona in ZONAS:
    os.makedirs(zona, exist_ok=True)

# ==========================================
# 2. FASE BRONZE: INGESTIÓN / DATOS CRUDOS
# ==========================================
def fase_bronze():
    print("[BRONZE] Generando fuentes de datos...")
    np.random.seed(42)
    n_registros = 10000
    
    df_conexiones = pd.DataFrame({
        "conexion_id": range(1, n_registros + 1),
        "player_id": np.random.randint(1, 1000, n_registros),
        "ping_ms": np.random.normal(60, 40, n_registros),
        "status": np.random.choice(["EXITOSO", "FALLIDO", "INVALIDO"], n_registros, p=[0.85, 0.12, 0.03]),
        "fecha": [datetime.now().strftime("%Y-%m-%d") for _ in range(n_registros)]
    })
    
    df_conexiones.loc[10:15, "player_id"] = np.nan
    df_conexiones.loc[20:25, "ping_ms"] = -50.0
    df_conexiones = pd.concat([df_conexiones, df_conexiones.iloc[100:105]], ignore_index=True)
    
    df_conexiones.to_csv("bronze/conexiones.csv", index=False)

    eventos = []
    tipos_evento = ["KILL", "DEATH", "CHAT", "HACK_DETECTED", "LEVEL_UP"]
    for i in range(1, n_registros + 1):
        evt = {
            "evento_id": i,
            "player_id": int(np.random.randint(1, 1050)),
            "tipo_evento": str(np.random.choice(tipos_evento)),
            "timestamp": datetime.now().isoformat()
        }
        eventos.append(evt)
    
    eventos[50]["tipo_evento"] = "COMANDO_INVALIDADO"
    eventos[60]["timestamp"] = "2030-12-31T23:59:59"
    
    with open("bronze/eventos.jsonl", "w") as f:
        for e in eventos:
            f.write(json.dumps(e) + "\n")
            
    print("[BRONZE] Listo.\n")

# ==========================================
# 3. FASE SILVER: CALIDAD Y TRANSFORMACIÓN
# ==========================================
def fase_silver():
    print("[SILVER] Aplicando reglas de calidad...")
    df_con = pd.read_csv("bronze/conexiones.csv")
    with open("bronze/eventos.jsonl", "r") as f:
        df_evt = pd.DataFrame([json.loads(line) for line in f])
        
    reporte_calidad = {"conexiones": {}, "eventos": {}}
    
    t_con = len(df_con)
    df_con = df_con.drop_duplicates()
    reporte_calidad["conexiones"]["duplicados_eliminados"] = t_con - len(df_con)
    
    t_con = len(df_con)
    df_con = df_con.dropna(subset=["player_id"])
    df_con["player_id"] = df_con["player_id"].astype(int)
    reporte_calidad["conexiones"]["nulos_eliminados"] = t_con - len(df_con)
    
    t_con = len(df_con)
    df_con = df_con[df_con["ping_ms"] >= 0]
    reporte_calidad["conexiones"]["rangos_invalidos_ping"] = t_con - len(df_con)

    t_evt = len(df_evt)
    df_evt = df_evt[df_evt["tipo_evento"].isin(["KILL", "DEATH", "CHAT", "HACK_DETECTED", "LEVEL_UP"])]
    reporte_calidad["eventos"]["categorias_invalidas"] = t_evt - len(df_evt)
    
    # FIX APLICADO AQUÍ: format='mixed'
    df_evt["parsed_time"] = pd.to_datetime(df_evt["timestamp"], format='mixed')
    t_evt = len(df_evt)
    df_evt = df_evt[df_evt["parsed_time"] <= datetime.now()]
    df_evt = df_evt.drop(columns=["parsed_time"])
    reporte_calidad["eventos"]["fechas_futuras"] = t_evt - len(df_evt)

    t_evt = len(df_evt)
    df_evt = df_evt[df_evt["player_id"].isin(df_con["player_id"])]
    reporte_calidad["eventos"]["claves_inconsistentes"] = t_evt - len(df_evt)

    with open("metrics/reporte_calidad.txt", "w") as f:
        f.write(json.dumps(reporte_calidad, indent=4))

    df_con.to_parquet("silver/conexiones_clean", partition_cols=["status"], index=False)
    df_evt.to_parquet("silver/eventos_clean.parquet", index=False)
    print("[SILVER] Listo.\n")

# ==========================================
# 4. FASE GOLD: ANALÍTICA CON DUCKDB
# ==========================================
def fase_gold():
    print("[GOLD] Ejecutando analítica SQL...")
    con = duckdb.connect()
    
    con.execute("SELECT player_id, COUNT(*) as total FROM 'silver/eventos_clean.parquet' GROUP BY player_id ORDER BY total DESC LIMIT 5").df().to_csv("gold/top_jugadores.csv", index=False)
    
    res_q2 = con.execute("SELECT tipo_evento, COUNT(*) as cant FROM 'silver/eventos_clean.parquet' GROUP BY tipo_evento ORDER BY cant DESC").df()
    res_q2.to_csv("gold/tipos_eventos.csv", index=False)
    
    con.execute("SELECT AVG(ping_ms) as ping_exitoso FROM 'silver/conexiones_clean/status=EXITOSO/*.parquet'").df().to_csv("gold/ping_promedio.csv", index=False)

    plt.figure(figsize=(8, 4))
    plt.bar(res_q2["tipo_evento"], res_q2["cant"], color="purple")
    plt.title("Distribución de Eventos")
    plt.savefig("metrics/grafico_eventos.png", bbox_inches='tight')
    print("[GOLD] Listo.\n")

# ==========================================
# 5. GENERACIÓN DE METADATOS
# ==========================================
def generar_metadatos():
    print("[METADATA] Generando catálogos...")
    cat = {"estado": "ok", "tablas": ["conexiones", "eventos"], "zonas": ZONAS}
    linaje = {"ejecucion": datetime.now().isoformat(), "script": "pipeline.py"}
    
    with open("metadata/catalogo.json", "w") as f: json.dump(cat, f)
    with open("metadata/linaje.json", "w") as f: json.dump(linaje, f)
    print("[METADATA] Listo.\n")

if __name__ == "__main__":
    t = time.time()
    fase_bronze()
    fase_silver()
    fase_gold()
    generar_metadatos()
    print(f"EXITO - TIEMPO: {time.time() - t:.2f}s")
