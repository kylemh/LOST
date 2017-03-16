--
-- PostgreSQL database dump
--

-- Dumped from database version 9.5.6
-- Dumped by pg_dump version 9.5.6

SET statement_timeout = 0;
SET lock_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SET check_function_bodies = false;
SET client_min_messages = warning;
SET row_security = off;

--
-- Name: plpgsql; Type: EXTENSION; Schema: -; Owner: 
--

CREATE EXTENSION IF NOT EXISTS plpgsql WITH SCHEMA pg_catalog;


--
-- Name: EXTENSION plpgsql; Type: COMMENT; Schema: -; Owner: 
--

COMMENT ON EXTENSION plpgsql IS 'PL/pgSQL procedural language';


SET search_path = public, pg_catalog;

SET default_tablespace = '';

SET default_with_oids = false;

--
-- Name: asset_at; Type: TABLE; Schema: public; Owner: kmh
--

CREATE TABLE asset_at (
    asset_fk integer NOT NULL,
    facility_fk integer NOT NULL,
    arrive_dt timestamp without time zone,
    depart_dt timestamp without time zone
);


ALTER TABLE asset_at OWNER TO kmh;

--
-- Name: assets; Type: TABLE; Schema: public; Owner: kmh
--

CREATE TABLE assets (
    asset_pk integer NOT NULL,
    asset_tag character varying(16),
    description text,
    disposed boolean
);


ALTER TABLE assets OWNER TO kmh;

--
-- Name: assets_asset_pk_seq; Type: SEQUENCE; Schema: public; Owner: kmh
--

CREATE SEQUENCE assets_asset_pk_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE assets_asset_pk_seq OWNER TO kmh;

--
-- Name: assets_asset_pk_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: kmh
--

ALTER SEQUENCE assets_asset_pk_seq OWNED BY assets.asset_pk;


--
-- Name: facilities; Type: TABLE; Schema: public; Owner: kmh
--

CREATE TABLE facilities (
    facility_pk integer NOT NULL,
    fcode character varying(6),
    common_name character varying(32),
    location character varying(128)
);


ALTER TABLE facilities OWNER TO kmh;

--
-- Name: facilities_facility_pk_seq; Type: SEQUENCE; Schema: public; Owner: kmh
--

CREATE SEQUENCE facilities_facility_pk_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE facilities_facility_pk_seq OWNER TO kmh;

--
-- Name: facilities_facility_pk_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: kmh
--

ALTER SEQUENCE facilities_facility_pk_seq OWNED BY facilities.facility_pk;


--
-- Name: in_transit; Type: TABLE; Schema: public; Owner: kmh
--

CREATE TABLE in_transit (
    in_transit_pk integer NOT NULL,
    request_fk integer NOT NULL,
    load_dt timestamp without time zone,
    unload_dt timestamp without time zone
);


ALTER TABLE in_transit OWNER TO kmh;

--
-- Name: in_transit_in_transit_pk_seq; Type: SEQUENCE; Schema: public; Owner: kmh
--

CREATE SEQUENCE in_transit_in_transit_pk_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE in_transit_in_transit_pk_seq OWNER TO kmh;

--
-- Name: in_transit_in_transit_pk_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: kmh
--

ALTER SEQUENCE in_transit_in_transit_pk_seq OWNED BY in_transit.in_transit_pk;


--
-- Name: requests; Type: TABLE; Schema: public; Owner: kmh
--

CREATE TABLE requests (
    request_pk integer NOT NULL,
    asset_fk integer NOT NULL,
    user_fk integer NOT NULL,
    src_fk integer NOT NULL,
    dest_fk integer NOT NULL,
    request_dt timestamp without time zone,
    approve_dt timestamp without time zone,
    approved boolean NOT NULL,
    approving_user_fk integer,
    completed boolean NOT NULL
);


ALTER TABLE requests OWNER TO kmh;

--
-- Name: requests_request_pk_seq; Type: SEQUENCE; Schema: public; Owner: kmh
--

CREATE SEQUENCE requests_request_pk_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE requests_request_pk_seq OWNER TO kmh;

--
-- Name: requests_request_pk_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: kmh
--

ALTER SEQUENCE requests_request_pk_seq OWNED BY requests.request_pk;


