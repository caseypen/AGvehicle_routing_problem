from gurobipy import Model, GRB, GurobiError, quicksum
import numpy as np
from gantt_plot import *
StatusDict = {getattr(GRB.Status, s): s for s in dir(GRB.Status) if s.isupper()}

class PMSP_Gurobi(object):
  """docstring for PMSP_Gurobi"""
  def __init__(self):
    # setting the solver attributes;
    self.schedules = {}
    self.order = []

  def solve(self, job_ids, request_times, process_intervals, machine_properties):
    solved = False
    pmsp_model, assign, order, startTime = self._create_model(job_ids, request_times, process_intervals, machine_properties)
    self._set_model_parms(pmsp_model)
    # solve the model
    try:
      pmsp_model.optimize()
      if pmsp_model.status == GRB.Status.OPTIMAL:
        solved = True
        self._formulate_schedules(job_ids, request_times, process_intervals,
                                  machine_properties, assign, order, startTime)
      else:
        statstr = StatusDict[pmsp_model.status]
        print('Optimization was stopped with status %s' %statstr)
        self._formulate_schedules(job_ids, request_times, process_intervals,
                                  machine_properties, assign, order, startTime)
    except GurobiError as e:
      print('Error code '+str(e.errno)+': '+str(e))

    return solved

  def _set_model_parms(self, m):
    m.setParam('MIPGap',0.2)
    m.setParam('TimeLimit',10)
    m.setParam('Heuristics',0.5)

  def _formulate_schedules(self, job_ids, request_times, process_intervals,
                           machines, assign, order, startTime):
    # print("variables: ", startTime.keys)
    start_times = np.zeros(len(job_ids))
    j_ids = list(job_ids)
    for i, j_id in enumerate(job_ids):
      self.schedules[j_id] = {}
      self.schedules[j_id]['start'] = startTime[j_id].x
      self.schedules[j_id]['finish'] = startTime[j_id].x + process_intervals[j_id]
      for m in range(len(machines)):
        if assign[j_id, m].x == 1:
          self.schedules[j_id]['machine'] = m
      start_times[i] = startTime[j_id].x
    
    self.order = job_ids[np.argsort(start_times)]

    return 
  def _create_model(self, job_ids, r_times, p_intervals, m_availabe):
    ## prepare the index for decision variables
    # start time of process
    jobs = tuple(job_ids)
    machines = tuple(range(len(machine_properties)))
    # order of executing jobs: tuple list
    jobPairs = [(i,j) for i in jobs for j in jobs if i<j]
    # assignment of jobs on machines
    job_machinePairs = [(i,k) for i in jobs for k in machines]

    ## parameters model (dictionary)
    # 1. release time
    release_time = dict(zip(jobs, tuple(r_times)))
    # 2. process time
    process_time = dict(zip(jobs, tuple(p_intervals)))
    # 3. machiane available time
    machine_time = dict(zip(machines, tuple(m_availabe)))
    # 4. define BigM
    BigM = np.sum(r_times) + np.sum(p_intervals) + np.sum(m_availabe)

    ## create model
    m = Model('PMSP')
    ## create decision variables
    # 1. assignments of jobs on machines
    z = m.addVars(job_machinePairs, vtype=GRB.BINARY, name='assign')    
    # 2. order of executing jobs
    y = m.addVars(jobPairs, vtype=GRB.BINARY, name='order')
    # 3. start time of executing each job
    startTime = m.addVars(jobs, name='startTime')
    ## create objective
    m.setObjective(quicksum(startTime), GRB.MINIMIZE) # TOTRY
    ## create constraints
    # 1. job release constraint
    m.addConstrs((startTime[i] >= release_time[i] for i in jobs),'job release constraint')
    # 2. machine available constraint
    m.addConstrs((startTime[i] >= machine_time[k] - BigM*(1-z[i,k]) for (i,k) in job_machinePairs), 'machine available constraint')
    # 3. disjunctive constraint
    m.addConstrs((startTime[j] >= startTime[i] + process_time[i] - BigM*((1-y[i,j]) + (1-z[j,k]) + (1-z[i,k]))
                  for k in machines for (i,j) in jobPairs), 'temporal disjunctive order1')
    m.addConstrs((startTime[i] >= startTime[j] + process_time[j] - BigM*(y[i,j] + (1-z[j,k])+(1-z[i,k]))
                  for k in machines for (i,j) in jobPairs), 'temporal disjunctive order2')
    # 4. one job is assigned to one and only one machine
    m.addConstrs((quicksum([z[i,k] for k in machines])==1 for i in jobs), 'job non-splitting')

    return m, z, y, startTime    


if __name__ == '__main__':
  job_num = 5
  machine_num = 5
  job_ids = np.arange(0, job_num, 1, dtype=np.int32)
  # machine_ids = np.arange(0, machine_num, 1, dtype=np.int32)
  np.random.seed(15) # 13 is not feasible solution
  request_times = np.random.randint(0, 20, size=(job_num), dtype=np.int32)
  process_intervals = np.random.randint(1, 20, size=(job_num), dtype=np.int32)
  machine_properties = np.zeros(machine_num)
  # machine_properties = np.random.randint(10, 30, size=(machine_num), dtype=np.int32)

  pmsp_solver = PMSP_Gurobi()
  
  # solver of PMSP
  solved = pmsp_solver.solve(job_ids, request_times, process_intervals, machine_properties)
  if solved:
    print("schedules", pmsp_solver.schedules)
    print("order", pmsp_solver.order)

  job_dict = formulate_jobs_dict(job_ids, request_times, process_intervals)
  gantt_chart_plot(job_dict, pmsp_solver.schedules, machine_properties, "gurobi solver")
  plt.show()