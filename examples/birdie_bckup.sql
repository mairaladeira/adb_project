--
-- PostgreSQL database dump
--

-- Dumped from database version 9.3.5
-- Dumped by pg_dump version 9.3.5
-- Started on 2015-02-01 16:47:43

SET statement_timeout = 0;
SET lock_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SET check_function_bodies = false;
SET client_min_messages = warning;

--
-- TOC entry 2008 (class 1262 OID 24626)
-- Name: birdie; Type: DATABASE; Schema: -; Owner: postgres
--

CREATE DATABASE birdie WITH TEMPLATE = template0 ENCODING = 'UTF8' LC_COLLATE = 'English_United States.1252' LC_CTYPE = 'English_United States.1252';


ALTER DATABASE birdie OWNER TO postgres;

\connect birdie

SET statement_timeout = 0;
SET lock_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SET check_function_bodies = false;
SET client_min_messages = warning;

--
-- TOC entry 178 (class 3079 OID 11750)
-- Name: plpgsql; Type: EXTENSION; Schema: -; Owner: 
--

CREATE EXTENSION IF NOT EXISTS plpgsql WITH SCHEMA pg_catalog;


--
-- TOC entry 2011 (class 0 OID 0)
-- Dependencies: 178
-- Name: EXTENSION plpgsql; Type: COMMENT; Schema: -; Owner: 
--

COMMENT ON EXTENSION plpgsql IS 'PL/pgSQL procedural language';


SET search_path = public, pg_catalog;

SET default_tablespace = '';

SET default_with_oids = false;

--
-- TOC entry 170 (class 1259 OID 24627)
-- Name: chirp; Type: TABLE; Schema: public; Owner: postgres; Tablespace: 
--

CREATE TABLE chirp (
    cid numeric NOT NULL,
    "timestamp" timestamp with time zone NOT NULL,
    author numeric NOT NULL,
    text character varying(80) NOT NULL
);


ALTER TABLE public.chirp OWNER TO postgres;

--
-- TOC entry 171 (class 1259 OID 24633)
-- Name: favorite; Type: TABLE; Schema: public; Owner: postgres; Tablespace: 
--

CREATE TABLE favorite (
    "user" numeric NOT NULL,
    chirp numeric NOT NULL
);


ALTER TABLE public.favorite OWNER TO postgres;

--
-- TOC entry 172 (class 1259 OID 24639)
-- Name: follower; Type: TABLE; Schema: public; Owner: postgres; Tablespace: 
--

CREATE TABLE follower (
    "user" numeric NOT NULL,
    friend numeric NOT NULL
);


ALTER TABLE public.follower OWNER TO postgres;

--
-- TOC entry 173 (class 1259 OID 24645)
-- Name: hashtag; Type: TABLE; Schema: public; Owner: postgres; Tablespace: 
--

CREATE TABLE hashtag (
    hid numeric NOT NULL,
    label character varying(40) NOT NULL,
    CONSTRAINT "Hashtag_label_check" CHECK (((label)::text ~~ '#%'::text))
);


ALTER TABLE public.hashtag OWNER TO postgres;

--
-- TOC entry 174 (class 1259 OID 24652)
-- Name: mention; Type: TABLE; Schema: public; Owner: postgres; Tablespace: 
--

CREATE TABLE mention (
    chirp numeric NOT NULL,
    "user" numeric NOT NULL
);


ALTER TABLE public.mention OWNER TO postgres;

--
-- TOC entry 175 (class 1259 OID 24658)
-- Name: rechirp; Type: TABLE; Schema: public; Owner: postgres; Tablespace: 
--

CREATE TABLE rechirp (
    rechirp numeric NOT NULL,
    chirp numeric NOT NULL
);


ALTER TABLE public.rechirp OWNER TO postgres;

--
-- TOC entry 176 (class 1259 OID 24664)
-- Name: taginchirp; Type: TABLE; Schema: public; Owner: postgres; Tablespace: 
--

CREATE TABLE taginchirp (
    tag numeric NOT NULL,
    chirp numeric NOT NULL
);


ALTER TABLE public.taginchirp OWNER TO postgres;

--
-- TOC entry 177 (class 1259 OID 24670)
-- Name: user; Type: TABLE; Schema: public; Owner: postgres; Tablespace: 
--

CREATE TABLE "user" (
    uid numeric NOT NULL,
    username character varying(25) NOT NULL,
    password text NOT NULL,
    date_of_registration date NOT NULL,
    geotag point,
    gravatar bytea
);


ALTER TABLE public."user" OWNER TO postgres;

--
-- TOC entry 1996 (class 0 OID 24627)
-- Dependencies: 170
-- Data for Name: chirp; Type: TABLE DATA; Schema: public; Owner: postgres
--

