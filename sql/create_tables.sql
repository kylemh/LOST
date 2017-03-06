CREATE TABLE roles (
    role_pk         SERIAL PRIMARY KEY,
    title           VARCHAR(32)
);

CREATE TABLE users (
    user_pk         SERIAL PRIMARY KEY, -- SERIAL acting as a unique integer are compared within queries faster than varchar(16)
    role_fk         INTEGER REFERENCES roles(role_pk) DEFAULT 1,
    username        VARCHAR(16) UNIQUE NOT NULL, -- Username size mandated via project specs
    password        VARCHAR(16) NOT NULL -- Password size mandated via project specs
);

CREATE TABLE facilities (
    facility_pk     SERIAL PRIMARY KEY,
    fcode           VARCHAR(6),
    common_name     VARCHAR(32),
    location        VARCHAR(128)
);

CREATE TABLE assets (
    asset_pk        SERIAL PRIMARY KEY,
    asset_tag       VARCHAR(16),
    description     TEXT,
    disposed        BOOLEAN
    -- Removed facility_fk as part of standard normalization
);

CREATE TABLE asset_at (
    asset_fk        INTEGER REFERENCES assets(asset_pk) NOT NULL,
    facility_fk     INTEGER REFERENCES facilities(facility_pk) NOT NULL,
    arrive_dt       TIMESTAMP, -- UTC
    depart_dt       TIMESTAMP -- UTC
);

CREATE TABLE requests (
    request_pk SERIAL PRIMARY KEY,
    asset_fk INTEGER REFERENCES assets(asset_pk) NOT NULL, -- Request requires an asset to be referenced
    user_fk INTEGER REFERENCES users(user_pk) NOT NULL, -- Request requires a requesting user to be referenced
    src_fk INTEGER REFERENCES facilities(facility_pk) NOT NULL, -- Request requires a source facility to move an asset FROM
    dest_fk INTEGER REFERENCES facilities(facility_pk) NOT NULL, -- Request requires a destination facility to move an asset TO
    request_dt TIMESTAMP,
    approve_dt TIMESTAMP,
    approved BOOLEAN NOT NULL
);

CREATE TABLE in_transit (
    in_transit_pk SERIAL PRIMARY KEY,
    request_fk INTEGER REFERENCES requests(request_pk) NOT NULL, -- Assets cannot be moved unless they have a corresponding approved request
    load_dt TIMESTAMP,
    unload_dt TIMESTAMP
);

INSERT INTO roles (role_pk, title) VALUES (1, 'Guest');
INSERT INTO roles (role_pk, title) VALUES (2, 'Logistics Officer');
INSERT INTO roles (role_pk, title) VALUES (3, 'Facilities Officer');

-- TEST DATA
INSERT INTO facilities (fcode,common_name,location) VALUES ('MB005','Moonbase','The Moon');
INSERT INTO facilities (fcode,common_name,location) VALUES ('DC','Washington, DC','Washington, DC');
INSERT INTO facilities (fcode,common_name,location) VALUES ('HQ','Headquarters','Eugene, OR');
INSERT INTO facilities (fcode,common_name,location) VALUES ('NC','National City','National City, CA');
INSERT INTO facilities (fcode,common_name,location) VALUES ('LANM','Los Alamos, NM','Los Alamos, NM');
INSERT INTO facilities (fcode,common_name,location) VALUES ('SPNV','Sparks, NV','Sparks, NV');
INSERT INTO facilities (fcode,common_name,location) VALUES ('S300','Site 300','Area 51, NV');
INSERT INTO facilities (fcode,common_name,location) VALUES ('GRLK','Groom Lake','Groom Lake, NV');

INSERT INTO users (role_fk, username, password) VALUES ('3', 'fac', 'abc');
INSERT INTO users (role_fk, username, password) VALUES ('2', 'log', 'abc');