# Final-compiler
### Guillermo Tanamachi - A01631327

## Uso

1. Escribir el código deseado en un archivo .txt
2. Correr el archivo **.\gtc.py <ruta_del_archivo.txt>** para compilar
3. Código de tres direcciones se redirigirá al archivo **.\output.txt**

> El código de tres direcciones será redirigido, pero el árbol sintáctico se imprimirá en consola

## Especificación del lenguaje

Tipos de datos:
- int
- float
- boolean

Opearciones:
- **Aritméticas:** +, -, *, /, ^
- **Booleanas:** and, or

Comparaciones (Sólo int y float):
- ==
- != 
- \>
- <
- \>=
- <=

Estructuras de flujo:
```
if (booleano | condición) {
  // Código if
}
```
```
while (booleano | condición) {
  // Código while
}
```
