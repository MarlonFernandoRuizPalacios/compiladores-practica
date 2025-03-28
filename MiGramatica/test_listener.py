from antlr4 import *
from MiGramaticaLexer import MiGramaticaLexer
from MiGramaticaParser import MiGramaticaParser
from MyListener import MyListener

def main():
    # Obtener entrada del usuario
    input_text = input("Ingrese el código a analizar (ej. for (i=0; i<3; i=i+1) { x=x+2; }): ")
    
    # Crear el analizador léxico y sintáctico
    lexer = MiGramaticaLexer(InputStream(input_text))
    stream = CommonTokenStream(lexer)
    parser = MiGramaticaParser(stream)
    tree = parser.programa()
    
    # Crear y ejecutar el listener
    listener = MyListener()
    walker = ParseTreeWalker()
    walker.walk(listener, tree)

if __name__ == '__main__':
    main()