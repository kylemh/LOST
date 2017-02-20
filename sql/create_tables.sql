-- Handle dropdb and createdb for lost
DROP DATABASE if exists lost;
CREATE DATABASE lost
    WITH OWNER osnapdev;
\connect lost

-- Wipe residuals
DROP TABLE if exists users;

create table users (
    user_pk     serial primary key, -- Serial acting as a unique integer are compared within queries faster than varchar(16)
    username    varchar(16) not null, -- Username size mandated via project specs
    password    varchar(16) not null, -- Password size mandated via project specs
);