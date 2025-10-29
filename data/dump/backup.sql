--
-- PostgreSQL database dump
--

\restrict 6mXbytnWTCtyNvDx27EVrUIzdveCf72p3ltftASV7LVgoGORYnscaNdqXmuglw9

-- Dumped from database version 16.10 (Debian 16.10-1.pgdg13+1)
-- Dumped by pg_dump version 16.10 (Debian 16.10-1.pgdg13+1)

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

--
-- Name: cardstatus; Type: TYPE; Schema: public; Owner: admin
--

CREATE TYPE public.cardstatus AS ENUM (
    'a_fazer',
    'em_andamento',
    'validacao',
    'concluido'
);


ALTER TYPE public.cardstatus OWNER TO admin;

SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- Name: alembic_version; Type: TABLE; Schema: public; Owner: admin
--

CREATE TABLE public.alembic_version (
    version_num character varying(32) NOT NULL
);


ALTER TABLE public.alembic_version OWNER TO admin;

--
-- Name: artefato; Type: TABLE; Schema: public; Owner: admin
--

CREATE TABLE public.artefato (
    id uuid DEFAULT gen_random_uuid() NOT NULL,
    nome character varying NOT NULL,
    created_at timestamp with time zone DEFAULT now() NOT NULL,
    updated_at timestamp with time zone DEFAULT now() NOT NULL
);


ALTER TABLE public.artefato OWNER TO admin;

--
-- Name: card; Type: TABLE; Schema: public; Owner: admin
--

CREATE TABLE public.card (
    id uuid DEFAULT gen_random_uuid() NOT NULL,
    status public.cardstatus NOT NULL,
    tempo_planejado_horas double precision NOT NULL,
    link character varying,
    descricao text,
    ciclo_id uuid NOT NULL,
    fase_id uuid NOT NULL,
    artefato_id uuid NOT NULL,
    responsavel_id uuid NOT NULL,
    created_at timestamp with time zone DEFAULT now() NOT NULL,
    updated_at timestamp with time zone DEFAULT now() NOT NULL
);


ALTER TABLE public.card OWNER TO admin;

--
-- Name: ciclo; Type: TABLE; Schema: public; Owner: admin
--

CREATE TABLE public.ciclo (
    id uuid DEFAULT gen_random_uuid() NOT NULL,
    nome character varying NOT NULL,
    versao character varying NOT NULL,
    projeto_id uuid NOT NULL,
    created_at timestamp with time zone DEFAULT now() NOT NULL,
    updated_at timestamp with time zone DEFAULT now() NOT NULL
);


ALTER TABLE public.ciclo OWNER TO admin;

--
-- Name: fase; Type: TABLE; Schema: public; Owner: admin
--

CREATE TABLE public.fase (
    id uuid DEFAULT gen_random_uuid() NOT NULL,
    nome character varying NOT NULL,
    descritivo text,
    ordem integer NOT NULL,
    created_at timestamp with time zone DEFAULT now() NOT NULL,
    updated_at timestamp with time zone DEFAULT now() NOT NULL
);


ALTER TABLE public.fase OWNER TO admin;

--
-- Name: faseartefato; Type: TABLE; Schema: public; Owner: admin
--

CREATE TABLE public.faseartefato (
    fase_id uuid NOT NULL,
    artefato_id uuid NOT NULL,
    created_at timestamp with time zone DEFAULT now() NOT NULL
);


ALTER TABLE public.faseartefato OWNER TO admin;

--
-- Name: projeto; Type: TABLE; Schema: public; Owner: admin
--

CREATE TABLE public.projeto (
    id uuid DEFAULT gen_random_uuid() NOT NULL,
    nome character varying NOT NULL,
    descritivo text,
    created_at timestamp with time zone DEFAULT now() NOT NULL,
    updated_at timestamp with time zone DEFAULT now() NOT NULL
);


ALTER TABLE public.projeto OWNER TO admin;

--
-- Name: projetousuario; Type: TABLE; Schema: public; Owner: admin
--

CREATE TABLE public.projetousuario (
    projeto_id uuid NOT NULL,
    usuario_id uuid NOT NULL,
    created_at timestamp with time zone DEFAULT now() NOT NULL
);


ALTER TABLE public.projetousuario OWNER TO admin;

--
-- Name: usuario; Type: TABLE; Schema: public; Owner: admin
--

CREATE TABLE public.usuario (
    id uuid DEFAULT gen_random_uuid() NOT NULL,
    nome character varying NOT NULL,
    email character varying NOT NULL,
    senha character varying NOT NULL,
    created_at timestamp with time zone DEFAULT now() NOT NULL,
    updated_at timestamp with time zone DEFAULT now() NOT NULL
);


