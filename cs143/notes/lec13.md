# Join Algorithms

## Hash Join Wrap-up

To compute $R \bowtie_{x} S$, 
first choose one of $R$ or $S$ to build hash on. Suppose we build on $S$:

First loop over $S$ to build hash table:

```python
h = HashTable::new()

for s in S:
  if h.has_key(s.x):
    h[x].push(s)
  else:
    h[x] = Vec::new()
    h[x].push(s)
```

Then, loop over $R$ while probing into $S$ to find matches:
```python
for r in R:
  if h.has_key(r.x):
    for s in h[x]:
      print(r.concat(s))
```

Try generalize the code above to the case where we join on multiple attributes.

## Merge Sort Join

Let us first review the merge sort algorithm.
It is a divide-and-conquer algorithm that sorts an array by recursively splitting it into halves, 
sorting each half, and then merging the sorted halves back together.

```python
def merge_sort(A):
  if len(A) <= 1:
    return A
  mid = len(A) // 2
  left = merge_sort(A[:mid])
  right = merge_sort(A[mid:])
  return merge(left, right)
```

The merge function takes two sorted arrays and merges them into a single sorted array.

```python
def merge(A, B):
  output = []
  i = 0
  j = 0

  while i < len(A) and j < len(B):
    if A[i] < B[j]:
      output.append(A[i])
      i += 1
    else:
      output.append(B[j])
      j += 1

  while i < len(A):
    output.append(A[i])
    i += 1
  while j < len(B):
    output.append(B[j])
    j += 1
  return output
```

First consider a simple case where we join two relations $R$ and $S$, each with a single attribute $x$.
In this case, we can sort both relations on $x$ and then merge them to find matches.

```python
def merge_join(R, S):
  R_sorted = merge_sort(R)
  S_sorted = merge_sort(S)

  return merge(R_sorted, S_sorted)
```

The general case is similar, we just need to retrieve the join attributes and carefully handle cartesian products.

```python
def merge_join(R, S, join_attrs):
  R_sorted = merge_sort(R, join_attrs)
  S_sorted = merge_sort(S, join_attrs)

  output = []
  i = 0
  j = 0

  while i < len(R_sorted) and j < len(S_sorted):
    if R_sorted[i][join_attrs] < S_sorted[j][join_attrs]:
      i += 1
    elif R_sorted[i][join_attrs] > S_sorted[j][join_attrs]:
      j += 1
    else:
      # Found a match, take the cartesian product
      i_start = i
      j_start = j
      i_end = ...
      j_end = ...
      for k in range(i_start, i_end):
        for l in range(j_start, j_end):
          output.append(R_sorted[k].concat(S_sorted[l]))
  return output
```

## Joining Many Relations
To join many relations, we can join a pair of relations at a time:
$((((R_1 \bowtie R_2) \bowtie R_3) \bowtie R_4) \bowtie \cdots)$.
The order of the joins matters, because the total run time is proportional 
to the total size of the intermediate results.
Example: suppose $R_1 \bowtie R_2$ is empty, but $|R_2 \bowtie R_3| = O(N^2)$.
Then joining $R_1$ and $R_2$ first will result in a total run time of $O(N)$ (why is it not instant?),
while joining $R_2$ and $R_3$ first will result in a total run time of $O(N^2)$.

But there are also examples where *any* join order will be suboptimal. Example in class.

Luckily, there is a (very old) algorithm, called Yannakakis algorithm, 
that always run in time $O(|IN| + |OUT|)$, for a class of queries called *acyclic queries*.

The predicate graph of a query has a vertex for each relation,
and an edge for each join predicate.
A query is acyclic if it can be rewritten into another query with an acyclic predicate graph.
But how do we know (efficiently) if it is possible to rewrite a query into an acyclic one?
We'll come back to this later.

Assume a query is acyclic, and we have rewritten it into one with an acyclic predicate graph.
Then the Yannakakis algorithm works as follows:

1. Traverse the tree bottom-up. For each internal node $R$, replace $R$ with $R \ltimes S_i$, for each child $S_i$ of $R$.
2. Traverse the tree top-down. For each internal node $R$, replace $R$ with $R \ltimes T$, where $T$ is the parent of $R$.
3. Compute the final result using binary hash join bottom-up.

In the above $R \ltimes S_i$ is the *semijoin* operation, which returns the tuples of $R$ that have a match in $S_i$.
In other words it removes any tuple in $R$ that does not have a match in $S_i$.

The key property is that, after the two semijoin passes, every tuple that remains in any relation
must contribute to an output.

This algorithm runs in time $O(|IN| + |OUT|)$, because each semijoin operation takes $O(|IN|)$ time,
and the final hash join takes $O(|OUT|)$ time.

Let us now consider the problem of checking if a query is acyclic. A simple way to do this is to
try dropping any subset of predicates, and see if the resulting query is still equivalent to the original query
and has an acyclic predicate graph. However this will take exponential time.
There is a more efficient algorithm that directly constructs the acyclic predicate graph from a *hypergraph* representation of the query.

A hypergraph generalizes a graph by allowing edges to connect more than two vertices.
Given a natural join query, the hypergraph of the query has a vertex for each attribute (a.k.a. variable),
and a hyperedge for each relation. The hyperedge for a relation $R(x_1, x_2, \ldots, x_n)$ covers the vertices $x_1, x_2, \ldots, x_n$.
You should draw pictures of the hypergraphs of some example queries.

An attribute is a *join attribute* if it appears in more than one relation.
A hyperedge $p$ is a *parent* of another hyperedge $e$, if $p$ covers all the join attributes in $e$.
A hyperedge $e$ is an *ear* if it has a parent.

We can now follow a simple algorithm to construct the acyclic predicate graph from the hypergraph representation of the query.

0. Initialize the predicate graph to contain one vertex per relation, but no edges.
1. Find an ear $e$ in the hypergraph, and find a parent $p$ of $e$.
2. In the predicate graph, connect the vertices corresponding to $p$ and $e$.
3. Remove $e$ from the hypergraph (and any vertex appearing only in $e$), and repeat from step 1.

If the query is acyclic, the above algorithm will terminate after removing all hyperedges from the hypergraph
and construct an acyclic predicate graph.
Otherwise, the algorithm will "get stuck" when it cannot find an ear, implying that the query is cyclic.