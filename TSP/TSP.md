### TSP 

TSP problem is often used to model the route planning problem in agricultural vehicle planning problems, like a vehicle equipped with a spray machine needs to go over a series of points in the field. This kind of problem can be modeled into a TSP problem. The TSP can be modeled into a mixed integer programming problem.

### Modeling:

We can use a $G=(V, A)$ graph to model the vertices which are needed to go over by a vehicle. $a_{ij}$ is used to express the arc connecting two vertices and the distance $d_{ij}$ represents the distance. The objective is to find a Hamiltonian Path with shortest total distance (A Hamiltonian path, also called a Hamilton path, is a graph path between two vertices of a graph that visits each vertex exactly once). 

##### 1. Parameters

- $\mathbf{V}$: the set includes $N$ vertices
  - $\mathbf{V}=\{v_1, v_2, \ldots, v_N\}$
- $d_{ij}$: the distance of two vertices, $i\neq j$

##### 2. Decision variables

- $x_{ij}$ :
  - 1, the arc is included in the tour;
  - 0, the arc is not included. 

##### 3. Mathematical model

-  Minimize the sum of tour distances
  
  - $min\sum\limits_{1\leq i\neq j\leq N}x_{ij}d_{ij}$ 
  
- Network flow of each node:
  
  - $\sum\limits_{i, j\neq i}^{N}x_{ij}=1, j\in \{1,2,\ldots, N\}$
  
  - $\sum\limits_{j,j\neq i}^n x_{ij}=1, i\in\{1,2,\ldots, N\}$
  
- No sub-tours (MTZ formulation) -Method I:
  - $u_i-u_j+nx_{ij}\leq n-1,\ \ \  2\leq i,j\leq n, i\neq j$
  - If there is sub-tour (with M nodes) except the one starting from and end with $v_1$, the M non-equalities are added together and we can get $n\leq n-1$, which is a contradiction, so the MTZ formulation guarantee that the sub-tour does not exist.
  - $u_1=1, u_i\in\mathcal{R}, 2\leq u_i\leq n$
    - Shrink the possible searching base;
  
- No sub-tours (DFJ formulation) -Method II:

  - $\sum_\limits{i\in S, j\in S}x_{ij} \leq |S|-1$
  - Implemented with lazy constraints in Gurobi;