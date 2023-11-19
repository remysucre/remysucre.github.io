# PANDA

In the last post, we talked about how to derive bounds on query output size using information theory. By applying Shannon inequalities, we were able to derive a tighter bound from cardinality constraints and degree constraints. But we only proved the bound by hand, for one single query. In this post, we show a general way to find the bound using linear programming, which we can implement in a query optimizer to automatically compute bounds. 

We will use the same query as before, and with input constraints $|R| = |S| = |T| = N$ and functional dependencies $XY \rightarrow U$ and $YU \rightarrow X$: 

$$
Q(X, Y, Z, U) = R(X, Y) \wedge S(Y, Z) \wedge T(Z, U) \wedge A(X, Z, U) \wedge B(X, Y, U). 
$$

Recall that we consider the uniform distribution over the query output:

$$
h(X, Y, Z, U) = \log |Q(X,Y,Z,U)| 
$$

Then we relate the size of an input relation to its entropy, and degree constraints to the conditional entropy: 

$$
\begin{align*}
\text{cardinality constraints: }&
\begin{cases}
h(X, Y) & \leq \log |R(X, Y)| \\
h(Y, Z) & \leq \log |S(Y, Z)| \\
h(Z, U) & \leq \log |T(Z, U)| 
\end{cases}\\\\
\text{degree constraints: }&
\begin{cases}
h(U \mid XZ) & \leq \log \max \text{deg}_A(U \mid XZ)\\
h(X \mid YU) & \leq \log \max \text{deg}_B(X \mid YU)
\end{cases}
\end{align*}
$$

Our goal is to calculate the largest possible output size, **which is the same as maximizing the output entropy under the above constraints**! Since all the constraints are linear, we can encode them in a linear program. In addition, we also need to encode the Shannon inequalities (submodularity and monotonicity) to relate the entropies over different variables to each other. That is, for all subsets of variables $\mathbf{U}, \mathbf{V}$ we have: 

$$
\begin{align*}
h(\mathbf{U}) & \leq h(\mathbf{U \cup V}) & \text{ monotonicity} \\
h(\mathbf{U\cup V}) + h(\mathbf{U\cap V})  & \leq h(\mathbf{U}) + h(\mathbf{V}) & \text{submudolarity}
\end{align*}
$$

Overall, the linear program is: 

$$
\begin{align*}
\textbf{maximize: } & h(X, Y, Z, U) \\
\textbf{subject to: } & \text{carinality constraints} \\
& \text{degree constraints} \\
& \text{monotonicity} \\
& \text{submodularity}
\end{align*}
$$

The solution of the linear program is then the $\log$ of the maximum output size of the query. 
