# Transactions

For this homework, you are encouraged to use AI to figure out the API of the SQL libraries!

So far we've only interacted with the DB on the command line, 
but in real applications, we would be writing programs that talk to the DB.
For example, if you have an online shop, every time a customer clicks "submit order"
the following chain of events take place:

* the customer's web browser sends a message (a.k.a. a *request*) to your website
* the message is received by a piece of software called the *web server*
* you wrote some code telling what the web server should do upon receiving every message
* the code you wrote probably asks the web server to insert the new order into a database
* when the database is updated, your code tells the web server to respond with a "success" message
* the "success" message gets sent to the customer and is displayed in the browser

In fact, building a database-backed website is one of the best ways to practice your DB knowledge.
However, working with the web involves a lot of tools that are not central to this class.
In this assignment, we will focus on the relationship between your code and the database, and ignore
the web part.

So far we have been using SQLite thanks to its simplicity, but to fully appreciate the
various flavors of transactions, we will move to a bigger system and use MySQL.
Installing MySQL is quite a bit of hassle, but thankfully www.pythonanywhere.com
provides a web environment with MySQL, for free! 

* Make a free account on www.pythonanywhere.com, follow the tutorial to understand how to create files and execute code.
* Create a MySQL database and start a new MySQL console connected to your database. Try creating a table, insert some rows and run a query.

As promised, we will be talking to the database from code instead of just the console. 
Here is a simple example of that (can you see what's happening?):

```python
import mysql.connector

# Connect to server
cnx = mysql.connector.connect(
    host="yourname.mysql.pythonanywhere-services.com",
    user="yourname",
    database='yourname$default',
    password="s3cre3t!(the-password-you-set)")

cnx.start_transaction()

# Get a cursor
cur = cnx.cursor(buffered=True)

# Insert a row
cur.execute("insert into R values (2)")

# Execute a query
cur.execute("SELECT x from R")

# Fetch one result
row = cur.fetchone()

print("x is: {0}".format(row[0]))

# commit the transaction
cnx.commit()

# Close connection
cnx.close()
```

A connection is self-explanantory: it's an active channel where you can send commands and queries to the DB.
The concept of a *cursor* is a bit informal: originally, a cursor was used so that we can iterate over the result
returned by a query. Imagine you have a query that returns a lot of rows: chances are you don't need all the rows, 
so for efficiency, the database won't return everything all at once. Rather, the cursor is like a pointer to "the current row",
and you can call "get next row" on it one by one to retrieve the results you need.
In any case, you can just think of it as something you need whenever you want to submit a command to the DB.

Let's now put some more interesting data into the DB:

* In the MySQL console, create a table with 2 columns: UID and score
* From your python program, insert 100 random UIDs and scores into the database

That's right, we'll try to re-create our in-class exercise of giving everyone free scores.

* Recreate the chaos when we all tried to give 10 extra points to everyone, without any coordination. What isolation level should you set? Refer to the [documentation](https://dev.mysql.com/doc/connector-python/en/connector-python-api-mysqlconnection-start-transaction.html).
* Now, what isolation level do you need to avoid the chaos? Also try out some other isolation levels - do they happen to be enough?
* The documentation says the default isolation level applies when the argument is not specified. Without looking it up, can you try out some experiments
and figure out what the default level is?
* What is the difference between REPEATABLE READ and SERIALIZABLE? Can you write some code that will result in different behavior under those two levels?
Hint: the `sleep()` command in SQL might be helpful.

The reason we used MySQL instead of SQLite is that the former allows for finer-grained concurrency control. Locking in MySQL is per-item,
(usually means per-row), whereas SQLite always locks the entire DB.

* To see the difference, write some python code to recreate when we did "everyone only gives points to oneself", in both MySQL and SQLite.
You will need the built-in [sqlite3](https://docs.python.org/3/library/sqlite3.html) library in python.
* To make the difference more pronounced, use `sleep` to make each database action take longer.
* Without looking it up, can you run some experiments to figure out SQLite's isolation level?
* Is it possible to have the phantom problem in SQLite? Why or why not?