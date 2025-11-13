% src/prolog_ai.pl
% Prolog AI for Teeko (5x5) with negamax + alpha-beta and optional iterative deepening.
% Exports:
%   best_move_ab(+Board, +Player, +MaxDepth, -Move, -Score)
%   best_move_iter(+Board, +Player, +MaxDepth, +TimeLimitSec, -BestMove, -BestScore)

:- module(prolog_ai, [best_move_ab/5, best_move_iter/6]).

:- use_module(library(lists)).

% Board: flat list of 25 ints (0 empty,1 p1,2 p2)

% Public: best_move_ab(Board, Player, MaxDepth, Move, Score)
best_move_ab(Board, Player, MaxDepth, BestMove, BestScore) :-
    % initial alpha/beta
    INF is 1000000,
    Alpha is -INF, Beta is INF,
    negamax_ab(Board, Player, MaxDepth, Alpha, Beta, BestScore, BestMove).

% Public: best_move_iter(Board, Player, MaxDepth, TimeLimitSec, BestMove, BestScore)
% Iterative deepening from depth 1..MaxDepth with time limit (seconds)
best_move_iter(Board, Player, MaxDepth, TimeLimitSec, BestMove, BestScore) :-
    get_time(T0),
    ( MaxDepth < 1 -> MaxDepth1 = 1 ; MaxDepth1 = MaxDepth ),
    best_move_iter_loop(Board, Player, 1, MaxDepth1, T0, TimeLimitSec, none, -1000000, BestMove, BestScore).

best_move_iter_loop(_Board, _Player, D, MaxD, _T0, _TL, LastMove, LastScore, MoveOut, ScoreOut) :-
    D > MaxD, !,
    ( LastMove = none -> MoveOut = none, ScoreOut = LastScore ; MoveOut = LastMove, ScoreOut = LastScore ).
best_move_iter_loop(Board, Player, D, MaxD, T0, TL, _LastMove, _LastScore, MoveOut, ScoreOut) :-
    get_time(Now),
    Elapsed is Now - T0,
    ( Elapsed > TL -> % time exhausted
        MoveOut = none, ScoreOut = -1000000
    ; % try search at depth D
      catch(
        ( best_move_ab(Board, Player, D, Move, Score) ),
        _,
        ( Move = none, Score = -1000000 )
      ),
      % After search, check time
      get_time(Now2),
      NewElapsed is Now2 - T0,
      ( NewElapsed > TL -> % time over after this depth: return latest found
          MoveOut = Move, ScoreOut = Score
      ; D1 is D + 1,
        best_move_iter_loop(Board, Player, D1, MaxD, T0, TL, Move, Score, MoveOut, ScoreOut)
      )
    ).

% Negamax with alpha-beta pruning
% negamax_ab(+Board, +Player, +Depth, +Alpha, +Beta, -BestScore, -BestMove)
negamax_ab(Board, Player, 0, _Alpha, _Beta, Score, none) :- !,
    evaluate(Board, Player, Score).
negamax_ab(Board, Player, Depth, Alpha, Beta, BestScore, BestMove) :-
        Depth > 0, !,
        ( terminal(Board, Winner), Winner =\= 0 ->
                ( Winner =:= Player -> BestScore = 100000 ; BestScore = -100000 ),
                BestMove = none
        ; valid_moves(Board, Player, Moves),
            Moves \= [],
            initial_ab_loop(Moves, Board, Player, Depth, Alpha, Beta, -1000000, none, BestScore, BestMove)
        ).

% Loop over moves, performing negamax and alpha-beta updates
initial_ab_loop([], _Board, _Player, _Depth, _Alpha, _Beta, BestScore, BestMove, BestScore, BestMove) :- !.
initial_ab_loop([Mv|Rest], Board, Player, Depth, Alpha, Beta, CurBest, CurBestMove, BestScore, BestMove) :-
    make_move(Board, Mv, Player, NB),
    Opp is 3 - Player,
    D1 is Depth - 1,
    negamax_ab(NB, Opp, D1, -Beta, -Alpha, Score1, _),
    Score is -Score1,
    ( Score > CurBest -> NewBest = Score, NewBestMove = Mv ; NewBest = CurBest, NewBestMove = CurBestMove ),
    Alpha1 is max(Alpha, Score),
    ( Alpha1 >= Beta -> BestScore = NewBest, BestMove = NewBestMove  % prune
    ; initial_ab_loop(Rest, Board, Player, Depth, Alpha1, Beta, NewBest, NewBestMove, BestScore, BestMove)
    ).

