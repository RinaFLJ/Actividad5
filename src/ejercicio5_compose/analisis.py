import os
import time
import pandas as pd
from sqlalchemy import create_engine
import numpy as np

# 1. Leer credenciales desde Docker Compose
DB_USER = os.environ.get('DB_USER')
DB_PASS = os.environ.get('DB_PASS')
DB_HOST = os.environ.get('DB_HOST')
DB_NAME = os.environ.get('DB_NAME')

engine = create_engine(f"postgresql://{DB_USER}:{DB_PASS}@{DB_HOST}:5432/{DB_NAME}")

# 2. Esperar a que PostgreSQL levante correctamente
print("Esperando a que la base de datos inicie...")
for _ in range(15):
    try:
        engine.connect()
        print("¡Conexión exitosa a PostgreSQL a través de la red interna!")
        break
    except Exception:
        time.sleep(2)
else:
    print("Error conectando a la DB.")
    exit(1)

# 3. Generar un dataset simulado
print("Generando dataset...")
np.random.seed(42)
df = pd.DataFrame({
    'jugador_id': range(1, 101),
    'puntaje': np.random.randint(100, 5000, 100),
    'horas_juego': np.random.uniform(10, 500, 100)
})

# 4. Cargar datos a la Base de Datos
print("Cargando datos a PostgreSQL...")
df.to_sql('estadisticas_jugadores', engine, if_exists='replace', index=False)

# 5. Ejecutar Consulta Analítica
print("Consultando la base de datos...")
query = "SELECT jugador_id, puntaje FROM estadisticas_jugadores ORDER BY puntaje DESC LIMIT 5"
top_jugadores = pd.read_sql(query, engine)

print("\n--- TOP 5 JUGADORES ---")
print(top_jugadores)
print("-----------------------\n")

# 6. Guardar evidencia local
top_jugadores.to_csv('resultado_consulta_compose.csv', index=False)
print("Resultados guardados en resultado_consulta_compose.csv")
