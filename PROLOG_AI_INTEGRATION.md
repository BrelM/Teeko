# Prolog AI Integration (MinMax / Alpha-Beta)

This document describes how to implement a MinMax-based AI (optionally with Alpha-Beta pruning) in Prolog and how to integrate it with the Python code in this project so you can enable computer players.

Contents
- Overview
- Prolog design: data representation and API
- MinMax & Alpha-Beta: predicates and pseudo-code
- Evaluation heuristics (what to score)
- Performance: iterative deepening, transposition table, move ordering, timeouts
- Python integration options
  - Option A: `pyswip` (embedded SWI-Prolog)
  - Option B: `swipl` subprocess call
- Example Python wrapper (`src/prolog_ai.py`) sketch
- How to wire into `src/ai.py` / `src/control.py` / `src/player.py`
- Testing & tuning checklist

---

## Overview

- Implement the game-search logic in Prolog where the ``best_move/4`` or ``best_move/5`` predicate returns the selected move and optionally a score.
- Keep the Prolog code focused on search, move generation, and evaluation; call it from Python when an AI player's turn arrives.
- Use a compact board representation (flat list or nested lists) for easy marshaling between Python and Prolog.

Goals for the Prolog side:
- `valid_moves(Board, Player, Moves)` — enumerate legal moves
- `make_move(Board, Move, Player, NewBoard)` — apply a move
- `terminal(Board, Winner)` — detect terminal/win states
- `evaluate(Board, Player, Score)` — heuristic evaluation
- `minimax/alphabeta` implementation to choose best move
- `best_move(Board, Player, MaxDepth, Move)` — public API predicate


## Data representation

Use simple integers for squares and a flat list for the board. Example (5×5 Teeko board):

- Use a flat list of 25 elements: index 0..24, row-major order.
- Cell values: `0 = empty`, `1 = player1`, `2 = player2`.

Prolog example board (conceptual):

```prolog
% Example initial board: all empty
Board = [0,0,0,0,0, 0,0,0,0,0, 0,0,0,0,0, 0,0,0,0,0, 0,0,0,0,0].
```

When communicating from Python, serialize the board into a Prolog list literal like: `[0,1,0,2,...]`.

Move representation:
- For placement moves: use the cell index (0..24).
- For movement moves: use a compound term `move(From,To)` or represent as `[From,To]`.


## Prolog API (recommended predicate signatures)

- `best_move(+Board, +Player, +MaxDepth, -Move).`
  - Board: list of 25 integers
  - Player: 1 or 2
  - MaxDepth: depth limit for MinMax
  - Move: chosen move (index or `move(From,To)`)

- `best_move(+Board, +Player, +MaxDepth, -Move, -Score).` — also return score
- `valid_moves(+Board, +Player, -Moves).`
- `make_move(+Board, +Move, +Player, -NewBoard).`
- `terminal(+Board, -Winner).` Winner = 0 (no), 1, 2, or tie
- `evaluate(+Board, +Player, -Score).`


## MinMax / Alpha-Beta (Prolog pseudo-code)

The Prolog version follows the usual search structure. Example pseudocode (sketch):

```prolog
% best_move(Board, Player, Depth, BestMove, BestScore)
best_move(Board, Player, Depth, BestMove, BestScore) :-
    valid_moves(Board, Player, Moves),
    % If no moves (shouldn't happen often), return fail or special value
    findall(Score-Mv,
            ( member(Mv, Moves),
              make_move(Board, Mv, Player, NewBoard),
              Opp is 3 - Player,
              D1 is Depth - 1,
              minimax(NewBoard, Opp, D1, Score0),
              Score is -Score0 ),
            Pairs),
    sort(0, @>=, Pairs, Sorted),
    Sorted = [BestScore-BestMove | _].

% minimax(Board, Player, Depth, Score)
minimax(Board, _Player, 0, Score) :-
    evaluate(Board, _Player, Score), !.
minimax(Board, Player, Depth, Score) :-
    terminal(Board, Winner),
    ( Winner =:= 0 ->
        ( valid_moves(Board, Player, Moves), Moves \= [] ->
            findall(S, ( member(M, Moves), make_move(Board, M, Player, NB), Opp is 3-Player, D1 is Depth-1, minimax(NB, Opp, D1, S0), S is -S0 ), Scores),
            max_list(Scores, Score)
        ; Score = 0 % no moves
        )
    ; % terminal
        ( Winner = Player -> Score = 10000 ; Score = -10000 )
    ).
```

