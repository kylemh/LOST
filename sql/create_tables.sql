-- noinspection SqlNoDataSourceInspectionForFile

-- noinspection SqlDialectInspectionForFile

/* ASSET TABLES */
CREATE TABLE products (
	product_pk serial primary key,
	vendor varchar(255),
	description varchar(255),
	alt_description varchar(255)
);

CREATE TABLE assets (
	asset_pk serial primary key,
	product_fk integer REFERENCES products(product_pk) NOT NULL,
	asset_tag varchar(255),
	description varchar(255),
	alt_description varchar(255)
);

CREATE TABLE vehicles (
	vehicle_pk serial primary key,
	asset_fk integer REFERENCES assets(asset_pk) NOT NULL
);

CREATE TABLE facilities (
	facility_pk serial primary key,
	fcode varchar(6),
	common_name varchar(255),
	location varchar(255)
);

CREATE TABLE asset_at (
	asset_fk integer REFERENCES assets(asset_pk) NOT NULL,
	facility_fk integer REFERENCES facilities(facility_pk) NOT NULL,
	arrive_dt timestamp,
	depart_dt timestamp
);

CREATE TABLE convoys (
	convoy_pk serial primary key,
	request varchar(255),
	source_fk integer REFERENCES facilities(facility_pk) NOT NULL,
	dest_fk integer REFERENCES facilities(facility_pk) NOT NULL,
	depart_dt timestamp, 
	arrive_dt timestamp 
);

CREATE TABLE used_by (
	vehicle_fk integer REFERENCES vehicles(vehicle_pk) NOT NULL,
	convoy_fk integer REFERENCES convoys(convoy_pk) NOT NULL
);

CREATE TABLE asset_on (
	asset_fk integer REFERENCES assets(asset_pk) NOT NULL,
	convoy_fk integer REFERENCES convoys(convoy_pk) NOT NULL,
	load_dt timestamp, 
	unload_dt timestamp 
);

/* USER TABLES */
CREATE TABLE users (
	user_pk serial primary key,
	username varchar(255),
	active boolean
);

CREATE TABLE roles (
	role_pk serial primary key,
	title varchar(128)
);

CREATE TABLE user_is (
	user_fk integer REFERENCES users(user_pk) NOT NULL,
	role_fk integer REFERENCES roles(role_pk) NOT NULL
);

CREATE TABLE user_supports (
	user_fk integer REFERENCES users(user_pk) NOT NULL,
	facility_fk integer REFERENCES facilities(facility_pk) NOT NULL
);

/* SECURITY TABLES */
CREATE TABLE levels (
	level_pk serial primary key,
	abbrv varchar(8),
	comment varchar(255)
);

CREATE TABLE compartments (
	compartment_pk serial primary key,
	abbrv varchar(8),
	comment varchar(255)
);

CREATE TABLE security_tags (
	tag_pk serial primary key,
	level_fk integer REFERENCES levels(level_pk) NOT NULL,
	compartment_fk integer REFERENCES compartments(compartment_pk) NOT NULL,
	user_fk integer REFERENCES users(user_pk),
	product_fk integer REFERENCES products(product_pk),
	asset_fk integer REFERENCES assets(asset_pk)
);
