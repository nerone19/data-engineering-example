help:
	@echo "run/db-migrator - Migrate sql schemas in the postgres DB."
	@echo "run/data-extractor - Extract data from the json/csv datasets and stores them in the DBs (mongo and postgres). Migration of schemas run before by default."
	@echo "run/preprocessor - Preprocess the dataset, cleaning raw_messages from unwanted characters."
	@echo "run/api - Runs the Flask application for exposing a WEB SERVER.."

run/db-migrator:
	docker compose --profile migrator up --build

run/data-extractor:
	docker compose --profile extractor up --build 

run/preprocessor:
	python ./src/preprocess.py

run/api:
	docker compose --profile api up --build --watch