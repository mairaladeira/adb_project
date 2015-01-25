--
-- PostgreSQL database dump
--

-- Dumped from database version 9.3.5
-- Dumped by pg_dump version 9.3.5
-- Started on 2015-01-25 01:46:05

SET statement_timeout = 0;
SET lock_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SET check_function_bodies = false;
SET client_min_messages = warning;

--
-- TOC entry 7 (class 2615 OID 16394)
-- Name: test; Type: SCHEMA; Schema: -; Owner: postgres
--

CREATE SCHEMA test;


ALTER SCHEMA test OWNER TO postgres;

--
-- TOC entry 173 (class 3079 OID 11750)
-- Name: plpgsql; Type: EXTENSION; Schema: -; Owner: 
--

CREATE EXTENSION IF NOT EXISTS plpgsql WITH SCHEMA pg_catalog;


--
-- TOC entry 1946 (class 0 OID 0)
-- Dependencies: 173
-- Name: EXTENSION plpgsql; Type: COMMENT; Schema: -; Owner: 
--

COMMENT ON EXTENSION plpgsql IS 'PL/pgSQL procedural language';


SET search_path = test, pg_catalog;

SET default_tablespace = '';

SET default_with_oids = false;

--
-- TOC entry 172 (class 1259 OID 16400)
-- Name: new; Type: TABLE; Schema: test; Owner: postgres; Tablespace: 
--

CREATE TABLE new (
    anew integer NOT NULL,
    bnew integer NOT NULL,
    cnew character(1),
    dnew character(1)
);


ALTER TABLE test.new OWNER TO postgres;

--
-- TOC entry 171 (class 1259 OID 16395)
-- Name: testing; Type: TABLE; Schema: test; Owner: postgres; Tablespace: 
--

CREATE TABLE testing (
    a integer NOT NULL,
    b integer,
    c character(1),
    d integer
);


ALTER TABLE test.testing OWNER TO postgres;

--
-- TOC entry 1938 (class 0 OID 16400)
-- Dependencies: 172
-- Data for Name: new; Type: TABLE DATA; Schema: test; Owner: postgres
--

COPY new (anew, bnew, cnew, dnew) FROM stdin;
\.


--
-- TOC entry 1937 (class 0 OID 16395)
-- Dependencies: 171
-- Data for Name: testing; Type: TABLE DATA; Schema: test; Owner: postgres
--

COPY testing (a, b, c, d) FROM stdin;
1	2	a	\N
3	4	b	\N
\.


--
-- TOC entry 1829 (class 2606 OID 16404)
-- Name: new_pkey; Type: CONSTRAINT; Schema: test; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY new
    ADD CONSTRAINT new_pkey PRIMARY KEY (anew, bnew);


--
-- TOC entry 1827 (class 2606 OID 16399)
-- Name: testing_pkey; Type: CONSTRAINT; Schema: test; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY testing
    ADD CONSTRAINT testing_pkey PRIMARY KEY (a);


--
-- TOC entry 1945 (class 0 OID 0)
-- Dependencies: 5
-- Name: public; Type: ACL; Schema: -; Owner: postgres
--

REVOKE ALL ON SCHEMA public FROM PUBLIC;
REVOKE ALL ON SCHEMA public FROM postgres;
GRANT ALL ON SCHEMA public TO postgres;
GRANT ALL ON SCHEMA public TO PUBLIC;


-- Completed on 2015-01-25 01:46:05

--
-- PostgreSQL database dump complete
--

