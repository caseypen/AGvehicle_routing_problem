### Time integer Modeling 

When the loading capacity of FRAILBot is constrained as one tray, the scheduling problem of FRAILBots can be modeled as Parallel Machines Scheduling Problems with release time constraints in the objective of minimizing total completion time of all the jobs.

#### Sets:

$J$: set of jobs, indexed $j=1,2,...,n$

$\mu$: set of machines, indexed $i=1,...,m$

$\tau$: set of time periods, indexed $t=1,...,l$ 

- We divide the time periods into $l$ time intervals and each of them is 1 second. 

#### Parameters:

$r_j$: release instant of jobs;

$p_j$: processing interval of job $j$;

$a_i$: available interval of machine $i$;

$l$: upper bound for makespan (total time required to process all jobs);

- The upper bound can be estimated from heuristic method (SRPT);

#### Decision Variables:

$C_j$: Completion time of job $j$, which is non-negative and used in minimizing total completion time: $\sum_{j\in J}C_j$;

$\chi^t_{ij}$: if job $j$ starts processing on machine $i\in \mu$ at time $t\in\tau$, then $\chi^t_{ki}$ is equal to 1;

#### Modeling:

$min\ \sum\limits_{j=0}^{n} C_j$

$s.t:$

- **Constraint 1 (job non-splitting)**: each job starts processing on only one machine at only one time point;
  - $\sum\limits_{i\in\mu}\sum\limits_{t=0}^{l-1}\chi^t_{ij}=1\ \ \ j\in J\ \ \ \ (1)$ 

- **Constraint 2 (machine non-splitting)**: each machine can only process one job at most; 
  - $\sum\limits_{i\in J}\sum\limits_{h=max(0,t-p_j)}^{t-1}\chi^h_{ij}=1\ \ \ j\in J, t=1,2,..., l\ \ \ \ (2)$

- **Constraint 3 (Completion time expression)**: 

  - $\sum\limits_{i\in\mu}\sum\limits_{t=0}^{l-1}(t+p_j)\chi^t_{ij}=C_j,\ \ j\in J\ \ \ \ (3)$

- **Job release constraints**: job cannot start processing before the release time:

  - $\sum\limits_{i\in\mu}\sum\limits_{t=0}^{r_j-1}\chi^t_{ij}=0,\ \ \ j\in J\ \ \ (4)$

- **Machine available time constraints**: machine cannot start working before the available time:
  - $\sum\limits_{j\in J}\sum\limits_{t=0}^{a_i-1}\chi^t_{ij}=0,\ \ \ i\in \mu\ \ \ (5)$

  