INSERT INTO chirp (cid, "timestamp", author, text) VALUES (1, '2014-10-10 10:33:44+02', 12, '@dog is my spirit animal');
INSERT INTO chirp (cid, "timestamp", author, text) VALUES (2, '2014-01-10 12:33:45+01', 1, 'Just chilling in #Lyon');
INSERT INTO chirp (cid, "timestamp", author, text) VALUES (3, '2014-10-10 10:33:46+02', 2, 'I wish we went to #Nantes');
INSERT INTO chirp (cid, "timestamp", author, text) VALUES (4, '2014-10-20 11:33:47+02', 3, 'I wish we went to #Nantes');
INSERT INTO chirp (cid, "timestamp", author, text) VALUES (5, '2014-10-10 10:54:48+02', 9, 'Just another brick in the wall…');
INSERT INTO chirp (cid, "timestamp", author, text) VALUES (6, '2013-12-10 10:33:49+01', 10, 'Thissss is Spartaaaa!!!! ');
INSERT INTO chirp (cid, "timestamp", author, text) VALUES (7, '2014-05-10 10:33:50+02', 12, 'meeeoowwwww');
INSERT INTO chirp (cid, "timestamp", author, text) VALUES (8, '2014-06-10 10:33:51+02', 13, 'meeeoowwwww');
INSERT INTO chirp (cid, "timestamp", author, text) VALUES (9, '2014-06-30 01:12:50+02', 6, 'Hello I love you won''t you tell me your name');
INSERT INTO chirp (cid, "timestamp", author, text) VALUES (10, '2014-07-10 10:50:12+02', 7, 'Dream of californication… ');
INSERT INTO chirp (cid, "timestamp", author, text) VALUES (11, '2014-07-20 10:21:15+02', 10, 'every day I love you less and less @t_gazelle');
INSERT INTO chirp (cid, "timestamp", author, text) VALUES (12, '2014-07-20 10:33:10+02', 14, 'Cause you look so fine that I really wanna make you mine!!');
INSERT INTO chirp (cid, "timestamp", author, text) VALUES (13, '2014-07-21 10:33:52+02', 4, 'In #Lyon with @KaiserCo @burcu @AlexGattino @alejandro @Iva');
INSERT INTO chirp (cid, "timestamp", author, text) VALUES (14, '2014-07-21 12:40:53+02', 11, 'I know what you did last summer >.< @MikePatton');
INSERT INTO chirp (cid, "timestamp", author, text) VALUES (15, '2014-07-22 20:33:54+02', 15, 'Just watched #NightmareBeforeChristmas with @t_gazelle');
INSERT INTO chirp (cid, "timestamp", author, text) VALUES (16, '2014-07-23 10:33:55+02', 15, 'oooooo it''s the final countdown!!!!! ');
INSERT INTO chirp (cid, "timestamp", author, text) VALUES (17, '2014-07-25 10:01:56+02', 15, 'I did my way!!! <3');
INSERT INTO chirp (cid, "timestamp", author, text) VALUES (18, '2014-07-27 10:33:57+02', 12, 'In #Nantes with my bff @dog');
INSERT INTO chirp (cid, "timestamp", author, text) VALUES (19, '2014-07-30 16:03:03+02', 3, 'Why the hell they don''t serve espresso with milk?? #France');
INSERT INTO chirp (cid, "timestamp", author, text) VALUES (20, '2014-07-30 16:08:10+02', 15, 'We''ll always have #Paris @JimMorrison');
INSERT INTO chirp (cid, "timestamp", author, text) VALUES (21, '2014-08-05 07:03:05+02', 15, 'Give me fuel give me fire !!! ');
INSERT INTO chirp (cid, "timestamp", author, text) VALUES (22, '2014-09-01 16:01:06+02', 8, 'Whyyy meeeee???');
INSERT INTO chirp (cid, "timestamp", author, text) VALUES (23, '2014-09-12 05:03:07+02', 1, 'A giraffe,  a giraffe!! <33333 #Zoo');
INSERT INTO chirp (cid, "timestamp", author, text) VALUES (24, '2014-09-12 16:04:08+02', 1, 'Don''t you touch the papers!!!! @KaiserCo');
INSERT INTO chirp (cid, "timestamp", author, text) VALUES (25, '2014-09-13 16:05:09+02', 1, 'Pole dancing is underrated!  #YOLO');
INSERT INTO chirp (cid, "timestamp", author, text) VALUES (26, '2014-09-13 16:10:10+02', 9, 'Yo soy tu madreee!! ');
INSERT INTO chirp (cid, "timestamp", author, text) VALUES (27, '2014-09-15 20:03:11+02', 3, 'We love #Belgrade <3 @Iva');
INSERT INTO chirp (cid, "timestamp", author, text) VALUES (28, '2014-09-29 03:05:12+02', 2, 'I wanna go to #Mamamia !!!!');
INSERT INTO chirp (cid, "timestamp", author, text) VALUES (29, '2014-10-01 02:01:13+02', 3, 'I wanna go to #Mamamia !!!!');
INSERT INTO chirp (cid, "timestamp", author, text) VALUES (30, '2014-10-01 04:05:14+02', 8, 'I wanna go to #Mamamia !!!!');
INSERT INTO chirp (cid, "timestamp", author, text) VALUES (31, '2014-10-01 09:03:15+02', 15, 'I wanna go to #Mamamia !!!!');
INSERT INTO chirp (cid, "timestamp", author, text) VALUES (32, '2014-10-02 06:03:16+02', 1, 'I wanna go to #Mamamia !!!!');
INSERT INTO chirp (cid, "timestamp", author, text) VALUES (33, '2014-10-02 16:03:17+02', 15, 'Don''t give up on your dreams, keep sleeping.');
INSERT INTO chirp (cid, "timestamp", author, text) VALUES (34, '2014-10-02 17:20:18+02', 11, 'I am Iron man!!! @AnthonyKiedis');
INSERT INTO chirp (cid, "timestamp", author, text) VALUES (35, '2014-10-02 17:03:19+02', 9, 'I wanna go to #Mamamia !!!!');
INSERT INTO chirp (cid, "timestamp", author, text) VALUES (36, '2014-10-02 19:03:20+02', 2, 'In love  #Lyon  <333');
INSERT INTO chirp (cid, "timestamp", author, text) VALUES (37, '2014-10-03 20:03:21+02', 1, 'Lets watch some animeee @cat');
INSERT INTO chirp (cid, "timestamp", author, text) VALUES (38, '2014-10-05 06:03:22+02', 9, 'Lets go to #Auchan');
INSERT INTO chirp (cid, "timestamp", author, text) VALUES (39, '2014-10-05 08:04:23+02', 12, 'Eat a Snickers!! :P @Iva');
INSERT INTO chirp (cid, "timestamp", author, text) VALUES (40, '2014-10-11 01:50:24+02', 12, 'The winter is coming..  xD @rabbit');
INSERT INTO chirp (cid, "timestamp", author, text) VALUES (41, '2014-10-12 05:03:25+02', 12, 'If a black cat crosses ur path, you''re doomed!!! xD @burcu');
INSERT INTO chirp (cid, "timestamp", author, text) VALUES (42, '2014-10-12 09:23:26+02', 3, 'No pain no gain! Studying in #Lyon');
INSERT INTO chirp (cid, "timestamp", author, text) VALUES (43, '2014-10-13 16:03:27+02', 2, 'No pain no gain! Studying in #Lyon');
INSERT INTO chirp (cid, "timestamp", author, text) VALUES (44, '2014-10-13 18:02:28+02', 12, 'Eating the best pizza in #Lyon #Mamamia @me');
INSERT INTO chirp (cid, "timestamp", author, text) VALUES (45, '2014-10-13 20:50:29+02', 10, 'Do not grow up! It is a trap!!! ');
INSERT INTO chirp (cid, "timestamp", author, text) VALUES (46, '2014-10-14 16:45:30+02', 9, 'I see skies are blue, the clouds are white… :) #Lyon');
INSERT INTO chirp (cid, "timestamp", author, text) VALUES (47, '2014-10-19 18:03:31+02', 6, 'Break on through to the other side!! B) @DamienRice');
INSERT INTO chirp (cid, "timestamp", author, text) VALUES (48, '2014-10-19 19:37:32+02', 5, 'You want it all but you can''t have it… @me');
INSERT INTO chirp (cid, "timestamp", author, text) VALUES (49, '2014-10-19 20:23:33+02', 10, 'wanna come over??? @cat');
INSERT INTO chirp (cid, "timestamp", author, text) VALUES (50, '2014-10-20 12:03:34+02', 8, 'Having fun by the river #Rhone #Lyon ');
INSERT INTO chirp (cid, "timestamp", author, text) VALUES (51, '2014-10-20 13:10:11+02', 9, 'I wanna but I''m not gonna');
INSERT INTO chirp (cid, "timestamp", author, text) VALUES (52, '2014-10-20 12:30:11+02', 13, 'Hey @me why you not follow :P');
INSERT INTO chirp (cid, "timestamp", author, text) VALUES (53, '2014-10-20 12:30:11+02', 11, 'Dream of californication… ');
INSERT INTO chirp (cid, "timestamp", author, text) VALUES (54, '2014-10-20 17:00:00+02', 11, 'Do not grow up! It is a trap!!!');
INSERT INTO chirp (cid, "timestamp", author, text) VALUES (55, '2014-10-17 00:00:00+02', 1, 'Only #Lyon');


