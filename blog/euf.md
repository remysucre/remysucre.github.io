# Understanding EUF by autopsy of 3 failed encodings of tensor algebra

Given a pair of queries (a.k.a programs) $Q_1$ and $Q_2$, 
 the _query equivalence problem_ asks if $Q_1$ and $Q_2$ returns the same
 result on all inputs.
This is very useful in many contexts: an instructor can check 
 a student's coding homework against the solutions; 
 an engineer can check a program against the spec; 
 or the optimizer can check some optimized code against the original.

For databases, query equivalence is known to be decidable
 for several classes of query languages, 
 including Unions of Conjunctive Queries (UCQs) under both set and bag semantics.
Notably, it is also decidable for UCQs over the semiring of Reals --
 otherwise known as _tensor algebra_ or _einsum_ expressions, 
 making the problem very relevant today.
For example, a set of equational axioms for tensor algebra can be used 
 as rewrite rules in an optimizing compiler for tensor computation, 
 and that's exactly what we did in SPORES.

Although there are several algorithms for deciding query equivalence, 
 I have been hunting for a long time for a solution purely based on SMT-solvers.
Such a solution is desirable, because when the solver determines two
 queries to be _not_ equivalent, it will also return a _witness_ input
 on which the pair of queries produce different results. 
Such a witness can help the user understand why the queries are different.
For example, it can be provided as feedback to a student, or added as a test case
 in a production codebase. 

An obvious way to encode the query equivalence problem in SMT is to 
 encode each equational axiom as an $\forall$-quantified formula.
For example, the commutativity of multiplication can be expressed 
 as $\forall x, y : x \times y = y \times x$.
I initially dismissed this approach, because quantified reasoning 
 in SMT is usually undecidable -- until I learned about the EUF fragment
 and its decision procedure implemented in z3.
In short, EUF (for Essentially Uninterpreted Functions) is a decidable 
 fragment of first-order logic that also permits quantification.
It is more general than the classic EPR fragment, 
 and also subsumes the Array Property Fragment.

Long story short, I spent a week trying to hack up a query equivalence checker
 in z3 while staying in the decidable EUF fragment, and failed.
Trying to make the best of the situation, I'm writing this so that 1. others 
 who want to try the same can save some time; 2. smarter people will read this
 and come up with a solution; and 3. to solidify my own understanding of the EUF fragment.

Let's get into it then.
To understand UCQs (or tensor algebra), 
 we can just think of it as the "$\sum$-notation" 
 we use in math when talking about matrices and tensors.
For example, matrix multiplication $C=AB$ is written as 
 $C_{ik} = \sum_{j} A_{ij} \times B_{jk}$.
With this notation, we can think of each matrix as a function 
 of type $\mathbb{N} \times \mathbb{N} \rightarrow \mathbb{R}$, 
 mapping each index to the value at that entry.
In SMT, it is therefore natural to use uninterpreted functions
 to represent matrices (where we use `Int` instead of `Nat` for simplicity):

```smt
(declare-fun A (Int Int) Real)
(declare-fun B (Int Int) Real)
```

With this, we can already get commutativity of multiply _for free_ from the 
 theory of real arithmetics!

```smt
(declare-const i Int)
(declare-const j Int)
(declare-const k Int)

(push)
(assert (not (= (* (A i j) (B j k)) (* (B j k) (A i j)))))
(check-sat) ; returns unsat
(pop)
```

Nevertheless, no existing theory provides the unbounded $\sum$ summation.
One trick I've used before is to introduce an uninterpreted function 
 `sum` of type $\mathbb{Z} \times \mathbb{R} \rightarrow \mathbb{R}$, 
 to reduce equivalence to syntactic equality.
Specifically: 

```smt
(declare-fun sum (Int Real) Real)

(push)
(assert (not (= (sum j (* (A i j) (B j k))) (sum j (* (B j k) (A i j))))))
(check-sat) ; returns unsat
(pop)
```

But we'd still like to encode properties of summation, for example 
 $\sum_j \sum_k e = \sum_k \sum_j e$.
Well, maybe we can just try that:

```smt
(assert (forall ((j Int) (k Int) (e Real)) (= (sum j (sum k e)) (sum k (sum j e)))))

(push)
(assert (not (= (sum k (sum j (* (A i j) (B j k)))) (sum j (sum k (* (B j k) (A i j)))))))
(check-sat); returns unsat
(pop)
```

It worked (at least for me)! But quantified reasoning is undecidable in general, 
 so did we get lucky?
Well, sort of. This is where _EUF_ comes in.
From the [paper](), the Essentially Uninterpreted Fragment, or **EUF, 
 applies when quantified variables appear only as arguments to uninterpreted functions**.
This is true for our `forall` quantified assertion above: all of `i`, `j` and `e` appear
 only as arguments to `sum`!
The paper also says _some_ EUF formulas are decidable, so that's encouraging.
Let's try encoding some more axioms:

```smt
(assert (forall ((x Real) (i Int) (e Real)) (= (* x (sum i e)) (sum i (* x e)))))
```

Uh-oh. Here `x` is quantified, but it is also an argument of the interpreted function `*`.
That means we're already out of the EUF fragment, so we can no longer guarantee decidability.
In this case, further assertions may still be solvable, but they can also return `unknwon` or
 go on forever.

The immediate idea to get around this problem, is to use an uninterpreted `mul` funciton instead 
 of the interpreted `*`, and encode the algebraic identities of `mul` with axioms:

```smt
(declare-fun mul (Real Real) Real)

; associativity
(assert (forall ((x Real) (y Real) (z Real)) (= (mul x (mul y z)) (mul (mul x y) z))))
```

Now every quantified variable is 