from reprep import Report
import numpy as np
from cbc.tools.math_utils import scale_score
from cbc.tools.plot_utils import create_histogram_2d

def create_report_test_case(tcid, tc):
    r = Report(tcid)
    r.add_child(tc_problem_plots(tc)) 
    if tc.has_ground_truth:
        r.add_child(tc_ground_truth_plots(tc))
    return r

def tc_problem_plots(tc, rid='problem_data'):
    r = Report(rid)
    R = tc.R
    n = R.shape[0]
    # zero diagonal
    Rz = (1 - np.eye(n)) * R
    
    f = r.figure(cols=3)
    
    r.data("Rz", Rz).display('posneg')
    f.sub('Rz', caption='The given correlation matrix (diagonal set to 0)')
    
    return r
    
def tc_ground_truth_plots(tc, rid='ground_truth'):
    r = Report(rid)
    assert tc.has_ground_truth
    
    cols = 4
    if tc.true_kernel is not None:
        cols += 1
    
    f = r.figure(cols=cols, caption='Ground truth plots.')

    n = r.data('true_C', tc.true_C).display('posneg')  
    f.sub(n, 'Actual cosine matrix')
    
    n = r.data('true_D', tc.true_D).display('scale')  
    f.sub(n, 'Actual distance matrix')
    
    n = plot_one_against_the_other(r, 'true_CvsR', tc.true_C, tc.R)
    f.sub(n, 'Sample histogram')
    
    true_C_order = scale_score(tc.true_C)
    R_order = scale_score(tc.R)
    with r.data_pylab('linearity') as pylab:
        x = true_C_order.flat
        y = R_order.flat
        pylab.plot(x, y, '.', markersize=0.2)
        pylab.xlabel('true_C score')
        pylab.ylabel('R score')
        
    f.sub('linearity', 'Linearity plot (the closer this is to a line, the better '
                        'we can solve)')
    
    if tc.true_kernel is not None:
        x = np.linspace(-1, 1, 512)
        y = tc.true_kernel(x)
        with r.data_pylab('kernel') as pylab:
            pylab.plot(x, y)
            pylab.xlabel('cosine')
            pylab.ylabel('correlation')
            pylab.axis((-1, 1, -1, 1))
        f.sub('kernel', caption='Actual analytical kernel')
    
    return r


def plot_one_against_the_other(r, nid, xval, yval):
    h = create_histogram_2d(xval, yval, resolution=128)
    n = r.data(nid, np.flipud(h.T)).display('scale')
    return n 

    
