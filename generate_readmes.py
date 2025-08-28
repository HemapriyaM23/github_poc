import os
import ast
from collections import defaultdict

README_TEMPLATE = """#{file_name}
## Code definition:
{definitions}
## Release Note
    v1.0
"""

def extract_defs(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        node = ast.parse(f.read(), filename=filepath)
    defs = []
    for n in node.body:
        if isinstance(n, ast.FunctionDef):
            doc = ast.get_docstring(n)
            doc_str = f": {doc.strip()}" if doc else ""
            defs.append(f"- **{n.name}**{doc_str}")
        elif isinstance(n, ast.ClassDef):
            doc = ast.get_docstring(n)
            doc_str = f": {doc.strip()}" if doc else ""
            defs.append(f"- **{n.name}**{doc_str}")
        elif isinstance(n, ast.Assign):
            for t in n.targets:
                if isinstance(t, ast.Name):
                    defs.append(f"- **{t.id}**: Module variable")
    return defs

def main():
    root = os.path.dirname(os.path.abspath(__file__))
    folder_pyfiles = defaultdict(list)
    for dirpath, _, files in os.walk(root):
        pyfiles = [f for f in files if f.endswith('.py') and f != os.path.basename(__file__)]
        for py in pyfiles:
            folder_pyfiles[dirpath].append(py)
    for folder, pyfiles in folder_pyfiles.items():
        readme_lines = []
        for py in pyfiles:
            defs = extract_defs(os.path.join(folder, py))
            defs_str = '\n'.join(defs) if defs else 'No functions or classes found.'
            readme_lines.append(README_TEMPLATE.format(file_name=py, definitions=defs_str))
        readme_path = os.path.join(folder, 'README.md')
        with open(readme_path, 'w', encoding='utf-8') as f:
            f.write('\n'.join(readme_lines))
    print('README.md files generated/updated for all folders.')

if __name__ == '__main__':
    main()
