% prolog_ai.pl
% Minimal Prolog MinMax example for Teeko (5x5)
% This is a starter implementation. It's intentionally simple and intended
% as a base you can extend with alpha-beta pruning, transposition tables,
% iterative deepening, and a stronger evaluation.

:- module(prolog_ai, [best_move/5]).

% Board is a flat list of 25 integers (0=empty,1=player1,2=player2)
% best_move(+Board, +Player, +MaxDepth, -Move, -Score)

:- use_module(library(lists)).

best_move(Board, Player, MaxDepth, BestMove, BestScore) :-
    valid_moves(Board, Player, Moves),
    Moves \= [],
    findall(Score-Mv,
            ( member(Mv, Moves),
              make_move(Board, Mv, Player, NewBoard),
              Opp is 3 - Player,
              D1 is MaxDepth - 1,
              minimax(NewBoard, Opp, D1, Score0),
              Score is -Score0
            ),
            Pairs),
    sort(0, @>=, Pairs, Sorted),
    Sorted = [BestScore-BestMove | _].

% If no moves, fail (caller should handle)

% minimax(+Board, +Player, +Depth, -Score)
minimax(Board, _Player, 0, Score) :- !,
    evaluate(Board, Score).
minimax(Board, Player, _Depth, Score) :-
    terminal(Board, Winner), !,
    ( Winner =:= 0 -> evaluate(Board, Score)
    ; ( Winner =:= Player -> Score = 10000 ; Score = -10000 )
    ).
minimax(Board, Player, Depth, Score) :-
    Depth > 0,
    valid_moves(Board, Player, Moves),
    Moves \= [],
    findall(S,
            ( member(M, Moves), make_move(Board, M, Player, NB), Opp is 3-Player, D1 is Depth-1, minimax(NB, Opp, D1, S0), S is -S0 ),
            Scores),
    max_list(Scores, Score).

% Valid moves: either placement (empty cells) if player has <4 pieces, else movement moves
valid_moves(Board, Player, Moves) :-
    count_pieces(Board, Player, Count),
    ( Count < 4 ->
        findall(Index, nth0(Index, Board, 0), Moves)
    ;
        % movement: for each piece index of Player, find adjacent empty indices
        findall(move(From,To),
                ( nth0(From, Board, Player), adjacent_empty(Board, From, To) ),
                Moves0),
        sort(Moves0, Moves)  % remove duplicates
    ).

adjacent_empty(Board, From, To) :-
    index_rc(From, FR, FC),
    between( Max(0, FR-1), MinR, R ),
    between( Max(0, FC-1), MinC, C ),
    % We will compute bounds differently below -- simpler approach used
    true.

% Helper: compute row/col from index
index_rc(Index, Row, Col) :-
    Row is Index // 5,
    Col is Index mod 5.

% Check adjacency and empty
adjacent_empty(Board, From, To) :-
    index_rc(From, FR, FC),
    % generate neighbor coordinates
    DR in -1..1, DC in -1..1,
    (DR \= 0 ; DC \= 0),
    TR is FR + DR, TC is FC + DC,
    TR >= 0, TR < 5, TC >= 0, TC < 5,
    To is TR * 5 + TC,
    nth0(To, Board, 0).

% count_pieces(Board, Player, Count)
count_pieces(Board, Player, Count) :-
    include(=(Player), Board, L),
    length(L, Count).

% make_move(Board, Move, Player, NewBoard)
% Move can be Index (placement) or move(From,To)
make_move(Board, Move, Player, NewBoard) :-
    ( integer(Move) ->
        % placement
        nth0(Move, Board, 0),
        set_nth0(Board, Move, Player, NewBoard)
    ; Move = move(From,To) ->
        nth0(From, Board, Player), nth0(To, Board, 0),
        set_nth0(Board, From, 0, Temp),
        set_nth0(Temp, To, Player, NewBoard)
    ).

% set_nth0(List, Index, Value, NewList)
set_nth0(List, Index, Value, NewList) :-
    same_length(List, NewList),
    append(Prefix, [_|Suffix], List),
    length(Prefix, Index),
    append(Prefix, [Value|Suffix], NewList).

% terminal(Board, Winner)
% Winner: 0=no winner, 1 or 2 = player
terminal(Board, Winner) :-
    ( has_four_in_a_row(Board, 1) -> Winner = 1
    ; has_four_in_a_row(Board, 2) -> Winner = 2
    ; Winner = 0
    ).

% has_four_in_a_row(Board, Player) checks rows, cols, diagonals and 2x2 squares
has_four_in_a_row(Board, Player) :-
    % horizontal
    between(0,4,R), between(0,1,C),
    I is R*5 + C, I1 is I+1, I2 is I+2, I3 is I+3,
    nth0(I, Board, Player), nth0(I1, Board, Player), nth0(I2, Board, Player), nth0(I3, Board, Player), !.
has_four_in_a_row(Board, Player) :-
    % vertical
    between(0,4,C), between(0,1,R),
    I is R*5 + C, I1 is I+5, I2 is I+10, I3 is I+15,
    nth0(I, Board, Player), nth0(I1, Board, Player), nth0(I2, Board, Player), nth0(I3, Board, Player), !.
has_four_in_a_row(Board, Player) :-
    % diag TL-BR
    between(0,1,R), between(0,1,C),
    I is R*5 + C, I1 is I+6, I2 is I+12, I3 is I+18,
    nth0(I, Board, Player), nth0(I1, Board, Player), nth0(I2, Board, Player), nth0(I3, Board, Player), !.
has_four_in_a_row(Board, Player) :-
    % diag TR-BL
    between(0,1,R), between(3,4,C),
    I is R*5 + C, I1 is I+4, I2 is I+8, I3 is I+12,
    nth0(I, Board, Player), nth0(I1, Board, Player), nth0(I2, Board, Player), nth0(I3, Board, Player), !.
has_four_in_a_row(Board, Player) :-
    % 2x2 squares
    between(0,3,R), between(0,3,C),
    I is R*5 + C, I1 is I+1, I2 is I+5, I3 is I+6,
    nth0(I, Board, Player), nth0(I1, Board, Player), nth0(I2, Board, Player), nth0(I3, Board, Player), !.

% evaluate(Board, Score)
% Very simple heuristic: center control + (my pieces - opp pieces)
evaluate(Board, Score) :-
    % center is index 12
    nth0(12, Board, CenterVal),
    ( CenterVal =:= 1 -> C1 = 1 ; C1 = 0 ),
    ( CenterVal =:= 2 -> C2 = 1 ; C2 = 0 ),
    include(=(1), Board, L1), length(L1, N1),
    include(=(2), Board, L2), length(L2, N2),
    Score is (N1 - N2) + (C1 - C2) * 2.

% helpers
Max(X,Y,X) :- X >= Y.
Max(X,Y,Y) :- X < Y.
Min(X,Y,X) :- X =< Y.
Min(X,Y,Y) :- X > Y.

% allow use of constraints lib predicates used in adjacent_empty
:- use_module(library(clpfd)).

% end of file
