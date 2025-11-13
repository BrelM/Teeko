import shutil, sys
print('swipl->', shutil.which('swipl'))
try:
    import src.prolog_ai as pa
    print('Imported src.prolog_ai, PYSWIP_AVAILABLE =', getattr(pa, 'PYSWIP_AVAILABLE', None))
    board = [0]*25
    mv, sc = pa.compute_best_move(board, 1, depth=2, timeout=1.0)
    print('compute_best_move ->', mv, sc)
except Exception as e:
    import traceback
    traceback.print_exc()
    sys.exit(1)