ALTER TABLE public.usuario OWNER TO admin;

--
-- Data for Name: alembic_version; Type: TABLE DATA; Schema: public; Owner: admin
--

COPY public.alembic_version (version_num) FROM stdin;
2948efb88529
teste
version_num_1
version_num_2
version_num_3
version_num_4
version_num_5
\.


--
-- Data for Name: artefato; Type: TABLE DATA; Schema: public; Owner: admin
--

COPY public.artefato (id, nome, created_at, updated_at) FROM stdin;
892184fa-b32e-47c7-ae46-8b34db24e234	nome_1	2025-10-29 16:00:28+00	2025-10-29 16:00:28+00
15cde74e-c9fc-4e27-b647-fd4bd6c07b08	nome_2	2025-10-29 16:00:28+00	2025-10-29 16:00:28+00
13e79331-7b32-4c00-a5f7-07bfbd506640	nome_3	2025-10-29 16:00:28+00	2025-10-29 16:00:28+00
aa74f843-e7a8-4ae5-8026-f73fd00083f4	nome_4	2025-10-29 16:00:28+00	2025-10-29 16:00:28+00
edefabb6-ae16-41e8-9446-1bf47e751a66	nome_5	2025-10-29 16:00:28+00	2025-10-29 16:00:28+00
\.


--
-- Data for Name: card; Type: TABLE DATA; Schema: public; Owner: admin
--

COPY public.card (id, status, tempo_planejado_horas, link, descricao, ciclo_id, fase_id, artefato_id, responsavel_id, created_at, updated_at) FROM stdin;
85829601-31f7-439d-9cc8-81f6bf8f034d	a_fazer	1.64	link_1	card_descricao_1	3460831c-3699-4c9e-baf1-205407bb8438	c39db310-ef5c-4ecb-a0ba-03786de2988a	1a35aa44-3370-411a-a8d4-81231b2ad93d	86b5573c-a4f2-4cc2-a5db-38255c0814dd	2025-10-29 16:00:28+00	2025-10-29 16:00:28+00
99e53759-0acf-4dad-813b-5c247f8ed4a2	em_andamento	3.17	link_2	card_descricao_2	8984a4ed-f401-4d77-9e0d-43bbdb7d174f	627beaf8-e41b-402c-8023-12a98266764d	771b254c-baea-4dae-8e28-20a6a00a9c53	3b05da01-dd1c-4d02-a095-07cb60c1dd20	2025-10-29 16:00:28+00	2025-10-29 16:00:28+00
23a4aa50-d9aa-4b62-a270-ef027f37d175	validacao	4.25	link_3	card_descricao_3	33e5dfc4-b781-4f6b-93a1-f83a3e6550ee	ea471d14-686f-4759-8c5e-4f4e732c983c	46f7b45d-16eb-4d7f-91c9-05a34395a3a4	e27a1744-ad2c-4a2c-afe6-0bdf2523e083	2025-10-29 16:00:28+00	2025-10-29 16:00:28+00
6c4c32b4-49e4-4f37-94bb-1e39df44e330	concluido	5.98	link_4	card_descricao_4	c6b5cbbf-f09b-44ab-86ee-8afaba541896	46c7e807-07a2-46ac-9239-b5a5df84aa24	0c937277-d8f9-4165-ab36-8812e7600ed8	88bff843-ecfb-48d1-9a19-b511ae580ce7	2025-10-29 16:00:28+00	2025-10-29 16:00:28+00
a3e8ef87-9c5b-44aa-a0bb-a0bfe3ac2c3a	a_fazer	6.82	link_5	card_descricao_5	db19835c-9905-4702-bb2b-81f2f8566c0c	f5a3fda5-52b6-45a3-b4ca-0067eec9a1bb	03d33415-11b3-489c-98e6-4b478805f689	1a6ca1a7-2ef1-46f3-9bff-d92ad4a83c42	2025-10-29 16:00:28+00	2025-10-29 16:00:28+00
\.


--
-- Data for Name: ciclo; Type: TABLE DATA; Schema: public; Owner: admin
--