Alpha-Beta variant: add `alpha` and `beta` parameters and prune when `alpha >= beta`. For performance, implement iterative deepening and move ordering.


## Evaluation heuristics

A robust evaluation function is essential. Ideas (combine into weighted sum):

- Win/loss detection: return large +/− constants when terminal.
- Threats: number of lines (rows/cols/diags) where the player has n pieces and opponent has none.
- Two-in-a-row / three-in-a-row counts (open-ended counts).
- Square potentials: how many 2×2 squares contain player's pieces.
- Center control: reward pieces closer to board center.
- Mobility: number of valid moves (more mobility is better).
- Clustering/compactness: penalize badly spread pieces.

Tune weights based on play testing.


## Performance tips

- Use iterative deepening: repeat depth 1..MaxDepth and return best result within time limit.
- Use transposition table (hash table) to cache evaluated boards. Implement either in Prolog (dynamic predicates) or in Python wrapper.
- Move ordering: order captures/winning moves first, or moves that increase alignment.
- Alpha-Beta pruning drastically reduces nodes — recommended.
- Limit search depth depending on phase: placement phase often smaller branching factor, movement phase may need deeper search.
- Respect a time budget per move; if time exceeds, return the best-so-far move.


## Python integration options

Two practical approaches:

### Option A — Embedded (pyswip)

Pros: Lower overhead, direct calls into Prolog. Cons: pyswip setup and data marshaling overhead.

Install:
```powershell
pip install pyswip
```

Example wrapper (sketch):

```python
# src/prolog_ai.py
from pyswip import Prolog
prolog = Prolog()
prolog.consult('prolog_ai.pl')  # Your Prolog file path

def board_to_prolog_list(board):
    # board is e.g., nested list or flat list of ints
    return '[' + ','.join(str(x) for x in board) + ']'

def get_ai_move(board, player, depth=3):
    b = board_to_prolog_list(board)
    qry = f"best_move({b},{player},{depth},Move,Score)"
    for sol in prolog.query(qry, maxresult=1):
        return sol['Move'], sol.get('Score')
    return None
```

Notes:
- Represent `Move` in a Prolog-friendly format; pyswip will return Prolog terms that you can parse.
- You may need to write Prolog helper predicates that print or serialize the chosen move into a simple form for easy parsing.


### Option B — subprocess (swipl command-line)

Pros: Simple, avoids additional Python packages. Cons: higher process cost per move; use caching or keep a long-running Prolog process if needed.

Example using `subprocess` to call SWI-Prolog (Windows `swipl.exe`):

```python
# src/prolog_ai.py
import subprocess, shlex, tempfile

SWIPL = 'swipl'  # or full path to swipl.exe
PROLOG_FILE = 'prolog_ai.pl'

def get_ai_move_subprocess(board, player, depth=3, timeout=5.0):
    b = '[' + ','.join(map(str, board)) + ']'
    # Construct a goal that writes the move in a machine-friendly format
    prolog_goal = f"(best_move({b},{player},{depth},Move,Score), write_canonical(Move), write(':'), write(Score), nl, halt)"
    cmd = [SWIPL, '-q', '-s', PROLOG_FILE, '-g', prolog_goal]
    try:
        out = subprocess.check_output(cmd, stderr=subprocess.STDOUT, timeout=timeout)
        text = out.decode('utf-8').strip()
        if not text:
            return None
        move_str, score_str = text.split(':')
        # parse move_str (canonical Prolog output) as needed
        return move_str, int(score_str)
    except subprocess.TimeoutExpired:
        # Timeout: fallback to some policy
        return None
```

Notes:
- `write_canonical/1` outputs a consistent text representation of a Prolog term — parse it in Python.
- For repeated moves, prefer a persistent Prolog process to avoid startup cost — e.g., use `pexpect` or a custom RPC over stdin/stdout.


## Example Python wrapper sketch (recommended: `src/prolog_ai.py`)

- Expose `compute_best_move(board, player_id, depth, timeout=None)` which returns a `Move` representing either a placement index or a movement `from->to`.
- If `player.is_ai`, call this helper in the controller when it's the AI player's turn.

Sketch:

