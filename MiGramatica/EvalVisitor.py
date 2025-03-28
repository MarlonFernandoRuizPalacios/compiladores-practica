from antlr4 import *
from MiGramaticaVisitor import MiGramaticaVisitor
from MiGramaticaParser import MiGramaticaParser

class EvalVisitor(MiGramaticaVisitor):
    def __init__(self):
        super().__init__()
        self.variables = {}
    
    def visitPrograma(self, ctx: MiGramaticaParser.ProgramaContext):
        for sentencia in ctx.sentencia():
            self.visit(sentencia)
        return self.variables
    
    def visitAssign(self, ctx: MiGramaticaParser.AssignContext):
        var_name = ctx.ID().getText()
        value = self.visit(ctx.expresion())
        self.variables[var_name] = value
        return value
    
    def visitForLoop(self, ctx: MiGramaticaParser.ForLoopContext):
        # 1. Ejecutar inicialización
        self.visit(ctx.inicializacion())
        
        # 2. Evaluar condición y ejecutar cuerpo mientras sea verdadera
        while self._evaluate_condition(ctx.condicion()):
            # Ejecutar cada sentencia en el cuerpo del for
            for sentencia in ctx.sentencia():
                self.visit(sentencia)
            
            # 3. Ejecutar actualización
            self.visit(ctx.actualizacion())
    
    def _evaluate_condition(self, cond_ctx):
        # Método auxiliar para evaluar condiciones
        left = self.variables.get(cond_ctx.ID().getText(), 0)
        right = int(cond_ctx.INT().getText())
        op = cond_ctx.op.text
        
        if op == '<':
            return left < right
        elif op == '>':
            return left > right
        elif op == '==':
            return left == right
        elif op == '!=':
            return left != right
        else:
            raise ValueError(f"Operador desconocido: {op}")
    
    def visitInicializacion(self, ctx: MiGramaticaParser.InicializacionContext):
        var_name = ctx.ID().getText()
        value = self.visit(ctx.expresion())
        self.variables[var_name] = value
        return value
    
    def visitActualizacion(self, ctx: MiGramaticaParser.ActualizacionContext):
        return self.visitAssign(ctx)  # Reutilizamos la lógica de asignación
    
    def visitMulDiv(self, ctx: MiGramaticaParser.MulDivContext):
        left = self.visit(ctx.expresion(0))
        right = self.visit(ctx.expresion(1))
        op = ctx.op.text
        
        if op == '*':
            return left * right
        else:  # '/'
            return left // right  # División entera
    
    def visitAddSub(self, ctx: MiGramaticaParser.AddSubContext):
        left = self.visit(ctx.expresion(0))
        right = self.visit(ctx.expresion(1))
        op = ctx.op.text
        
        if op == '+':
            return left + right
        else:  # '-'
            return left - right
    
    def visitInt(self, ctx: MiGramaticaParser.IntContext):
        return int(ctx.INT().getText())
    
    def visitVariable(self, ctx: MiGramaticaParser.VariableContext):
        var_name = ctx.ID().getText()
        return self.variables.get(var_name, 0)