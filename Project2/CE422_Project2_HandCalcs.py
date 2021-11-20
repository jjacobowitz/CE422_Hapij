# -*- coding: utf-8 -*-
"""
Jared Jacobowitz
Fall 2021
CE422 Finite Element Method
Project 2

Code to calculate the reaction forces, moment, stress, and displacement
"""

def moment(P, x):
    """Moment in a simply supported beam"""
    return P*x/2

def moment_of_inertia(b, h):
    """Moment of inertia of a rectangle"""
    return b*h**3/12

def displacement(P, L, x, E, I):
    """Displacement of simply supported beam loaded at the center"""
    return -P*x*(3*L**2 - 4*x**2)/(48*E*I)

def stress(M, c, I):
    """Stress in a beam under pure bending"""
    return M*c/I

def main():
    E = 200e9           # Pa; Young's modulus steel
    L = 40              # m; length of the beam
    h = 4               # m; height of the beam
    b = 1               # m; depth of the beam
    P = -10e3           # N; applied force
    
    x = L/2             # m; location of applied force
    
    M_max = moment(P, x)
    I = moment_of_inertia(b, h)
    delta_max = displacement(P, L, x, E, I)
    stress_max = stress(M_max, h/2, I)
    
    print(f"{M_max=} Nm, {I=} m^4, {delta_max=} m, {stress_max=} Pa")

if __name__ == "__main__":
    main()
