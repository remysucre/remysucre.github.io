---
pagetitle: Remy Wang
---

# Remy Wang

- Email: remywang at cs.washington.edu
- Links: [Blog](./blog/index.html), [DBLP](https://dblp.org/pid/185/9964.html), [Photo](./imgs/remywang.png)

I'm a PhD student at [UWDB](http://db.cs.washington.edu/) and [PLSE](http://uwplse.org/)
advised by [Dan Suciu](https://homes.cs.washington.edu/~suciu/).
I optimize modern data systems with advanced techniques from programming languages and databases. 
**I will start as an Assistant Professor at UCLA in 2024.**

___

_SIGMOD'23_ We propose [free join](https://arxiv.org/abs/2301.10841), a new join algorithm unifying and generalizing traditional binary joins with worst-case optimal joins. Free join brings the best of both worlds, and outperforms both binary join and WCOJ in practice.

_EGRAPHS'22_ We tease out [deep connections](https://remy.wang/reports/dfta.pdf) among e-graphs, finite-state tree automata, and version space algebra. By fusing together powerful ideas from these different perspectives, we gain orders-of-magnitude speedup and discover a new technique for automated proofs.

_PODS'22_ **Best Paper** [Datalog^o^](https://arxiv.org/abs/2105.14435) is a query language that generalizes Datalog. It can express a wide range of computation from shortest paths to network centrality. In the paper we study its convergence behavior.

_SIGMOD'22_ **Invited to SIGMOD Record** We also developed a [query optimizer](https://arxiv.org/abs/2202.10390) for Datalog^o^ based on program synthesis.

_POPL'22_ Using advanced join algorithms, we made [pattern matching](https://arxiv.org/abs/2108.02290) in a rewrite system asymptotically faster.

_MLSys'21_ [Tensat](https://github.com/uwplse/tensat) is an optimizer for deep learning inference using equality saturation. It achieves state-of-the-art inference speed with very fast compilation.

_POPL'21_ **Distinguished Paper** [egg](https://egraphs-good.github.io/) is the rewrite engine underlying a new class of optimizers including Tensat and SPORES (see below). It implements an efficient algorithm for equality saturation.

_OOPSLA'21_ **Distinguished Paper** We used egg to [invent rewrite rules](https://egraphs-good.github.io/) that are in turn given to egg itself for equality saturation.

_VLDB'20_ [SPORES](https://dl.acm.org/doi/10.14778/3407790.3407799) is an optimizer for large scale linear algebra. It transforms linear algebra code through the powerful abstraction of relational algebra.

___

I have been very lucky to work with many brilliant undergraduate / master students:

[Jonathan Leang](https://www.linkedin.com/in/jleang) meticuously performed many intricate experiments for SPORES. Jonathan now works at Snowflake, and at the same time (!!) teaches Databases at UW.

[Yihong Zhang](https://effect.systems/) turned our idea of relational pattern matching into implementation and a publication. With this work, Yihong won 1st place in the PLDI 2021 Student Research Competition.