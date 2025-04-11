import sys
from antlr4 import *
from CSVLexer import CSVLexer
from CSVParser import CSVParser
from CSVListener import CSVListener
import re

class Loader(CSVListener):
    EMPTY = ""
    def __init__(self):
        self.rows = []
        self.header = []
        self.currentRowFieldValues = []

    def enterRow(self, ctx:CSVParser.RowContext):
        self.currentRowFieldValues = []

    def exitText(self, ctx:CSVParser.TextContext):
        self.currentRowFieldValues.append(ctx.getText())

    def exitString(self, ctx:CSVParser.StringContext):
        self.currentRowFieldValues.append(ctx.getText().strip('"'))

    def exitEmpty(self, ctx:CSVParser.EmptyContext):
        self.currentRowFieldValues.append(self.EMPTY)

    def exitHeader(self, ctx:CSVParser.HeaderContext):
        self.header = list(self.currentRowFieldValues)

    def exitRow(self, ctx:CSVParser.RowContext):
        if ctx.parentCtx.getRuleIndex() == CSVParser.RULE_header:
            return

        m = {}
        for i, val in enumerate(self.currentRowFieldValues):
            key = self.header[i] if i < len(self.header) else f"col_{i}"
            m[key] = val.strip()
        self.rows.append(m)

def limpiar_cantidad(valor):
    """Limpia el valor de Cantidad y lo convierte a float si es válido"""
    if not valor or valor.lower() == "n/a":
        return None
    # Quitar $ y comas
    valor_limpio = re.sub(r'[^\d.]', '', valor)
    try:
        return float(valor_limpio)
    except ValueError:
        return None

def main(argv):
    input_stream = FileStream(argv[1], encoding='utf-8')
    lexer = CSVLexer(input_stream)
    stream = CommonTokenStream(lexer)
    parser = CSVParser(stream)
    tree = parser.csvFile()

    loader = Loader()
    walker = ParseTreeWalker()
    walker.walk(loader, tree)

    seen_rows = set()
    repeated_rows = []
    month_counter = {}
    month_totals = {}
    invalid_cantidad_rows = []

    for row in loader.rows:
        row_tuple = tuple(sorted(row.items()))
        if row_tuple in seen_rows:
            repeated_rows.append(row)
        else:
            seen_rows.add(row_tuple)

        mes = row.get("Mes", "").capitalize()
        cantidad_raw = row.get("Cantidad", "").strip()
        cantidad = limpiar_cantidad(cantidad_raw)

        # Contar ocurrencias por mes
        if mes:
            month_counter[mes] = month_counter.get(mes, 0) + 1

        # Validar y sumar cantidades
        if cantidad is not None:
            month_totals[mes] = month_totals.get(mes, 0.0) + cantidad
        else:
            invalid_cantidad_rows.append(row)

    print("\n--- Filas procesadas ---")
    for row in loader.rows:
        print(row)

    print("\n--- Frecuencia por mes ---")
    for mes, count in month_counter.items():
        print(f"{mes}: {count} veces")

    print("\n--- Filas repetidas ---")
    for row in repeated_rows:
        print(row)

    print("\n--- Cantidades inválidas o vacías ---")
    for row in invalid_cantidad_rows:
        print(row)

    print("\n--- Total de montos por mes ---")
    print(month_totals)

if __name__ == '__main__':
    main(sys.argv)
