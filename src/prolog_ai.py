"""
prolog_ai.py
Python wrapper for Prolog AI (MinMax). Supports two modes:
 - subprocess call to `swipl` (default)
 - pyswip embedded (optional)

Provides `compute_best_move(board_flat, player_id, depth=3, use_pyswip=False, timeout=5.0)`

Board format: flat list of 25 ints (0 empty, 1 player1, 2 player2)
Move format returned: either integer index (placement) or tuple (from_index, to_index) for movement
"""
from pathlib import Path
import subprocess
import shlex
import sys

ROOT = Path(__file__).resolve().parent
PROLOG_FILE = ROOT / 'prolog_ai.pl'
SWIPL_CMD = 'swipl'  # adjust if swipl not on PATH

# Prefer pyswip (embedded SWI-Prolog) when available. Fallback to subprocess mode
_PYSWIP_PROLOG_CLASS = None
try:
    from pyswip import Prolog as _Prolog
    _PYSWIP_PROLOG_CLASS = _Prolog
    PYSWIP_AVAILABLE = True
except Exception:
    PYSWIP_AVAILABLE = False


def _board_to_prolog_list(board_flat):
    return '[' + ','.join(str(int(x)) for x in board_flat) + ']'


def _parse_move_text(move_text):
    move_text = move_text.strip()
    # canonical Prolog output for integer is like 5
    # for compound move(3,7) it will be move(3,7)
    if move_text.isdigit():
        return int(move_text)
    # try parse move(From,To)
    if move_text.startswith('move(') and move_text.endswith(')'):
        inner = move_text[5:-1]
        parts = [p.strip() for p in inner.split(',')]
        if len(parts) == 2 and parts[0].isdigit() and parts[1].isdigit():
            return (int(parts[0]), int(parts[1]))
    # fallback: None
    return None


def compute_best_move(board_flat, player_id, depth=3, use_pyswip=True, timeout=5.0):
    """Compute best move. Returns either int index (placement) or (from,to) tuple for movement.

    If use_pyswip=True, try to use pyswip embedded SWI-Prolog. Otherwise call swipl subprocess.
    """
    if use_pyswip:
        if not PYSWIP_AVAILABLE:
            # pyswip not installed; fall back to subprocess mode
            use_pyswip = False
        else:
            try:
                prolog = None
                cls = _PYSWIP_PROLOG_CLASS
                if cls is None:
                    raise RuntimeError('pyswip Prolog class not available')
                prolog = cls()
                prolog.consult(str(PROLOG_FILE))
                b = _board_to_prolog_list(board_flat)
                if timeout and timeout > 0:
                    qry = f"best_move_iter({b},{player_id},{depth},{float(timeout)},Move,Score)"
                else:
                    qry = f"best_move_ab({b},{player_id},{depth},Move,Score)"
                for sol in prolog.query(qry, maxresult=1):
                    mv = sol.get('Move')
                    sc = sol.get('Score')
                    s = str(mv)
                    try:
                        score_val = int(sc) if sc is not None else None
                    except Exception:
                        score_val = None
                    return _parse_move_text(s), score_val
                return None, None
            except Exception:
                # any pyswip failure -> fall back to subprocess mode
                use_pyswip = False

    # Use subprocess mode
    if not PROLOG_FILE.exists():
        raise FileNotFoundError(f"Prolog file not found: {PROLOG_FILE}")

    b = _board_to_prolog_list(board_flat)
    # Choose iterative deepening predicate if timeout provided (>0), else call alpha-beta search
    if timeout and timeout > 0:
        # best_move_iter(Board, Player, MaxDepth, TimeLimitSec, Move, Score)
        goal = f"(prolog_ai:best_move_iter({b},{player_id},{depth},{float(timeout)},Move,Score), write_canonical(Move), write(':'), write(Score), nl, halt)"
    else:
        # best_move_ab(Board, Player, MaxDepth, Move, Score)
        goal = f"(prolog_ai:best_move_ab({b},{player_id},{depth},Move,Score), write_canonical(Move), write(':'), write(Score), nl, halt)"

    cmd = [SWIPL_CMD, '-q', '-s', str(PROLOG_FILE), '-g', goal]

    try:
        out = subprocess.check_output(cmd, stderr=subprocess.STDOUT, timeout=timeout)
    except subprocess.CalledProcessError as e:
        # prolog error; return None
        return None, None
    except subprocess.TimeoutExpired:
        return None, None

    text = out.decode('utf-8', errors='ignore').strip()
    if not text:
        return None, None
    # Expect format like: move(3,7):42 or 5:12
    if ':' in text:
        move_part, score_part = text.split(':', 1)
        move = _parse_move_text(move_part)
        try:
            score = int(score_part.strip())
        except Exception:
            score = None
        return move, score
    else:
        # fallback
        move = _parse_move_text(text)
        return move, None


if __name__ == '__main__':
    # simple CLI for testing
    import json
    if len(sys.argv) < 3:
        print('Usage: prolog_ai.py <player> <depth> [board_flat_as_json]')
        sys.exit(2)
    player = int(sys.argv[1])
    depth = int(sys.argv[2])
    if len(sys.argv) >= 4:
        board_flat = json.loads(sys.argv[3])
    else:
        board_flat = [0]*25
    mv, score = compute_best_move(board_flat, player, depth=depth)
    print('MOVE ->', mv, 'SCORE ->', score)
