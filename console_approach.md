# 2.0 Command Line Interface (CLI) Approach

This section provides console commands to run spark-submit and Presto analysis of business questions. 

## Docker

- Bring up cluster
```
docker-compose up -d
```

- Ensure `docker-compose.yml` file to ensure cloudera container has a port section with below:
```yaml
    ports:
      - "8888:8888"
```

## Kafka

- Create "events" topic
```
docker-compose exec kafka kafka-topics --create --topic events --partitions 1 --replication-factor 1 --if-not-exists --zookeeper zookeeper:32181
```

## Flask

- Run game engine API
```
docker-compose exec mids env FLASK_APP=/w205/project-3-ruby-han/game_api.py flask run --host 0.0.0.0
```

## Apache Bench

- Seed events by running shell script - static
```
sh ab.sh
```

## Streaming

- Set up to watch Kafka
```
docker-compose exec mids kafkacat -C -b kafka:29092 -t events -o beginning
```

- Run it
```
docker-compose exec spark spark-submit /w205/project-3-ruby-han/stream_and_hive.py

```

- Feed it 
```
while true; do
  docker-compose exec mids \
    ab -n 10 -H "Host: user1.comcast.com" \
      http://localhost:5000/purchase_a_sword
  sleep 10
done
```

## Hadoop

- Check what wrote to HDFS
```
docker-compose exec cloudera hadoop fs -ls /tmp/
```

Output:
```
Found 5 items
drwxrwxrwt   - root   supergroup          0 2021-04-11 08:04 /tmp/checkpoints_for_sword_purchases
drwxrwxrwt   - mapred mapred              0 2016-04-06 02:26 /tmp/hadoop-yarn
drwx-wx-wx   - hive   supergroup          0 2021-04-11 08:04 /tmp/hive
drwxrwxrwt   - mapred hadoop              0 2016-04-06 02:28 /tmp/logs
drwxrwxrwt   - root   supergroup          0 2021-04-11 08:07 /tmp/purchase_events
```

## Presto

- Hive metastore
```
docker-compose exec cloudera hive
```

```
create external table if not exists default.sword_purchases (
    Accept string,
    Host string,
    User_Agent string,
    event_type string,
    timestamp string,
    raw_event string
  )
  stored as parquet 
  location '/tmp/sword_purchases'
  tblproperties ("parquet.compress"="SNAPPY");
```

- Read with Presto
```
docker-compose exec presto presto --server presto:8080 --catalog hive --schema default
```

- Analyses - show tables
```
presto:default> show tables;
```

Output:
```
      Table      
-----------------
 purchase_events 
 sword_purchases 
(2 rows)

Query 20210411_080851_00002_b7bfs, FINISHED, 1 node
Splits: 2 total, 1 done (50.00%)
0:00 [2 rows, 72B] [6 rows/s, 238B/s]
```

- Business Question 1: How many sword purchases from continuous seed of data `purchase_events` table are there? 720.
```
presto:default> select count(*) from purchase_events;
```

Output:
```
 _col0 
-------
   720 
(1 row)

Query 20210411_081817_00012_b7bfs, FINISHED, 1 node
Splits: 72 total, 57 done (79.17%)
0:01 [580 rows, 127KB] [534 rows/s, 117KB/s]
```

- Business Question 2: How many users are there? 2.
```
presto:default> select count(distinct Host) from purchase_events;
```

Output:
```
 _col0 
-------
     2 
(1 row)

Query 20210411_081903_00013_b7bfs, FINISHED, 1 node
Splits: 78 total, 63 done (80.77%)
0:02 [640 rows, 143KB] [322 rows/s, 71.9KB/s]
```
