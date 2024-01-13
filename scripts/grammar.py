import subprocess
import sys
import pathlib
import re

output_file = 'frontend/parser/Parser.py'
source_dir = 'grammar'
build_dir = 'build'
root = r'C:\Users\Days_\PycharmProjects\KiwiPreview'

# REPLACEMENTS
# ------------>
REPLACEMENTS = {
    'CNAME': 'INDENT',
    'NULL': 'DEDENT'
}


def replacement(match):
    return REPLACEMENTS[match.group(1)] if match.group(1) in REPLACEMENTS else match.group(1)


build_path = pathlib.Path(root) / build_dir
source_path = pathlib.Path(root) / source_dir
output_path = pathlib.Path(root) / output_file

if __name__ == '__main__':
    try:
        grammar = str()
        for file in source_path.glob('*.gram'):
            with open(file, 'r') as f:
                if file.stem == 'main':
                    grammar = f.read() + '\n' + grammar
                else:
                    grammar += f.read() + '\n'
        grammar = re.sub(r'\b([A-Z]+)\b', replacement, grammar, flags=re.DOTALL)
        grammar = re.sub(r'^\s*(->\s*)+', str(), grammar, flags=re.MULTILINE)
        # Run replacements on the grammar file
        build_path.mkdir(parents=True, exist_ok=True)
        with open(build_path / 'grammar', 'w+') as f:
            f.write(grammar)
        # `python -m pegen -o <output-file> <source-file>`
        subprocess.run(['python', '-m', 'pegen', '-o', output_file, build_path.relative_to(root) / 'grammar'],
                       cwd=root, check=True)
        with open(output_path, 'r') as f:
            lines = f.readlines()
        with open(output_path, 'w') as f:
            for line in lines:
                if re.fullmatch(r"\s*if\s*__name__\s*==\s*'__main__'\s*:\s*", line):
                    break
                f.write(line)
        subprocess.run(['black', output_file], cwd=root, check=True)
    except subprocess.CalledProcessError as e:
        sys.exit(e.returncode)