--
-- Name: roles; Type: TABLE; Schema: public; Owner: kmh
--

CREATE TABLE roles (
    role_pk integer NOT NULL,
    title character varying(32)
);


ALTER TABLE roles OWNER TO kmh;

--
-- Name: roles_role_pk_seq; Type: SEQUENCE; Schema: public; Owner: kmh
--

CREATE SEQUENCE roles_role_pk_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE roles_role_pk_seq OWNER TO kmh;

--
-- Name: roles_role_pk_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: kmh
--

ALTER SEQUENCE roles_role_pk_seq OWNED BY roles.role_pk;


--
-- Name: users; Type: TABLE; Schema: public; Owner: kmh
--

CREATE TABLE users (
    user_pk integer NOT NULL,
    role_fk integer DEFAULT 1,
    username character varying(16) NOT NULL,
    password character varying(16) NOT NULL,
    active boolean DEFAULT true
);


ALTER TABLE users OWNER TO kmh;

--
-- Name: users_user_pk_seq; Type: SEQUENCE; Schema: public; Owner: kmh
--

CREATE SEQUENCE users_user_pk_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE users_user_pk_seq OWNER TO kmh;

--
-- Name: users_user_pk_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: kmh
--

ALTER SEQUENCE users_user_pk_seq OWNED BY users.user_pk;


--
-- Name: asset_pk; Type: DEFAULT; Schema: public; Owner: kmh
--

ALTER TABLE ONLY assets ALTER COLUMN asset_pk SET DEFAULT nextval('assets_asset_pk_seq'::regclass);


--
-- Name: facility_pk; Type: DEFAULT; Schema: public; Owner: kmh
--

ALTER TABLE ONLY facilities ALTER COLUMN facility_pk SET DEFAULT nextval('facilities_facility_pk_seq'::regclass);


--
-- Name: in_transit_pk; Type: DEFAULT; Schema: public; Owner: kmh
--

ALTER TABLE ONLY in_transit ALTER COLUMN in_transit_pk SET DEFAULT nextval('in_transit_in_transit_pk_seq'::regclass);


--
-- Name: request_pk; Type: DEFAULT; Schema: public; Owner: kmh
--

ALTER TABLE ONLY requests ALTER COLUMN request_pk SET DEFAULT nextval('requests_request_pk_seq'::regclass);


--
-- Name: role_pk; Type: DEFAULT; Schema: public; Owner: kmh
--

ALTER TABLE ONLY roles ALTER COLUMN role_pk SET DEFAULT nextval('roles_role_pk_seq'::regclass);


--
-- Name: user_pk; Type: DEFAULT; Schema: public; Owner: kmh
--

ALTER TABLE ONLY users ALTER COLUMN user_pk SET DEFAULT nextval('users_user_pk_seq'::regclass);


--
-- Data for Name: asset_at; Type: TABLE DATA; Schema: public; Owner: kmh
--

COPY asset_at (asset_fk, facility_fk, arrive_dt, depart_dt) FROM stdin;
1	1	1928-06-06 00:00:00	2002-06-14 00:00:00
4	2	1998-02-06 00:00:00	\N
5	3	2004-03-19 00:00:00	\N
7	3	2004-03-19 00:00:00	\N
8	3	2004-03-19 00:00:00	2008-07-11 00:00:00
9	3	2004-03-19 00:00:00	2008-06-05 00:00:00
10	3	2004-03-19 00:00:00	\N
11	10	2017-03-05 00:00:00	\N
6	3	2004-03-19 00:00:00	2017-03-14 00:00:00
6	4	2017-03-18 00:00:00	\N
\.


--
-- Data for Name: assets; Type: TABLE DATA; Schema: public; Owner: kmh
--

COPY assets (asset_pk, asset_tag, description, disposed) FROM stdin;
1	SG001	Stargate	t
2	SG001	Stargate	t
3	SG001	Stargate	t
4	SG002	Stargate	f
5	PJ001	Puddle Jumper	f
6	PJ002	Puddle Jumper	t
7	PJ003	Puddle Jumper	f
8	PJ004	Puddle Jumper	t
9	PJ005	Puddle Jumper	t
10	PJ006	Puddle Jumper	f
11	X001A	Alien skin samples	f
\.


--
-- Name: assets_asset_pk_seq; Type: SEQUENCE SET; Schema: public; Owner: kmh
--

