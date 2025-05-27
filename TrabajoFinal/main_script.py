import os
import sys
import json
import pandas as pd
from antlr4 import InputStream, CommonTokenStream
from antlr4.tree.Tree import ParseTree
#from graphviz import Digraph
from EmployeeDSLLexer import EmployeeDSLLexer
from EmployeeDSLParser import EmployeeDSLParser
from employee_dsl_interpreter import parse_and_interpret

# --- Utility to generate parse tree image ---
def save_parse_tree(root: ParseTree, parser, out_path: str):
    dot = Digraph(format='png')
    def recurse(node):
        nid = str(id(node))
        if hasattr(node, 'getRuleIndex') and node.getRuleIndex() >= 0:
            label = parser.ruleNames[node.getRuleIndex()]
        else:
            label = node.getText().replace('"', '\\"')
        dot.node(nid, label)
        for i in range(node.getChildCount()):
            child = node.getChild(i)
            cid = str(id(child))
            recurse(child)
            dot.edge(nid, cid)
    recurse(root)
    dot.render(out_path, cleanup=True)

# --- Core functionality ---
def print_result(result, title):
    sep = "=" * 50
    print(f"\n{sep}\nEjecutando: {title}\n{sep}")
    print(f"Registros encontrados: {result['record_count']}")
    if result['aggregations']:
        print("\nAgregaciones:")
        for name, val in result['aggregations'].items():
            func, col = name.split('_', 1)
            fmt = f"{val:.2f}" if func in ('sum','average') else f"{val}"
            print(f"{func.capitalize()} de {col}: {fmt}")
    if result['record_count'] > 0:
        print("\nPrimeros 5 registros:")
        for i, rec in enumerate(result['filtered_data'][:5], 1):
            print(f"{i}. {json.dumps(rec, ensure_ascii=False)}")
    if result['record_count'] > 5:
        print(f"... y {result['record_count'] - 5} registros más.")
    print(sep + "\n")


def run_script(content, name):
    try:
        result = parse_and_interpret(content)
        print_result(result, name)
        return True
    except Exception as e:
        print(f"Error al ejecutar {name}: {e}")
        return False

# --- Command implementations ---
def cmd_extract(json_file='example_scripts.json', out_dir='scripts'):
    if not os.path.exists(json_file):
        print(f"El archivo '{json_file}' no existe.")
        return
    os.makedirs(out_dir, exist_ok=True)
    for s in json.load(open(json_file, encoding='utf-8')):
        fname = os.path.join(out_dir, f"script_{str(s['numero']).zfill(2)}.dsl")
        open(fname, 'w', encoding='utf-8').write(s['contenido'])
        print(f"Extraído: {fname}")


def cmd_run_all(scripts_dir='scripts'):
    if not os.path.exists(scripts_dir):
        os.makedirs(scripts_dir)
        print(f"Directorio '{scripts_dir}' creado. Coloque archivos .dsl aquí.")
        return
    files = sorted(f for f in os.listdir(scripts_dir) if f.endswith('.dsl'))
    if not files:
        print(f"No se encontraron scripts en '{scripts_dir}'.")
        return
    succ = sum(run_script(open(os.path.join(scripts_dir, f), encoding='utf-8').read(), f) for f in files)
    print(f"\nEjecución completada: {succ} de {len(files)} scripts ejecutados correctamente.")


def cmd_run_json(json_file='example_scripts.json'):
    if not os.path.exists(json_file):
        print(f"El archivo '{json_file}' no existe.")
        return
    scripts = json.load(open(json_file, encoding='utf-8'))
    succ = 0
    for s in scripts:
        title = f"Script {s['numero']}: {s.get('titulo','')}"
        if run_script(s['contenido'], title): succ += 1
    print(f"\nEjecución completada: {succ} de {len(scripts)} scripts ejecutados correctamente.")