COPY public.ciclo (id, nome, versao, projeto_id, created_at, updated_at) FROM stdin;
a8812e0d-bcf2-4f7a-99f3-76368f5a2522	nome_1	versao_1	856ea309-3f98-4e90-853a-44a53540c650	2025-10-29 16:00:28+00	2025-10-29 16:00:28+00
13fc5f18-0466-40c3-84cc-a5c6f5b7da62	nome_2	versao_2	700b387c-c59b-40a7-9eb2-8536e6249169	2025-10-29 16:00:28+00	2025-10-29 16:00:28+00
e5eeafc9-ab69-4471-979d-d58a3927d115	nome_3	versao_3	75c750fd-3f65-4f77-8b60-0433091b3742	2025-10-29 16:00:28+00	2025-10-29 16:00:28+00
4908d0e0-94b6-4992-b18a-41a1c61b3fe4	nome_4	versao_4	8fadf239-98e1-4873-9106-78ac92c0e860	2025-10-29 16:00:28+00	2025-10-29 16:00:28+00
01c7a16b-16d4-47a0-810c-26a1fcbb1cb3	nome_5	versao_5	540996cb-7988-41b5-9b76-57b1c913b698	2025-10-29 16:00:28+00	2025-10-29 16:00:28+00
\.


--
-- Data for Name: fase; Type: TABLE DATA; Schema: public; Owner: admin
--

COPY public.fase (id, nome, descritivo, ordem, created_at, updated_at) FROM stdin;
16462638-1fa0-45c9-9b9e-2879c1f5b5a6	nome_1	descritivo_1	1	2025-10-29 16:00:28+00	2025-10-29 16:00:28+00
2f36bbd1-bb5a-48e4-8c00-1ca0a5f1c6a7	nome_2	descritivo_2	2	2025-10-29 16:00:28+00	2025-10-29 16:00:28+00
8f84e4e8-b555-4a34-ab07-39f72dafb20d	nome_3	descritivo_3	3	2025-10-29 16:00:28+00	2025-10-29 16:00:28+00
f9fa48e3-20aa-41da-9baf-c357cddfbed7	nome_4	descritivo_4	4	2025-10-29 16:00:28+00	2025-10-29 16:00:28+00
b8be9547-16e4-4e55-9a9b-7c736b114cc7	nome_5	descritivo_5	5	2025-10-29 16:00:28+00	2025-10-29 16:00:28+00
\.


--
-- Data for Name: faseartefato; Type: TABLE DATA; Schema: public; Owner: admin
--

COPY public.faseartefato (fase_id, artefato_id, created_at) FROM stdin;
ff87a284-3b32-4a1b-9bda-d88d31d78dca	c380522c-9789-4257-b291-cde5b4ceeb80	2025-10-29 16:00:28+00
03a69e1d-b8d4-4cfd-941d-94377790e216	4a6bc0ad-a96b-4ad5-baff-9a293d3fe6e3	2025-10-29 16:00:28+00
f4680ea6-9672-4ee8-829b-99057841f17d	7ebe601a-c13b-4a0e-8a09-776aabbfb4e0	2025-10-29 16:00:28+00
c050d33c-e75d-448a-aebd-5cd0f1fe1206	d6b33c5d-6f67-4f69-b977-28951a6f693f	2025-10-29 16:00:28+00
7ffe29f2-41d6-4ad2-996e-d8b79f16af81	d3b8c5f5-3941-4dec-91ee-6e3163081333	2025-10-29 16:00:28+00
\.


--
-- Data for Name: projeto; Type: TABLE DATA; Schema: public; Owner: admin
--

COPY public.projeto (id, nome, descritivo, created_at, updated_at) FROM stdin;
bbe075bc-e6f4-48a3-b970-b1604d82f47b	nome_1	descritivo_1	2025-10-29 16:00:28+00	2025-10-29 16:00:28+00
f86a4f58-bd8a-4ea2-b9b8-f3bf9d0ff647	nome_2	descritivo_2	2025-10-29 16:00:28+00	2025-10-29 16:00:28+00
319cc887-ef2a-472c-959e-1fc558a08959	nome_3	descritivo_3	2025-10-29 16:00:28+00	2025-10-29 16:00:28+00
307be86b-1b78-4cbd-8fa3-49d9a864800c	nome_4	descritivo_4	2025-10-29 16:00:28+00	2025-10-29 16:00:28+00
30fb8e9f-952c-41ff-93f6-82716be19d4c	nome_5	descritivo_5	2025-10-29 16:00:28+00	2025-10-29 16:00:28+00
\.


--
-- Data for Name: projetousuario; Type: TABLE DATA; Schema: public; Owner: admin
--

