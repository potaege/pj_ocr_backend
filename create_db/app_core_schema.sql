--
-- PostgreSQL database dump
--

\restrict zTemoQW0jlolmLhpEzcBBYfrUGyC9oMIRNKdLeq4YDwigouGZDE0zKWp4JstKTR

-- Dumped from database version 18.1
-- Dumped by pg_dump version 18.1

-- Started on 2026-01-29 00:45:17

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET transaction_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- TOC entry 221 (class 1259 OID 19122)
-- Name: thai_id; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.thai_id (
    user_id integer NOT NULL,
    citizen_id character(13) NOT NULL,
    prefix_name_th character varying(10) NOT NULL,
    first_name_th character varying(50) NOT NULL,
    last_name_th character varying(50) NOT NULL,
    prefix_name_eng character varying(10) NOT NULL,
    first_name_en character varying(50) NOT NULL,
    last_name_en character varying(50) NOT NULL,
    birthday date NOT NULL,
    religion character varying(50) NOT NULL,
    address_rest text NOT NULL,
    sub_district_th text NOT NULL,
    district_th text NOT NULL,
    province_th text NOT NULL,
    issue_date date NOT NULL,
    expiry_date date NOT NULL,
    created_at timestamp without time zone DEFAULT CURRENT_TIMESTAMP,
    updated_at timestamp without time zone DEFAULT CURRENT_TIMESTAMP
);


ALTER TABLE public.thai_id OWNER TO postgres;

--
-- TOC entry 220 (class 1259 OID 19072)
-- Name: users; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.users (
    user_id integer NOT NULL,
    username character varying(25) NOT NULL,
    password character varying(255) NOT NULL,
    email character varying(50) NOT NULL,
    name character varying(50) NOT NULL,
    surname character varying(50) NOT NULL,
    created_at timestamp without time zone DEFAULT CURRENT_TIMESTAMP NOT NULL,
    updated_at timestamp without time zone DEFAULT CURRENT_TIMESTAMP NOT NULL
);


ALTER TABLE public.users OWNER TO postgres;

--
-- TOC entry 219 (class 1259 OID 19071)
-- Name: users_user_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.users_user_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.users_user_id_seq OWNER TO postgres;

--
-- TOC entry 4923 (class 0 OID 0)
-- Dependencies: 219
-- Name: users_user_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.users_user_id_seq OWNED BY public.users.user_id;


--
-- TOC entry 4759 (class 2604 OID 19075)
-- Name: users user_id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.users ALTER COLUMN user_id SET DEFAULT nextval('public.users_user_id_seq'::regclass);


--
-- TOC entry 4767 (class 2606 OID 19146)
-- Name: thai_id pk_thai_id; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.thai_id
    ADD CONSTRAINT pk_thai_id PRIMARY KEY (user_id);


--
-- TOC entry 4769 (class 2606 OID 19148)
-- Name: thai_id uq_citizen_id; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.thai_id
    ADD CONSTRAINT uq_citizen_id UNIQUE (citizen_id);


--
-- TOC entry 4765 (class 2606 OID 19087)
-- Name: users users_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_pkey PRIMARY KEY (user_id);


--
-- TOC entry 4770 (class 2606 OID 19149)
-- Name: thai_id fk_thai_id_user; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.thai_id
    ADD CONSTRAINT fk_thai_id_user FOREIGN KEY (user_id) REFERENCES public.users(user_id) ON DELETE CASCADE;


-- Completed on 2026-01-29 00:45:18

--
-- PostgreSQL database dump complete
--

\unrestrict zTemoQW0jlolmLhpEzcBBYfrUGyC9oMIRNKdLeq4YDwigouGZDE0zKWp4JstKTR

