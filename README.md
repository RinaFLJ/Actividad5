# Infraestructura para Ciencia de Datos - Evaluación Integradora 1

Este repositorio contiene la entrega técnica y el código fuente correspondiente a la Evaluación Integradora 1 de la asignatura **Infraestructura para Ciencia de Datos** de la carrera Ingeniería Civil en Ciencia de Datos (UTEM). 

El proyecto abarca desde la manipulación de hardware en bajo nivel y la creación de pipelines analíticos contenerizados, hasta la propuesta de una arquitectura de procesamiento OLAP acelerada por hardware (GPU).

---

## 📊 Resumen Rápido de Resultados (Métricas del Informe)

Para una visualización rápida de los logros empíricos obtenidos en las pruebas locales:

### ⚡ Ejercicio 3: Paralelismo Local y Medición de Speedup
Se procesó un dataset de 600.000 registros sintéticos utilizando la librería `multiprocessing` de Python para evaluar la escalabilidad y el impacto del overhead en la CPU:

* **Secuencial (1 proceso):** 16.09 segundos | Speedup: 1.00x | Eficiencia: 100.00%
* **Paralelo (2 procesos):** 10.87 segundos | Speedup: 1.48x | Eficiencia: 74.00%
* **Paralelo (4 procesos):** 5.71 segundos | Speedup: 2.81x | Eficiencia: 70.43%

*Conclusión Técnica:* El Speedup obtenido demuestra un comportamiento no lineal. La pérdida de eficiencia al usar más núcleos se explica por el *overhead* asociado a la serialización de datos y al costo de conmutación de contexto del sistema operativo.

### 🔄 Ejercicio 4: Pipeline Big Data (Docker + Parquet)
* **Tiempo de ejecución total:** 0.45 segundos.
* **Procesamiento:** Ingesta de datos crudos con anomalías en la zona **Bronze**, aplicación de 6 reglas estrictas de calidad en la zona **Silver**, y ejecución de consultas analíticas optimizadas mediante DuckDB sobre almacenamiento columnar Parquet particionado en la zona **Gold**. Todo aislado eficientemente en un contenedor Docker.

### 🌐 Ejercicio 5: Infraestructura con Docker Compose
* **Resultado:** Orquestación exitosa de un entorno de microservicios con una red privada segura de tipo Bridge (`data_net`) y un volumen persistente (`pgdata`). El motor analítico logró conectarse de forma aislada a PostgreSQL 15, poblar la base de datos y extraer con éxito el Top 5 de puntajes de jugadores directamente a un archivo CSV.

---

## 🛠️ Entorno de Ejecución y Reproducibilidad

Para garantizar la reproducibilidad de los experimentos documentados, el entorno base utilizado fue el siguiente:

* **Sistema Operativo:** Linux Mint
* **CPU:** AMD Ryzen 5 5500 (6 núcleos físicos, 12 hilos)
* **GPU:** MSI NVIDIA GeForce RTX 3050 (6GB VRAM)
* **Memoria RAM:** 32 GB
* **Dependencias Core:** Python 3.10/3.12 (entornos virtuales), Docker Engine, Docker Compose V2, QEMU y NASM.

---

## 📂 Contenidos del Repositorio

El repositorio se estructura en los siguientes componentes principales:

### PARTE I: Arquitectura Computacional y Big Data (Ejercicios Prácticos)
* **`/src/Ejercicio 1`:** Código en ensamblador (`boot.asm`) y script de automatización (`build.sh`) para compilar y ejecutar el micro sistema operativo en QEMU, escribiendo directamente en la dirección física de la memoria VGA (`0xB8000`).
* **`/src/Ejercicio 3`:** Script de procesamiento paralelo y análisis empírico de curvas de tiempo, Speedup y Eficiencia.
* **`/src/Ejercicio 4`:** Código del pipeline analítico utilizando la Arquitectura Medallón junto con su respectivo `Dockerfile` para un despliegue inmutable.
* **`/src/Ejercicio 5`:** Configuración de microservicios mediante `docker-compose.yml`, script de analítica con persistencia relacional en PostgreSQL.

### PARTE II: Anteproyecto Integrador (Aceleración OLAP por GPU)
* **Título:** Evaluación de Aceleración por Hardware en Procesamiento OLAP: Evolución Histórica del Rendimiento de Héroes en Overwatch mediante GPU.
* **Planteamiento:** Análisis del cambio del "meta" competitivo evaluando la variación de estadísticas de personajes (como el impacto de Junkrat desde su aparición en la beta de 2015 hasta el presente) cruzando decenas de millones de registros de telemetría.
* **Solución Técnica:** Migración del procesamiento secuencial de CPU tradicional (Pandas) hacia un paralelismo masivo ejecutado directamente sobre la VRAM y los núcleos CUDA de la GPU mediante la suite **NVIDIA RAPIDS (cuDF)**.
* **Análisis de Riesgo:** Documentación del límite estricto de memoria (*Out of Memory*) de los 6GB de VRAM de la RTX 3050 frente a la capacidad de la CPU de utilizar el archivo de paginación (*Swap*) del disco duro.

---

## 👨‍💻 Autor
**Fabrizio Larco Jorquera** *Ingeniería Civil en Ciencia de Datos* *Universidad Tecnológica Metropolitana (UTEM) - Mayo 2026*