--
-- TOC entry 1997 (class 0 OID 24633)
-- Dependencies: 171
-- Data for Name: favorite; Type: TABLE DATA; Schema: public; Owner: postgres
--

INSERT INTO favorite ("user", chirp) VALUES (1, 1);
INSERT INTO favorite ("user", chirp) VALUES (1, 3);
INSERT INTO favorite ("user", chirp) VALUES (1, 6);
INSERT INTO favorite ("user", chirp) VALUES (1, 9);
INSERT INTO favorite ("user", chirp) VALUES (1, 13);
INSERT INTO favorite ("user", chirp) VALUES (1, 15);
INSERT INTO favorite ("user", chirp) VALUES (1, 17);
INSERT INTO favorite ("user", chirp) VALUES (1, 21);
INSERT INTO favorite ("user", chirp) VALUES (1, 28);
INSERT INTO favorite ("user", chirp) VALUES (1, 36);
INSERT INTO favorite ("user", chirp) VALUES (1, 39);
INSERT INTO favorite ("user", chirp) VALUES (1, 42);
INSERT INTO favorite ("user", chirp) VALUES (1, 47);
INSERT INTO favorite ("user", chirp) VALUES (1, 50);
INSERT INTO favorite ("user", chirp) VALUES (2, 1);
INSERT INTO favorite ("user", chirp) VALUES (2, 2);
INSERT INTO favorite ("user", chirp) VALUES (2, 7);
INSERT INTO favorite ("user", chirp) VALUES (2, 14);
INSERT INTO favorite ("user", chirp) VALUES (2, 24);
INSERT INTO favorite ("user", chirp) VALUES (2, 38);
INSERT INTO favorite ("user", chirp) VALUES (2, 44);
INSERT INTO favorite ("user", chirp) VALUES (2, 51);
INSERT INTO favorite ("user", chirp) VALUES (3, 2);
INSERT INTO favorite ("user", chirp) VALUES (3, 3);
INSERT INTO favorite ("user", chirp) VALUES (3, 21);
INSERT INTO favorite ("user", chirp) VALUES (3, 18);
INSERT INTO favorite ("user", chirp) VALUES (3, 24);
INSERT INTO favorite ("user", chirp) VALUES (3, 25);
INSERT INTO favorite ("user", chirp) VALUES (3, 28);
INSERT INTO favorite ("user", chirp) VALUES (3, 50);
INSERT INTO favorite ("user", chirp) VALUES (3, 51);
INSERT INTO favorite ("user", chirp) VALUES (4, 26);
INSERT INTO favorite ("user", chirp) VALUES (4, 21);
INSERT INTO favorite ("user", chirp) VALUES (4, 28);
INSERT INTO favorite ("user", chirp) VALUES (4, 29);
INSERT INTO favorite ("user", chirp) VALUES (5, 5);
INSERT INTO favorite ("user", chirp) VALUES (5, 39);
INSERT INTO favorite ("user", chirp) VALUES (5, 9);
INSERT INTO favorite ("user", chirp) VALUES (6, 39);
INSERT INTO favorite ("user", chirp) VALUES (6, 30);
INSERT INTO favorite ("user", chirp) VALUES (6, 15);
INSERT INTO favorite ("user", chirp) VALUES (6, 32);
INSERT INTO favorite ("user", chirp) VALUES (7, 49);
INSERT INTO favorite ("user", chirp) VALUES (7, 32);
INSERT INTO favorite ("user", chirp) VALUES (7, 13);
INSERT INTO favorite ("user", chirp) VALUES (7, 29);
INSERT INTO favorite ("user", chirp) VALUES (7, 7);
INSERT INTO favorite ("user", chirp) VALUES (7, 18);
INSERT INTO favorite ("user", chirp) VALUES (9, 34);
INSERT INTO favorite ("user", chirp) VALUES (9, 28);
INSERT INTO favorite ("user", chirp) VALUES (9, 51);
INSERT INTO favorite ("user", chirp) VALUES (10, 44);
INSERT INTO favorite ("user", chirp) VALUES (10, 20);
INSERT INTO favorite ("user", chirp) VALUES (10, 33);
INSERT INTO favorite ("user", chirp) VALUES (11, 12);
INSERT INTO favorite ("user", chirp) VALUES (11, 49);
INSERT INTO favorite ("user", chirp) VALUES (12, 45);
INSERT INTO favorite ("user", chirp) VALUES (12, 25);
INSERT INTO favorite ("user", chirp) VALUES (12, 19);
INSERT INTO favorite ("user", chirp) VALUES (13, 1);
INSERT INTO favorite ("user", chirp) VALUES (13, 35);
INSERT INTO favorite ("user", chirp) VALUES (13, 46);
INSERT INTO favorite ("user", chirp) VALUES (13, 29);
INSERT INTO favorite ("user", chirp) VALUES (14, 24);
INSERT INTO favorite ("user", chirp) VALUES (14, 32);
INSERT INTO favorite ("user", chirp) VALUES (15, 13);
INSERT INTO favorite ("user", chirp) VALUES (15, 45);
INSERT INTO favorite ("user", chirp) VALUES (15, 28);
INSERT INTO favorite ("user", chirp) VALUES (15, 10);
INSERT INTO favorite ("user", chirp) VALUES (15, 12);
INSERT INTO favorite ("user", chirp) VALUES (15, 18);
INSERT INTO favorite ("user", chirp) VALUES (15, 22);
INSERT INTO favorite ("user", chirp) VALUES (15, 49);
INSERT INTO favorite ("user", chirp) VALUES (15, 32);


