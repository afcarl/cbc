from . import np
from ..tools import random_rotation, random_directions, assert_allclose
from .points_alignment import (find_best_orthogonal_transform,
    overlap_error_after_orthogonal_transform)
import unittest


N = 10


class UtilsTests(unittest.TestCase):

    def test_find_best_rotation(self):
        for i in range(N): #@UnusedVariable
            X = random_directions(20)
            R = random_rotation()
            Y = np.dot(R, X)
            Rest = find_best_orthogonal_transform(X, Y)
            assert_allclose(R, Rest)
            Rest2 = find_best_orthogonal_transform(Y, X)
            assert_allclose(R.T, Rest2)

    def test_overlap_error(self):
        for i in range(N): #@UnusedVariable
            X = random_directions(20)
            R = random_rotation()
            Y = np.dot(R, X)
            e1 = overlap_error_after_orthogonal_transform(X, Y)
            atol = 1E-7
            assert_allclose(e1, 0, atol=atol)
            e2 = overlap_error_after_orthogonal_transform(Y, X)
            assert_allclose(e2, 0, atol=atol)

