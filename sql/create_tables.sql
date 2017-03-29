CREATE TABLE roles (
    role_pk         SERIAL PRIMARY KEY,
    title           VARCHAR(32)
);

-- TODO: Add minimum values for username and password
CREATE TABLE users (
    user_pk         SERIAL PRIMARY KEY, -- SERIAL acting as a unique integer are compared within queries faster than varchar(16)
    role_fk         INTEGER REFERENCES roles(role_pk) DEFAULT 1,
    username        VARCHAR(16) UNIQUE NOT NULL, -- Username size mandated via project specs
    salt            BYTEA NOT NULL, -- Password salt for db obfuscation
    password        BYTEA NOT NULL, -- Password size mandated via project specs
    active          BOOLEAN DEFAULT TRUE -- Added as required by HW9
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
    approved BOOLEAN NOT NULL,
    approving_user_fk INTEGER REFERENCES users(user_pk), -- Needed for data export/import
    completed BOOLEAN NOT NULL
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
INSERT INTO facilities (fcode,common_name,location) VALUES ('MB001', 'Moonbase', 'The Moon');
INSERT INTO facilities (fcode,common_name,location) VALUES ('DC', 'The Capitol', 'Washington, D.C.');
INSERT INTO facilities (fcode,common_name,location) VALUES ('HQ', 'Headquarters', 'Cheyenne Mountain Complex, CO');
INSERT INTO facilities (fcode,common_name,location) VALUES ('NC', 'National City', 'National City, CA');
INSERT INTO facilities (fcode,common_name,location) VALUES ('S300', 'Site 300', 'Area 51, NV');
INSERT INTO facilities (fcode,common_name,location) VALUES ('GRLK', 'Groom Lake', 'Groom Lake, NV');
INSERT INTO facilities (fcode,common_name,location) VALUES ('UO', 'University of Oregon', 'Eugene, OR');
