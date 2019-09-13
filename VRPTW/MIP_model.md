### Mathematical modeling of VRPTW

Many agricultural vehicle logistics and dispatching problems can be modeled into VRPTW. In general, VRPTW is to design a set of minimum cost routes, originating and terminating at a central depot, for a fleet of vehicles which services a set of customers with known demands. The customers are only assigned once to one vehicle such that the vehicle capacities are not exceeded. The service at a customer must be in a time window defined by the earliest time and latest time when the customer permits the start of the service time. One of typical case modeled into VRPTW is the agricultural logistics of a fleet of homogeneous crop-transport vehicles in the harvesting scenario.

##### 1. Parameters:

- $V$: a fleet of heterogeneous vehicles;
- $C$: a set of customers ($N$);
- $G$: a directed graph, with $|C|+2$  vertices;
- $c_{ij}$: cost of two vertices (one route);
- $t_{ij}$: transition time from vertex $i$ to vertex $j$;
- $q$: capacity of each vehicle;
- $d_i$: demand of customer $i$;
- $[a_i, b_i]$: time window of customer $i$;
  - $a_i$: a vehicle cannot start serving customer $i$ until time $a_i$;
  - $b_i$:A vehicle must arrive at the customer $i$ before $b_i$;
  - $[a_0,b_0]$: the start depot time window;
  - $[a_{n+1}, b_{n+1}]$: the end depot time window;

##### 2. Decision variables:

- $x_{ijk}$: the arc $(i,j)$ is traversed by vehicle $k$;
- $s_{ik}$: start serving time of vehicle $k$ on the customer $i$ if and only if $x_{ijk}$ is not zero; otherwise, it means nothing;
  - $a_0$ is assumed to be zero;
  - $s_{0k}$ is also assumed to be zero;

##### 3. Objective:

We want to design a set of minimal cost routes, one for each vehicle, such that each customer is visited exactly once, are every route originates at vertex $0$ and ends at vertex $n+1$.

The objective function is $min\sum\limits_{k\in V}\sum\limits_{i\in N}\sum\limits_{j\in N}c_{ij}x_{ijk}$.

##### 4. Constraints:

- Each customer is visited exactly once:
  - $\sum\limits_{k\in V}\sum\limits_{j\in V} x_{ijk}=1\ \ \forall i \in C$
- No vehicle is loaded with more than its capacity allowed:
  - $\sum\limits_{i\in C}d_i\sum\limits_{j\in N}x_{ijk}\leq q\ \ \ \forall k\in V$
- Each vehicle starts from depot $v_0$ and ends with $v_{n+1}$
  - $\sum\limits_{j\in N} x_{0jk}=1\ \ \  \forall k \in V$
  - $\sum\limits_{i\in N} x_{i(n+1)k}=1\ \ \  \forall k \in V$
- The vehicle must leave a vertex $h$ after entering:
  - $\sum\limits_{i\in N} x_{ihk}-\sum\limits_{j\in N}x_{hjk}=0, \ \ \ \ \forall h\in C, \ \forall k\in V$
- Vehicle $k$ cannot arrive at $j$ before $s_{ik}+t_{ij}$, if it is traveling from $i$ to $j$, $K$ is a big scalar:
  - $s_{ik}+t_{ij}-K(1-x_{ijk})\leq s_{jk}, \ \ \forall i,j \in N, \forall k\in V$
- Time window constraint:
  - $a_i \leq s_{ik} \leq b_i,\ \ \forall i\in N, \forall k\in V$;
- Integer constraint:
  - $x_{ijk}\in{0,1}, \forall i,j \in N, \forall k\in V$