## DSL para Consultas de Empleados con ANTLR4 y Python

Este proyecto implementa un Lenguaje de Dominio Específico (DSL) para realizar consultas sobre datos de empleados almacenados en formato CSV. El proyecto utiliza ANTLR4 para el análisis léxico y sintáctico, y Python para la interpretación de las consultas.

## Descripción del Trabajo

Este proyecto implementa un Lenguaje de Dominio Específico (DSL) para consultas sobre datos de empleados en CSV, con:

- **Gramática ANTLR4** (`EmployeeDSL.g4`): define la sintaxis de comandos, filtros, agregaciones, ordenamientos y `print;`.
- **Intérprete en Python** (`employee_dsl_interpreter.py`): visitor que acumula operaciones y las ejecuta en un DataFrame de pandas, mostrando trazas DEBUG.
- **CLI principal** (`main_script.py`):  
  - `extract`, `run-all`, `run-json`, `run <n>`, `interactive`  
  - **`menu`** con 4 opciones:  
    1. Mostrar script y parse tree en consola  
    2. Mostrar columnas de `empleados.csv`  
    3. Generar imagen PNG del parse tree (requiere Python `graphviz` + binario Graphviz en `PATH`)  
    4. Salir  
- **Scripts de ejemplo**: 40 consultas en `example_scripts.json` (y extraíbles a `scripts/`).
- **Datos de prueba**: `empleados.csv` con 300 registros generados.

Con este conjunto se cubre diseño de gramática, parsing, visita de AST, ejecución diferida, interfaz de usuario y visualización gráfica del árbol sintáctico.  

## Estructura del Proyecto

```text
TrabajoFinal/
├── EmployeeDSL.g4
├── EmployeeDSLLexer.py
├── EmployeeDSLLexer.tokens
├── EmployeeDSLLexer.interp
├── EmployeeDSLParser.py
├── EmployeeDSLListener.py
├── EmployeeDSLVisitor.py
├── EmployeeDSL.tokens
├── EmployeeDSL.interp
├── employee_dsl_interpreter.py
├── main_script.py
├── example_scripts.json
├── empleados.csv
├── scripts/                   # DSL files extraídos (opción `extract`)
│   ├── script_01.dsl
│   ├── script_02.dsl
│   └── … 
├── __pycache__/
└── readme.txt
```

## Requisitos de Instalación

Python 3.7 o superior

ANTLR4 runtime para Python

pandas

numpy

graphviz

Instalar dependencias:
```pip install antlr4-python3-runtime pandas numpy```

```pip install graphviz```

## Pasos para Ejecutar el Proyecto

# 1. Generar datos de prueba

python generate_employee_data.py

Esto creará un archivo empleados.csv con 300 registros de empleados.

# 2. Extraer los scripts de ejemplo

python main.py extract

Esto extraerá los 40 scripts de ejemplo del archivo example_scripts.txt y los guardará como archivos individuales en el directorio scripts/.

# 3. Ejecutar scripts
Ejecutar todos los scripts de ejemplo:
```python main.py run-all```
Ejecutar un script específico (por ejemplo, el script 5):
```python main.py run 5```
Ejecutar en modo interactivo:
```python main.py interactive```
En el modo interactivo, puedes escribir comandos DSL línea por línea y ver los resultados inmediatamente después de un comando print;.

## Sintaxis del DLS

Comandos básicos:
load: Carga un archivo CSV

```load "empleados.csv";```
filter: Aplica un filtro a los datos

```
filter column "edad" > 25;
filter column "departamento" == "Tecnología";
filter column "salario" between 3000 and 4000;
```
aggregate: Realiza una operación de agregación
```
aggregate count column "id_empleado";
aggregate sum column "dias_laborados";
aggregate average column "salario";
```
sort: Ordena los datos
```
sort column "salario" desc;
sort column "edad" asc;
```
print: Ejecuta todas las operaciones acumuladas y muestra los resultados
```
print;
```
# Operadores soportados:
Comparación: >, <, >=, <=, ==, !=
Rango: between
Lógicos: and, or

## Parse Tree

Para visualizar el Parse Tree de un script específico se puede utlizar el comando:
```python3 main_script.py menu```
selecionar la tercera opcion y elegir el script el cual desea ver su arbol

## Detalles de Implementación

Gramática ANTLR4: Define la sintaxis del DSL, incluyendo reglas para comandos, filtros, agregaciones, y operadores.

Intérprete: Implementa un visitante que recorre el árbol sintáctico y acumula las operaciones para ejecutarlas cuando se encuentra un comando print;.

Conversión JSON: Los datos se cargan desde CSV y se convierten internamente a formato JSON para facilitar su manipulación y consulta.

Ejecución Diferida: Las operaciones de filtrado, agregación y ordenamiento se acumulan y solo se ejecutan cuando se encuentra un comando print;.

## Ejemplos

# Ejemplo 1: Filtrar empleados mayores de 25 años
```
load "empleados.csv";
filter column "edad" > 25;
aggregate count column "id_empleado";
aggregate average column "salario";
aggregate sum column "dias_laborados";
print;
```
# Ejemplo 2: Filtrar empleados de Tecnología con alto salario
```
load "empleados.csv";
filter column "departamento" == "Tecnología";
filter column "salario" > 3000;
aggregate count column "id_empleado";
aggregate average column "edad";
print;
```
# Ejemplo 3: Rango salarial específico
```
load "empleados.csv";
filter column "salario" between 3000 and 4000;
aggregate count column "id_empleado";
aggregate average column "edad";
print;
```
