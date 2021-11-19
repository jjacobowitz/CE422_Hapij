# -*- coding: utf-8 -*-
"""
Jared Jacobowitz
Fall 2021
CE422 Finite Element Method
Gauss Quadrature weights and nodes

Calculating the weights and points for 2-point Legendre-Gauss Quadrature
"""
from scipy.optimize import fsolve

def equation(p):
    w1, w2, x1, x2 = p
    eq1 = w1 + w2 - 2
    eq2 = w1*x1 + w2*x2 
    eq3 = w1*x1**2 + w2*x2**2 - (2/3)
    eq4 = w1*x1**3 + w2*x2**3
    return eq1, eq2, eq3, eq4

w1, w2, x1, x2 = fsolve(equation, (1, 1, 1, 1))
print(f"{w1=}, {w2=}, {x1=}, {x2=}")