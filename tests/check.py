"""Run all retained suites and public-edition regressions with timeouts."""
from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]
commands = [
    [sys.executable, str(ROOT / 'tests' / 'test_parser.py')],
    [sys.executable, str(ROOT / 'tests' / 'test_runtime.py')],
    [sys.executable, str(ROOT / 'tests' / 'test_all.py')],
    [sys.executable, '-m', 'unittest', 'discover', '-s', str(ROOT / 'tests'), '-p', 'test_regressions.py', '-v'],
]
failed = False
for command in commands:
    try:
        result = subprocess.run(command, cwd=ROOT, timeout=30)
        failed |= result.returncode != 0
    except subprocess.TimeoutExpired:
        print('Suite exceeded its 30-second timeout.', file=sys.stderr)
        failed = True
sys.exit(1 if failed else 0)
