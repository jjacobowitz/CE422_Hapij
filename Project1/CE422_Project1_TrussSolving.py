# -*- coding: utf-8 -*-
"""
Jared Jacobowitz
Fall 2021
CE422 Finite Element Methods

Project 1 truss solving
"""
import numpy as np
import pandas as pd

# trig values
theta = np.deg2rad(60)
s = np.sin(theta)
c = np.cos(theta)

# member geometric properties
length = 5              # m; member lengths
area = 0.0254**2        # m^2; member cross-sectional area

# material properties
# source: http://www.matweb.com/search/datasheet.aspx?bassnum=MS0001&ckck=1
Youngs = 200e9          # Pa; Young's modulus of steel
yield_stress = 350e6    # Pa; yield stress of steel

# applied loads
P1 = 10000          # N; force 1 (negative vertical force on node B)
P2 = 25000          # N; force 2 (negative vertical force on node L)

# nodal x and y equations
A = {"x":{"AB":1, "AC":c, "Ax":1},
     "y":{"AC":-s, "Ay":1}}
B = {"x":{"AB":-1, "BC":-c, "BD":c},
     "y":{"BC":-s, "BD":-s}}
C = {"x":{"AC":-c, "BC":c, "CD":1, "CE":c},
     "y":{"AC":s, "BC":s, "CE":-s}}
D = {"x":{"CD":-1, "BD":-c, "DE":-c, "DF":c},
     "y":{"BD":s, "DE":-s, "DF":-s}}
E = {"x":{"CE":-c, "DE":c, "EF":1, "EG":c},
     "y":{"CE":s, "DE":s, "EG":-s}}
F = {"x":{"DF":-c, "EF":-1, "FG":-c, "FH":c, "FI":1},
     "y":{"DF":s, "FG":-s, "FH":-s}}
G = {"x":{"EG":-c, "FG":c, "GH":1},
     "y":{"EG":s, "FG":s}}
H = {"x":{"FH":-c, "GH":-1, "HI":c, "HJ":1},
     "y":{"FH":s, "HI":s, "Hy":1}}
I = {"x":{"FI":-1, "HI":-c, "IJ":c, "IK":1},
     "y":{"HI":-s, "IJ":-s}}
J = {"x":{"HJ":-1, "IJ":-c, "JK":c, "JL":1},
     "y":{"IJ":s, "JK":s}}
K = {"x":{"IK":-1, "JK":-c, "KL":c},
     "y":{"JK":-s, "KL":-s}}
L = {"x":{"JL":-1, "KL":-c},
     "y":{"KL":s}}

# list of nodes for loop
nodes = [A, B, C, D, E, F, G, H, I , J, K, L]

# list of members for loop
members = ["AB", "AC", "BC", "BD", "CD", "CE", "DE", "DF", "EF", "EG", "FG", 
           "FH", "FI", "GH", "HI", "HJ", "IJ", "IK", "JK", "JL", "KL", 
           "Ax", "Ay", "Hy"]

# "A" matrix for Ax=b; this is the matrix of x and y statics eqns for each node
A_matrix = np.zeros((24,24))

# Fill "A" matrix with statics equations
row = 0
for node in nodes:
    for indx, member in enumerate(members):
        A_matrix[row][indx] = node["x"].get(member, 0)
        A_matrix[row+1][indx] = node["y"].get(member, 0)
    row += 2        # every 2 rows is a new node; rows alternate x and y
        
# "b" matrix for Ax=b; this is the matrix of loads
b = np.zeros((24,1))
b[3] = P1
b[23] = P2

# "x" matrix for Ax=b
x = np.linalg.solve(A_matrix, b)

member_loads = x[:-3]
reaction_forces = x[-3:].copy()

# stress is force over area (doesn't apply to reactions)
stresses = member_loads/area

# stress = Youngs*strain -> strain = stress/Youngs
strains = stresses/Youngs

# check if any members fail; show the FOS of the highest stressed member
print(np.max(np.abs(stresses)) > yield_stress)
print("FOS", yield_stress/np.max(np.abs(stresses)))

# print the member results
results = dict()
for member, load, stress, strain in zip(members, x, stresses, strains, ):
    print(member)
    print(f"\t Load: {load[0]:.3e}N")
    print(f"\t Stress: {stress[0]:.3e}Pa")
    print(f"\t Strain: {strain[0]:.3e}")
    results[member] = {"load [N]":load[0],
                       "stress [Pa]":stress[0],
                       "strain":strain[0]}

# print the reactions
reactions = dict()
for reaction, load in zip(members[-3:], reaction_forces):
    print(f"{reaction}: {load[0]:.3f}N")
    reactions[reaction] = load[0]

# save into Pandas DataFrame
df = pd.DataFrame(np.hstack((member_loads, 
                             stresses, 
                             strains)), 
                  index=members[:-3],
                  columns=["Load [N]", "Stress [Pa]", "Strain"])