SELECT pg_catalog.setval('assets_asset_pk_seq', 11, true);


--
-- Data for Name: facilities; Type: TABLE DATA; Schema: public; Owner: kmh
--

COPY facilities (facility_pk, fcode, common_name, location) FROM stdin;
1	HQ	Headquarters	\N
2	DC	Capital	\N
3	M0A	Alpha Site	\N
4	M0B	Beta Site	\N
5	M0G	Gamma Site	\N
6	P4OM	Olympus	\N
7	P4HB	Hellas Basin	\N
8	G001	Abydos	\N
9	OR1876	University of Oregon	Eugene, OR
10	MB001	Moonbase	The Moon
\.


--
-- Name: facilities_facility_pk_seq; Type: SEQUENCE SET; Schema: public; Owner: kmh
--

SELECT pg_catalog.setval('facilities_facility_pk_seq', 10, true);


--
-- Data for Name: in_transit; Type: TABLE DATA; Schema: public; Owner: kmh
--

COPY in_transit (in_transit_pk, request_fk, load_dt, unload_dt) FROM stdin;
1	1	2005-02-21 00:00:00	2005-02-23 00:00:00
2	2	2006-01-24 00:00:00	2006-01-27 00:00:00
3	3	2006-10-13 00:00:00	2006-10-15 00:00:00
4	4	2007-02-18 00:00:00	2007-02-19 00:00:00
5	5	2008-04-14 00:00:00	2008-04-16 00:00:00
6	6	2008-09-28 00:00:00	2008-10-01 00:00:00
7	7	2008-11-01 00:00:00	2008-11-03 00:00:00
8	8	2009-02-28 00:00:00	2009-03-02 00:00:00
9	9	2009-04-06 00:00:00	2009-04-08 00:00:00
10	10	2010-01-17 00:00:00	2010-01-20 00:00:00
11	11	2011-03-27 00:00:00	2011-03-29 00:00:00
12	12	2011-04-30 00:00:00	2011-05-02 00:00:00
13	13	2011-06-27 00:00:00	2011-06-30 00:00:00
14	14	2012-10-14 00:00:00	2012-10-15 00:00:00
15	15	2013-06-01 00:00:00	2013-06-03 00:00:00
16	16	2013-07-09 00:00:00	2013-07-11 00:00:00
17	17	2014-01-06 00:00:00	2014-01-08 00:00:00
18	18	2014-04-07 00:00:00	2014-04-09 00:00:00
19	19	2014-05-26 00:00:00	2014-05-28 00:00:00
20	20	2014-06-02 00:00:00	2014-06-04 00:00:00
21	21	2014-08-19 00:00:00	2014-08-21 00:00:00
22	22	2014-09-21 00:00:00	2014-09-22 00:00:00
23	23	2014-12-06 00:00:00	2014-12-08 00:00:00
24	24	2015-04-11 00:00:00	2015-04-12 00:00:00
25	25	2015-05-24 00:00:00	2015-05-26 00:00:00
26	26	2016-10-09 00:00:00	2016-10-11 00:00:00
27	28	2017-03-14 00:00:00	2017-03-18 00:00:00
\.


--
-- Name: in_transit_in_transit_pk_seq; Type: SEQUENCE SET; Schema: public; Owner: kmh
--

SELECT pg_catalog.setval('in_transit_in_transit_pk_seq', 27, true);


--
-- Data for Name: requests; Type: TABLE DATA; Schema: public; Owner: kmh
--

