--
-- PostgreSQL database dump
--

-- Dumped from database version 9.3.5
-- Dumped by pg_dump version 9.3.5
-- Started on 2015-02-01 16:46:54

SET statement_timeout = 0;
SET lock_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SET check_function_bodies = false;
SET client_min_messages = warning;

--
-- TOC entry 1950 (class 1262 OID 24751)
-- Name: dbnormalizer; Type: DATABASE; Schema: -; Owner: postgres
--

CREATE DATABASE dbnormalizer WITH TEMPLATE = template0 ENCODING = 'UTF8' LC_COLLATE = 'English_United States.1252' LC_CTYPE = 'English_United States.1252';


ALTER DATABASE dbnormalizer OWNER TO postgres;

\connect dbnormalizer

SET statement_timeout = 0;
SET lock_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SET check_function_bodies = false;
SET client_min_messages = warning;

--
-- TOC entry 173 (class 3079 OID 11750)
-- Name: plpgsql; Type: EXTENSION; Schema: -; Owner: 
--

CREATE EXTENSION IF NOT EXISTS plpgsql WITH SCHEMA pg_catalog;


--
-- TOC entry 1953 (class 0 OID 0)
-- Dependencies: 173
-- Name: EXTENSION plpgsql; Type: COMMENT; Schema: -; Owner: 
--

COMMENT ON EXTENSION plpgsql IS 'PL/pgSQL procedural language';


SET search_path = public, pg_catalog;

SET default_tablespace = '';

SET default_with_oids = false;

--
-- TOC entry 171 (class 1259 OID 24766)
-- Name: compositepk; Type: TABLE; Schema: public; Owner: postgres; Tablespace: 
--

CREATE TABLE compositepk (
    col1pk integer NOT NULL,
    col2pk integer NOT NULL,
    col3 character(1),
    col4 character(1)
);


ALTER TABLE public.compositepk OWNER TO postgres;

--
-- TOC entry 170 (class 1259 OID 24752)
-- Name: tane; Type: TABLE; Schema: public; Owner: postgres; Tablespace: 
--

CREATE TABLE tane (
    a integer,
    b character(1),
    c character(1),
    d character varying,
    tuple_id integer NOT NULL
);


ALTER TABLE public.tane OWNER TO postgres;

--
-- TOC entry 172 (class 1259 OID 32958)
-- Name: testing; Type: TABLE; Schema: public; Owner: postgres; Tablespace: 
--

CREATE TABLE testing (
    a integer NOT NULL,
    b integer,
    c character(1),
    d integer
);


ALTER TABLE public.testing OWNER TO postgres;

--
-- TOC entry 1944 (class 0 OID 24766)
-- Dependencies: 171
-- Data for Name: compositepk; Type: TABLE DATA; Schema: public; Owner: postgres
--

INSERT INTO compositepk (col1pk, col2pk, col3, col4) VALUES (1, 1, 'a', 'a');
INSERT INTO compositepk (col1pk, col2pk, col3, col4) VALUES (1, 3, 'b', 'c');
INSERT INTO compositepk (col1pk, col2pk, col3, col4) VALUES (2, 2, 'd', 'b');
INSERT INTO compositepk (col1pk, col2pk, col3, col4) VALUES (1, 2, 'd', 'a');
INSERT INTO compositepk (col1pk, col2pk, col3, col4) VALUES (2, 1, 'a', 'a');


--
-- TOC entry 1943 (class 0 OID 24752)
-- Dependencies: 170
-- Data for Name: tane; Type: TABLE DATA; Schema: public; Owner: postgres
--

INSERT INTO tane (a, b, c, d, tuple_id) VALUES (1, 'a', '$', 'Flower', 1);
INSERT INTO tane (a, b, c, d, tuple_id) VALUES (1, 'A', '@', 'Tulip', 2);
INSERT INTO tane (a, b, c, d, tuple_id) VALUES (2, 'A', '$', 'Daffodil', 3);
INSERT INTO tane (a, b, c, d, tuple_id) VALUES (2, 'A', '$', 'Flower', 4);
INSERT INTO tane (a, b, c, d, tuple_id) VALUES (2, 'b', '@', 'Lily', 5);
INSERT INTO tane (a, b, c, d, tuple_id) VALUES (3, 'b', '$', 'Orchid', 6);
INSERT INTO tane (a, b, c, d, tuple_id) VALUES (3, 'C', '@', 'Flower', 7);
INSERT INTO tane (a, b, c, d, tuple_id) VALUES (3, 'C', '#', 'Rose', 8);
INSERT INTO tane (a, b, c, d, tuple_id) VALUES (2, 'X', '$', 'DD', 9);


--
-- TOC entry 1945 (class 0 OID 32958)
-- Dependencies: 172
-- Data for Name: testing; Type: TABLE DATA; Schema: public; Owner: postgres
--

INSERT INTO testing (a, b, c, d) VALUES (1, 2, 'a', 1);
INSERT INTO testing (a, b, c, d) VALUES (3, 4, 'b', 1);
INSERT INTO testing (a, b, c, d) VALUES (4, 4, 'b', 2);


--
-- TOC entry 1833 (class 2606 OID 24773)
-- Name: new_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY compositepk
    ADD CONSTRAINT new_pkey PRIMARY KEY (col1pk, col2pk);


--
-- TOC entry 1831 (class 2606 OID 24759)
-- Name: paper_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY tane
    ADD CONSTRAINT paper_pkey PRIMARY KEY (tuple_id);


--
-- TOC entry 1835 (class 2606 OID 32962)
-- Name: testing_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY testing
    ADD CONSTRAINT testing_pkey PRIMARY KEY (a);


--
-- TOC entry 1952 (class 0 OID 0)
-- Dependencies: 5
-- Name: public; Type: ACL; Schema: -; Owner: postgres
--

REVOKE ALL ON SCHEMA public FROM PUBLIC;
REVOKE ALL ON SCHEMA public FROM postgres;
GRANT ALL ON SCHEMA public TO postgres;
GRANT ALL ON SCHEMA public TO PUBLIC;


-- Completed on 2015-02-01 16:46:55

--
-- PostgreSQL database dump complete
--

