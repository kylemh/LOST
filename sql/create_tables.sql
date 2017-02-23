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
    facility_fk     INTEGER REFERENCES facilities(facility_pk),
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

CREATE TABLE convoys (
    convoy_pk       SERIAL PRIMARY KEY,
    request_id      VARCHAR(16),
    src_fk          INTEGER REFERENCES facilities(facility_pk) NOT NULL,
    dst_fk          INTEGER REFERENCES facilities(facility_pk) NOT NULL,
    depart_dt       TIMESTAMP, -- UTC
    arrive_dt       TIMESTAMP  -- UTC
);

CREATE TABLE vehicles (
    vehicle_pk      SERIAL PRIMARY KEY,
    asset_fk        INTEGER REFERENCES assets(asset_pk) NOT NULL -- Convoy vehicles must be OSNAP assets
);

CREATE TABLE asset_on (
    asset_fk    INTEGER REFERENCES assets(asset_pk) NOT NULL,
    convoy_fk   INTEGER REFERENCES convoys(convoy_pk) NOT NULL,
    load_dt     TIMESTAMP, -- UTC
    unload_dt   TIMESTAMP  -- UTC
);

INSERT INTO roles (role_pk, title) VALUES (1, 'Guest');
INSERT INTO roles (role_pk, title) VALUES (2, 'Logistics Officer');
INSERT INTO roles (role_pk, title) VALUES (3, 'Facilities Officer');

-- REMOVE AFTER COMPLETION
INSERT INTO facilities (fcode,common_name) VALUES ('MB005','Moonbase');
INSERT INTO facilities (fcode,common_name) VALUES ('DC','Washington, DC');
INSERT INTO facilities (fcode,common_name) VALUES ('HQ','Headquarters');
INSERT INTO facilities (fcode,common_name) VALUES ('NC','National City');
INSERT INTO facilities (fcode,common_name) VALUES ('LANM','Los Alamos, NM');
INSERT INTO facilities (fcode,common_name) VALUES ('SPNV','Sparks, NV');
INSERT INTO facilities (fcode,common_name) VALUES ('S300','Site 300');
INSERT INTO facilities (fcode,common_name) VALUES ('GRLK','Groom Lake');