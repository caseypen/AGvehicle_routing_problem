from gurobipy import Model, GRB, GurobiError, quicksum
import numpy as np
import matplotlib.pyplot as plt

StatusDict = {getattr(GRB.Status, s): s for s in dir(GRB.Status) if s.isupper()}
init_solution = [(1, 6), (2, 14), (3, 10), (4, 5), (5, 9), (6, 12), (7, 15), (8, 16), (9, 18), (10, 4), (11, 19),
                   (12, 7), (13, 11), (14, 3), (15, 20), (16, 2), (17, 13), (18, 17), (19, 1), (20, 8)]
class TSP_Gurobi(object):
  """docstring for PMSP_Gurobi"""
  def __init__(self):
    # setting the solver attributes;
    self.route = []
    self.route_order = []
  def solve(self, city_ids, map_points):
    
    # map_points: N by 2
    # city_ids: (N,)
    solved = False
    self.city_num = len(city_ids)
    self.city_ids = city_ids
    # define the model and solution matrix
    tsp_m, X = self._create_model(city_ids, map_points)
    self._set_model_parms(tsp_m)
    # call back function
    def subtour_elim(model, where):
      # if we got a solution, we need to check it
      if where == GRB.callback.MIPSOL:
        selected = []
        # make a list of edges selected in the solution
        for i in model._cities:
          sol = model.cbGetSolution([model._x[i,j] for (i,j) in model._cityArcs])
          selected += [(i,j) for n, (i,j) in enumerate(model._cityArcs) if sol[n] > 0.5]
        # get the shortest subtour
        tour = self.subtour(selected)
        # print("tour ", tour)
        if len(tour) < self.city_num:
          # DFJ constraint
          expr = 0
          for i in range(len(tour)):
            for j in range(len(tour)):
              if tour[i]!=tour[j]:
                expr += model._x[tour[i],tour[j]]
          # print("expr", expr)
          model.cbLazy(expr <= len(tour)-1)
    try:
      tsp_m.optimize(subtour_elim)
      if tsp_m.status == GRB.Status.OPTIMAL:
        solved = True
        # print("solution", tsp_m.getAttr('x', X))
        self._formulate_route(tsp_m, X, city_ids)
      else:
        statstr = StatusDict[tsp_m.status]
        print('Optimization was stopped with status %s' %statstr)
        
    except GurobiError as e:
      print('Error code '+str(e.errno)+': '+str(e))

    return solved
  
  # return the edges of a cycle 
  def subtour(self, arcs):
    
    current_city = self.city_ids[0]
    init_city = current_city
    cycle = []
    cycle_order = [init_city]
    while True:
      for prev, nxt in arcs:
        if current_city == prev: 
          next_city = nxt
          cycle.append((prev, nxt))
          cycle_order.append(nxt)
          break
      if next_city == init_city:
        cycle_order.pop()
        break
      else:
        current_city = next_city

    return cycle_order

  def _set_model_parms(self, m):
    # permittable gap
    # m.setParam('MIPGap',0.2)
    # time limit
    # m.setParam('TimeLimit',10)
    # percentage of time on heuristics
    # m.setParam('Heuristics',0.5)
    m.params.LazyConstraints = 1

  def _formulate_route(self, tsp_m, X, city_ids):
    # print("variables: ", startTime.keys)
    solution = tsp_m.getAttr('x', X)
    selected = []
    for i in city_ids:
      for j in city_ids: 
        if (i!=j) and (solution[i,j] > 0.5):
          selected.append((i,j))
    print("selected", selected)
    self.route = selected
    # print("route: ", selected)
    self.route_order.append(city_ids[0])
    prev = city_ids[0]
    for i in range(len(city_ids)):
      for c_id in city_ids[1:]:
        if (prev, c_id) in selected:
          self.route_order.append(c_id)
          prev = c_id
    print("route_order ids", self.route_order)

    return 

  def calculate_distances(self, city_ids, map_points):
    distances_map = {}
    for i, c_iid in enumerate(city_ids):
      a = map_points[i,:]
      for j, c_jid in enumerate(city_ids):
        if i != j:
          b = map_points[j,:]
          distances_map[(c_iid, c_jid)] = np.linalg.norm(a-b)

    return distances_map

  def _create_model(self, city_ids, map_points):
    depot_id = city_ids[0]
    city_num = len(city_ids)
    ## prepare the index for decision variables
    # index of network flow
    cities = tuple(city_ids)

    # connecting arcs of the cities
    cityArcs = [(i,j) for i in cities for j in cities if i != j]
    
    ## parameters model (dictionary)
    # 1. distance map
    distances_map = self.calculate_distances(city_ids, map_points)

    ## create model
    m = Model('TSP')
    ## create decision variables
    # 1. choice of arcs between cities
    x = m.addVars(cityArcs, vtype=GRB.BINARY, name='route')    
    m._x = x
    m._cities = cities
    m._cityArcs = cityArcs
    ## create objective: minimum route distance
    m.setObjective(quicksum([x[i,j]*distances_map[(i,j)] for (i,j) in cityArcs]), GRB.MINIMIZE) # TOTRY
    ## create constraints
    # 1. Network flow
    m.addConstrs((quicksum([x[i,j] for j in cities if i!=j])==1 for i in cities), 'Network flow1')
    m.addConstrs((quicksum([x[i,j] for i in cities if i!=j])==1 for j in cities), 'Network flow2')
    for (i,j) in cityArcs:
      if (i,j) in init_solution:
        x[i,j].start = 1
    return m, x


if __name__ == '__main__':
  city_num = 20
  np.random.seed(1)
  # map points generated
  map_points = np.random.uniform(10, 100, (city_num, 2))
  city_ids = range(1, city_num+1)
  tsp_solver = TSP_Gurobi()
  solved = tsp_solver.solve(city_ids, map_points)

  if solved:
    fig, ax = plt.subplots()
    ax.scatter(map_points[:,0], map_points[:,1], color='red')
    for i in range(city_num):
      ax.annotate(str(city_ids[i]), (map_points[i,0], map_points[i,1]))

    for (i,j) in tsp_solver.route:
      line_xs = [map_points[i-1,0], map_points[j-1,0]]
      line_ys = [map_points[i-1,1], map_points[j-1,1]]
      ax.plot(line_xs, line_ys, 'b--')
    plt.show()
