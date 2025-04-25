# What is this for?
Creates an application able to expose data about ships's travels stored inside a CSV dataset and a JSON one.
The data is stored inside Databases, both Sql and noSql (Postgres for the former and Mongo for the latter).

# How to start.
`make run/preprocessor`: for preprocessing/cleaning the csv dataset's raw messages.
`make run/data-extractor`: for storing data inside the sql and noSql databases. Before storing inside the SQL db, a schema migration is applied under the hood.
`make run/api`: For running the Web Server, responsible of exposing API Endpoints.