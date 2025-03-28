from antlr4 import *
from MiGramaticaVisitor import MiGramaticaVisitor
from MiGramaticaParser import MiGramaticaParser

class EvalVisitor(MiGramaticaVisitor):
    def __init__(self):
        super().__init__()
        self.variables = {}
    
    # Visitar el programa principal
    def visitPrograma(self, ctx: MiGramaticaParser.ProgramaContext):
        for sentencia in ctx.sentencia():
            self.visit(sentencia)
        return self.variables
    
    # Visitar una asignación
    def visitAssign(self, ctx: MiGramaticaParser.AssignContext):
        var_name = ctx.ID().getText()
        value = self.visit(ctx.expresion())
        self.variables[var_name] = value
        return value
    
    # Visitar un ciclo for
    def visitForLoop(self, ctx: MiGramaticaParser.ForLoopContext):
        # Procesar inicialización
        self.visit(ctx.inicializacion())
        
        # Ejecutar el ciclo mientras la condición sea verdadera
        while self.visit(ctx.condicion()):
            # Ejecutar cada sentencia en el cuerpo del for
            for sentencia in ctx.sentencia():
                self.visit(sentencia)
            
            # Procesar actualización
            self.visit(ctx.actualizacion())
    
    # Visitar una condición
    def visitCondicion(self, ctx: MiGramaticaParser.CondicionContext):
        var_value = self.variables.get(ctx.ID().getText(), 0)
        condition_value = int(ctx.INT().getText())
        op = ctx.op.text
        
        if op == '<':
            return var_value < condition_value
        elif op == '>':
            return var_value > condition_value
        elif op == '==':
            return var_value == condition_value
        elif op == '!=':
            return var_value != condition_value
        else:
            raise ValueError(f"Operador desconocido: {op}")
    
    # Visitar operaciones de suma/resta
    def visitAddSub(self, ctx: MiGramaticaParser.AddSubContext):
        left = self.visit(ctx.expresion(0))
        right = self.visit(ctx.expresion(1))
        op = ctx.op.text
        
        if op == '+':
            return left + right
        else:  # '-'
            return left - right
    
    # Visitar operaciones de multiplicación/división
    def visitMulDiv(self, ctx: MiGramaticaParser.MulDivContext):
        left = self.visit(ctx.expresion(0))
        right = self.visit(ctx.expresion(1))
        op = ctx.op.text
        
        if op == '*':
            return left * right
        else:  # '/'
            return left // right  # División entera
    
    # Visitar un entero
    def visitInt(self, ctx: MiGramaticaParser.IntContext):
        return int(ctx.INT().getText())
    
    # Visitar una variable
    def visitVariable(self, ctx: MiGramaticaParser.VariableContext):
        var_name = ctx.ID().getText()
        return self.variables.get(var_name, 0)