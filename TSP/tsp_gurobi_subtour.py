import math
import random
from gurobipy import *


# Callback - use lazy constraints to eliminate sub-tours

def subtourelim(model, where):
  # if we got a solution, we check the solution in the call back function
  if where == GRB.callback.MIPSOL:
    selected = []
    # make a list of edges selected in the solution
    for i in range(n):
      sol = model.cbGetSolution([model._vars[i,j] for j in range(n)])
      selected += [(i,j) for j in range(n) if sol[j] > 0.5]
    # find the shortest cycle in the selected edge list
    tour = subtour(selected)
    if len(tour) < n:
      # add a subtour elimination constraint
      expr = 0
      for i in range(len(tour)):
        for j in range(i+1, len(tour)):
          expr += model._vars[tour[i], tour[j]]
      model.cbLazy(expr <= len(tour)-1)


# Euclidean distance between two points

def distance(points, i, j):
  dx = points[i][0] - points[j][0]
  dy = points[i][1] - points[j][1]
  return math.sqrt(dx*dx + dy*dy)


# Given a list of edges, finds the shortest subtour

def subtour(edges):
  visited = [False]*n
  cycles = []
  lengths = []
  selected = [[] for i in range(n)]
  for x,y in edges:
    selected[x].append(y)
  # print("selected", selected)
  while True:
    current = visited.index(False)
    thiscycle = [current]
    # find the cycle
    while True:
      # initialize the first one and set it as visted
      visited[current] = True
      # keep checking its neighbours
      neighbors = [x for x in selected[current] if not visited[x]]
      if len(neighbors) == 0:
        break
      current = neighbors[0]
      thiscycle.append(current)
    cycles.append(thiscycle)
    lengths.append(len(thiscycle))
    if sum(lengths) == n:
      break
  return cycles[lengths.index(min(lengths))]

n = 50

# Create n random points

random.seed(1)
points = []
for i in range(n):
  points.append((random.randint(0,100),random.randint(0,100)))

m = Model()


# Create variables

vars = {}
for i in range(n):
   for j in range(i+1):
     vars[i,j] = m.addVar(obj=distance(points, i, j), vtype=GRB.BINARY,
                          name='e'+str(i)+'_'+str(j))
     vars[j,i] = vars[i,j]
   m.update()


# Add degree-2 constraint, and forbid loops

for i in range(n):
  m.addConstr(quicksum(vars[i,j] for j in range(n)) == 2)
  vars[i,i].ub = 0

m.update()


# Optimize model

m._vars = vars
m.params.LazyConstraints = 1
m.optimize(subtourelim)

solution = m.getAttr('x', vars)
selected = [(i,j) for i in range(n) for j in range(n) if solution[i,j] > 0.5]
assert len(subtour(selected)) == n