--
-- TOC entry 1998 (class 0 OID 24639)
-- Dependencies: 172
-- Data for Name: follower; Type: TABLE DATA; Schema: public; Owner: postgres
--

INSERT INTO follower ("user", friend) VALUES (1, 2);
INSERT INTO follower ("user", friend) VALUES (1, 3);
INSERT INTO follower ("user", friend) VALUES (1, 4);
INSERT INTO follower ("user", friend) VALUES (1, 8);
INSERT INTO follower ("user", friend) VALUES (1, 9);
INSERT INTO follower ("user", friend) VALUES (2, 1);
INSERT INTO follower ("user", friend) VALUES (2, 3);
INSERT INTO follower ("user", friend) VALUES (2, 8);
INSERT INTO follower ("user", friend) VALUES (2, 9);
INSERT INTO follower ("user", friend) VALUES (2, 12);
INSERT INTO follower ("user", friend) VALUES (2, 13);
INSERT INTO follower ("user", friend) VALUES (2, 15);
INSERT INTO follower ("user", friend) VALUES (3, 1);
INSERT INTO follower ("user", friend) VALUES (3, 2);
INSERT INTO follower ("user", friend) VALUES (3, 8);
INSERT INTO follower ("user", friend) VALUES (3, 9);
INSERT INTO follower ("user", friend) VALUES (3, 15);
INSERT INTO follower ("user", friend) VALUES (4, 1);
INSERT INTO follower ("user", friend) VALUES (4, 2);
INSERT INTO follower ("user", friend) VALUES (4, 3);
INSERT INTO follower ("user", friend) VALUES (4, 8);
INSERT INTO follower ("user", friend) VALUES (4, 9);
INSERT INTO follower ("user", friend) VALUES (5, 6);
INSERT INTO follower ("user", friend) VALUES (5, 7);
INSERT INTO follower ("user", friend) VALUES (6, 5);
INSERT INTO follower ("user", friend) VALUES (6, 7);
INSERT INTO follower ("user", friend) VALUES (7, 5);
INSERT INTO follower ("user", friend) VALUES (7, 11);
INSERT INTO follower ("user", friend) VALUES (8, 1);
INSERT INTO follower ("user", friend) VALUES (8, 2);
INSERT INTO follower ("user", friend) VALUES (8, 3);
INSERT INTO follower ("user", friend) VALUES (8, 9);
INSERT INTO follower ("user", friend) VALUES (9, 1);
INSERT INTO follower ("user", friend) VALUES (9, 2);
INSERT INTO follower ("user", friend) VALUES (9, 3);
INSERT INTO follower ("user", friend) VALUES (9, 8);
INSERT INTO follower ("user", friend) VALUES (10, 2);
INSERT INTO follower ("user", friend) VALUES (10, 13);
INSERT INTO follower ("user", friend) VALUES (11, 7);
INSERT INTO follower ("user", friend) VALUES (12, 1);
INSERT INTO follower ("user", friend) VALUES (12, 13);
INSERT INTO follower ("user", friend) VALUES (12, 10);
INSERT INTO follower ("user", friend) VALUES (12, 8);
INSERT INTO follower ("user", friend) VALUES (12, 15);
INSERT INTO follower ("user", friend) VALUES (13, 12);
INSERT INTO follower ("user", friend) VALUES (13, 14);
INSERT INTO follower ("user", friend) VALUES (14, 5);
INSERT INTO follower ("user", friend) VALUES (14, 6);
INSERT INTO follower ("user", friend) VALUES (14, 11);
INSERT INTO follower ("user", friend) VALUES (15, 1);
INSERT INTO follower ("user", friend) VALUES (15, 2);
INSERT INTO follower ("user", friend) VALUES (15, 3);
INSERT INTO follower ("user", friend) VALUES (15, 12);