COPY requests (request_pk, asset_fk, user_fk, src_fk, dest_fk, request_dt, approve_dt, approved, approving_user_fk, completed) FROM stdin;
1	5	1	3	8	2005-02-18 00:00:00	2005-02-20 00:00:00	t	3	t
2	10	5	3	8	2006-01-20 00:00:00	2006-01-22 00:00:00	t	6	t
3	10	8	8	1	2006-10-13 00:00:00	2006-10-13 00:00:00	t	6	t
4	10	1	1	8	2007-02-16 00:00:00	2007-02-17 00:00:00	t	3	t
5	7	5	3	4	2008-04-11 00:00:00	2008-04-13 00:00:00	t	7	t
6	5	4	8	3	2008-09-26 00:00:00	2008-09-28 00:00:00	t	3	t
7	10	1	8	1	2008-10-31 00:00:00	2008-11-01 00:00:00	t	3	t
8	9	1	3	6	2009-02-27 00:00:00	2009-02-28 00:00:00	t	7	t
9	8	4	3	2	2009-04-03 00:00:00	2009-04-05 00:00:00	t	7	t
10	6	8	3	1	2010-01-15 00:00:00	2010-01-17 00:00:00	t	3	t
11	8	4	2	6	2011-03-25 00:00:00	2011-03-26 00:00:00	t	2	t
12	7	5	4	8	2011-04-29 00:00:00	2011-04-30 00:00:00	t	9	t
13	10	8	1	5	2011-06-24 00:00:00	2011-06-26 00:00:00	t	3	t
14	9	1	6	5	2012-10-12 00:00:00	2012-10-13 00:00:00	t	6	t
15	10	5	5	4	2013-05-31 00:00:00	2013-06-01 00:00:00	t	2	t
16	7	8	8	5	2013-07-05 00:00:00	2013-07-08 00:00:00	t	9	t
17	7	5	5	8	2014-01-03 00:00:00	2014-01-05 00:00:00	t	7	t
18	8	8	6	5	2014-04-04 00:00:00	2014-04-05 00:00:00	t	7	t
19	5	1	3	6	2014-05-23 00:00:00	2014-05-24 00:00:00	t	2	t
20	5	5	6	8	2014-05-30 00:00:00	2014-05-31 00:00:00	t	3	t
21	8	4	5	3	2014-08-15 00:00:00	2014-08-18 00:00:00	t	9	t
22	6	4	1	4	2014-09-19 00:00:00	2014-09-21 00:00:00	t	6	t
23	7	4	8	1	2014-12-05 00:00:00	2014-12-06 00:00:00	t	6	t
24	7	1	1	6	2015-04-10 00:00:00	2015-04-11 00:00:00	t	9	t
25	7	1	6	1	2015-05-22 00:00:00	2015-05-24 00:00:00	t	3	t
26	8	4	3	5	2016-10-07 00:00:00	2016-10-08 00:00:00	t	2	t
27	1	10	1	2	2017-03-15 04:15:07.478001	\N	f	\N	t
28	6	10	3	4	2017-03-15 04:15:20.307617	2017-03-15 04:15:42.445517	t	11	t
\.


--
-- Name: requests_request_pk_seq; Type: SEQUENCE SET; Schema: public; Owner: kmh
--

SELECT pg_catalog.setval('requests_request_pk_seq', 28, true);


--
-- Data for Name: roles; Type: TABLE DATA; Schema: public; Owner: kmh
--

COPY roles (role_pk, title) FROM stdin;
1	Guest
2	Logistics Officer
3	Facilities Officer
\.


--
-- Name: roles_role_pk_seq; Type: SEQUENCE SET; Schema: public; Owner: kmh
--

SELECT pg_catalog.setval('roles_role_pk_seq', 1, false);


--
-- Data for Name: users; Type: TABLE DATA; Schema: public; Owner: kmh
--

COPY users (user_pk, role_fk, username, password, active) FROM stdin;
1	2	malcom	svalley	t
2	3	kaylee	sh1ny	t
3	3	inara	AeICfUZdNUyg	t
4	2	jayne	b00m	t
5	2	river	2x2HandsOfBlue	t
6	3	shepherd	h4v3n	f
7	3	simon	river	t
8	2	zoe	svalley	t
9	3	wash	dinosaurs	f
10	2	log	abc	t
11	3	fac	abc	t
\.


--
-- Name: users_user_pk_seq; Type: SEQUENCE SET; Schema: public; Owner: kmh
--

SELECT pg_catalog.setval('users_user_pk_seq', 11, true);


--
-- Name: assets_pkey; Type: CONSTRAINT; Schema: public; Owner: kmh
--

ALTER TABLE ONLY assets
    ADD CONSTRAINT assets_pkey PRIMARY KEY (asset_pk);


--
-- Name: facilities_pkey; Type: CONSTRAINT; Schema: public; Owner: kmh
--

ALTER TABLE ONLY facilities
    ADD CONSTRAINT facilities_pkey PRIMARY KEY (facility_pk);


