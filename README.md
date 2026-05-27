# Infraestructura para Ciencia de Datos - Evaluación Integradora 1

[cite_start]Este repositorio contiene la entrega técnica y el código fuente correspondiente a la Evaluación Integradora 1 de la asignatura **Infraestructura para Ciencia de Datos** de la carrera Ingeniería Civil en Ciencia de Datos (UTEM)[cite: 77, 78]. 

[cite_start]El proyecto abarca desde la manipulación de hardware en bajo nivel y la creación de pipelines analíticos contenerizados, hasta la propuesta de una arquitectura de procesamiento OLAP acelerada por hardware (GPU)[cite: 94, 96].

---

## 📊 Resumen Rápido de Resultados (Métricas del Informe)

Para una visualización rápida de los logros empíricos obtenidos en las pruebas locales:

### ⚡ Ejercicio 3: Paralelismo Local y Medición de Speedup
[cite_start]Se procesó un dataset de 600.000 registros sintéticos utilizando la librería `multiprocessing` de Python para evaluar la escalabilidad y el impacto del overhead en la CPU[cite: 146, 147]:

* **Secuencial (1 proceso):** 16.09 segundos | Speedup: 1.00x | [cite_start]Eficiencia: 100.00% [cite: 147]
* **Paralelo (2 procesos):** 10.87 segundos | Speedup: 1.48x | [cite_start]Eficiencia: 74.00% [cite: 147]
* **Paralelo (4 procesos):** 5.71 segundos | Speedup: 2.81x | [cite_start]Eficiencia: 70.43% [cite: 147]

[cite_start]*Conclusión Técnica:* El Speedup obtenido demuestra un comportamiento no lineal[cite: 172]. [cite_start]La pérdida de eficiencia al usar más núcleos se explica por el *overhead* asociado a la serialización de datos y al costo de conmutación de contexto del sistema operativo[cite: 173].

### 🔄 Ejercicio 4: Pipeline Big Data (Docker + Parquet)
* [cite_start]**Tiempo de ejecución total:** 0.45 segundos[cite: 217].
* [cite_start]**Procesamiento:** Ingesta de datos crudos con anomalías en la zona **Bronze**, aplicación de 6 reglas estrictas de calidad en la zona **Silver**, y ejecución de consultas analíticas optimizadas mediante DuckDB sobre almacenamiento columnar Parquet particionado en la zona **Gold**[cite: 184, 185, 186]. [cite_start]Todo aislado eficientemente en un contenedor Docker[cite: 192].

### 🌐 Ejercicio 5: Infraestructura con Docker Compose
* [cite_start]**Resultado:** Orquestación exitosa de un entorno de microservicios con una red privada segura de tipo Bridge (`data_net`) y un volumen persistente (`pgdata`)[cite: 227, 232, 233]. [cite_start]El motor analítico logró conectarse de forma aislada a PostgreSQL 15, poblar la base de datos y extraer con éxito el Top 5 de puntajes de jugadores directamente a un archivo CSV[cite: 230, 237, 272].

---

## 🛠️ Entorno de Ejecución y Reproducibilidad

[cite_start]Para garantizar la reproducibilidad de los experimentos documentados, el entorno base utilizado fue el siguiente[cite: 86]:

* [cite_start]**Sistema Operativo:** Linux Mint [cite: 87]
* [cite_start]**CPU:** AMD Ryzen 5 5500 (6 núcleos físicos, 12 hilos) [cite: 88]
* [cite_start]**GPU:** MSI NVIDIA GeForce RTX 3050 (6GB VRAM) [cite: 88]
* [cite_start]**Memoria RAM:** 32 GB [cite: 89]
* [cite_start]**Dependencias Core:** Python 3.10/3.12 (entornos virtuales), Docker Engine, Docker Compose V2, QEMU y NASM[cite: 91].

---

## 📂 Contenidos del Repositorio

El repositorio se estructura en los siguientes componentes principales:

### PARTE I: Arquitectura Computacional y Big Data (Ejercicios Prácticos)
* [cite_start]**`/src/Ejercicio 1`:** Código en ensamblador (`boot.asm`) y script de automatización (`build.sh`) para compilar y ejecutar el micro sistema operativo en QEMU, escribiendo directamente en la dirección física de la memoria VGA (`0xB8000`)[cite: 107, 110, 111].
* [cite_start]**`/src/Ejercicio 3`:** Script de procesamiento paralelo y análisis empírico de curvas de tiempo, Speedup y Eficiencia[cite: 142].
* [cite_start]**`/src/Ejercicio 4`:** Código del pipeline analítico utilizando la Arquitectura Medallón junto con su respectivo `Dockerfile` para un despliegue inmutable[cite: 180, 182].
* [cite_start]**`/src/Ejercicio 5`:** Configuración de microservicios mediante `docker-compose.yml`, script de analítica con persistencia relacional en PostgreSQL[cite: 225, 229, 230].

### PARTE II: Anteproyecto Integrador (Aceleración OLAP por GPU)
* [cite_start]**Título:** Evaluación de Aceleración por Hardware en Procesamiento OLAP: Evolución Histórica del Rendimiento de Héroes en Overwatch mediante GPU[cite: 291].
* [cite_start]**Planteamiento:** Análisis del cambio del "meta" competitivo evaluando la variación de estadísticas de personajes (como el impacto de Junkrat desde su aparición en la beta de 2015 hasta el presente) cruzando decenas de millones de registros de telemetría[cite: 293, 294].
* [cite_start]**Solución Técnica:** Migración del procesamiento secuencial de CPU tradicional (Pandas) hacia un paralelismo masivo ejecutado directamente sobre la VRAM y los núcleos CUDA de la GPU mediante la suite **NVIDIA RAPIDS (cuDF)**[cite: 295, 298, 299].
* [cite_start]**Análisis de Riesgo:** Documentación del límite estricto de memoria (*Out of Memory*) de los 6GB de VRAM de la RTX 3050 frente a la capacidad de la CPU de utilizar el archivo de paginación (*Swap*) del disco duro[cite: 317, 318, 319].

---

## 👨‍💻 Autor
[cite_start]**Fabrizio Larco Jorquera** *Ingeniería Civil en Ciencia de Datos* *Universidad Tecnológica Metropolitana (UTEM) - Mayo 2026* [cite: 78, 79]
