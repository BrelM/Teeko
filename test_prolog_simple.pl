% Simple test to debug the AI

:- use_module(src.prolog_ai).

test_empty :-
    Board = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    write('Testing empty board for player 1 at depth 2'), nl,
    best_move_ab(Board, 1, 2, Move, Score),
    write('Move: '), write(Move), write(', Score: '), write(Score), nl.

test_valid_moves :-
    Board = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    write('Testing valid_moves on empty board for player 1'), nl,
    valid_moves(Board, 1, Moves),
    write('Moves: '), write(Moves), nl,
    length(Moves, Len),
    write('Number of moves: '), write(Len), nl.

:- test_valid_moves, nl, test_empty, halt.