--
-- Name: in_transit_pkey; Type: CONSTRAINT; Schema: public; Owner: kmh
--

ALTER TABLE ONLY in_transit
    ADD CONSTRAINT in_transit_pkey PRIMARY KEY (in_transit_pk);


--
-- Name: requests_pkey; Type: CONSTRAINT; Schema: public; Owner: kmh
--

ALTER TABLE ONLY requests
    ADD CONSTRAINT requests_pkey PRIMARY KEY (request_pk);


--
-- Name: roles_pkey; Type: CONSTRAINT; Schema: public; Owner: kmh
--

ALTER TABLE ONLY roles
    ADD CONSTRAINT roles_pkey PRIMARY KEY (role_pk);


--
-- Name: users_pkey; Type: CONSTRAINT; Schema: public; Owner: kmh
--

ALTER TABLE ONLY users
    ADD CONSTRAINT users_pkey PRIMARY KEY (user_pk);


--
-- Name: users_username_key; Type: CONSTRAINT; Schema: public; Owner: kmh
--

ALTER TABLE ONLY users
    ADD CONSTRAINT users_username_key UNIQUE (username);


--
-- Name: asset_at_asset_fk_fkey; Type: FK CONSTRAINT; Schema: public; Owner: kmh
--

ALTER TABLE ONLY asset_at
    ADD CONSTRAINT asset_at_asset_fk_fkey FOREIGN KEY (asset_fk) REFERENCES assets(asset_pk);


--
-- Name: asset_at_facility_fk_fkey; Type: FK CONSTRAINT; Schema: public; Owner: kmh
--

ALTER TABLE ONLY asset_at
    ADD CONSTRAINT asset_at_facility_fk_fkey FOREIGN KEY (facility_fk) REFERENCES facilities(facility_pk);


--
-- Name: in_transit_request_fk_fkey; Type: FK CONSTRAINT; Schema: public; Owner: kmh
--

ALTER TABLE ONLY in_transit
    ADD CONSTRAINT in_transit_request_fk_fkey FOREIGN KEY (request_fk) REFERENCES requests(request_pk);


--
-- Name: requests_approving_user_fk_fkey; Type: FK CONSTRAINT; Schema: public; Owner: kmh
--

ALTER TABLE ONLY requests
    ADD CONSTRAINT requests_approving_user_fk_fkey FOREIGN KEY (approving_user_fk) REFERENCES users(user_pk);


--
-- Name: requests_asset_fk_fkey; Type: FK CONSTRAINT; Schema: public; Owner: kmh
--

ALTER TABLE ONLY requests
    ADD CONSTRAINT requests_asset_fk_fkey FOREIGN KEY (asset_fk) REFERENCES assets(asset_pk);


--
-- Name: requests_dest_fk_fkey; Type: FK CONSTRAINT; Schema: public; Owner: kmh
--

ALTER TABLE ONLY requests
    ADD CONSTRAINT requests_dest_fk_fkey FOREIGN KEY (dest_fk) REFERENCES facilities(facility_pk);


--
-- Name: requests_src_fk_fkey; Type: FK CONSTRAINT; Schema: public; Owner: kmh
--

ALTER TABLE ONLY requests
    ADD CONSTRAINT requests_src_fk_fkey FOREIGN KEY (src_fk) REFERENCES facilities(facility_pk);


--
-- Name: requests_user_fk_fkey; Type: FK CONSTRAINT; Schema: public; Owner: kmh
--

ALTER TABLE ONLY requests
    ADD CONSTRAINT requests_user_fk_fkey FOREIGN KEY (user_fk) REFERENCES users(user_pk);


--
-- Name: users_role_fk_fkey; Type: FK CONSTRAINT; Schema: public; Owner: kmh
--

ALTER TABLE ONLY users
    ADD CONSTRAINT users_role_fk_fkey FOREIGN KEY (role_fk) REFERENCES roles(role_pk);


--
-- Name: public; Type: ACL; Schema: -; Owner: postgres
--

REVOKE ALL ON SCHEMA public FROM PUBLIC;
REVOKE ALL ON SCHEMA public FROM postgres;
GRANT ALL ON SCHEMA public TO postgres;
GRANT ALL ON SCHEMA public TO PUBLIC;


--
-- PostgreSQL database dump complete
--

