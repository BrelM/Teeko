from pyswip import Prolog

prolog = Prolog()
prolog.consult('src/prolog_ai.pl')
board = [0]*25
b = '[' + ','.join(str(x) for x in board) + ']'
print('Query best_move_ab:')
for sol in prolog.query(f"prolog_ai:best_move_ab({b},1,2,Move,Score)", maxresult=5):
    print('SOL:', sol)

print('\nQuery best_move_iter:')
for sol in prolog.query(f"prolog_ai:best_move_iter({b},1,2,1,Move,Score)", maxresult=5):
    print('SOL:', sol)
