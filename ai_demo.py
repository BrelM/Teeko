"""
ai_demo.py
Run multiple AI-vs-AI games using the Prolog AI wrapper and log results to CSV.

Usage:
  python ai_demo.py --games 10 --depth 3 --timeout 2.0 --out results.csv

Notes:
- Requires `src.prolog_ai.compute_best_move` to be available (swipl or pyswip).
- Runs headless (no GUI).
"""
import argparse
import csv
import time
import random
from pathlib import Path

from src.player import Player
from src.control import GameController
from src import prolog_ai


def run_single_game(game_id, depth, timeout, max_moves=200, start_player=1):
    p1 = Player('AI1', 1, is_ai=True, ai_depth=depth, ai_timeout=timeout)
    p2 = Player('AI2', 2, is_ai=True, ai_depth=depth, ai_timeout=timeout)
    controller = GameController(p1, p2)

    # If starting player is 2, switch turn
    if start_player == 2:
        controller.switch_turn()

    moves = 0
    t0 = time.time()
    while not controller.is_game_over() and moves < max_moves:
        current = controller.get_current_player()
        board_flat = controller.board.get_board_flat()
        mv, score = prolog_ai.compute_best_move(board_flat, current.player_id, depth=depth, timeout=timeout)
        if mv is None:
            # No move found / timeout -> consider draw
            break
        if controller.board.get_phase() == 'placement':
            if isinstance(mv, int):
                r, c = controller.board.index_to_rc(mv)
                success, msg = controller.place_piece(r, c)
            else:
                # unexpected move format during placement
                success = False
        else:
            if isinstance(mv, tuple) and len(mv) == 2:
                fr, to = mv
                fr_r, fr_c = controller.board.index_to_rc(fr)
                to_r, to_c = controller.board.index_to_rc(to)
                success, msg = controller.move_piece(fr_r, fr_c, to_r, to_c)
            else:
                # unexpected move format
                success = False
        moves += 1
        if not success:
            # if AI made invalid move, stop and consider loss for current player
            break

    duration = time.time() - t0
    winner = controller.get_winner()
    if winner is None:
        winner_id = 0
    else:
        winner_id = winner.player_id

    return {
        'game_id': game_id,
        'winner': winner_id,
        'moves': moves,
        'duration': round(duration, 3)
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--games', type=int, default=10)
    parser.add_argument('--depth', type=int, default=3)
    parser.add_argument('--timeout', type=float, default=1.5, help='per-move timeout in seconds (iterative deepening)')
    parser.add_argument('--out', type=str, default='ai_demo_results.csv')
    parser.add_argument('--seed', type=int, default=None)
    args = parser.parse_args()

    if args.seed is not None:
        random.seed(args.seed)

    out_path = Path(args.out)
    with out_path.open('w', newline='') as csvfile:
        fieldnames = ['game_id', 'winner', 'moves', 'duration']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()

        for i in range(1, args.games + 1):
            # Alternate starting player for variety
            start_player = 1 if (i % 2 == 1) else 2
            print(f'Running game {i}/{args.games} (start_player={start_player})...')
            result = run_single_game(i, args.depth, args.timeout, start_player=start_player)
            writer.writerow(result)
            print('  ->', result)

    print(f'Done. Results written to {out_path.resolve()}')


if __name__ == '__main__':
    main()