% Valid moves: similar logic as earlier
valid_moves(Board, Player, Moves) :-
    count_pieces(Board, Player, Count),
    ( Count < 4 -> % placement
        findall(Index, nth0(Index, Board, 0), Moves)
    ; % movement
        findall(move(From,To), ( nth0(From, Board, Player), neighbor_index(From, To), nth0(To, Board, 0) ), Moves0),
        sort(Moves0, Moves)
    ).

% neighbor_index(Index, NeighborIndex) for adjacent squares (including diag)
neighbor_index(Index, Neighbor) :-
    index_rc(Index, R, C),
    between(-1, 1, DR),
    between(-1, 1, DC),
    \+ (DR =:= 0, DC =:= 0),
    TR is R + DR,
    TC is C + DC,
    TR >= 0, TR < 5, TC >= 0, TC < 5,
    Neighbor is TR * 5 + TC.

% Make move: placement integer or move(From,To)
make_move(Board, Move, Player, NewBoard) :-
    ( integer(Move) -> nth0(Move, Board, 0), set_nth0(Board, Move, Player, NewBoard)
    ; Move = move(From,To) -> nth0(From, Board, Player), nth0(To, Board, 0), set_nth0(Board, From, 0, Temp), set_nth0(Temp, To, Player, NewBoard)
    ).

set_nth0(List, Index, Value, NewList) :-
    same_length(List, NewList),
    append(Prefix, [_|Suffix], List), length(Prefix, Index), append(Prefix, [Value|Suffix], NewList).

% Terminal detection
terminal(Board, Winner) :-
    ( has_four_in_a_row(Board, 1) -> Winner = 1
    ; has_four_in_a_row(Board, 2) -> Winner = 2
    ; Winner = 0
    ).

% has_four_in_a_row: horizontal, vertical, diagonal and 2x2 squares
has_four_in_a_row(Board, Player) :-
    between(0,4,R), between(0,1,C), I is R*5 + C, I1 is I+1, I2 is I+2, I3 is I+3, nth0(I, Board, Player), nth0(I1, Board, Player), nth0(I2, Board, Player), nth0(I3, Board, Player), !.
has_four_in_a_row(Board, Player) :-
    between(0,4,C), between(0,1,R), I is R*5 + C, I1 is I+5, I2 is I+10, I3 is I+15, nth0(I, Board, Player), nth0(I1, Board, Player), nth0(I2, Board, Player), nth0(I3, Board, Player), !.
has_four_in_a_row(Board, Player) :-
    between(0,1,R), between(0,1,C), I is R*5 + C, I1 is I+6, I2 is I+12, I3 is I+18, nth0(I, Board, Player), nth0(I1, Board, Player), nth0(I2, Board, Player), nth0(I3, Board, Player), !.
has_four_in_a_row(Board, Player) :-
    between(0,1,R), between(3,4,C), I is R*5 + C, I1 is I+4, I2 is I+8, I3 is I+12, nth0(I, Board, Player), nth0(I1, Board, Player), nth0(I2, Board, Player), nth0(I3, Board, Player), !.
has_four_in_a_row(Board, Player) :-
    between(0,3,R), between(0,3,C), I is R*5 + C, I1 is I+1, I2 is I+5, I3 is I+6, nth0(I, Board, Player), nth0(I1, Board, Player), nth0(I2, Board, Player), nth0(I3, Board, Player), !.

% count pieces
count_pieces(Board, Player, Count) :- include(=(Player), Board, L), length(L, Count).

% evaluation for Player: simple heuristic
evaluate(Board, Player, Score) :-
    include(=(Player), Board, L1), length(L1, N1),
    Opp is 3 - Player, include(=(Opp), Board, L2), length(L2, N2),
    % center control
    nth0(12, Board, CV), (CV =:= Player -> CPlayer = 1 ; CPlayer = 0), (CV =:= Opp -> COpp = 1 ; COpp = 0),
    Score is (N1 - N2) + 2*(CPlayer - COpp).

% index/rc helpers
index_rc(Index, Row, Col) :- Row is Index // 5, Col is Index mod 5.

% end of prolog_ai.pl