```python
# src/prolog_ai.py
import subprocess

def compute_best_move(board_flat, player_id, depth=3, use_pyswip=False, timeout=5.0):
    if use_pyswip:
        # use pyswip wrapper
        from pyswip import Prolog
        prolog = Prolog()
        prolog.consult('prolog_ai.pl')
        b = '[' + ','.join(map(str, board_flat)) + ']'
        qry = f"best_move({b},{player_id},{depth},Move,Score)"
        for sol in prolog.query(qry, maxresult=1):
            return sol['Move']
    else:
        # subprocess call
        PROLOG_FILE = 'prolog_ai.pl'
        SWIPL = 'swipl'
        b = '[' + ','.join(map(str, board_flat)) + ']'
        goal = f"(best_move({b},{player_id},{depth},Move,Score), write_canonical(Move), write(':'), write(Score), nl, halt)"
        cmd = [SWIPL, '-q', '-s', PROLOG_FILE, '-g', goal]
        out = subprocess.check_output(cmd, stderr=subprocess.STDOUT, timeout=timeout)
        text = out.decode().strip()
        move_str, score_str = text.split(':')
        return move_str
```


## Wiring into the Python codebase

1. Add a wrapper module `src/prolog_ai.py` (see sketch above).
2. In `src/player.py`, ensure `Player` can be AI-controlled:`is_ai = True` and optionally have `ai_depth`, `ai_timeout` fields.
3. In `src/control.py` (GameController) or the game loop, when it is an AI player's turn:
   - If phase == "placement": call `compute_best_move` to get a cell index, then call `place_piece(row, col)`.
   - If phase == "movement": call `compute_best_move` to get `move(From,To)` and call `move_piece(from_row, from_col, to_row, to_col)`.

Example (in controller or GUI main loop):

```python
# when it's the current player's turn and player.is_ai:
player = controller.get_current_player()
if player.is_ai:
    board_flat = controller.board.get_board_flat()  # implement this convenience method
    move = prolog_ai.compute_best_move(board_flat, player.player_id, depth=player.ai_depth)
    if is_placement_move(move):
        r, c = index_to_rc(move)
        controller.place_piece(r, c)
    else:
        from_index, to_index = parse_move(move)
        controller.move_piece(*index_to_rc(from_index), *index_to_rc(to_index))
```


## Example: board helper methods to add in `src/ai.py` or `src/control.py`

- `get_board_flat()` returns the board as a flat list 0..24 suitable for passing to Prolog.
- `index_to_rc(index)` and `rc_to_index(r,c)` helpers.

Add these small helpers to `src/ai.py` (TeekoBoard) so Prolog wrapper receives the right format.


## Testing & tuning checklist

- [ ] Implement `prolog_ai.pl` with `best_move/5` and helper predicates.
- [ ] Add `src/prolog_ai.py` to call Prolog and parse the returned move.
- [ ] Add `get_board_flat()` to `TeekoBoard` (or add a small converter in `prolog_ai.py`).
- [ ] Add a test harness to compare random positions against a shallow MinMax to confirm reasonable moves.
- [ ] Tune evaluation weights with self-play.
- [ ] Add timeouts and iterative deepening for robust performance.


## Notes and tips

- Start with a simple MinMax (depth 2–4) and a simple evaluation function; make it fast and correct before adding pruning or heavy heuristics.
- Use Alpha-Beta as soon as possible — the speed improvement is substantial.
- For Windows users, ensure SWI-Prolog (`swipl.exe`) is installed and on PATH if using subprocess.
- If using `pyswip`, install the package and ensure SWI-Prolog development headers are available if needed.


## Appendix: minimal Prolog helper idea

A small Prolog file `prolog_ai.pl` might export:

```prolog
:- module(prolog_ai, [best_move/5]).

% Implement: valid_moves/3, make_move/4, terminal/2, evaluate/3
% Implement: minimax/5 or alphabeta/7

best_move(Board, Player, Depth, BestMove, BestScore) :-
    % compute and unify BestMove and BestScore
    ...
```

Keep the implementation in a single committed Prolog source file (`prolog_ai.pl`) and consult it from Python.

---

If you'd like, I can:
- Create a starter `prolog_ai.pl` with a working MinMax and very simple evaluation (toy example), or
- Create `src/prolog_ai.py` wrapper (subprocess + parsing) and add `get_board_flat()` helper into `src/ai.py`, or
- Provide a full example that uses `pyswip`.

Tell me which option you prefer and I will implement the code (Prolog file and/or Python wrapper) and wire it into the codebase.
