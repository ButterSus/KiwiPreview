import subprocess
import sys

root = r'C:\Users\Days_\PycharmProjects\KiwiPreview'

if __name__ == '__main__':
    try:
        # `handshown -o docs`
        subprocess.run(['handshown', '-o', 'docs'], cwd=root, check=True)
    except subprocess.CalledProcessError as e:
        sys.exit(e.returncode)
