CREATE KEYSPACE wind 
WITH replication = {'class': 'SimpleStrategy', 'replication_factor': '1'};

USE wind;

CREATE TABLE winddata (
    stationid text,
    time timestamp,
    direction float,
    temp float,
    velocity float,
    PRIMARY KEY (stationid, time)
);




