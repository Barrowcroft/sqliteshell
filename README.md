# sqliteshell
# A simple SQLite shell

A simple command line interface to a SQLite database.

Installation: 

Install as a UV tools using:

`uv tool install git+https://git@github.com/barrowcroft/sqliteshell.git`

and run with

`uvx sqliteshell`

### Use:

Once installed the shell can be invoked from the commanbd line using "uvx SQLiteShell".

A list of commands can be printed by typing ".help".

| Command                        | Purpose                          |
|-------------------------------|----------------------------------|
|.close|Closes the current database.|
|.create|Create and opens an database.
|.describe|Describes a table, view, index or trigger.|
|.edit|Edit a file / script.|
|.help|Shows this list of recognisable commands.|
|.indices|Prints a list of indices in the database.|
|.open|Opens a database.|
|.schema|Prints the database schema.|
|.script|Runs a query from a script file. (No data returned)|
|.tables|Prints a list of tables in the database.|
|.triggers|Prints a list of triggers in the database.|
|.views| Prints a list of views in the database.|