--
-- TOC entry 1999 (class 0 OID 24645)
-- Dependencies: 173
-- Data for Name: hashtag; Type: TABLE DATA; Schema: public; Owner: postgres
--

INSERT INTO hashtag (hid, label) VALUES (1, '#Lyon');
INSERT INTO hashtag (hid, label) VALUES (2, '#Nantes');
INSERT INTO hashtag (hid, label) VALUES (3, '#NightmareBeforeChristmas');
INSERT INTO hashtag (hid, label) VALUES (4, '#France');
INSERT INTO hashtag (hid, label) VALUES (5, '#Paris');
INSERT INTO hashtag (hid, label) VALUES (6, '#Zoo');
INSERT INTO hashtag (hid, label) VALUES (7, '#YOLO');
INSERT INTO hashtag (hid, label) VALUES (8, '#Belgrade');
INSERT INTO hashtag (hid, label) VALUES (9, '#Mamamia');
INSERT INTO hashtag (hid, label) VALUES (10, '#Auchan');
INSERT INTO hashtag (hid, label) VALUES (11, '#Rhone');


--
-- TOC entry 2000 (class 0 OID 24652)
-- Dependencies: 174
-- Data for Name: mention; Type: TABLE DATA; Schema: public; Owner: postgres
--

INSERT INTO mention (chirp, "user") VALUES (1, 13);
INSERT INTO mention (chirp, "user") VALUES (11, 14);
INSERT INTO mention (chirp, "user") VALUES (13, 2);
INSERT INTO mention (chirp, "user") VALUES (13, 8);
INSERT INTO mention (chirp, "user") VALUES (13, 9);
INSERT INTO mention (chirp, "user") VALUES (13, 1);
INSERT INTO mention (chirp, "user") VALUES (13, 3);
INSERT INTO mention (chirp, "user") VALUES (14, 5);
INSERT INTO mention (chirp, "user") VALUES (15, 14);
INSERT INTO mention (chirp, "user") VALUES (18, 13);
INSERT INTO mention (chirp, "user") VALUES (20, 6);
INSERT INTO mention (chirp, "user") VALUES (24, 2);
INSERT INTO mention (chirp, "user") VALUES (27, 1);
INSERT INTO mention (chirp, "user") VALUES (34, 7);
INSERT INTO mention (chirp, "user") VALUES (37, 12);
INSERT INTO mention (chirp, "user") VALUES (39, 1);
INSERT INTO mention (chirp, "user") VALUES (40, 10);
INSERT INTO mention (chirp, "user") VALUES (41, 8);
INSERT INTO mention (chirp, "user") VALUES (44, 15);
INSERT INTO mention (chirp, "user") VALUES (47, 4);
INSERT INTO mention (chirp, "user") VALUES (48, 15);
INSERT INTO mention (chirp, "user") VALUES (49, 12);
INSERT INTO mention (chirp, "user") VALUES (52, 15);


