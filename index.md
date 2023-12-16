---
pagetitle: Remy Wang
---

# Remy Wang

- Email: remywang at cs.ucla.edu
- Links: [Blog](./blog/index.html), [DBLP](https://dblp.org/pid/185/9964.html), [Photo](./imgs/remy.jpg)

I'm a research fellow at Simons Institute @ UC Berkeley 
 (and recent graduate of [UWDB](http://db.cs.washington.edu/) and [PLSE](http://uwplse.org/)).
I optimize modern data systems with advanced techniques from programming languages and databases. 
**I will start as an Assistant Professor at UCLA in 2024.**
If you want to join my lab, 
 please read [this](projects.html) before contacting me.

___

[SIGMOD'23] **SIGMOD Research Highlight Award** We propose [free join](https://arxiv.org/abs/2301.10841), a new join algorithm unifying and generalizing traditional binary joins with worst-case optimal joins. Free join brings the best of both worlds, and outperforms both binary join and WCOJ in practice.

[EGRAPHS'22] We tease out [deep connections](https://remy.wang/reports/dfta.pdf) among e-graphs, finite-state tree automata, and version space algebra. By fusing together powerful ideas from these different perspectives, we gain orders-of-magnitude speedup and discover a new technique for automated proofs.

[PODS'22] **Best Paper** [Datalog^o^](https://arxiv.org/abs/2105.14435) is a query language that generalizes Datalog. It can express a wide range of computation from shortest paths to network centrality. In the paper we study its convergence behavior.

[SIGMOD'22] **Invited to SIGMOD Record** We also developed a [query optimizer](https://arxiv.org/abs/2202.10390) for Datalog^o^ based on program synthesis.

[POPL'22] Using advanced join algorithms, we made [pattern matching](https://arxiv.org/abs/2108.02290) in a rewrite system asymptotically faster.

[MLSys'21] [Tensat](https://github.com/uwplse/tensat) is an optimizer for deep learning inference using equality saturation. It achieves state-of-the-art inference speed with very fast compilation.

[POPL'21] **Distinguished Paper** [egg](https://egraphs-good.github.io/) is the rewrite engine underlying a new class of optimizers including Tensat and SPORES (see below). It implements an efficient algorithm for equality saturation.

[OOPSLA'21] **Distinguished Paper** We used egg to [invent rewrite rules](https://dl.acm.org/doi/10.1145/3485496) that are in turn given to egg itself for equality saturation.

[VLDB'20] [SPORES](https://dl.acm.org/doi/10.14778/3407790.3407799) is an optimizer for large scale linear algebra. It transforms linear algebra code through the powerful abstraction of relational algebra.

___

I have been very lucky to work with many brilliant undergraduate / master students:

[Jonathan Leang](https://www.linkedin.com/in/jleang) meticuously performed many intricate experiments for SPORES. Jonathan now works at Snowflake, and at the same time (!!) teaches Databases at UW.

[Yihong Zhang](https://effect.systems/) turned our idea of relational pattern matching into implementation and a publication. With this work, Yihong won 1st place in the PLDI 2021 Student Research Competition.
