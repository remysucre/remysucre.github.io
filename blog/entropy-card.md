---
header-includes: |
  <style>
  table {
    display: table;
    margin: auto;
    width: auto;
  }
  .katex-display { overflow: auto hidden }
  </style>
---

# The Entropic Framework for Cardinality Bounds

One of the most exciting developments in database theory in recent years is the entropic framework for cardinality bounds, which emerges from deep connections between database theory and information theory. In this blog post, I explain the fundamental concepts and key steps for estimating join size via information inequalities. This post is based on a lecture by Dan Suciu during the Simons Institute program [Logic and Algorithms in Database Theory and AI](https://simons.berkeley.edu/programs/logic-algorithms-database-theory-ai). The technique is developed in a line of work including [AGM13](https://arxiv.org/abs/1711.03860), [GLVV12](https://theory.stanford.edu/~valiant/papers/GLV_pods.pdf), [GM14](https://arxiv.org/pdf/1111.1109.pdf), [ANS16](https://arxiv.org/abs/1604.00111), [ANS17](https://arxiv.org/abs/1612.02503). See [Suc23](https://arxiv.org/abs/2304.11996) for a wonderful survey of the literature. 

The intuition behind using information theory to estimate join output size is that the *entropy of a relation*, a notion to be made precise later, carries information about the relation. Inequalities over entropic functions have also been studied for decades, so we can leverage the results to derive bounds for database queries. 

We begin by reviewing several basic definitions in information theory. First, the *entropy* $h(X)$ of a finite random variable $X$ is defined as follows: 

$$
h(X) \stackrel{\text{def}}{=} -\sum_i p_i \log p_i
$$

where $p_i$ is the probability of the outcome $X_i$, and $\log$ has base 2. Intuitively, the entropy measures the *randomness* of $X$: if $X$ is deterministic, then: 

$$
p_i = \begin{cases}
1 & \text{when } i = c \\
0 & \text{when } i \neq c
\end{cases}
$$

for some constant $c$. Therefore $h(X)= - 1 \log 1 = 0$. If $X$ is uniform (as random as it gets), then $h(X) = - m \times \frac{1}{m} \times \log \frac{1}{m} = \log m$, where $m$ is the size of the support for $X$. 

When $\mathbf{X}$ is a set of variables, $h(\mathbf{X})$ denotes the entropy over the joint distribution over the set. We write $h(\mathbf{X}\mathbf{Y})$ for $h(\mathbf{X}\cup \mathbf{Y})$, and $h(XY)$ for $h(\{X, Y\})$. For a set of $n$ random variables $\mathbf{X}$, we define the *entropic vector* as a function from any subset of $\mathbf{X}$ to the entropy of their joint distribution: 

$$
(h(\mathbf{X}_S))_{S \subseteq [n]} \in \mathbb{R}^{2^n}_+
$$

As an example, let's consider the distribution over $X,Y,Z$ as shown in the table below: 

| X   | Y   | Z   | p   |
| --- | --- | --- | --- |
| 0   | 0   | 0   | 1/4 |
| 0   | 1   | 1   | 1/4 |
| 1   | 0   | 1   | 1/4 |
| 1   | 1   | 0   | 1/4 |

The entropic vector $h$ then has values as shown in the Hasse diagram below: 

<div style="text-align: center;">
<img title="" src="hasse.svg" alt="hasse.svg" width="350">
</div>

We next define the *conditional entropy* as an analog to the conditional distribution: 

$$
h(\mathbf{V}\mid \mathbf{U}) \stackrel{\text{def}}{=} h(\mathbf{UV}) - h(\mathbf{U})
$$

Importantly, *the conditional entropy is not an entropic vector*! In other words, there may not always be a distribution whose entropies corresponds to a given conditional entropy. Instead, the conditional entropy can be equivalently defined as the expectation of the entropy of $\mathbf{V}$ given $\mathbf{U}$: 

$$
h(\mathbf{V\mid U}) = \mathop{{}\mathbb{E}}_\mathbf{u}[h(\mathbf{V}\mid \mathbf{U}=\mathbf{u})]
$$

The reader can verify this is indeed equivalent to the definition on our example above. 

One final bit of notation we need is the *conditional mutual information*: 

$$
I_h(\mathbf{V};\mathbf{W}\mid\mathbf{U}) \stackrel{\text{def}}{=} h(\mathbf{UV}) + h(\mathbf{UW}) - h(\mathbf{UVW}) - h(\mathbf{U})
$$

The key property is that $\mathbf{V}$ and $\mathbf{W}$ are independent given $\mathbf{U}$ iff $I_h(\mathbf{V};\mathbf{W}\mid\mathbf{U})=0$. Rearranging in terms of conditional entropies can perhaps make the definition more intuitive: 

$$
\begin{align*}
I_h(\mathbf{V;W \mid U}) 
& = (h(\mathbf{UV}) - h(\mathbf{U})) - (h(\mathbf{UVW}) - h(\mathbf{UW})) \\
& = h(\mathbf{V\mid U}) - h(\mathbf{V\mid UW})
\end{align*}
$$

Here we see that $I_h$ measures how much less random $\mathbf{V}$ becomes once we know $\mathbf{W}$, if we already knew $\mathbf{U}$. Or, how much more information we gain about $\mathbf{V}$ after conditioning on $\mathbf{W}$. Note that the definition is symmetric: $I_h(\mathbf{V;W\mid U}) = I_h(\mathbf{W;V\mid U})$. 

From these definitions, the three fundamental entropic inequalities, called *Shannon inequalities*, fall out very naturally: 

$$
\begin{align*}
0 & \leq h(\mathbf{U}) \leq \log |\text{supp}(\mathbf{U})| \\
0 & \leq h(\mathbf{U \mid V}) \\
0 & \leq I_h(\mathbf{V;W\mid U})
\end{align*}
$$

where $|\text{supp}(\mathbf{U})|$ is the size of the support of $\mathbf{U}$, i.e. number of possible outcomes. The second inequality is called *monotonicity*, because it is equivalent to $h(\mathbf{V}) \leq h(\mathbf{UV})$, which says the distribution over more variables becomes more random. The last inequality is called *submodularity* (a.k.a. "law of diminishing returns"). If we replace $\mathbf{V}$ with $\delta$, we can rewrite the inequality as  $h(\mathbf{U\cup W} \cup \delta) - h(\mathbf{U\cup W}) \leq h(\mathbf{U}\cup\delta) - h(\mathbf{U})$ which is exactly the law of diminishing returns. 

OK, enough about entropies! How can we use them for databases? The key idea is to see a relation as a distribution over its tuples. Our example before (copied here) assigns the same probability to every tuple in the relation, so it defines a uniform distribution over the tuples. 

| X   | Y   | Z   | p   |
| --- | --- | --- | --- |
| 0   | 0   | 0   | 1/4 |
| 0   | 1   | 1   | 1/4 |
| 1   | 0   | 1   | 1/4 |
| 1   | 1   | 0   | 1/4 |

Then, we can use the first Shannon inequality to connect the entropy of a relation to its size, because the relation $R(X, Y, Z)$ is exactly the support $\text{supp}(XYZ)$, so $h(XYZ) \leq \log |R|$. Similarly, we can connect the conditional entropy to *degree constraints*.  For two sets of attributes $\mathbf{U, V}$ and values $\mathbf{u}$, define the *degree* of $\mathbf{V}$ given $\mathbf{U = u}$, written $\text{deg}(\mathbf{V \mid U=u})$, as the number of tuples with distinct $\mathbf{V}$ values given $\mathbf{U=u}$. For example, $\text{deg}(XY\mid Z=0)=2$, $\text{deg}(X\mid YZ=01)=1$, and $\text{deg}(XYZ\mid \emptyset) = |R| = 4$. The max degree of $\mathbf{V}$ given $\mathbf{U}$, written $\max \text{deg}(\mathbf{V \mid U})$, is the maximum of $\text{deg}(\mathbf{V \mid U = u})$ over all $\mathbf{u \in U}$. Then we have: 

$$
\begin{align*}
h(\mathbf{V \mid U}) & = \mathop{{}\mathbb{E}}_\mathbf{u}[h(\mathbf{V}\mid \mathbf{U}=\mathbf{u})] \\
& \leq \max_\mathbf{u} h(\mathbf{V}\mid \mathbf{U}=\mathbf{u}) \\
& \leq \max_\mathbf{u} \log (\text{deg}(\mathbf{V} \mid \mathbf{U=u})) \\
& = \log (\max \text{deg}(\mathbf{V\mid U}))
\end{align*}
$$

With this, we can translate bounds on the size of relations and degree constraints into bounds on entropies. Note that degree constraints generalize functional dependencies (FDs). For example an FD $X \rightarrow Y$ can be expressed as $\text{deg}(Y\mid X) \leq 1$. This means we can take advantage of functional dependencies (e.g. primary keys) when deriving bounds on query output size. Let's try it! 

Consider the following query: 

$$
Q(X, Y, Z, U) = R(X, Y) \wedge S(Y, Z) \wedge T(Z, U) \wedge A(X, Z, U) \wedge B(X, Y, U)
$$

And suppose we know $|R| = |S| = |T| = N$, but we don't how large $A$ and $B$ can be. Then $Q$ can be as large as the cartesian product of $R$ and $T$, so $|Q| \leq N^2$. But suppose we also know the FDs $XZ \rightarrow U$ and $YU \rightarrow X$ hold, we can use the Shannon inequalities to derive a tighter bound. First, consider a uniform distribution over the *output* of $Q$. Then $h(XY) \leq \log |\pi_{XY}Q|\leq \log |R|$ because the projection of the output on $XY$ must be in the input $R(X, Y)$, and similarly for $S(Y, Z)$ and $T(Z, U)$. By the same reasoning, $h(U\mid XZ) \leq \log \max \text{deg}_Q(U \mid XZ) \leq \log \max \text{deg}_A (U \mid XZ)$, because the degree of any (sets of) attribute(s) in the output is bounded by the degree in the input. We can now derive: 

$$
\begin{align*}
& \log |R| + \log |S| + \log |T| + \log \max \text{deg}_A (U \mid XZ) + \log \max \text{deg}_B (X \mid YU) \\
\geq & h(XY) + h(YZ) + h(ZU) + h(U\mid XZ) + h(X \mid YU) \\
\geq & \underline{h(XYZ) + h(Y)} + h(ZU) + h(U\mid XZ) + h(X \mid YU) \\
\geq & h(XYZ) + \underline{h(YZU)} + h(U\mid XZ) + h(X \mid YU) \\
\geq & h(XYZ) + h(YZU) + \underline{h(U\mid XYZ) + h(X \mid YZU)} \\
= & 2h(XYZU) = 2 \log(|Q|)
\end{align*}
$$

All inequalities after the first one follow from submodularity, and the second-to-last equality follows from the definition of conditional entropy. Removing the $\log$ by exponentiation on both sides, we get: 

$$
|Q| \leq \sqrt{|R|\cdot |S| \cdot |T| \cdot \max \text{deg}(U \mid XZ) \cdot \max \text{deg}(X\mid YU)} = N^{\frac{3}{2}} 
$$

And it's tighter than the naïve $N^2$ bound! 

Of course, to use these entropic bounds in a database system, we can't ask a database theorist to find a proof every time we want to run a new query. Instead we need an automated way to compute a bound, given a set of input sizes and degree constraints. In the next post, we will see how to do exactly that by encoding the constraints, together with the Shannon inequalities, into a linear program (LP). In fact, we can even extract a proof from the LP, and use the proof to derive a query evaluation algorithm that meets the maximum output size bound! 
