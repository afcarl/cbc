from . import CalibTestCase, contract, pickle, nottest
from ..utils import Ticker
import os


@nottest
@contract(returns='dict(str: tuple(Callable, dict))')
def get_mino_testcases(directory):
    print('Loading Mino data from disk...')
    sets = ['mino1_grid24',
            'mino1_center',
            'mino1_middle',
            'mino1_midcen',
            'mino1_patch32',
            'mino1_patch32s4',
            'mino1_grid24art',
            'mino1_centerart',
            'mino1_middleart',
            'mino1_midcenart',
            'mino1_patch32art',
            'mino1_patch32s4art']

    sets += ['mino4_grid24',
            'mino4_center',
            'mino4_middle',
            'mino4_midcen',
            'mino4_patch32',
            'mino4_patch32s4',
            'mino4_grid24art',
            'mino4_centerart',
            'mino4_middleart',
            'mino4_midcenart',
            'mino4_patch32art',
            'mino4_patch32s4art']

    tcs = {}
    ticker = Ticker('Generating real cases')

    def add_test_case(tcid, function, args):
        ticker(tcid)
        tcs[tcid] = (function, args)

    for s in sets:
        filename = os.path.join(directory, '%s_stats.pickle' % s)
        with open(filename) as f:
            data = pickle.load(f)

        R = data['y_corr']
        S = data['true_S']
        tcid = '%s-y_corr' % s
        add_test_case(tcid, test_case, dict(tcid=tcid, R=R, S=S, kernel=None))

    return tcs


def test_case(tcid, R, S, kernel):
    tc = CalibTestCase(tcid, R)
    if S is not None:
        tc.set_ground_truth(S, kernel=kernel)
    return tc


