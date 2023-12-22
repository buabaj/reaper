import ast
import argparse 
import multiprocessing
import json
import os


CHECKS = [
    'imports',
    'functions', 
    'classes',
    'methods',
    'attributes',
    'locals',
    'globals'
]

class Reaper:

    def __init__(self, source, config, filename):
        self.source = source
        self.config = config
        self.tree = ast.parse(self.source)
        self.filename = filename  # Store the filename

    def run(self):
        results = {}
        for check in self.config['checks']:
            if check in CHECKS:
                results[check] = getattr(self, f'check_{check}')()
        print(f"File: {self.filename}")  # Print the filename
        print(json.dumps(results, indent=2))

    def check_imports(self):
        imports = [n for n in ast.walk(self.tree) if isinstance(n, ast.Import)]
        return [i.names[0].name for i in imports if not self._is_used(i.names[0].name, self.tree)]

    def check_functions(self):
        functions = [n for n in ast.walk(self.tree) if isinstance(n, ast.FunctionDef)]
        return [f.name for f in functions if not self._is_used(f.name, self.tree)]

    def check_classes(self):
        classes = [n for n in ast.walk(self.tree) if isinstance(n, ast.ClassDef)]
        return [c.name for c in classes if not self._is_used(c.name, self.tree)]

    def check_methods(self):
        methods = []
        for n in ast.walk(self.tree):
            if isinstance(n, ast.ClassDef):
                methods.extend([m.name for m in n.body if isinstance(m, ast.FunctionDef)])
        return [m for m in set(methods) if not self._is_used(m, self.tree)]

    def check_attributes(self):
        attributes = []
        for n in ast.walk(self.tree):
            if isinstance(n, ast.Attribute):
                attributes.append(n.attr)
        return [a for a in set(attributes) if not self._is_used(a, self.tree)]

    def check_locals(self):
        locals_ = []
        for n in ast.walk(self.tree):
            if isinstance(n, ast.FunctionDef) or isinstance(n, ast.Module):
                for node in n.body:
                    if isinstance(node, ast.Assign) and not (isinstance(node.value, ast.Call) and isinstance(node.value.func, ast.Name)):
                        locals_.extend(t.id for t in node.targets if isinstance(t, ast.Name))
        return [l for l in set(locals_) if not self._is_used(l, self.tree)]

    def check_globals(self):
        globals_ = [n.id for n in ast.walk(self.tree) if isinstance(n, ast.Global)]
        return [g for g in globals_ if not self._is_used(g, self.tree)]

    def _is_used(self, name, scope):
        for node in ast.walk(scope):
            if isinstance(node, ast.Name) and node.id == name:
                return True
            if isinstance(node, ast.Import) and name in [n.name for n in node.names]:
                return True
        return False


import os

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('paths', nargs='+', help='Files or directory path(s) containing Python code')
    parser.add_argument('-c', '--config', required=True)

    args = parser.parse_args()

    with open(args.config) as f:
        config = json.load(f)

    python_files = []

    for path in args.paths:
        if os.path.isdir(path):
            for root, dirs, files in os.walk(path):
                for file in files:
                    if file.endswith('.py'):
                        python_files.append(os.path.join(root, file))
        elif os.path.isfile(path) and path.endswith('.py'):
            python_files.append(path)

    with multiprocessing.Pool() as pool:
        reapers = [Reaper(open(file).read(), config, file) for file in python_files]
        pool.map(Reaper.run, reapers)
