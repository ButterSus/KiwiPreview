import subprocess
import sys

output_file = 'frontend/syntax/moduleSyntaxAnalyzerInterface.py'
source_file = 'resources/kiwi.gram'
root = r'C:\Users\Days_\PycharmProjects\KiwiPreview'

if __name__ == '__main__':
    try:
        # `python -m pegen -o <output-file> <source-file>`
        subprocess.run(['python', '-m', 'pegen', '-o', output_file, source_file], cwd=root, check=True)

        # reformat the generated file with black
        subprocess.run(['black', output_file], cwd=root, check=True)
    except subprocess.CalledProcessError as e:
        sys.exit(e.returncode)
