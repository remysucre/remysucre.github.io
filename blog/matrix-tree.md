Matrix tree theorem: $\tau(G) = \det(L_G[i])$

Fact:
$$
\det(A + E_{ii}) = \det(A) + \det(A[i])
$$
which follows from the definition of determinant:
$$
\det(A = (a_{jj})) = \sum_\pi \text{sgn}(\pi) a_{1\pi(1)} a_{2\pi(2)} \cdots a_{n\pi(n)}
$$

**Base case**: $G$ has 2 vertices but no edge:
$$
L_G = \begin{bmatrix}
    0 & 0\\
    0 & 0
\end{bmatrix}
$$
so $L_G[i] = [0]$ and $\det(L_G[i]) = 0$.

**Inductive case**: assume $G$ is connected:
$$
\begin{align*}
\tau(G) & = \tau(G - e) + \tau(G / e)\\
& = \det(L_{G-e}[i]) + \det(L_{G / e}[j])\\
& = \det(L_{G-e}[i]) + \det(L_G[i,j])\\
& = \det(L_{G-e}[i]) + \det(L_{G-e}[i,j])\\
& = \det(L_{G-e}[i]) + \det(L_{G-e}[i][j])\\
& = \det(L_{G-e}[i] + E_{jj})\\
& = \det(L_G[i])
\end{align*}
$$