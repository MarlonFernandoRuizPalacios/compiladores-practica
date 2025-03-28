from antlr4 import *
from MiGramaticaLexer import MiGramaticaLexer
from MiGramaticaParser import MiGramaticaParser
from EvalVisitor import EvalVisitor

def main():
    # Obtener entrada del usuario
    input_text = input("Ingrese el código a ejecutar (ej. for (i=0; i<3; i=i+1) { x=x+2; }): ")
    
    # Crear el analizador léxico y sintáctico
    lexer = MiGramaticaLexer(InputStream(input_text))
    stream = CommonTokenStream(lexer)
    parser = MiGramaticaParser(stream)
    tree = parser.programa()
    
    # Crear y ejecutar el visitor
    visitor = EvalVisitor()
    variables = visitor.visit(tree)
    
    # Mostrar resultados
    print("\nEstado final de las variables:")
    for var, value in variables.items():
        print(f"{var} = {value}")

if __name__ == '__main__':
    main()