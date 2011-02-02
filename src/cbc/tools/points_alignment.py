import numpy as np
from contracts import contract, check 
import geometry # for the orthogonal contract @UnusedImport

# TODO: use the native ones
@contract(X='array[KxN],K>=2,K<N', Y='array[KxN]', returns='array[KxK],orthogonal')
def find_best_orthogonal_transform(X, Y):
    ''' Finds the best orthogonal transform R (R in O(K)) between X and Y,
        such that R X ~= Y. '''
    YX = np.dot(Y, X.T)
    check('array[KxK]', YX)
    
    U, S, V = np.linalg.svd(YX) #@UnusedVariable
    
    best = np.dot(U, V)
    return best
    
@contract(X='array[KxN],(K=2|K=3)', Y='array[KxN]', returns='float,>=0')
def overlap_error_after_orthogonal_transform(X, Y):
    ''' Computes the norm of the residual after X and Y (vectors of direction)
        are optimally rotated/mirrored to best overlap with each other. 
        The result is returned in average degrees.
    '''
    O = find_best_orthogonal_transform(X, Y)
    X2 = np.dot(O, X)
    return average_geodesic_error(X2, Y)

# TODO: add unit test for these
@contract(X='directions,array[KxN]', Y='directions,array[KxN]',)
def average_geodesic_error(X, Y):
    return np.arccos(np.clip((X * Y).sum(axis=0), -1, +1)).mean() 


    