--
-- TOC entry 2001 (class 0 OID 24658)
-- Dependencies: 175
-- Data for Name: rechirp; Type: TABLE DATA; Schema: public; Owner: postgres
--

INSERT INTO rechirp (rechirp, chirp) VALUES (4, 3);
INSERT INTO rechirp (rechirp, chirp) VALUES (8, 7);
INSERT INTO rechirp (rechirp, chirp) VALUES (29, 28);
INSERT INTO rechirp (rechirp, chirp) VALUES (30, 28);
INSERT INTO rechirp (rechirp, chirp) VALUES (31, 28);
INSERT INTO rechirp (rechirp, chirp) VALUES (32, 28);
INSERT INTO rechirp (rechirp, chirp) VALUES (35, 28);
INSERT INTO rechirp (rechirp, chirp) VALUES (43, 42);
INSERT INTO rechirp (rechirp, chirp) VALUES (53, 10);
INSERT INTO rechirp (rechirp, chirp) VALUES (54, 45);


--
-- TOC entry 2002 (class 0 OID 24664)
-- Dependencies: 176
-- Data for Name: taginchirp; Type: TABLE DATA; Schema: public; Owner: postgres
--

INSERT INTO taginchirp (tag, chirp) VALUES (1, 2);
INSERT INTO taginchirp (tag, chirp) VALUES (2, 3);
INSERT INTO taginchirp (tag, chirp) VALUES (2, 4);
INSERT INTO taginchirp (tag, chirp) VALUES (3, 15);
INSERT INTO taginchirp (tag, chirp) VALUES (2, 18);
INSERT INTO taginchirp (tag, chirp) VALUES (4, 19);
INSERT INTO taginchirp (tag, chirp) VALUES (5, 20);
INSERT INTO taginchirp (tag, chirp) VALUES (6, 23);
INSERT INTO taginchirp (tag, chirp) VALUES (7, 25);
INSERT INTO taginchirp (tag, chirp) VALUES (8, 27);
INSERT INTO taginchirp (tag, chirp) VALUES (9, 28);
INSERT INTO taginchirp (tag, chirp) VALUES (9, 29);
INSERT INTO taginchirp (tag, chirp) VALUES (9, 30);
INSERT INTO taginchirp (tag, chirp) VALUES (9, 31);
INSERT INTO taginchirp (tag, chirp) VALUES (9, 32);
INSERT INTO taginchirp (tag, chirp) VALUES (9, 35);
INSERT INTO taginchirp (tag, chirp) VALUES (1, 36);
INSERT INTO taginchirp (tag, chirp) VALUES (10, 38);
INSERT INTO taginchirp (tag, chirp) VALUES (1, 42);
INSERT INTO taginchirp (tag, chirp) VALUES (1, 43);
INSERT INTO taginchirp (tag, chirp) VALUES (1, 44);
INSERT INTO taginchirp (tag, chirp) VALUES (9, 44);
INSERT INTO taginchirp (tag, chirp) VALUES (1, 46);
INSERT INTO taginchirp (tag, chirp) VALUES (1, 50);
INSERT INTO taginchirp (tag, chirp) VALUES (11, 50);
INSERT INTO taginchirp (tag, chirp) VALUES (1, 55);