def cmd_run_one(num, scripts_dir='scripts'):
    fname = os.path.join(scripts_dir, f"script_{num.zfill(2)}.dsl")
    if os.path.exists(fname):
        run_script(open(fname, encoding='utf-8').read(), fname)
    else:
        print(f"El script {num} no existe en '{scripts_dir}'.")


def cmd_interactive():
    print("Modo interactivo. Escribe comandos DSL y termina con ';'. 'exit' para salir.")
    buffer = []
    while True:
        line = input('>> ').strip()
        if line.lower() == 'exit': break
        buffer.append(line)
        if line.endswith(';') and line.startswith('print'):
            run_script('\n'.join(buffer), 'Interactivo')
            buffer.clear()


def cmd_menu():
    df = pd.read_csv('empleados.csv')
    with open('example_scripts.json', encoding='utf-8') as f:
        scripts = json.load(f)
    while True:
        print("\nMenú principal:")
        print("1) Mostrar un test específico con su árbol de análisis")
        print("2) Mostrar una o varias columnas específicas de toda la data")
        print("3) Generar imagen de árbol sintáctico para un script")
        print("q) Salir")
        choice = input("Seleccione una opción: ").strip().lower()
        if choice == '1':
            for i, s in enumerate(scripts, 1): print(f"{i}) {s['titulo']}")
            sel = input("Seleccione un script por número (o 'q' para salir): ").strip().lower()
            if sel == 'q': continue
            if sel.isdigit() and 1 <= int(sel) <= len(scripts):
                s = scripts[int(sel) - 1]
                print(f"\nMostrando script: {s['titulo']}\n")
                print(s['contenido'])
                lexer = EmployeeDSLLexer(InputStream(s['contenido']))
                token_stream = CommonTokenStream(lexer)
                parser = EmployeeDSLParser(token_stream)
                tree = parser.program()
                print("\nÁrbol de análisis sintáctico (parse tree):")
                print(tree.toStringTree(recog=parser))
                run_script(s['contenido'], f"Script: {s['titulo']}")
        elif choice == '2':
            cols = df.columns.tolist()
            for i, c in enumerate(cols, 1): print(f"{i}) {c}")
            sel = input('Seleccione (comas o "a"=todas): ').strip().lower()
            if sel == 'a': sel_cols = cols
            else:
                idxs = [int(x) - 1 for x in sel.split(',') if x.isdigit()]
                sel_cols = [cols[i] for i in idxs if 0 <= i < len(cols)]
            print(df[sel_cols].to_string(index=False))
        elif choice == '3':
            for i, s in enumerate(scripts, 1): print(f"{i}) {s['titulo']}")
            sel = input("Seleccione un script por número (o 'q' para salir): ").strip().lower()
            if sel == 'q': continue
            if sel.isdigit() and 1 <= int(sel) <= len(scripts):
                s = scripts[int(sel) - 1]
                print(f"\nGenerando imagen del árbol sintáctico para: {s['titulo']}")
                lexer = EmployeeDSLLexer(InputStream(s['contenido']))
                token_stream = CommonTokenStream(lexer)
                parser = EmployeeDSLParser(token_stream)
                tree = parser.program()
                out_name = f"parse_tree_{str(sel).zfill(2)}"
                save_parse_tree(tree, parser, out_name)
                print(f"Imagen guardada como {out_name}.png")
        elif choice == 'q':
            break

# --- CLI dispatch ---
def main():
    cmds = {
        'extract': cmd_extract,
        'run-all': cmd_run_all,
        'run-json': cmd_run_json,
        'run': cmd_run_one,
        'interactive': cmd_interactive,
        'menu': cmd_menu,
    }
    if len(sys.argv) < 2 or sys.argv[1] not in cmds:
        print("Uso: python main_script.py [extract|run-all|run-json|run <n>|interactive|menu]")
        return
    cmd = sys.argv[1]
    arg = sys.argv[2] if len(sys.argv) > 2 else None
    if cmd == 'run': cmds[cmd](arg)
    else: cmds[cmd]()

if __name__ == '__main__':
    main()
