create table users (
    user_pk         serial primary key, -- SERIAL acting as a unique integer are compared within queries faster than varchar(16)
    username        varchar(16) unique not null, -- Username size mandated via project specs
    password        varchar(16) not null -- Password size mandated via project specs
);