--
-- TOC entry 2003 (class 0 OID 24670)
-- Dependencies: 177
-- Data for Name: user; Type: TABLE DATA; Schema: public; Owner: postgres
--

INSERT INTO "user" (uid, username, password, date_of_registration, geotag, gravatar) VALUES (1, 'Iva', 'rUtPDnzz', '2013-10-09', '(44.799999999999997,20.466007000000001)', NULL);
INSERT INTO "user" (uid, username, password, date_of_registration, geotag, gravatar) VALUES (2, 'KaiserCO', '3g2Nccfk', '2013-12-10', '(14.583299999999999,120.9667)', NULL);
INSERT INTO "user" (uid, username, password, date_of_registration, geotag, gravatar) VALUES (3, 'AlexGattino', 'g7RC3nrK', '2013-05-11', '(44.799999999999997,20.466007000000001)', NULL);
INSERT INTO "user" (uid, username, password, date_of_registration, geotag, gravatar) VALUES (4, 'DamienRice', 'f6KWf8Pe', '2013-10-12', '(53,-8)', NULL);
INSERT INTO "user" (uid, username, password, date_of_registration, geotag, gravatar) VALUES (5, 'MikePatton', '6ZyvsYgM', '2013-01-04', '(47.2181,1.5528)', NULL);
INSERT INTO "user" (uid, username, password, date_of_registration, geotag, gravatar) VALUES (6, 'JimMorrison', '3HAzJMFK', '2013-12-04', '(47.2181,1.5528)', NULL);
INSERT INTO "user" (uid, username, password, date_of_registration, geotag, gravatar) VALUES (7, 'AnthonyKiedis', 'UBEcNYsZ', '2013-10-15', '(47.2181,1.5528)', NULL);
INSERT INTO "user" (uid, username, password, date_of_registration, geotag, gravatar) VALUES (8, 'burcu', 'ptWG59DZ', '2013-10-16', '(39.916699999999999,32.833300000000001)', NULL);
INSERT INTO "user" (uid, username, password, date_of_registration, geotag, gravatar) VALUES (9, 'alejandro', '46vrLhxG', '2013-10-17', '(10.5,-66.916700000000006)', NULL);
INSERT INTO "user" (uid, username, password, date_of_registration, geotag, gravatar) VALUES (10, 'rabbit', 'wKBkCZjj', '2013-10-18', '(45.759999999999998,4.8399999999999999)', NULL);
INSERT INTO "user" (uid, username, password, date_of_registration, geotag, gravatar) VALUES (11, 'RobertDJunior', 'cx9uYu2u', '2013-10-19', '(45.759999999999998,4.8399999999999999)', NULL);
INSERT INTO "user" (uid, username, password, date_of_registration, geotag, gravatar) VALUES (12, 'cat', 'jTAbJ2h6', '2013-10-02', '(45.759999999999998,4.8399999999999999)', NULL);
INSERT INTO "user" (uid, username, password, date_of_registration, geotag, gravatar) VALUES (13, 'dog', 'DcawJN3F', '2013-12-04', '(45.759999999999998,4.8399999999999999)', NULL);
INSERT INTO "user" (uid, username, password, date_of_registration, geotag, gravatar) VALUES (14, 't_gazelle', 'tDNUFQTE', '2013-03-22', '(45.759999999999998,4.8399999999999999)', NULL);
INSERT INTO "user" (uid, username, password, date_of_registration, geotag, gravatar) VALUES (15, 'me', 'W9xzcPqv', '2013-10-01', '(45.759999999999998,4.8399999999999999)', NULL);


--
-- TOC entry 1859 (class 2606 OID 24677)
-- Name: Chirp_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY chirp
    ADD CONSTRAINT "Chirp_pkey" PRIMARY KEY (cid);


--
-- TOC entry 1861 (class 2606 OID 24679)
-- Name: Favorite_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY favorite
    ADD CONSTRAINT "Favorite_pkey" PRIMARY KEY ("user", chirp);


--
-- TOC entry 1863 (class 2606 OID 24681)
-- Name: Follower_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY follower
    ADD CONSTRAINT "Follower_pkey" PRIMARY KEY ("user", friend);


--
-- TOC entry 1865 (class 2606 OID 24683)
-- Name: Hashtag_label_key; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY hashtag
    ADD CONSTRAINT "Hashtag_label_key" UNIQUE (label);


