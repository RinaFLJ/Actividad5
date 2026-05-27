[bits 16]
[org 0x7c00]

start:
    ; 1. Configurar segmentos de memoria
    xor ax, ax
    mov ds, ax
    mov ss, ax
    mov sp, 0x7c00
    mov ax, 0xb800
    mov es, ax

    ; 2. Limpiar pantalla completa
    mov di, 0
    mov cx, 2000         ; 80 columnas x 25 filas
    mov ax, 0x0720       ; Espacio en blanco, fondo negro, letra gris
    rep stosw

    ; 3. Dibujar Escudo UTEM (Centrado arriba)
    mov si, msg_logo
    mov di, 160 * 1 + 64 ; Fila 1, Columna 32 (Centro)
    mov ah, 0x0B         ; Color Cyan
    mov cx, 9            ; 9 lineas de logo
.logo_loop:
    push cx
    mov cx, 16           ; 16 caracteres por linea
.logo_line:
    lodsb
    mov byte [es:di], al
    inc di
    mov byte [es:di], ah
    inc di
    loop .logo_line
    add di, 128          ; Salto a la siguiente linea
    pop cx
    loop .logo_loop

    ; 4. Imprimir Titulo y Nombre (Debajo del logo)
    mov ah, 0x0E         ; Color Amarillo
    mov si, msg_curso
    mov di, 160 * 12 + 16 ; Fila 12, Columna 8
    call print_string

    mov ah, 0x0A         ; Color Verde claro
    mov si, msg_nombre
    mov di, 160 * 14 + 16 ; Fila 14, Columna 8
    call print_string

    ; 5. Imprimir las 3 lineas explicativas
    mov ah, 0x0F         ; Color Blanco
    mov si, msg_exp1
    mov di, 160 * 17 + 10 ; Fila 17, Columna 5
    call print_string

    mov si, msg_exp2
    mov di, 160 * 19 + 10 ; Fila 19, Columna 5
    call print_string

    mov si, msg_exp3
    mov di, 160 * 21 + 10 ; Fila 21, Columna 5
    call print_string

    ; 6. Detener el procesador
halt_loop:
    cli
    hlt
    jmp halt_loop

; -----------------------------------------------------
; FUNCION: Imprimir cadena en memoria VGA
; -----------------------------------------------------
print_string:
.next_char:
    lodsb
    or al, al
    jz .done
    mov byte [es:di], al
    inc di
    mov byte [es:di], ah
    inc di
    jmp .next_char
.done:
    ret

; -----------------------------------------------------
; DATOS TEXTUALES
; -----------------------------------------------------
msg_logo    db "  ____________  ", " |        ### | ", " |        ### | ", " | @@@@       | ", " |  @@@       | ", " |   @        | ", "  \          /  ", "   '--------'   ", "    U T E M     "

msg_curso   db "Curso: INFB6074 - Infraestructura de Datos", 0
msg_nombre  db "Nombre: Fabrizio Larco Jorquera", 0

msg_exp1    db "1. El Bootloader es cargado por la BIOS en 0x7C00.", 0
msg_exp2    db "2. La CPU en Real Mode solo puede direccionar 1MB.", 0
msg_exp3    db "3. La memoria VGA inicia en 0xB8000 (Modo Texto).", 0

; -----------------------------------------------------
; FIRMA DE ARRANQUE (Requisito estricto de 512 bytes)
; -----------------------------------------------------
times 510 - ($ - $$) db 0
dw 0xAA55