COPY public.projetousuario (projeto_id, usuario_id, created_at) FROM stdin;
da8ec701-8bb3-4dea-847d-180a3a1c0de8	5c258b02-e54a-4201-be48-55883dd93cb4	2025-10-29 16:00:28+00
f25f194c-3d63-4c64-b833-65a24ec84bd6	802cdfd4-161a-492e-a523-676d35e4b838	2025-10-29 16:00:28+00
1c66a7d4-18ab-48ec-a224-3ab76d693281	0c01460f-bead-4b34-adad-115374c9ebb1	2025-10-29 16:00:28+00
75428ad7-651c-4f16-ad94-b72d53418f26	c1c4d886-a58e-43ad-a126-c8295e5f8877	2025-10-29 16:00:28+00
62124035-4b9f-4aaa-9ac3-3686b7e23198	0eeedde0-3220-4cd6-99fc-450a827f1c4a	2025-10-29 16:00:28+00
\.


--
-- Data for Name: usuario; Type: TABLE DATA; Schema: public; Owner: admin
--

COPY public.usuario (id, nome, email, senha, created_at, updated_at) FROM stdin;
c05b195b-ee6f-4b70-b016-0f5c3210ff63	nome_1	email1@example.com	senha_1	2025-10-29 16:00:28+00	2025-10-29 16:00:28+00
0823d2f1-088d-4783-a9f6-1d8792161abf	nome_2	email2@example.com	senha_2	2025-10-29 16:00:28+00	2025-10-29 16:00:28+00
c5571f34-f6eb-44a7-a272-2ab0c98f2d46	nome_3	email3@example.com	senha_3	2025-10-29 16:00:28+00	2025-10-29 16:00:28+00
d00897b6-d80a-4bb3-8e70-063266948890	nome_4	email4@example.com	senha_4	2025-10-29 16:00:28+00	2025-10-29 16:00:28+00
a3b02d10-2903-46cd-842f-a8f702dcd466	nome_5	email5@example.com	senha_5	2025-10-29 16:00:28+00	2025-10-29 16:00:28+00
\.


--
-- Name: alembic_version alembic_version_pkc; Type: CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.alembic_version
    ADD CONSTRAINT alembic_version_pkc PRIMARY KEY (version_num);


--
-- Name: artefato artefato_pkey; Type: CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.artefato
    ADD CONSTRAINT artefato_pkey PRIMARY KEY (id);


--
-- Name: card card_pkey; Type: CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.card
    ADD CONSTRAINT card_pkey PRIMARY KEY (id);


--
-- Name: ciclo ciclo_pkey; Type: CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.ciclo
    ADD CONSTRAINT ciclo_pkey PRIMARY KEY (id);


--
-- Name: fase fase_pkey; Type: CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.fase
    ADD CONSTRAINT fase_pkey PRIMARY KEY (id);


--
-- Name: faseartefato faseartefato_pkey; Type: CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.faseartefato
    ADD CONSTRAINT faseartefato_pkey PRIMARY KEY (fase_id, artefato_id);


--
-- Name: projeto projeto_pkey; Type: CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.projeto
    ADD CONSTRAINT projeto_pkey PRIMARY KEY (id);


--
-- Name: projetousuario projetousuario_pkey; Type: CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.projetousuario
    ADD CONSTRAINT projetousuario_pkey PRIMARY KEY (projeto_id, usuario_id);


--
-- Name: usuario usuario_pkey; Type: CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.usuario
    ADD CONSTRAINT usuario_pkey PRIMARY KEY (id);


--
-- Name: ix_artefato_nome; Type: INDEX; Schema: public; Owner: admin
--

CREATE INDEX ix_artefato_nome ON public.artefato USING btree (nome);


--
-- Name: ix_card_status; Type: INDEX; Schema: public; Owner: admin
--

CREATE INDEX ix_card_status ON public.card USING btree (status);


--
-- Name: ix_ciclo_nome; Type: INDEX; Schema: public; Owner: admin
--

CREATE INDEX ix_ciclo_nome ON public.ciclo USING btree (nome);


--
-- Name: ix_fase_nome; Type: INDEX; Schema: public; Owner: admin
--

CREATE INDEX ix_fase_nome ON public.fase USING btree (nome);


--
-- Name: ix_projeto_nome; Type: INDEX; Schema: public; Owner: admin
--

CREATE INDEX ix_projeto_nome ON public.projeto USING btree (nome);


--
-- Name: ix_usuario_email; Type: INDEX; Schema: public; Owner: admin
--

CREATE UNIQUE INDEX ix_usuario_email ON public.usuario USING btree (email);


--
-- Name: ix_usuario_nome; Type: INDEX; Schema: public; Owner: admin
--

CREATE INDEX ix_usuario_nome ON public.usuario USING btree (nome);


--
-- PostgreSQL database dump complete
--

\unrestrict 6mXbytnWTCtyNvDx27EVrUIzdveCf72p3ltftASV7LVgoGORYnscaNdqXmuglw9

