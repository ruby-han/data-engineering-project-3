# Project 3: Understanding User Behavior

- You're a data scientist at a game development company  

- Your latest mobile game has two events you're interested in tracking: `buy a
  sword` & `join guild`

- Each has metadata characterstic of such events (i.e., sword type, guild name,
  etc)

# Tasks

- Instrument your API server to log events to Kafka

- Assemble a data pipeline to catch these events: use Spark streaming to filter
  select event types from Kafka, land them into HDFS/parquet to make them
  available for analysis using Presto. 

- Use Apache Bench to generate test data for your pipeline.

- Produce an analytics report where you provide a description of your pipeline
  and some basic analysis of the events. Explaining the pipeline is key for this project!

# Files in Repo

- `ab.sh` - shell script used to seed streaming of data

- `batch_mode.py` - python script to seed batched/static data

- `commands.txt` - commands used to execute project 3 

- `console_approach.md` - commands used to filter for select event types from Kafka, land them into HDFS/parquet for analysis in Presto

- `docker-compose.yml` - spinning the pipeline

- `game_api.py` - game engine python script

- `project_3_instructions.md` - original project 3 descriptions and instructions

- `project_3.ipynb` - project 3 report (business q&a, data pipeline {Docker, Kafka, Flask, Apache Bench, Apache Spark, HDFS})

- `stream_and hive.py` - python script to stream continuous data
