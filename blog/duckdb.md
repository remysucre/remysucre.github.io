# DuckDB Considered Harmful

I love DuckDB. It's [decades of database research](https://duckdb.org/why_duckdb#standing-on-the-shoulders-of-giants) 
 in a [single binary](https://github.com/duckdb/duckdb/releases),
 blazingly fast and completely free.
But systems like it have been weaponized by reviewers for DB conferences to
 carelessly dismiss important research.
I have served as a reviewer for 10+ database conferences and journals
 and written my fair share of papers,
 and there is a worrying trend that I call the "DuckDB effect":
 many reviewers take a naïve, irresponsible approach in their work,
 and blindly reject papers that do not immediately outperform
 the state-of-the-art.
Their review usually comes in the form of "why don't you compare to DuckDB?".
Sometimes they will show mercy and hand out a Revision to demand such a comparison, 
 even if the comparison makes no sense.
Arguably this is even worse than outright rejection,
 because the authors are now incentivized to hack their way
 into a win against the best system,
 and whatever tricks they come up with usually
 have nothing to do with the key insights of the paper. 
I call this *intellectual pollution* because it makes the paper dirty.

So why shouldn't you compare to DuckDB?
Because scientific progress is not a straight line.
If we require every next paper to outperform the previous one,
 we are forcing ourselves into a greedy algorithm that
 will get trapped in local optima.
The relational model itself took decades to mature and
 become competitive with earlier navigational systems, 
 and it took around 30 years for deep learning to be vindicated.
Of course, ideas that can be immediately applied to
 current systems are valuable and impactful,
 but revisiting core principles and restarting from scratch
 is more likely to lead to breakthroughs.
The latter is particularly challenging in the context of database research,
 because the field is so mature that system architecture has converged
 to a few highly optimized key components,
 and any improvement to one component will receive diminishing returns.
But if we want to bring vitality back to the field, 
 we have to invest in risky ideas that do not pay off immediately.

I urge my fellow reviewers to take a more nuanced approach when evaluating papers.
Instead of focusing on numbers, look for insights.
Instead of demanding packaged solutions, judge an idea by its potential.
Use your knowledge and experience to fill in the gaps,
 and imagine different futures that a paper makes possible.
Don't just rank papers by their position on some leaderboard,
 but ask yourself if you have learned something new.