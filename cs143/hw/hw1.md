# The Dark Side of the City of Angels

In this homework we will put our SQL-fu to use, getting a peek to the dark underworld of our city. We will be exploring the public Crime Dataset of Los Angeles. Buckle up, becuase what lies ahead may not be what you expect. 

The dataset is hosted on data.gov, home to hundreds of thousands of public datasets spanning all domains of the American life. I highly recommend you to poke around the website and see what you can find. The [LA Crime dataset](https://catalog.data.gov/dataset/crime-data-from-2020-to-present) we're working with is apparently the second most-viewd dataset on the website. 

Start by downloading the CSV (Comma Separated Values File) data from [this page](https://catalog.data.gov/dataset/crime-data-from-2020-to-present). Once download finishes, load the data into [SQLite Browser](https://sqlitebrowser.org/dl/) as follows (these instructions are for macOS; if you use linux/windows please refer to the SQLite [documentation](https://github.com/sqlitebrowser/sqlitebrowser/wiki)): 

1. Create a new database with File > New Database. It will ask you for a name and a location to save the database file. Give any name you like and click "save". Another window titled "Edit table definition" will popup - that is for creating new tables. ignore that by clicking cancel. 

2. Now, we will import our dataset as a table into the database. Click File > Import > Table from CSV file. Locate the CSV file you just downloaded, and click Open. Another window pops up with a preview of the data. Change the Table name to "crime", and make sure the Field seperator is set to "," (comma), and you should be able to see a spreadsheet-like preview of the data with many rows and columns. Click OK. 

Now we have our data in the database! Take a look around by clicking on "Browse Data". This should display a spreadsheet showing the entire table. Note that the table is very wide with many columns - bad design! Also note that there are NULLs *literally every where*. So this data is a bit dirty, and we will clean it up first. But to clean it up we first need to understand what's in the data. Let's go column by column. 

The first column is a bit mysterious and contains a bunch of random numbers. Usually, this is some kind of ID used to uniquely idenitfy each data record. In other words, it should form a **primary key** of the table. Let's test out our hypothesis: 

* What SQL query can you write to check if the `DR_NO` column is a primary key?

> There are different ways to do this, including using `GROUP BY`:

```sql
SELECT * FROM crime GROUP BY DR_NO HAVING COUNT(*) > 1
```

The second and third columns are more self-explanatory: `Date Rptd` probably means date reported, and `Date OCC` is the date that the crime actually occured. After each date we also see a time, but it looks like the time is always 12 AM? Let's check if that's the case. To do that, we first need to pull out the time part out of the string. 

* Write a SQL query to extract the time out of each of the two columns. You may ask AI to find the appropriate SQLite feature for this. Tip: when you have spaces and other weird charactors in column names, you need to quote it: `SELECT "Date Rptd" FROM crime;`

* Now, write another query to see if the time is always 12 AM. 

Spoiler: turns out the time is always 12 AM, so we can just drop that. 

* Write a query that extracts the date from the two columns. 

There is a small problem: SQLite [requires](https://sqlite.org/lang_datefunc.html#tmval) date to be stored in `YYYY-MM-DD`, but in this dataset it's stored as `MM/DD/YYYY`. 

* Write a query that corrects the date. 

Now moving on to the `TIME OCC` column. You guessed it from the name: it's the time that the crime actually occured. If you read a few entries you'll realize they are using "military time", i.e. 2100 means 21:00. 

* Write a query that combines the `DATE OCC` column and `TIME OCC` column into SQLite datetime format `YYYY-MM-DD HH:MM`

The next two columns are `AREA` and `AREA NAME`. If you sort by `AREA` (by clicking on it), you'll see that the `AREA` column is probably some kind of `ID` for `AREA NAME`. But it's not a primary key for this table! 

* Write a query to check if `AREA` uniquely determines `AREA NAME`. 

Next comes a column named `Rpt Dist No`. Compare this to `AREA`, you'll find some patterns. 

* Write a query to check if `AREA` always appears at the front of `Rpt Dist No`

The column `Part 1-2` seems to suggest some crimes has part 1 and part 2, but I actually couldn't figure out a way to link two parts of the same crime together. So if you found a way, please let me know! 

After that we have `Crm Cd`, which should determine `Crm Cd Desc`, and you can check that in the usual way. I'm not 100% sure what `Mocodes` are but searching online it seems to be some "modus operandi" codes describing specific activities invovled in the crime. The next columns of age, sex and descent are self-explanantory. The premis,  weapon, and status columns are also similar to what we have seen. 

But now we see four columns `Crm Cd 1` - `Crm Cd 4` again! This seems to suggest certain incidents involve multiple crimes. But this way of keeping track of multiple crimes is pretty awkward, evident by the NULLs everywhere. 

* Think about how you would instead store multiple crimes. We will get back to this when we decompose the table. 

Finally, we have some columns recording the location and coordinates of the crimes. Then we're done! Phew! 

So we've said the organization of the table isn't ideal - there are way too many columns! We know the solution is to decompose the table into multiple ones. Given that we have a primary key, there is actually a rather extreme way of decomposition: 

* Decompose the table into as many tables as possible to minimize the number of columns per table. How many tables do you need? How many columns for each table? 

There is another nice side effect of this extreme decomposition: if there is a NULL in an entry, we can just drop that row without really losing information. 

* For each table in your decomposition, drop any row containing NULLs. 

* After dropping the NULLs, how can you reconstruct the original table? 

Decomposing tables like that is usually not necessary, and can complicate our queries. Usually it suffices to remove strict independency and dependency as we have done in class. There isn't really any useful strict independency despite some trivial ones in this table: 

* There are actually lots of "trivial"/"degenerate" independencies cause by the primary key. Can you find some examples? 

In other words, if we decompose using the trivial independencies, we would end up with the extreme decomposition above. So we won't do that. Instead, we will deal with the dependencies. For example, because we know `AREA` determines `AREA NAME`, we can "factor out" the `AREA NAME` column into a separate table. I.e., we keep the `AREA` column, and make a new table with columns `AREA` and `AREA NAME`. 

* Write a SQL query to create the new table with the two columns. 

Now do the same for all other strict dependencies in the table *except for* those from the primary key. 

There is one dependency that's very special: recall that `Rpt Dist No` determines `AREA`, so we would be factoring them out into a separate table. But that table will look a bit silly, where the `AREA` column simply drops the last 2 digits from the `Rpt Dist No` column. This is a case when *database views* can be very helpful: instead of actually creating the physical table, we create a *virtual table* that computes the `AREA` code from `Rpt Dist No`. 

* Write a query using only the `Rpt Dist No` but returns the same result as `SELECT DISTINCT "Rpt Dist No", AREA FROM crime`. 

The last bit to clean up is the issue with the crime codes: every row has a `Crm Cd` column as well as additional `Crm Cd 1` through `Crm Cd 4`. Also, it seems `Crm Cd` is always contained in one of the `Crm Cd n` columns and therefore might be redundant. 

* Write a query to check if that's always the case. Be careful with NULLs! 

The current way of storing crime code is quite awkward, and that's an artifact of using only one table to store all information. But we're using a database, and we can use more tables! 

* Write a SQL query to separate the crime codes into another table. Drop the NULLs. 

At this point, our table is more or less clean! Your table schema should look something like this: 

```
crime(DR_NO, Date Rptd, Date OCC, TIME OCC, Rpt Dist No, 
      Part 1-2, mocodes, age, sex, descent, 
      Premis Cd, Weapon Cd, Status, 
      Location, Cross Street, Lat, Lon)

dist_area(Rpt Dist No, AREA) (virtual table)

area(AREA, AREA_NAME)

code(DR_NO, Crm Cd) (this consolidates all crime codes)

code_desc(Crm Cd, Crm Cd Desc)

premise(Premis Cd, Premis Desc)

weapon(Weapon Cd, Weapon Desc)

status(Status, Status Desc)
```

We can create these new tables in two different ways:

1. Use `CREATE TABLE` to actually create them "physically"

2. Create them as views/"virtual tables"

Let's try the first approach first. 

* Be careful to save your work. For example, you can first save a version of the DB containig both the original table and the new ones.

* Now save two different copies of the DB file, one with the original crime table created directly from CSV, and another with only the decomposed tables. Compare their size. 

The benefit of creating the table physically is that we can save space, and we can query the decomposed tables directly. The issue is that, if the city of LA sends us new data, it's probably in the form of the original table, and we would have to manually insert those into our new schema. That's where views come in: 

* Create the new tables as views. Then try inserting a new row into the crime table, and watch the change automatically appear in the views. 

With the data cleaned, now we can ask some interesting questions! For example: 

* What are the most popular weapons?

* What are the least popular weapons? 

* How many different weapons are there? 

* What's the "most dangerous" neighborhood? 

There's also a nice plot feature in SQLite browser that lets you do some quick visualization, for example

* What's the crime distribution over hours of the day? 

* What's the crime distribution over months of a year? 

My favorite one is this: 

* Plot `LAT` against `LON`, and you might recognize the shape. You'll need to remove 0.0 which denotes missing values, and it also helps to subtract min(lat) and min(lon) from lat and lon (you'll need nested queries). The visualization could be a little laggy due to having too many points. 

If you're really up for it, use some proper visualization library together with the SQLite library for your favorite language to run some more analysis. Make some interactive maps, go wild! 
