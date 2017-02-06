create table products (
    product_pk      serial primary key,
    vendor          varchar(128) not null,
    description     text,
    alt_description text,
    product_name    varchar(128),
    product_model   varchar(128),
    price           numeric
);

create table assets (
    asset_pk        serial primary key,
    product_fk      integer, -- Nullable, not purchased asset
    asset_tag       varchar(32),
    description     text,
    alt_description text
);

create table vehicles (
    vehicle_pk      serial primary key,
    asset_fk        integer REFERENCES assets(asset_pk) not null -- Convoy vehicles must be OSNAP assets
);

create table facilities (
    facility_pk     serial primary key,
    fcode           varchar(16),
    common_name     varchar(128),
    location        varchar(128) -- May make this a reference later
);

create table asset_at (
    asset_fk        integer REFERENCES assets(asset_pk) not null,
    facility_fk     integer REFERENCES facilities(facility_pk) not null,
    arrive_dt       timestamp, -- UTC
    depart_dt       timestamp -- UTC
);

create table convoys (
    convoy_pk       serial primary key,
    request_id      varchar(16),
    src_fk          integer REFERENCES facilities(facility_pk) not null,
    dst_fk          integer REFERENCES facilities(facility_pk) not null,
    depart_dt       timestamp, -- UTC
    arrive_dt       timestamp  -- UTC
);

create table waypoints (
    convoy_fk   integer REFERENCES convoys(convoy_pk) not null,
    point_dt    timestamp --UTC
);

create table used_by (
    vehicle_fk  integer REFERENCES vehicles(vehicle_pk) not null,
    convoy_fk   integer REFERENCES convoys(convoy_pk) not null
);

create table asset_on (
    asset_fk    integer REFERENCES assets(asset_pk) not null,
    convoy_fk   integer REFERENCES convoys(convoy_pk) not null,
    load_dt     timestamp, -- UTC
    unload_dt   timestamp  -- UTC
);

create table users (
    user_pk     serial primary key,
    username    varchar(64) not null,
    active      boolean default FALSE
);

create table roles (
    role_pk     serial primary key,
    title       varchar(32)
);

create table user_is (
    user_fk     integer REFERENCES users(user_pk) not null,
    role_fk     integer REFERENCES roles(role_pk) not null
);

create table user_supports (
    user_fk     integer REFERENCES users(user_pk) not null,
    facility_fk integer REFERENCES facilities(facility_pk) not null
);

create table sec_levels (
    level_pk    integer primary key, -- levels have order
    abbrv       varchar(3),
    comment     varchar(128)
);

create table sec_compartments (
    compartment_pk  serial primary key,
    abbrv           varchar(8),
    comment         varchar(128)
);

create table security_tags (
    tag_pk          serial primary key,
    level_fk        integer REFERENCES sec_levels(level_pk) not null,
    compartment_fk  integer REFERENCES sec_compartments(compartment_pk) not null,
    -- Need to add a constraint so that exactly one of the following is set
    user_fk         integer REFERENCES users(user_pk),
    asset_fk        integer REFERENCES assets(asset_pk),
    product_fk      integer REFERENCES products(product_pk)
);