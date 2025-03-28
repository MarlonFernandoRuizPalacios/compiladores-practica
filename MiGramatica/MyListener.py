from antlr4 import *
from MiGramaticaListener import MiGramaticaListener
from MiGramaticaParser import MiGramaticaParser

class MyListener(MiGramaticaListener):
    def __init__(self):
        super().__init__()
    
    # Detectar cuando se sale de un for loop
    def exitForLoop(self, ctx: MiGramaticaParser.ForLoopContext):
        print(f"\nDetectado ciclo For:")
        print(f"  Cuerpo del For contiene {len(ctx.sentencia())} sentencias")
    
    # Detectar la inicialización del for
    def exitInicializacion(self, ctx: MiGramaticaParser.InicializacionContext):
        var_name = ctx.ID().getText()
        value = ctx.expresion().getText()
        print(f"  Inicialización: {var_name} = {value}")
    
    # Detectar la condición del for
    def exitCondicion(self, ctx: MiGramaticaParser.CondicionContext):
        var_name = ctx.ID().getText()
        operator = ctx.op.text
        value = ctx.INT().getText()
        print(f"  Condición: {var_name} {operator} {value}")
    
    # Detectar la actualización del for
    def exitActualizacion(self, ctx: MiGramaticaParser.ActualizacionContext):
        var_name = ctx.ID().getText()
        expression = ctx.expresion().getText()
        print(f"  Actualización: {var_name} = {expression}")
    
    # Detectar asignaciones (dentro o fuera del for)
    def exitAssign(self, ctx: MiGramaticaParser.AssignContext):
        var_name = ctx.ID().getText()
        expression = ctx.expresion().getText()
        print(f"  Asignación detectada: {var_name} = {expression}")