--
-- TOC entry 1867 (class 2606 OID 24685)
-- Name: Hashtag_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY hashtag
    ADD CONSTRAINT "Hashtag_pkey" PRIMARY KEY (hid);


--
-- TOC entry 1869 (class 2606 OID 24687)
-- Name: Mention_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY mention
    ADD CONSTRAINT "Mention_pkey" PRIMARY KEY (chirp, "user");


--
-- TOC entry 1871 (class 2606 OID 24689)
-- Name: Rechirp_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY rechirp
    ADD CONSTRAINT "Rechirp_pkey" PRIMARY KEY (rechirp, chirp);


--
-- TOC entry 1873 (class 2606 OID 24691)
-- Name: Taginchirp_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY taginchirp
    ADD CONSTRAINT "Taginchirp_pkey" PRIMARY KEY (tag, chirp);


--
-- TOC entry 1875 (class 2606 OID 24693)
-- Name: User_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY "user"
    ADD CONSTRAINT "User_pkey" PRIMARY KEY (uid);


--
-- TOC entry 1877 (class 2606 OID 24695)
-- Name: User_username_key; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY "user"
    ADD CONSTRAINT "User_username_key" UNIQUE (username);


--
-- TOC entry 1878 (class 2606 OID 24696)
-- Name: Chirp_author_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY chirp
    ADD CONSTRAINT "Chirp_author_fkey" FOREIGN KEY (author) REFERENCES "user"(uid);


--
-- TOC entry 1879 (class 2606 OID 24701)
-- Name: Favorite_chirp_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY favorite
    ADD CONSTRAINT "Favorite_chirp_fkey" FOREIGN KEY (chirp) REFERENCES chirp(cid);


--
-- TOC entry 1880 (class 2606 OID 24706)
-- Name: Favorite_user_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY favorite
    ADD CONSTRAINT "Favorite_user_fkey" FOREIGN KEY ("user") REFERENCES "user"(uid);


--
-- TOC entry 1881 (class 2606 OID 24711)
-- Name: Follower_friend_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY follower
    ADD CONSTRAINT "Follower_friend_fkey" FOREIGN KEY (friend) REFERENCES "user"(uid) ON UPDATE CASCADE ON DELETE CASCADE;


--
-- TOC entry 1882 (class 2606 OID 24716)
-- Name: Follower_user_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY follower
    ADD CONSTRAINT "Follower_user_fkey" FOREIGN KEY ("user") REFERENCES "user"(uid) ON UPDATE CASCADE ON DELETE CASCADE;


--
-- TOC entry 1883 (class 2606 OID 24721)
-- Name: Mention_chirp_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY mention
    ADD CONSTRAINT "Mention_chirp_fkey" FOREIGN KEY (chirp) REFERENCES chirp(cid) ON UPDATE CASCADE ON DELETE CASCADE;


--
-- TOC entry 1884 (class 2606 OID 24726)
-- Name: Mention_user_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY mention
    ADD CONSTRAINT "Mention_user_fkey" FOREIGN KEY ("user") REFERENCES "user"(uid) ON UPDATE CASCADE ON DELETE CASCADE;


--
-- TOC entry 1885 (class 2606 OID 24731)
-- Name: Rechirp_chirp_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY rechirp
    ADD CONSTRAINT "Rechirp_chirp_fkey" FOREIGN KEY (chirp) REFERENCES chirp(cid) ON UPDATE CASCADE ON DELETE CASCADE;


--
-- TOC entry 1886 (class 2606 OID 24736)
-- Name: Rechirp_rechirp_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY rechirp
    ADD CONSTRAINT "Rechirp_rechirp_fkey" FOREIGN KEY (rechirp) REFERENCES chirp(cid) ON UPDATE CASCADE ON DELETE CASCADE;


--
-- TOC entry 1887 (class 2606 OID 24741)
-- Name: Taginchirp_chirp_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY taginchirp
    ADD CONSTRAINT "Taginchirp_chirp_fkey" FOREIGN KEY (chirp) REFERENCES chirp(cid) ON UPDATE CASCADE ON DELETE CASCADE;


--
-- TOC entry 1888 (class 2606 OID 24746)
-- Name: Taginchirp_tag_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY taginchirp
    ADD CONSTRAINT "Taginchirp_tag_fkey" FOREIGN KEY (tag) REFERENCES hashtag(hid) ON UPDATE CASCADE ON DELETE CASCADE;


--
-- TOC entry 2010 (class 0 OID 0)
-- Dependencies: 6
-- Name: public; Type: ACL; Schema: -; Owner: postgres
--

REVOKE ALL ON SCHEMA public FROM PUBLIC;
REVOKE ALL ON SCHEMA public FROM postgres;
GRANT ALL ON SCHEMA public TO postgres;
GRANT ALL ON SCHEMA public TO PUBLIC;


-- Completed on 2015-02-01 16:47:43

--
-- PostgreSQL database dump complete
--

