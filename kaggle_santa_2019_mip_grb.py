# Santa's Workshop Tour 2019 MIP Formulation
# by Ernee Kozyreff (@ekozyreff)

import numpy as np
import pandas as pd
from gurobipy import *

# Load file with input data

family_data = pd.read_csv("family_data.csv")


# Build array p: p[f] is the number of people on family f

p = family_data.n_people.values


# Build matrix c: c[f,d] is the preference cost of family f on day d

# To make the code cleaner, the day range will be from 0 to 99 instead of from 1 to 100
# This is the reason for the "- 1" inserted below

c = np.zeros(shape = (5000,100))

for family in range(5000):
    
    for day in range(100):
        c[family,day] = 500 + 36*p[family] + 398*p[family]
    
    choice_0 = family_data.choice_0[family] - 1
    c[family,choice_0] = 0
    
    choice_1 = family_data.choice_1[family] - 1
    c[family,choice_1] = 50
    
    choice_2 = family_data.choice_2[family] - 1
    c[family,choice_2] = 50 + 9*p[family]
    
    choice_3 = family_data.choice_3[family] - 1
    c[family,choice_3] = 100 + 9*p[family]
    
    choice_4 = family_data.choice_4[family] - 1
    c[family,choice_4] = 200 + 9*p[family]
    
    choice_5 = family_data.choice_5[family] - 1
    c[family,choice_5] = 200 + 18*p[family]
    
    choice_6 = family_data.choice_6[family] - 1
    c[family,choice_6] = 300 + 18*p[family]
    
    choice_7 = family_data.choice_7[family] - 1
    c[family,choice_7] = 300 + 36*p[family]
    
    choice_8 = family_data.choice_8[family] - 1
    c[family,choice_8] = 400 + 36*p[family]
    
    choice_9 = family_data.choice_9[family] - 1
    c[family,choice_9] = 500 + 36*p[family]


# Build matrix a: a[d,i,j] is the accounting penalty of having i people on day d and j people on day d+1

a = np.zeros(shape = (100,301,301))

for d in range(100):
    for i in range(125,301):
        for j in range(125,301):
            a[d,i,j] = (i - 125) / 400 * i ** (0.5 + abs(i - j) / 50)


# Create a new model

m = Model()


# Insert variables with their corresponding objective function coefficient

# x[f,d] is 1 if family f is assigned to day d, and 0 otherwise

x = {}
for f in range(5000):
    for d in range(100):
        x[f,d] = m.addVar(obj=c[f,d], vtype=GRB.BINARY, name='x'+'_'+str(f)+'_'+str(d))
m.update()


# y[d,i,j] is 1 if there are i people on day d and j people on day d+1, and 0 otherwise

y = {}
for d in range(100):
    for i in range(125,301):
        for j in range(125,301):
            y[d,i,j] = m.addVar(obj=a[d,i,j], vtype=GRB.BINARY, name='y'+'_'+str(d)+'_'+str(i)+'_'+str(j))
m.update()


# n[d] is the total number of people on day d

n = {}
for d in range(100):
    n[d] = m.addVar(obj=0, vtype=GRB.INTEGER, name='n'+'_'+str(d))
m.update()


# Insert constraints

# Constraints (1) -- see PDF file for explanation

for f in range(5000):
    m.addConstr(quicksum(x[f,d] for d in range(100)) == 1)
m.update()


# Constraints (2) -- see PDF file for explanation

for d in range(100):
    m.addConstr(quicksum(p[f] * x[f,d] for f in range(5000)) - n[d] == 0)
m.update()


# Constraints (3) -- see PDF file for explanation

for d in range(100):
    m.addConstr(n[d] - quicksum(i * y[d,i,j] for i in range(125,301) for j in range(125,301)) == 0)
m.update()


# Constraints (4) -- see PDF file for explanation

for d in range(100):
    m.addConstr(quicksum(y[d,i,j] for i in range(125,301) for j in range(125,301)) == 1)
m.update()


# Constraints (5) -- see PDF file for explanation

for d in range(99):
    for j in range(125,301):
        m.addConstr((quicksum(y[d,i,j] for i in range(125,301)))  - (quicksum(y[d+1,j,k] for k in range(125,301))) == 0)
m.update()


# Constraints (6) -- see PDF file for explanation

for d in range(100):
    m.addConstr(quicksum(p[f] * x[f,d] for f in range(5000)) >= 125)
m.update()

for d in range(100):
    m.addConstr(quicksum(p[f] * x[f,d] for f in range(5000)) <= 300)
m.update()


# Set a time limit (optional)
                
# m.setParam('TimeLimit', 3600.0)


# Set MIP gap to zero (this is important, otherwise the optimization will stop earlier than desired)
                
m.setParam('MIPGapAbs', 0)


# Set NumericFocus to 2 to improve numerical accuracy (default value is 0 and it may lead to incorrect solutions)

m.setParam('NumericFocus', 2)


# Write feasible solutions found during optimization to external files (optional)
# This only works in Gurobi version 9 and above

# m.setParam('SolFiles', "sol")


# Start optimization

m.optimize()


# Write submission csv file

solution = np.zeros(shape = (5000,2), dtype=np.int64)

for f in range(5000):
    solution[f,0] = f
    for d in range(100):
        if x[f,d].x > 0:
            solution[f,1] = d + 1

submission = pd.DataFrame(solution, columns=['family_id', 'assigned_day'])

submission.to_csv("submission_%g.csv" % m.objVal, sep=',', index=False)

# End of code
