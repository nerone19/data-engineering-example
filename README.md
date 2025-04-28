# What is this for?
Creates an application able to expose data about ships's travels stored inside a CSV dataset and a JSON one.
The data is stored inside Databases, both Sql and noSql (Postgres for the former and Mongo for the latter).

# How to start: steps
(1) `make run/preprocessor`: for preprocessing/cleaning the csv dataset's raw messages.
`make run/db-migrator`: for applying schema migration on the sql db (optional).
(2) `make run/data-extractor`: for storing data inside the sql and noSql databases. Before storing inside the SQL db, a schema migration is applied under the hood by default.
(3) `make run/api`: For running the Web Server, responsible of exposing API Endpoints.