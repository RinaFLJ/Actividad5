# Infraestructura-Actividad1
Trabajo de la actividad 1

# Actividad N° 1: Boot de Micro S.O. en QEMU

**Asignatura:** Infraestructura para Ciencia de Datos
**Estudiante:** Fabrizio Larco Jorquera
[cite_start]**Fecha:** 08 de abril de 2026

## 1\. Descripción del Proyecto

Este proyecto consiste en la construcción de un micro sistema operativo desarrollado en lenguaje ensamblador (x86). El objetivo es comprender las capas fundamentales de un entorno de cómputo: código fuente, ensamblado, artefacto binario y virtualización. Al iniciar, el sistema despliega el mensaje "Hola" en pantalla a través de la emulación en QEMU.

## 2. Estructura del Repositorio

Para asegurar la trazabilidad del proceso, el proyecto se organiza de la siguiente manera:

  *`src/`: Contiene el código fuente en ensamblador (`boot.asm`).
  *`docs/`: Informe académico y documentación técnica.
  *`img/`: Evidencias visuales (capturas de pantalla) del funcionamiento.
  *`boot.bin`: Artefacto binario generado para el arranque.

## 3. Requisitos del Sistema

Para reproducir este proyecto en un entorno Linux (distribuciones basadas en Debian/Ubuntu), es necesario instalar:

  * **NASM:** Ensamblador para la generación del binario.
  * **QEMU:** Entorno de emulación para la ejecución.

Instalación rápida:

```bash
sudo apt update && sudo apt install nasm qemu-system-x86 -y
```

## 4. Instrucciones de Reproducción

Siga estos pasos para compilar y ejecutar el micro S.O. desde la raíz del repositorio:

### Paso A: Compilación (Generación del artefacto)

```bash
nasm -f bin src/boot.asm -o boot.bin
```

### Paso B: Ejecución en entorno virtualizado

```bash
qemu-system-x86_64 -drive format=raw,file=boot.bin
```

# 5. Reflexión Académica 

La relevancia de esta actividad para la **Ingeniería Civil en Ciencia de Datos** radica en la comprensión de la relación entre el hardware, el software base y la virtualización. Este conocimiento es fundamental para abordar posteriormente entornos más complejos como máquinas virtuales, contenedores (Docker) y la automatización de infraestructura reproducible.

-----