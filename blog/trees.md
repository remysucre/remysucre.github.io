# Listing Spanning Trees of $K_n$

We want to enumerate all spanning trees of a complete graph by edits with constant delay.

Several related algorithms are known: [Shioura, Tamura & Uno](https://doi.org/10.1137/S0097539794270881)
has an *amortized* constant time algorithm for generating all spanning trees of a graph, 
and so does [Kapoor & Ramesh](https://doi.org/10.1137/S009753979225030X).
But to enumerate in worst-case constant time, one must output the trees in some
[Gray code](https://en.wikipedia.org/wiki/Gray_code) order, meaning the difference
between two consecutive outputs must be constant.
[M.J. Smith](https://hdl.handle.net/1828/19740) has an algorithm outputing the trees
in Gray code order, but that algorithm also only runs in amortized constant time.
Donald Knuth provided [an implementation](https://cs.stanford.edu/~knuth/programs/grayspspan.w) based on Smith's and claimed the algorithm runs in $O(m+n+t)$ time.
Knuth gave his [10th annual Christmas Tree Lecture](https://youtu.be/LDHlaxewCmE?feature=shared) 
on the topic of spanning tree generation.
Also, the exact problem we're trying to solve is listed as a (challenge) excercise in Knuth's The Art of Computer Programming book
(Vol. 4A. Combinatorial algorithms. Part 1, Sec. 7.2.1.6 Ex. 101).
[Torsten Mütze](https://arxiv.org/pdf/2202.01280) stated the problem to be open as of 2024.
[Cameron, Grubb, and Sawada](https://www.socs.uoguelph.ca/~sawada/papers/FanSpanningTrees.pdf)
has an amortized constant time algorithm for listing the spanning trees of a Fan Graph in Pivot Gray Code order.

[Nakano and Uno](https://link.springer.com/chapter/10.1007/978-3-540-30559-0_3)
gave a worst-case constant time algorithm for generating free trees over exactly $n$ vertices.
However, the vertiecs are not labeled.
[Another paper of the pair](https://dl.acm.org/doi/10.1007/11604686_22)
generates labeled trees (called *colored trees* there), but it's for trees over *up to* $n$ vertices.

A straightforward way to generate spanning trees of $K_n$ is to first generate
[Prüfer sequences](https://en.wikipedia.org/wiki/Prüfer_sequence), 
then convert each one to a tree,
since [there is a bijection](https://en.wikipedia.org/wiki/Prüfer_sequence#Cayley's_formula) between trees and sequences.
To generate Prüfer sequences is just to generate arrays over $n$ symbols of length $n-2$, 
which can be done in constant delay using loopless base-n gray code algorithms like the Algorithm L by Donald Knuth.
However, this is not enough, because a local change on the Prüfer sequence [does not necessarily](https://www.ac.tuwien.ac.at/files/pub/gottlieb-01.pdf) correspond to
a local change on the corresponding tree.
So a gray code order for the sequence may not correspond to a gray code order for the trees, 
and the constant delay does not carry over to tree edits.