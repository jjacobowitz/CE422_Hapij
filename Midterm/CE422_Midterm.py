# -*- coding: utf-8 -*-
"""
Jared Jacobowitz
Fall 2021
CE422 Finite Element Methods

Midterm Calculations
"""
import numpy as np

# =============================================================================
# Problem 5
# =============================================================================
L12 = 91
L23 = 75
L13 = 48
theta = np.deg2rad(20)
P = 41.2
E = 1
A = 1

c = -L23/L12
s = L13/L12

F = np.array([[P*np.cos(theta)],
              [P*np.sin(theta)]])
K = A*E*np.array([[1/L23 + c**2/L12, c*s/L12],
                  [c*s/L12, s**2/L12]])
d = np.linalg.solve(K, F)

print(f"u1 = {d[0,0]:.2f}")
print(f"v1 = {d[1,0]:.2f}")

R3x = -d[0,0]/L23
print(f"R3x = {R3x:.2f}")
