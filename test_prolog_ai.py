"""
Simple test harness for Prolog AI integration.
Runs a few sample positions through the Python wrapper and prints results.
This test will skip if swipl is not available or if Prolog file missing.
"""
from pathlib import Path
import shutil
import sys

try:
    from src.prolog_ai import compute_best_move
except Exception as e:
    print('Could not import prolog_ai:', e)
    sys.exit(0)

PROLOG = Path(__file__).resolve().parent / 'src' / 'prolog_ai.pl'
if not PROLOG.exists():
    print('Prolog file not found:', PROLOG)
    sys.exit(0)

# check swipl executable
if not shutil.which('swipl'):
    print('swipl not found on PATH; subprocess mode will fail. Install SWI-Prolog or run with pyswip.')

# Empty board test
board_empty = [0]*25
print('Empty board, player 1, depth 2:')
print(compute_best_move(board_empty, 1, depth=2, timeout=1.0))

# A near-winning position for player 1 (horizontal 3 in a row at top row positions 0,1,2)
board_test = [1,1,1,0,0,
              0,0,0,0,0,
              0,0,0,0,0,
              0,0,0,0,0,
              0,0,0,0,0]
print('Near-win board, player 1, depth 3:')
print(compute_best_move(board_test, 1, depth=3, timeout=1.0))

print('Done.')
