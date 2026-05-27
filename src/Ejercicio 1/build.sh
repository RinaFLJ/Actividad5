#!/bin/bash
echo "Compilando el micro sistema operativo..."
# Esto crea el archivo boot.bin a partir de tu código
nasm -f bin boot.asm -o boot.bin

echo "Ejecutando en QEMU..."
# Esto lanza la ventana emulada
qemu-system-i386 -drive format=raw,file=boot.bin