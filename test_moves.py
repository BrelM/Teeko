#!/usr/bin/env python3
"""Test if Prolog AI finds moves correctly."""
import subprocess
import os

os.environ['Path'] = os.environ.get('Path', '') + ';C:\\Program Files\\swipl\\bin'

# Test 1: Check valid_moves
board = '[0]*25'
goal = f'''(
  consult('src/prolog_ai'),
  Board = {board},
  prolog_ai:valid_moves(Board, 1, Moves),
  length(Moves, Len),
  write('Moves count: '), write(Len), nl,
  write('First 5 moves: '),
  (Moves = [M1,M2,M3,M4,M5|_] -> write([M1,M2,M3,M4,M5]) ; write(Moves)), nl,
  halt
)'''

print("Test 1: valid_moves")
try:
    result = subprocess.run(
        ['swipl', '-q', '-g', goal],
        capture_output=True,
        text=True,
        timeout=5
    )
    print(result.stdout)
    if result.stderr:
        print("STDERR:", result.stderr)
except subprocess.TimeoutExpired:
    print("TIMEOUT")

# Test 2: Check make_move
goal2 = '''(
  consult('src/prolog_ai'),
  Board = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
  prolog_ai:make_move(Board, 0, 1, NewBoard),
  write('New board: '), write(NewBoard), nl,
  halt
)'''

print("\nTest 2: make_move")
try:
    result = subprocess.run(
        ['swipl', '-q', '-g', goal2],
        capture_output=True,
        text=True,
        timeout=5
    )
    print(result.stdout)
    if result.stderr:
        print("STDERR:", result.stderr)
except subprocess.TimeoutExpired:
    print("TIMEOUT")

# Test 3: Check evaluate
goal3 = '''(
  consult('src/prolog_ai'),
  Board = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
  prolog_ai:evaluate(Board, 1, Score),
  write('Evaluation: '), write(Score), nl,
  halt
)'''

print("\nTest 3: evaluate")
try:
    result = subprocess.run(
        ['swipl', '-q', '-g', goal3],
        capture_output=True,
        text=True,
        timeout=5
    )
    print(result.stdout)
    if result.stderr:
        print("STDERR:", result.stderr)
except subprocess.TimeoutExpired:
    print("TIMEOUT")
