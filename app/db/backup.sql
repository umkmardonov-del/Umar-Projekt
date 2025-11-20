--
-- PostgreSQL database dump
--

\restrict BUNxYGYYI6jj6cSDlyciyXmjC53PBORGgIFPHM08BHe9Q39TFtVHdNOykhAOakf

-- Dumped from database version 18.0
-- Dumped by pg_dump version 18.0

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

--
-- Name: tier; Type: TYPE; Schema: public; Owner: postgres
--

CREATE TYPE public.tier AS ENUM (
    'basic',
    'premium',
    'ultra'
);


ALTER TYPE public.tier OWNER TO postgres;

--
-- Name: usage_mode; Type: TYPE; Schema: public; Owner: postgres
--

CREATE TYPE public.usage_mode AS ENUM (
    'mobile',
    'stationary'
);


ALTER TYPE public.usage_mode OWNER TO postgres;

SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- Name: alembic_version; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.alembic_version (
    version_num character varying(32) NOT NULL
);


ALTER TABLE public.alembic_version OWNER TO postgres;

--
-- Name: cables; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.cables (
    id uuid NOT NULL,
    hdmi character varying(80) NOT NULL,
    ethernet character varying(80) NOT NULL,
    usb_c character varying(80) NOT NULL,
    display_port character varying(80) NOT NULL
);


ALTER TABLE public.cables OWNER TO postgres;

--
-- Name: chairs; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.chairs (
    id uuid NOT NULL,
    height_max integer NOT NULL,
    height_min integer NOT NULL,
    max_weight integer NOT NULL,
    description character varying(200) NOT NULL
);


ALTER TABLE public.chairs OWNER TO postgres;

--
-- Name: departments; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.departments (
    id uuid NOT NULL,
    name character varying(100) NOT NULL
);


ALTER TABLE public.departments OWNER TO postgres;

--
-- Name: desks; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.desks (
    id uuid NOT NULL,
    height_adjustable boolean NOT NULL,
    dimensions character varying(20) NOT NULL,
    description character varying(200) NOT NULL
);


ALTER TABLE public.desks OWNER TO postgres;

--
-- Name: docking_stations; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.docking_stations (
    id uuid NOT NULL,
    display_port integer NOT NULL,
    hdmi integer NOT NULL,
    usb character varying(80) NOT NULL,
    usb_c integer NOT NULL,
    thunderbolt integer NOT NULL,
    ethernet integer NOT NULL,
    audio integer NOT NULL,
    power_usage numeric(6,3) NOT NULL
);


ALTER TABLE public.docking_stations OWNER TO postgres;

--
-- Name: keyboards; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.keyboards (
    id uuid NOT NULL,
    connection_style character varying(50) NOT NULL,
    layout character varying(100) NOT NULL,
    weight integer NOT NULL,
    dimensions character varying(20) NOT NULL,
    description character varying(200) NOT NULL
);


ALTER TABLE public.keyboards OWNER TO postgres;

--
-- Name: laptops; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.laptops (
    id uuid NOT NULL,
    processor character varying(50) NOT NULL,
    operating_system character varying(50) NOT NULL,
    memory character varying(50) NOT NULL,
    disc_memory character varying(50) NOT NULL,
    screen_size integer NOT NULL,
    resolution_height integer NOT NULL,
    resolution_width integer NOT NULL,
    refresh_rate integer NOT NULL,
    graphics_card character varying(100) NOT NULL,
    camera character varying(100) NOT NULL,
    power_usage numeric(6,3) NOT NULL
);


ALTER TABLE public.laptops OWNER TO postgres;

--
-- Name: monitors; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.monitors (
    id uuid NOT NULL,
    resolution_height integer NOT NULL,
    resolution_width integer NOT NULL,
    latency integer NOT NULL,
    refresh_rate integer NOT NULL,
    power_usage numeric(6,3) NOT NULL,
    screen_size integer NOT NULL,
    connectors character varying(200) NOT NULL
);


ALTER TABLE public.monitors OWNER TO postgres;

--
-- Name: mouses; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.mouses (
    id uuid NOT NULL,
    dpi integer NOT NULL,
    connection_style character varying(50) NOT NULL,
    weight integer NOT NULL,
    battery character varying(50) NOT NULL,
    description character varying(200) NOT NULL
);


ALTER TABLE public.mouses OWNER TO postgres;

--
-- Name: package_items; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.package_items (
    id uuid NOT NULL,
    package_id uuid NOT NULL,
    product_id uuid NOT NULL,
    quantity integer NOT NULL,
    CONSTRAINT ck_package_items_quantity_positive CHECK ((quantity > 0))
);


ALTER TABLE public.package_items OWNER TO postgres;

--
-- Name: packages; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.packages (
    id uuid NOT NULL,
    department_id uuid NOT NULL,
    tier public.tier NOT NULL,
    usage_mode public.usage_mode NOT NULL
);


ALTER TABLE public.packages OWNER TO postgres;

--
-- Name: products; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.products (
    id uuid NOT NULL,
    name character varying(200) NOT NULL,
    price numeric(7,2) NOT NULL,
    product_type character varying(50) NOT NULL
);


ALTER TABLE public.products OWNER TO postgres;

--
-- Name: webcams; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.webcams (
    id uuid NOT NULL,
    fps integer NOT NULL,
    resolution character varying(30) NOT NULL,
    dfov_adjustable boolean NOT NULL,
    connection_style character varying(50) NOT NULL,
    description character varying(200) NOT NULL
);


ALTER TABLE public.webcams OWNER TO postgres;

--
-- Name: workstations; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.workstations (
    id uuid NOT NULL,
    processor character varying(50) NOT NULL,
    operating_system character varying(50) NOT NULL,
    memory character varying(50) NOT NULL,
    power_usage numeric(6,3) NOT NULL,
    disc_memory character varying(50) NOT NULL,
    screen_size numeric(6,3) NOT NULL,
    resolution_height integer NOT NULL,
    resolution_width integer NOT NULL,
    refresh_rate integer NOT NULL,
    graphics_card character varying(100) NOT NULL,
    camera character varying(100) NOT NULL
);


ALTER TABLE public.workstations OWNER TO postgres;

--
-- Data for Name: alembic_version; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.alembic_version (version_num) FROM stdin;
f13c49f9b61f
\.


--
-- Data for Name: cables; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.cables (id, hdmi, ethernet, usb_c, display_port) FROM stdin;
cd27224f-3934-4b7f-a721-7b5a68b76544	HDMI: valonic HDMI Kabel kurz 20 cm	Patchkabel Cat.7 LAN Kabel RJ45 Cat.6a Stecker orange 1 m	Callstel USB‑C Kurz‑Kabel (2er‑Set)	Hama DisplayPort‑Kabel 00200929
337398d7-fc7e-4ab6-93ec-2dd3f1755e35	SpeaKa Professional HDMI Anschlusskabel HDMI-A Stecker	Schwaiger CAT6 Netzwerkkabel	Ugreen USB‑C auf USB‑C	ISY IDP‑3020 DisplayPort‑Kabel
09949847-54d3-4187-b186-4f3ba7662b5f	Oehlbach Flex Evolution 8K HDMI	Cable Matters Snagless 10 Gigabit CAT6 Kurz	Hama USB‑C‑Kabel	Cable Matters Aktives DisplayPort 1.4 Kabel
\.


--
-- Data for Name: chairs; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.chairs (id, height_max, height_min, max_weight, description) FROM stdin;
70a32933-9c5f-4c86-8752-b96da53c89b2	140	129	110	string
361807b0-308b-4856-9e41-e86b8fb725ca	124	107	136	string
a6939d8b-9bde-4cc6-bccc-9858fce44f9c	115	107	136	string
\.


--
-- Data for Name: departments; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.departments (id, name) FROM stdin;
feafc6f0-d0fc-42b6-b137-67d0e7b262bd	IT
09baca34-fa9b-4c7c-a172-e66584bfc0f4	Corporate
a689b5b1-22af-422f-ad72-7f468e637c7e	Finance
04bf7ca3-7163-443e-bb72-c1c8907950d0	Marketing
dbf5fe69-3316-43ab-b97e-eacd1d7a24bf	HR
\.


--
-- Data for Name: desks; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.desks (id, height_adjustable, dimensions, description) FROM stdin;
1920f61c-324f-4394-90ef-06824da53ca0	t	120x60	ausreichend für Büroarbeit
69feb6ce-46dd-416e-9609-143682f21433	t	120x60	bessere Mechanik und Belastbarkeit, mehr Spielraum
fc55a6ea-3a5a-45a3-b307-2f844147503b	t	160x80	hochwertige Materialien, gute Marke, langlebige Konstruktion
\.


--
-- Data for Name: docking_stations; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.docking_stations (id, display_port, hdmi, usb, usb_c, thunderbolt, ethernet, audio, power_usage) FROM stdin;
1f6b7678-7187-42c8-9519-2cf883ce82bd	2	1	3x USB 3.2 Gen, 2x USB 2.0	1	0	1	1	5.000
8f9207ab-78a0-488c-8642-49e3fa711f1c	2	1	4x USB 3.2 Gen, 1x USB4	2	0	1	1	6.000
e768f283-f448-4a3c-8369-410c98876344	2	1	3x USB 3.2 Gen 2	2	2	1	1	9.000
\.


--
-- Data for Name: keyboards; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.keyboards (id, connection_style, layout, weight, dimensions, description) FROM stdin;
dcc784ed-bb4c-4b8c-a745-9e41433284df	USB-A	2,5 Zonen Layout mit Ziffernblock	570	425x145x20mm	Neigung einstellbar, Lebenszyklus 10 Millionen Klicks
c9263a73-7622-4e03-b8f2-c489f86e25a2	kabellos mit dongle + bluetooth	standard	586	437x129x15mm	integrierter, wiederaufladbarer Akku, 3 Monate Akkulaufzeit, Neigung einstellbar, Lebenszyklus 10 Millionen Klicks
8cb86222-596e-4cea-82cc-47c560a11352	Bluetooth/USB	ergonomisch geteiltes Split-Design	296	288x137x9mm	integrierte Software, LED-Pausenanzeige, ultradünn, Magnetverbindung
\.


--
-- Data for Name: laptops; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.laptops (id, processor, operating_system, memory, disc_memory, screen_size, resolution_height, resolution_width, refresh_rate, graphics_card, camera, power_usage) FROM stdin;
7b1d1dfc-37d3-47f0-b674-537bf6251e53	Intel Core Ultra 7 255U Prozessor, bis zu 5,20 GHz	 Windows 11 Home 64	32 GB DDR5-5600MT/s - 2x 16GB	1 TB SSD M.2 2280 PCIe 4.0 TLC Opal	16	1200	1920	60	Integrierte Grafikkarte	5MP-RGB- und Infrarotkamera mit Mikrofon und Abdeckung	49.000
d86dd0b6-3c43-405e-b282-8583d0897518	AMD Ryzen™ 3 210 Prozessor	Windows 11 Home 64	8 GB DDR5-5600MT/s (SODIMM)	256 GB SSD M.2 2242 PCIe 4.0 TLC Opa	14	1200	1920	60	Integrierte Grafik	720p-HD-RGB-Kamera	30.000
00e94756-1231-44aa-9d3e-665a4b26aadd	AMD Ryzen™ 5 PRO 754OU Prozessor 3,20-4,90 GHz	 Windows 11 Home 64	16 GB LPDDR5X-6400MT/s	512 GB SSD M.2 2280 PCIe 4.0	14	1200	1920	60	Integrierte Grafikkarte	5MP-RGB- und Infrarotkamera mit Mikrofon und Abdeckung	35.000
\.


--
-- Data for Name: monitors; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.monitors (id, resolution_height, resolution_width, latency, refresh_rate, power_usage, screen_size, connectors) FROM stdin;
d48b8232-8a89-42a7-b8c2-66f5913839e2	1920	1200	7	60	12.400	24	HDMI, DisplayPort, 2x VGA, 2x 3.0 USB
33335893-90a7-4da2-883c-7a363effa39e	2560	1440	6	120	15.000	27	HDMI, 2x DisplayPort, 1x USB-C, 3x 3.0 USB
a3d863e3-53ef-4a6d-987c-60067ce03357	3840	2160	6	120	18.000	27	HDMI, DisplayPort, USB-C, 3x 3.0 USB
992a6c56-2c83-47c5-b9a9-5a28932337e9	3840	2160	6	60	18.000	27	HDMI, DisplayPort, USB-C, 3x 3.0 USB
\.


--
-- Data for Name: mouses; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.mouses (id, dpi, connection_style, weight, battery, description) FROM stdin;
2a2ccc14-99a4-4806-8894-ca83045b0781	1200	USB-Dongle	55	Batterien	
bffb32eb-6498-433e-bc9f-9480a48ce462	2400	USB-C Dongle	55	Batterien	6 verschiedene Tasten
235cc53b-2afe-4f91-9659-21cf926e36bb	19000	Bluetooth/kabelgebundenen USB-C	73	Aufladbar über USB-C (70 Std. AKkulaufzeit	6 programmierbare Tasten
\.


--
-- Data for Name: package_items; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.package_items (id, package_id, product_id, quantity) FROM stdin;
eb2e05df-6d31-4b7a-b663-444bdd59c03c	c926bb27-b79b-454e-bf64-2a131729e57f	d86dd0b6-3c43-405e-b282-8583d0897518	1
2100fa72-1dbd-48b2-badb-5b5bf89a6d9a	c926bb27-b79b-454e-bf64-2a131729e57f	d48b8232-8a89-42a7-b8c2-66f5913839e2	1
bc72624b-c1f9-44c5-95e0-d2a67e6e72e5	c926bb27-b79b-454e-bf64-2a131729e57f	dcc784ed-bb4c-4b8c-a745-9e41433284df	1
a01ec8b3-a66c-4cdf-96ed-b8008c9a8d12	c926bb27-b79b-454e-bf64-2a131729e57f	2a2ccc14-99a4-4806-8894-ca83045b0781	1
f3368d79-a825-41b9-9873-b90981956d4c	c926bb27-b79b-454e-bf64-2a131729e57f	1920f61c-324f-4394-90ef-06824da53ca0	1
6cf55758-034d-4bdf-b627-0473a20f64b6	c926bb27-b79b-454e-bf64-2a131729e57f	70a32933-9c5f-4c86-8752-b96da53c89b2	1
55a9a788-f91a-41ac-a4c6-c5756cca4a7e	c926bb27-b79b-454e-bf64-2a131729e57f	cd27224f-3934-4b7f-a721-7b5a68b76544	1
a188fe3f-1134-4076-b6f1-06d4c55f0456	c926bb27-b79b-454e-bf64-2a131729e57f	1f6b7678-7187-42c8-9519-2cf883ce82bd	1
75966edb-6ba8-4224-883f-b926196bdf1f	d21814b5-cb1b-4b50-98b3-08b41ba06547	00e94756-1231-44aa-9d3e-665a4b26aadd	1
10e850bc-bc13-4c30-812b-93d849f3e1b6	d21814b5-cb1b-4b50-98b3-08b41ba06547	33335893-90a7-4da2-883c-7a363effa39e	1
716a120b-d8ee-42f1-9e30-0773eeb3d1ca	d21814b5-cb1b-4b50-98b3-08b41ba06547	c9263a73-7622-4e03-b8f2-c489f86e25a2	1
9b715f3e-753c-4339-9afd-bfa8f6cba267	d21814b5-cb1b-4b50-98b3-08b41ba06547	bffb32eb-6498-433e-bc9f-9480a48ce462	1
85c9bdb9-1333-4861-82ec-d4d533153a37	d21814b5-cb1b-4b50-98b3-08b41ba06547	69feb6ce-46dd-416e-9609-143682f21433	1
2df51e49-1fe7-4d8c-addf-2508a29a3ad7	d21814b5-cb1b-4b50-98b3-08b41ba06547	361807b0-308b-4856-9e41-e86b8fb725ca	1
c74cdd9c-dac7-4564-80e1-b6c7cdfe4cd6	d21814b5-cb1b-4b50-98b3-08b41ba06547	337398d7-fc7e-4ab6-93ec-2dd3f1755e35	1
c0fb91e0-d983-4235-ba04-a0287c933480	d21814b5-cb1b-4b50-98b3-08b41ba06547	be3923cb-a269-487e-bba7-e93f334bc4e2	1
93d9a313-9925-4bdc-80af-e15348f632b5	d21814b5-cb1b-4b50-98b3-08b41ba06547	8f9207ab-78a0-488c-8642-49e3fa711f1c	1
12e2e3d6-8c84-4c99-9a7f-76fbb1c7da75	e8451cd3-5af5-4d6a-b01e-ca9ace89c7b1	7b1d1dfc-37d3-47f0-b674-537bf6251e53	1
8fc4a309-c24c-4084-9d1e-5aa8fd2d32d9	e8451cd3-5af5-4d6a-b01e-ca9ace89c7b1	a3d863e3-53ef-4a6d-987c-60067ce03357	2
ae36d196-24e3-4638-ac6d-f7dd25b58c7c	e8451cd3-5af5-4d6a-b01e-ca9ace89c7b1	8cb86222-596e-4cea-82cc-47c560a11352	1
b16a40db-1689-4648-8d1e-988af3442666	e8451cd3-5af5-4d6a-b01e-ca9ace89c7b1	235cc53b-2afe-4f91-9659-21cf926e36bb	1
6c0a7d72-f18c-4221-a442-0f5285aedcad	e8451cd3-5af5-4d6a-b01e-ca9ace89c7b1	fc55a6ea-3a5a-45a3-b307-2f844147503b	1
70e4e6c6-f7de-44c2-bb6b-94842d62e638	e8451cd3-5af5-4d6a-b01e-ca9ace89c7b1	a6939d8b-9bde-4cc6-bccc-9858fce44f9c	1
44dc7b02-9e8f-4e3c-a31c-9b14bfa6f94e	e8451cd3-5af5-4d6a-b01e-ca9ace89c7b1	09949847-54d3-4187-b186-4f3ba7662b5f	1
7750b81d-89c7-41eb-b087-33564b1e7022	e8451cd3-5af5-4d6a-b01e-ca9ace89c7b1	9d308540-fe0a-4136-b380-32853b653754	1
c9c4c6a3-b788-41dc-8fc1-1cf67ec6077a	e8451cd3-5af5-4d6a-b01e-ca9ace89c7b1	e768f283-f448-4a3c-8369-410c98876344	1
98770734-ed4b-434c-a8d1-596a10b8b57c	2bad1b66-1a04-4343-a48f-a64ae191bf83	d86dd0b6-3c43-405e-b282-8583d0897518	1
44ca2b74-d1ee-49b7-ad21-6eaa22c58bdb	2bad1b66-1a04-4343-a48f-a64ae191bf83	d48b8232-8a89-42a7-b8c2-66f5913839e2	1
3db792f5-681a-4d47-964b-9b7d4c1f3bc6	2bad1b66-1a04-4343-a48f-a64ae191bf83	dcc784ed-bb4c-4b8c-a745-9e41433284df	1
bf59ba08-5798-4e2a-aec5-4dba1ac07d27	2bad1b66-1a04-4343-a48f-a64ae191bf83	2a2ccc14-99a4-4806-8894-ca83045b0781	1
e502631d-f3f7-4079-8aba-fcb0453d64f6	2bad1b66-1a04-4343-a48f-a64ae191bf83	1920f61c-324f-4394-90ef-06824da53ca0	1
64fb567f-ff2d-407e-99d6-a4d0bbf20bdb	2bad1b66-1a04-4343-a48f-a64ae191bf83	70a32933-9c5f-4c86-8752-b96da53c89b2	1
d0454fcf-d172-4be6-bf80-f0439d3a4dcf	2bad1b66-1a04-4343-a48f-a64ae191bf83	cd27224f-3934-4b7f-a721-7b5a68b76544	1
8ad0087b-bde5-4605-a2d9-3ed6a3fe888c	2bad1b66-1a04-4343-a48f-a64ae191bf83	1f6b7678-7187-42c8-9519-2cf883ce82bd	1
09e5ee94-1461-454a-a5e5-6a59d72d62fc	71bf2a64-5bf2-4cf5-95d8-78f169dbb655	00e94756-1231-44aa-9d3e-665a4b26aadd	1
820d22a0-57e0-4990-9187-e41e24811076	71bf2a64-5bf2-4cf5-95d8-78f169dbb655	33335893-90a7-4da2-883c-7a363effa39e	1
cf319268-7f0d-4575-a8c4-c3f9a7f27edb	71bf2a64-5bf2-4cf5-95d8-78f169dbb655	c9263a73-7622-4e03-b8f2-c489f86e25a2	1
4981c7a1-b5f1-47ad-89de-670f9e87207b	71bf2a64-5bf2-4cf5-95d8-78f169dbb655	bffb32eb-6498-433e-bc9f-9480a48ce462	1
5b5f95fe-93e5-4465-9304-fffc531812d5	71bf2a64-5bf2-4cf5-95d8-78f169dbb655	69feb6ce-46dd-416e-9609-143682f21433	1
8f568f55-aa8c-4fd4-910e-c090f9c083e1	71bf2a64-5bf2-4cf5-95d8-78f169dbb655	361807b0-308b-4856-9e41-e86b8fb725ca	1
785eafe1-d71e-4c58-89dc-587eae76569d	71bf2a64-5bf2-4cf5-95d8-78f169dbb655	337398d7-fc7e-4ab6-93ec-2dd3f1755e35	1
86cef6a2-4520-4db7-aa23-11cf32236e7c	71bf2a64-5bf2-4cf5-95d8-78f169dbb655	be3923cb-a269-487e-bba7-e93f334bc4e2	1
cc45f3fa-f1ee-4f6e-9fcf-7bc8ee498a7c	71bf2a64-5bf2-4cf5-95d8-78f169dbb655	8f9207ab-78a0-488c-8642-49e3fa711f1c	1
63de6f18-c0fb-4a57-b26a-1b16197255b9	9678a458-6f10-4648-b2db-76b0d98f2fb5	7b1d1dfc-37d3-47f0-b674-537bf6251e53	1
e40d3066-2975-4e48-a023-94fca475f348	9678a458-6f10-4648-b2db-76b0d98f2fb5	a3d863e3-53ef-4a6d-987c-60067ce03357	2
7848d2e3-1edc-40af-ab3a-299953540efa	9678a458-6f10-4648-b2db-76b0d98f2fb5	8cb86222-596e-4cea-82cc-47c560a11352	1
e38d8834-6244-497e-a93f-ca8349d84bc0	9678a458-6f10-4648-b2db-76b0d98f2fb5	235cc53b-2afe-4f91-9659-21cf926e36bb	1
6eeade3a-197f-4d58-adcb-d37fc9f4eae3	9678a458-6f10-4648-b2db-76b0d98f2fb5	fc55a6ea-3a5a-45a3-b307-2f844147503b	1
68a91cc9-226b-494c-8bb7-3b2c52aa217b	9678a458-6f10-4648-b2db-76b0d98f2fb5	a6939d8b-9bde-4cc6-bccc-9858fce44f9c	1
39fa790b-b4a4-42a7-aed1-46da70aed25b	9678a458-6f10-4648-b2db-76b0d98f2fb5	09949847-54d3-4187-b186-4f3ba7662b5f	1
cc54ef20-6802-40e9-a145-a92c53e16936	9678a458-6f10-4648-b2db-76b0d98f2fb5	9d308540-fe0a-4136-b380-32853b653754	1
9a3de1fc-d531-4655-b2ab-65bcee7ba2d8	9678a458-6f10-4648-b2db-76b0d98f2fb5	e768f283-f448-4a3c-8369-410c98876344	1
ab3f8305-dbd3-4446-964e-d2660f9edc5b	ffd5f171-663f-4051-aa10-38c8882bd02b	d86dd0b6-3c43-405e-b282-8583d0897518	1
36d48b37-188b-4662-8621-0d7cee0cfaa8	ffd5f171-663f-4051-aa10-38c8882bd02b	d48b8232-8a89-42a7-b8c2-66f5913839e2	1
72b04476-f18c-4298-8a48-a08e4fb51de4	ffd5f171-663f-4051-aa10-38c8882bd02b	dcc784ed-bb4c-4b8c-a745-9e41433284df	1
a580422e-369f-4f71-a79f-a2884c9bce47	ffd5f171-663f-4051-aa10-38c8882bd02b	2a2ccc14-99a4-4806-8894-ca83045b0781	1
9db52a07-9326-4ad1-9b60-5b776b3d85c2	ffd5f171-663f-4051-aa10-38c8882bd02b	1920f61c-324f-4394-90ef-06824da53ca0	1
d38bef07-20bc-4ec4-b70f-7bf3b99dd56e	ffd5f171-663f-4051-aa10-38c8882bd02b	70a32933-9c5f-4c86-8752-b96da53c89b2	1
75ce425e-a6bd-4a49-a973-6ba2b104edc7	ffd5f171-663f-4051-aa10-38c8882bd02b	cd27224f-3934-4b7f-a721-7b5a68b76544	1
e56012e7-1b28-42b7-8166-9b7f65d4692f	ffd5f171-663f-4051-aa10-38c8882bd02b	1f6b7678-7187-42c8-9519-2cf883ce82bd	1
74d7f607-f24b-4be9-a9d7-8fd0c1d0b311	15a865a3-584d-4945-be54-e3fb2550d44d	00e94756-1231-44aa-9d3e-665a4b26aadd	1
47cbd455-db23-4987-ab78-920bcb4a2048	15a865a3-584d-4945-be54-e3fb2550d44d	33335893-90a7-4da2-883c-7a363effa39e	1
424e194a-6b5f-4a80-bffb-2f0e28ae62bc	15a865a3-584d-4945-be54-e3fb2550d44d	c9263a73-7622-4e03-b8f2-c489f86e25a2	1
75c77d60-5578-481a-97f5-b5316b06436c	15a865a3-584d-4945-be54-e3fb2550d44d	bffb32eb-6498-433e-bc9f-9480a48ce462	1
b0f2fe88-e225-4ad5-9dca-a099cdf27c75	15a865a3-584d-4945-be54-e3fb2550d44d	69feb6ce-46dd-416e-9609-143682f21433	1
ae0ed4f4-aa95-4e9b-8509-4e064eb9be48	15a865a3-584d-4945-be54-e3fb2550d44d	361807b0-308b-4856-9e41-e86b8fb725ca	1
9045a14c-7ef1-4f91-9ab5-2fb297059a7c	15a865a3-584d-4945-be54-e3fb2550d44d	337398d7-fc7e-4ab6-93ec-2dd3f1755e35	1
9807b6de-17c6-4d9a-a431-98d40a03850e	15a865a3-584d-4945-be54-e3fb2550d44d	be3923cb-a269-487e-bba7-e93f334bc4e2	1
34a0bee4-67fa-4416-821c-90f423cee36a	15a865a3-584d-4945-be54-e3fb2550d44d	8f9207ab-78a0-488c-8642-49e3fa711f1c	1
dccc72bf-7503-4316-8754-6792dfaf8d48	f1c0d97d-392e-4f04-835d-281b462205a9	7b1d1dfc-37d3-47f0-b674-537bf6251e53	1
df457c4f-2627-4846-bb3b-3ecd4f80f7c3	f1c0d97d-392e-4f04-835d-281b462205a9	a3d863e3-53ef-4a6d-987c-60067ce03357	2
eba54109-bf8f-4a36-9fa4-6bfae76e84ad	f1c0d97d-392e-4f04-835d-281b462205a9	8cb86222-596e-4cea-82cc-47c560a11352	1
e1bc853e-a7e8-47a9-9764-07ea9e6e9f33	f1c0d97d-392e-4f04-835d-281b462205a9	235cc53b-2afe-4f91-9659-21cf926e36bb	1
163232e0-51a9-4a3b-b264-afa1be1a1609	f1c0d97d-392e-4f04-835d-281b462205a9	fc55a6ea-3a5a-45a3-b307-2f844147503b	1
5b65b23f-7c17-4618-933c-53e5710eaced	f1c0d97d-392e-4f04-835d-281b462205a9	a6939d8b-9bde-4cc6-bccc-9858fce44f9c	1
3e2c88a5-ba60-4759-ba0e-06c8a9af1080	f1c0d97d-392e-4f04-835d-281b462205a9	09949847-54d3-4187-b186-4f3ba7662b5f	1
30b45b0c-a0c4-4b2c-90ae-b01dd97bc639	f1c0d97d-392e-4f04-835d-281b462205a9	9d308540-fe0a-4136-b380-32853b653754	1
46c69023-f130-4ffb-8648-982d28c2763f	f1c0d97d-392e-4f04-835d-281b462205a9	e768f283-f448-4a3c-8369-410c98876344	1
bba8a184-0a86-4f0b-8227-54dc11339a6f	25f37a6a-7bdb-46b0-ac6c-a277daffa974	d86dd0b6-3c43-405e-b282-8583d0897518	1
71f44cf8-402a-48ab-a271-96cbf74688af	25f37a6a-7bdb-46b0-ac6c-a277daffa974	d48b8232-8a89-42a7-b8c2-66f5913839e2	1
c7696582-68ae-4c2a-94cd-e747650b4bdf	25f37a6a-7bdb-46b0-ac6c-a277daffa974	dcc784ed-bb4c-4b8c-a745-9e41433284df	1
f033119d-6a2a-482f-a749-dba30ff07343	25f37a6a-7bdb-46b0-ac6c-a277daffa974	2a2ccc14-99a4-4806-8894-ca83045b0781	1
73b86981-1709-4dc6-ae73-84cc5db897b5	25f37a6a-7bdb-46b0-ac6c-a277daffa974	1920f61c-324f-4394-90ef-06824da53ca0	1
13d19cec-abf4-48b3-b5e1-e9f13bf25224	25f37a6a-7bdb-46b0-ac6c-a277daffa974	70a32933-9c5f-4c86-8752-b96da53c89b2	1
ef4c4bf9-3fc8-44ca-b311-b605b90ff7f7	25f37a6a-7bdb-46b0-ac6c-a277daffa974	cd27224f-3934-4b7f-a721-7b5a68b76544	1
ad7ecfe8-01d1-4796-b599-24720df6179c	25f37a6a-7bdb-46b0-ac6c-a277daffa974	1f6b7678-7187-42c8-9519-2cf883ce82bd	1
9f61df5b-51e9-4814-af0f-b110c7d5f6a2	423baa40-2c00-4c35-b55e-0d9cef62b452	00e94756-1231-44aa-9d3e-665a4b26aadd	1
bbb44a5c-e3ad-467d-b239-3ac264705502	423baa40-2c00-4c35-b55e-0d9cef62b452	33335893-90a7-4da2-883c-7a363effa39e	1
1e5e1193-fd0c-47b2-a753-d94f8d93bf95	423baa40-2c00-4c35-b55e-0d9cef62b452	c9263a73-7622-4e03-b8f2-c489f86e25a2	1
bb65615d-6312-430d-8043-3318f35babf5	423baa40-2c00-4c35-b55e-0d9cef62b452	bffb32eb-6498-433e-bc9f-9480a48ce462	1
a45bf36f-3c08-4675-8e75-78a9655e01be	423baa40-2c00-4c35-b55e-0d9cef62b452	69feb6ce-46dd-416e-9609-143682f21433	1
7543dced-8ccf-4f55-89c8-dee22da783a6	423baa40-2c00-4c35-b55e-0d9cef62b452	361807b0-308b-4856-9e41-e86b8fb725ca	1
819c60e4-9be0-4710-8120-9ac80b0266b2	423baa40-2c00-4c35-b55e-0d9cef62b452	337398d7-fc7e-4ab6-93ec-2dd3f1755e35	1
03a6bce0-42d4-4b66-b24d-27b8acf4e152	423baa40-2c00-4c35-b55e-0d9cef62b452	be3923cb-a269-487e-bba7-e93f334bc4e2	1
6a957719-f0d5-4536-bbee-2bc78912006b	423baa40-2c00-4c35-b55e-0d9cef62b452	8f9207ab-78a0-488c-8642-49e3fa711f1c	1
23e1dd9b-2a7a-43e1-86a6-0e966f18d2cb	f2188f63-c7a0-44d2-8d24-d699766b68cb	7b1d1dfc-37d3-47f0-b674-537bf6251e53	1
32842cf5-c44d-43ae-bb0e-41b7c7f82915	f2188f63-c7a0-44d2-8d24-d699766b68cb	a3d863e3-53ef-4a6d-987c-60067ce03357	2
c49397eb-ca0b-4bef-b1b7-6eeb6d08ac7d	f2188f63-c7a0-44d2-8d24-d699766b68cb	8cb86222-596e-4cea-82cc-47c560a11352	1
a17228bf-dbfe-4ff4-92c0-fbe3701ce3d4	f2188f63-c7a0-44d2-8d24-d699766b68cb	235cc53b-2afe-4f91-9659-21cf926e36bb	1
80093b1e-8dd6-4410-963c-bfbc82a15284	f2188f63-c7a0-44d2-8d24-d699766b68cb	fc55a6ea-3a5a-45a3-b307-2f844147503b	1
8f96de66-47e2-47c9-8c8e-90eaa26522c5	f2188f63-c7a0-44d2-8d24-d699766b68cb	a6939d8b-9bde-4cc6-bccc-9858fce44f9c	1
113fde9d-6afe-42c7-830a-78b0fc5f2c88	f2188f63-c7a0-44d2-8d24-d699766b68cb	09949847-54d3-4187-b186-4f3ba7662b5f	1
1c510c0c-f552-4174-a92e-da656fa35d4f	f2188f63-c7a0-44d2-8d24-d699766b68cb	9d308540-fe0a-4136-b380-32853b653754	1
d1eca589-c12e-4195-a64a-55e9b46ee794	f2188f63-c7a0-44d2-8d24-d699766b68cb	e768f283-f448-4a3c-8369-410c98876344	1
b6e8d999-e2a8-44bc-ace6-8c2183a28f9e	c14f40fe-61a3-45c0-acd1-0e17154512ce	d86dd0b6-3c43-405e-b282-8583d0897518	1
99f0ccdd-08f3-42b9-b999-14fb864cca9d	c14f40fe-61a3-45c0-acd1-0e17154512ce	d48b8232-8a89-42a7-b8c2-66f5913839e2	1
544fa033-2262-4501-aac3-f04367e3ae67	c14f40fe-61a3-45c0-acd1-0e17154512ce	dcc784ed-bb4c-4b8c-a745-9e41433284df	1
40df50e9-23c4-4fdb-9285-9707453fb80e	c14f40fe-61a3-45c0-acd1-0e17154512ce	2a2ccc14-99a4-4806-8894-ca83045b0781	1
b79c099b-ce55-43e5-8f59-6192ef32a068	c14f40fe-61a3-45c0-acd1-0e17154512ce	1920f61c-324f-4394-90ef-06824da53ca0	1
2ded177f-fb08-4ced-bbf2-fdccb3818995	c14f40fe-61a3-45c0-acd1-0e17154512ce	70a32933-9c5f-4c86-8752-b96da53c89b2	1
19264e10-e873-42af-8487-a099e1cf608b	c14f40fe-61a3-45c0-acd1-0e17154512ce	cd27224f-3934-4b7f-a721-7b5a68b76544	1
ab94c05c-604e-4fd8-be3c-f754114b97b5	c14f40fe-61a3-45c0-acd1-0e17154512ce	1f6b7678-7187-42c8-9519-2cf883ce82bd	1
117bf840-06b9-4541-a525-7d23ed1a0a5d	b45b0f62-34b3-4fbc-8dff-16ac822e656b	00e94756-1231-44aa-9d3e-665a4b26aadd	1
10870476-a789-4297-ae7c-b483e0eaea2f	b45b0f62-34b3-4fbc-8dff-16ac822e656b	33335893-90a7-4da2-883c-7a363effa39e	1
1e485056-f01f-432e-989b-2977870894fc	b45b0f62-34b3-4fbc-8dff-16ac822e656b	c9263a73-7622-4e03-b8f2-c489f86e25a2	1
f8470a67-4408-43b8-b7a3-9f3e06f1258f	b45b0f62-34b3-4fbc-8dff-16ac822e656b	bffb32eb-6498-433e-bc9f-9480a48ce462	1
d17d1249-db9b-409d-bf5b-909c0ce341b5	b45b0f62-34b3-4fbc-8dff-16ac822e656b	69feb6ce-46dd-416e-9609-143682f21433	1
192679a4-c47e-4e9c-8fa8-8053d9ac3238	b45b0f62-34b3-4fbc-8dff-16ac822e656b	361807b0-308b-4856-9e41-e86b8fb725ca	1
ceb7cdad-319d-4070-833d-bd0d9ab78db5	b45b0f62-34b3-4fbc-8dff-16ac822e656b	337398d7-fc7e-4ab6-93ec-2dd3f1755e35	1
750842a2-91e4-4fc3-bec6-8ce30bf9ce4d	b45b0f62-34b3-4fbc-8dff-16ac822e656b	be3923cb-a269-487e-bba7-e93f334bc4e2	1
ac3462ca-53f7-4272-9251-3116c49c0886	b45b0f62-34b3-4fbc-8dff-16ac822e656b	8f9207ab-78a0-488c-8642-49e3fa711f1c	1
6adddafe-113f-4d50-b30b-a382c61935b5	9f9feac3-c609-4713-8f68-7b47a72220f9	7b1d1dfc-37d3-47f0-b674-537bf6251e53	1
d5dc5961-2548-4893-bd97-5245f3f40f9c	9f9feac3-c609-4713-8f68-7b47a72220f9	a3d863e3-53ef-4a6d-987c-60067ce03357	2
ef6da511-67d8-488e-8384-a798b0dcccbd	9f9feac3-c609-4713-8f68-7b47a72220f9	8cb86222-596e-4cea-82cc-47c560a11352	1
b4a7090a-db8e-420d-8fce-576c1a41df70	9f9feac3-c609-4713-8f68-7b47a72220f9	235cc53b-2afe-4f91-9659-21cf926e36bb	1
df70375e-86bd-4d09-88f8-9794320f6f99	9f9feac3-c609-4713-8f68-7b47a72220f9	fc55a6ea-3a5a-45a3-b307-2f844147503b	1
cd0489f9-00a5-4184-9bbb-9c4faa698224	9f9feac3-c609-4713-8f68-7b47a72220f9	a6939d8b-9bde-4cc6-bccc-9858fce44f9c	1
59e0f937-670f-4bdd-933a-d77a75ef769a	9f9feac3-c609-4713-8f68-7b47a72220f9	09949847-54d3-4187-b186-4f3ba7662b5f	1
a57366f7-2155-45a4-9f65-66489935d336	9f9feac3-c609-4713-8f68-7b47a72220f9	9d308540-fe0a-4136-b380-32853b653754	1
af932ce9-d56d-4679-a4f7-606ab99a9d6c	9f9feac3-c609-4713-8f68-7b47a72220f9	e768f283-f448-4a3c-8369-410c98876344	1
c174422c-29e2-46f3-8d68-f4a87d31ec38	d6ac4c24-caf1-4d26-b085-f8ac9487b1fa	6d04d10e-cebe-4087-8faf-9c4eeefc1be1	1
31d2e189-8cda-458d-8ab9-4a4af5bbf920	d6ac4c24-caf1-4d26-b085-f8ac9487b1fa	dcc784ed-bb4c-4b8c-a745-9e41433284df	1
39a0d677-611c-4812-bd63-67a311d5b893	d6ac4c24-caf1-4d26-b085-f8ac9487b1fa	2a2ccc14-99a4-4806-8894-ca83045b0781	1
290f69b8-a826-4e17-865c-76667252a2f3	d6ac4c24-caf1-4d26-b085-f8ac9487b1fa	1920f61c-324f-4394-90ef-06824da53ca0	1
0a8dc382-5e77-47d6-b119-3edcc04a14fe	d6ac4c24-caf1-4d26-b085-f8ac9487b1fa	70a32933-9c5f-4c86-8752-b96da53c89b2	1
dba2b5b0-92e2-4fe0-9e90-edd8371ec7ea	d6ac4c24-caf1-4d26-b085-f8ac9487b1fa	cd27224f-3934-4b7f-a721-7b5a68b76544	1
9fed0caa-5044-487b-b449-5fa7c59b7645	84d450f0-4433-4c2b-8aba-2f2ef72f5e35	b5e84ccb-a1f6-4e35-972b-f2af8fd03dd8	1
87d12f9f-4b1c-4758-aced-ae8e5ed30a11	84d450f0-4433-4c2b-8aba-2f2ef72f5e35	33335893-90a7-4da2-883c-7a363effa39e	1
0c159482-5be3-4b62-939b-7ca724c94a43	84d450f0-4433-4c2b-8aba-2f2ef72f5e35	c9263a73-7622-4e03-b8f2-c489f86e25a2	1
b50ef614-7004-4262-859b-2cf02c7db86c	84d450f0-4433-4c2b-8aba-2f2ef72f5e35	bffb32eb-6498-433e-bc9f-9480a48ce462	1
4c15ccde-abfd-44b9-8323-0ec33ed29a2b	84d450f0-4433-4c2b-8aba-2f2ef72f5e35	69feb6ce-46dd-416e-9609-143682f21433	1
f6f76289-dff3-4de7-9fb6-500ebe35138b	84d450f0-4433-4c2b-8aba-2f2ef72f5e35	361807b0-308b-4856-9e41-e86b8fb725ca	1
d440e917-0078-41dc-9710-b0849f8f7e51	84d450f0-4433-4c2b-8aba-2f2ef72f5e35	337398d7-fc7e-4ab6-93ec-2dd3f1755e35	1
51cae535-c15c-4ccc-ac7e-af5737191b09	84d450f0-4433-4c2b-8aba-2f2ef72f5e35	be3923cb-a269-487e-bba7-e93f334bc4e2	1
bac4a72f-da1c-43e6-bf5d-013c5d44dca3	22bd725d-fa28-43ab-a058-eb02a3333238	7442ca46-b5ca-4446-9829-4c6321ef2d90	1
9bc64344-819a-4d65-b8bc-820f9e728635	22bd725d-fa28-43ab-a058-eb02a3333238	a3d863e3-53ef-4a6d-987c-60067ce03357	2
d916a5e6-1b4d-4720-99f4-5a52c918c49d	22bd725d-fa28-43ab-a058-eb02a3333238	8cb86222-596e-4cea-82cc-47c560a11352	1
7ea9597d-69f8-4f26-8cc3-3cff04d584ef	22bd725d-fa28-43ab-a058-eb02a3333238	235cc53b-2afe-4f91-9659-21cf926e36bb	1
e042b62f-e119-407f-9e10-35add7b44c66	22bd725d-fa28-43ab-a058-eb02a3333238	fc55a6ea-3a5a-45a3-b307-2f844147503b	1
fdd1ce66-4212-4ad1-bf73-715c9f065b1f	22bd725d-fa28-43ab-a058-eb02a3333238	a6939d8b-9bde-4cc6-bccc-9858fce44f9c	1
2c6b50bc-d230-4a45-aba3-6b037b360710	22bd725d-fa28-43ab-a058-eb02a3333238	09949847-54d3-4187-b186-4f3ba7662b5f	1
24df59c1-5254-45d4-8881-24d5fb407a8f	22bd725d-fa28-43ab-a058-eb02a3333238	9d308540-fe0a-4136-b380-32853b653754	1
1b05a36b-5223-4377-a583-b6185dc4e1f8	25164396-303c-45d4-ba62-e2cda6cf7c36	6d04d10e-cebe-4087-8faf-9c4eeefc1be1	1
486a5412-c3fe-4abf-865a-cf5d310708fe	25164396-303c-45d4-ba62-e2cda6cf7c36	dcc784ed-bb4c-4b8c-a745-9e41433284df	1
f5c52cad-6b06-4d82-822f-382121271150	25164396-303c-45d4-ba62-e2cda6cf7c36	2a2ccc14-99a4-4806-8894-ca83045b0781	1
5e3091f4-7c34-4c4b-ba9d-e28df3a0da13	25164396-303c-45d4-ba62-e2cda6cf7c36	1920f61c-324f-4394-90ef-06824da53ca0	1
3485fb94-e969-4313-bd32-4245effa4b36	25164396-303c-45d4-ba62-e2cda6cf7c36	70a32933-9c5f-4c86-8752-b96da53c89b2	1
6ddb680c-7b9d-4619-94bf-f5b3df3f81df	25164396-303c-45d4-ba62-e2cda6cf7c36	cd27224f-3934-4b7f-a721-7b5a68b76544	1
ea87414c-f83f-484a-95d5-363a6f1704d4	3214667b-d56e-4330-8f5f-2213fa36c97b	b5e84ccb-a1f6-4e35-972b-f2af8fd03dd8	1
9962882c-1b9d-46c7-94db-06a7ebe7e833	3214667b-d56e-4330-8f5f-2213fa36c97b	33335893-90a7-4da2-883c-7a363effa39e	1
dd661401-0d21-412d-b1a0-c05406989cb4	3214667b-d56e-4330-8f5f-2213fa36c97b	c9263a73-7622-4e03-b8f2-c489f86e25a2	1
4522b603-88e8-4988-a4d7-b65ba89fd46a	3214667b-d56e-4330-8f5f-2213fa36c97b	bffb32eb-6498-433e-bc9f-9480a48ce462	1
b752fd37-1a16-4d64-ac87-48fee6810a4e	3214667b-d56e-4330-8f5f-2213fa36c97b	69feb6ce-46dd-416e-9609-143682f21433	1
ee6be161-2c10-40ea-9e74-25b65262f6a4	3214667b-d56e-4330-8f5f-2213fa36c97b	361807b0-308b-4856-9e41-e86b8fb725ca	1
c6d4c9d0-32de-47e8-be0c-f9d850c89a30	3214667b-d56e-4330-8f5f-2213fa36c97b	337398d7-fc7e-4ab6-93ec-2dd3f1755e35	1
4b687a16-640e-4585-a8d4-63bcc4804c42	3214667b-d56e-4330-8f5f-2213fa36c97b	be3923cb-a269-487e-bba7-e93f334bc4e2	1
8a6eec61-20ad-42f2-a8db-6d8216560b52	a8ed4944-d264-4eae-8890-9913ae0a8d88	7442ca46-b5ca-4446-9829-4c6321ef2d90	1
27bcc22d-f60b-400f-9e9b-29452b772ff9	a8ed4944-d264-4eae-8890-9913ae0a8d88	a3d863e3-53ef-4a6d-987c-60067ce03357	2
5399970a-bece-4107-86ec-4ceb5020f4ab	a8ed4944-d264-4eae-8890-9913ae0a8d88	8cb86222-596e-4cea-82cc-47c560a11352	1
446a7b3a-a412-445d-a53e-29ef46cd6e10	a8ed4944-d264-4eae-8890-9913ae0a8d88	235cc53b-2afe-4f91-9659-21cf926e36bb	1
9d6b0469-65ed-4d1b-96cc-a7669197106c	a8ed4944-d264-4eae-8890-9913ae0a8d88	fc55a6ea-3a5a-45a3-b307-2f844147503b	1
bef712bc-ac37-473b-8af6-d8996820accd	a8ed4944-d264-4eae-8890-9913ae0a8d88	a6939d8b-9bde-4cc6-bccc-9858fce44f9c	1
063f68d0-2461-4db9-8bde-203b94275db6	a8ed4944-d264-4eae-8890-9913ae0a8d88	09949847-54d3-4187-b186-4f3ba7662b5f	1
90ca60fd-f6d7-412a-842d-071b7acf0b1e	a8ed4944-d264-4eae-8890-9913ae0a8d88	9d308540-fe0a-4136-b380-32853b653754	1
e7c2c88b-c166-44c9-8b6e-8844b1a6a226	1424042a-da88-49d5-8f77-962c91effcd6	6d04d10e-cebe-4087-8faf-9c4eeefc1be1	1
82859a8b-4ebb-4480-a73c-ceec458a03b4	1424042a-da88-49d5-8f77-962c91effcd6	dcc784ed-bb4c-4b8c-a745-9e41433284df	1
07503674-2e04-469a-aaed-7b6eff51c21b	1424042a-da88-49d5-8f77-962c91effcd6	2a2ccc14-99a4-4806-8894-ca83045b0781	1
27e5b1ef-02d0-4208-8a59-2060032f1b65	1424042a-da88-49d5-8f77-962c91effcd6	1920f61c-324f-4394-90ef-06824da53ca0	1
6fc2b33c-263e-4969-9ce2-86146d0a6fe5	1424042a-da88-49d5-8f77-962c91effcd6	70a32933-9c5f-4c86-8752-b96da53c89b2	1
6159db20-17c5-4d2a-afa9-1771fc773444	1424042a-da88-49d5-8f77-962c91effcd6	cd27224f-3934-4b7f-a721-7b5a68b76544	1
256b5500-4c1b-43f6-baa1-a2c2b550569a	14fb996c-911f-493b-97cf-6c2d2e790800	b5e84ccb-a1f6-4e35-972b-f2af8fd03dd8	1
36eec5af-c2b3-4ae2-8af5-0f9235cd8be6	14fb996c-911f-493b-97cf-6c2d2e790800	33335893-90a7-4da2-883c-7a363effa39e	1
8ec205a8-16de-41f5-8969-0c2b8bc2aa93	14fb996c-911f-493b-97cf-6c2d2e790800	c9263a73-7622-4e03-b8f2-c489f86e25a2	1
3a1d98e9-1120-4d2c-b4f0-94ed2182cc4e	14fb996c-911f-493b-97cf-6c2d2e790800	bffb32eb-6498-433e-bc9f-9480a48ce462	1
85faadcb-e8d5-495d-8d7f-32f79a5d2603	14fb996c-911f-493b-97cf-6c2d2e790800	69feb6ce-46dd-416e-9609-143682f21433	1
0fa3b158-7dbd-4977-be46-c212ce975857	14fb996c-911f-493b-97cf-6c2d2e790800	361807b0-308b-4856-9e41-e86b8fb725ca	1
ffefa1e8-7c6d-4184-9b59-c0b858e886b2	14fb996c-911f-493b-97cf-6c2d2e790800	337398d7-fc7e-4ab6-93ec-2dd3f1755e35	1
6f84bb5c-4752-4767-bc31-ec38f41b8513	14fb996c-911f-493b-97cf-6c2d2e790800	be3923cb-a269-487e-bba7-e93f334bc4e2	1
9ced776e-7c53-4256-886e-f2a2eb9f6d72	11bb6a7b-4c81-4b88-aff3-215a72c108dc	7442ca46-b5ca-4446-9829-4c6321ef2d90	1
8cce75c6-785c-49ed-975f-26b576039817	11bb6a7b-4c81-4b88-aff3-215a72c108dc	a3d863e3-53ef-4a6d-987c-60067ce03357	2
0c03dc61-dc78-4ed8-8ebf-9cb1cf58a838	11bb6a7b-4c81-4b88-aff3-215a72c108dc	8cb86222-596e-4cea-82cc-47c560a11352	1
69440f80-d0e5-4791-a03e-97b23eff6575	11bb6a7b-4c81-4b88-aff3-215a72c108dc	235cc53b-2afe-4f91-9659-21cf926e36bb	1
acf0577f-f2a2-4cce-a288-275e91a518e1	11bb6a7b-4c81-4b88-aff3-215a72c108dc	fc55a6ea-3a5a-45a3-b307-2f844147503b	1
a9ba2e4b-24be-49fb-abde-aa3694aa14d8	11bb6a7b-4c81-4b88-aff3-215a72c108dc	a6939d8b-9bde-4cc6-bccc-9858fce44f9c	1
4d5f43d2-2b82-4b1c-839f-fb2539e25166	11bb6a7b-4c81-4b88-aff3-215a72c108dc	09949847-54d3-4187-b186-4f3ba7662b5f	1
ea816582-fabc-4555-8f59-15668e04bb08	11bb6a7b-4c81-4b88-aff3-215a72c108dc	9d308540-fe0a-4136-b380-32853b653754	1
d3194af8-370d-45b4-ae11-27025504ba21	0e7b90d0-2a06-43bf-9170-b7f4073be95b	6d04d10e-cebe-4087-8faf-9c4eeefc1be1	1
77f95dec-43e8-4f1c-b575-f27037afd010	0e7b90d0-2a06-43bf-9170-b7f4073be95b	dcc784ed-bb4c-4b8c-a745-9e41433284df	1
50f82af4-669d-40a7-8778-86910f4b8ad8	0e7b90d0-2a06-43bf-9170-b7f4073be95b	2a2ccc14-99a4-4806-8894-ca83045b0781	1
5a29b474-4d68-4227-a1f8-3adb4ae964c2	0e7b90d0-2a06-43bf-9170-b7f4073be95b	1920f61c-324f-4394-90ef-06824da53ca0	1
ef2ba6d2-cd42-4a70-9e5f-3bf2d85dfd6f	0e7b90d0-2a06-43bf-9170-b7f4073be95b	70a32933-9c5f-4c86-8752-b96da53c89b2	1
d7ef7a43-b2a1-4c72-a81c-7e6782f8d12d	0e7b90d0-2a06-43bf-9170-b7f4073be95b	cd27224f-3934-4b7f-a721-7b5a68b76544	1
d1ed47f0-b556-40f4-bdb4-f690b8e92770	b85b3b7b-8e6d-4863-ac0c-6c538b680dba	b5e84ccb-a1f6-4e35-972b-f2af8fd03dd8	1
49c26f2b-55a9-4a83-a3d1-165c7ffc01da	b85b3b7b-8e6d-4863-ac0c-6c538b680dba	33335893-90a7-4da2-883c-7a363effa39e	1
135e599e-6f62-48d1-955b-8df86d00f820	b85b3b7b-8e6d-4863-ac0c-6c538b680dba	c9263a73-7622-4e03-b8f2-c489f86e25a2	1
e82f6a08-d60f-4b4a-9015-0dd013a037cd	b85b3b7b-8e6d-4863-ac0c-6c538b680dba	bffb32eb-6498-433e-bc9f-9480a48ce462	1
87bac6e3-db57-4c88-b9e6-895515f2932c	b85b3b7b-8e6d-4863-ac0c-6c538b680dba	69feb6ce-46dd-416e-9609-143682f21433	1
6da70294-a132-49a3-8bcf-90c2ae3cc585	b85b3b7b-8e6d-4863-ac0c-6c538b680dba	361807b0-308b-4856-9e41-e86b8fb725ca	1
083919ac-a46a-4858-b194-e942332f61a7	b85b3b7b-8e6d-4863-ac0c-6c538b680dba	337398d7-fc7e-4ab6-93ec-2dd3f1755e35	1
f84c7730-7087-49d8-af93-ffb5d2a216fe	b85b3b7b-8e6d-4863-ac0c-6c538b680dba	be3923cb-a269-487e-bba7-e93f334bc4e2	1
88b8d973-86fd-40e3-84b7-9305a81fc1f9	d9a8f4ab-b98b-43c8-8343-9fbd38378ee6	7442ca46-b5ca-4446-9829-4c6321ef2d90	1
3428820e-2ff7-4190-ae0a-03c1e6bdf5a6	d9a8f4ab-b98b-43c8-8343-9fbd38378ee6	a3d863e3-53ef-4a6d-987c-60067ce03357	2
11f0f66c-a16f-42ec-8dfb-d1b575911de2	d9a8f4ab-b98b-43c8-8343-9fbd38378ee6	8cb86222-596e-4cea-82cc-47c560a11352	1
e1870a75-be5f-4f24-92ba-ce8d239d54c1	d9a8f4ab-b98b-43c8-8343-9fbd38378ee6	235cc53b-2afe-4f91-9659-21cf926e36bb	1
7d6e3f40-82bd-4966-8fd5-e926c5508744	d9a8f4ab-b98b-43c8-8343-9fbd38378ee6	fc55a6ea-3a5a-45a3-b307-2f844147503b	1
6bc5a183-238e-4934-94fc-2cd968c97449	d9a8f4ab-b98b-43c8-8343-9fbd38378ee6	a6939d8b-9bde-4cc6-bccc-9858fce44f9c	1
1185ffc2-67b2-4b3e-929a-a5c768fc6ac1	d9a8f4ab-b98b-43c8-8343-9fbd38378ee6	09949847-54d3-4187-b186-4f3ba7662b5f	1
753dcee9-adf4-4182-a53f-0e2909e1b73b	d9a8f4ab-b98b-43c8-8343-9fbd38378ee6	9d308540-fe0a-4136-b380-32853b653754	1
879fed5f-fb77-4e6c-847d-0168c8813d3e	87e56f5e-e495-4635-b6eb-0336f15d90b8	6d04d10e-cebe-4087-8faf-9c4eeefc1be1	1
5ef4e172-3aab-4b7d-9c52-129241d0e63a	87e56f5e-e495-4635-b6eb-0336f15d90b8	dcc784ed-bb4c-4b8c-a745-9e41433284df	1
95880a70-808c-4a31-a104-c48a71076278	87e56f5e-e495-4635-b6eb-0336f15d90b8	2a2ccc14-99a4-4806-8894-ca83045b0781	1
6afb45a4-e7a8-41ba-9b67-420620432030	87e56f5e-e495-4635-b6eb-0336f15d90b8	1920f61c-324f-4394-90ef-06824da53ca0	1
6e6c6e72-066f-450a-80f5-a8b9ec840118	87e56f5e-e495-4635-b6eb-0336f15d90b8	70a32933-9c5f-4c86-8752-b96da53c89b2	1
4d410e76-982f-4c85-af80-15352dd879eb	87e56f5e-e495-4635-b6eb-0336f15d90b8	cd27224f-3934-4b7f-a721-7b5a68b76544	1
4f6ec206-dd27-4331-8a85-cde7cf4bbe30	0adc160c-71e4-4cec-90e9-573916d72419	b5e84ccb-a1f6-4e35-972b-f2af8fd03dd8	1
c6c5f1f3-409e-44d6-8ffc-883781a31e6d	0adc160c-71e4-4cec-90e9-573916d72419	33335893-90a7-4da2-883c-7a363effa39e	1
13153cca-941e-46c6-a82b-5ebec685e8cc	0adc160c-71e4-4cec-90e9-573916d72419	c9263a73-7622-4e03-b8f2-c489f86e25a2	1
8a6ebb22-a787-4982-bd5d-9eb8391f8341	0adc160c-71e4-4cec-90e9-573916d72419	bffb32eb-6498-433e-bc9f-9480a48ce462	1
83f60e89-725c-47c7-a13e-85059051fad2	0adc160c-71e4-4cec-90e9-573916d72419	69feb6ce-46dd-416e-9609-143682f21433	1
e5c741bc-39c2-4f7c-951d-abd9b7823cb0	0adc160c-71e4-4cec-90e9-573916d72419	361807b0-308b-4856-9e41-e86b8fb725ca	1
2e2c0130-d649-4b7b-9f46-6172217002d5	0adc160c-71e4-4cec-90e9-573916d72419	337398d7-fc7e-4ab6-93ec-2dd3f1755e35	1
9c1255eb-820f-42f9-a02d-139cca8b80f1	0adc160c-71e4-4cec-90e9-573916d72419	be3923cb-a269-487e-bba7-e93f334bc4e2	1
94120720-817e-4a0d-b28c-5884418e9ccc	d7e29b58-cec6-4a4c-92f8-1eb8782f7bda	7442ca46-b5ca-4446-9829-4c6321ef2d90	1
45dfb426-1548-4664-a0ea-2f84deebd85d	d7e29b58-cec6-4a4c-92f8-1eb8782f7bda	a3d863e3-53ef-4a6d-987c-60067ce03357	2
58e4e0ad-2079-44ef-b91a-378ae22f8575	d7e29b58-cec6-4a4c-92f8-1eb8782f7bda	8cb86222-596e-4cea-82cc-47c560a11352	1
fafe6db3-cb85-4b71-833d-52ef84451c8b	d7e29b58-cec6-4a4c-92f8-1eb8782f7bda	235cc53b-2afe-4f91-9659-21cf926e36bb	1
f2595380-d319-4428-b63a-b902d9fd5660	d7e29b58-cec6-4a4c-92f8-1eb8782f7bda	fc55a6ea-3a5a-45a3-b307-2f844147503b	1
38d72b85-e416-4c01-8a67-e34ae54d450c	d7e29b58-cec6-4a4c-92f8-1eb8782f7bda	a6939d8b-9bde-4cc6-bccc-9858fce44f9c	1
9a0f3f66-2582-4a8e-833b-0c09d2e5caa2	d7e29b58-cec6-4a4c-92f8-1eb8782f7bda	09949847-54d3-4187-b186-4f3ba7662b5f	1
3a749082-710c-4018-9235-88b0737ca2ae	d7e29b58-cec6-4a4c-92f8-1eb8782f7bda	9d308540-fe0a-4136-b380-32853b653754	1
\.


--
-- Data for Name: packages; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.packages (id, department_id, tier, usage_mode) FROM stdin;
c926bb27-b79b-454e-bf64-2a131729e57f	09baca34-fa9b-4c7c-a172-e66584bfc0f4	basic	mobile
d21814b5-cb1b-4b50-98b3-08b41ba06547	09baca34-fa9b-4c7c-a172-e66584bfc0f4	premium	mobile
e8451cd3-5af5-4d6a-b01e-ca9ace89c7b1	09baca34-fa9b-4c7c-a172-e66584bfc0f4	ultra	mobile
2bad1b66-1a04-4343-a48f-a64ae191bf83	a689b5b1-22af-422f-ad72-7f468e637c7e	basic	mobile
71bf2a64-5bf2-4cf5-95d8-78f169dbb655	a689b5b1-22af-422f-ad72-7f468e637c7e	premium	mobile
9678a458-6f10-4648-b2db-76b0d98f2fb5	a689b5b1-22af-422f-ad72-7f468e637c7e	ultra	mobile
ffd5f171-663f-4051-aa10-38c8882bd02b	dbf5fe69-3316-43ab-b97e-eacd1d7a24bf	basic	mobile
15a865a3-584d-4945-be54-e3fb2550d44d	dbf5fe69-3316-43ab-b97e-eacd1d7a24bf	premium	mobile
f1c0d97d-392e-4f04-835d-281b462205a9	dbf5fe69-3316-43ab-b97e-eacd1d7a24bf	ultra	mobile
25f37a6a-7bdb-46b0-ac6c-a277daffa974	feafc6f0-d0fc-42b6-b137-67d0e7b262bd	basic	mobile
423baa40-2c00-4c35-b55e-0d9cef62b452	feafc6f0-d0fc-42b6-b137-67d0e7b262bd	premium	mobile
f2188f63-c7a0-44d2-8d24-d699766b68cb	feafc6f0-d0fc-42b6-b137-67d0e7b262bd	ultra	mobile
c14f40fe-61a3-45c0-acd1-0e17154512ce	04bf7ca3-7163-443e-bb72-c1c8907950d0	basic	mobile
b45b0f62-34b3-4fbc-8dff-16ac822e656b	04bf7ca3-7163-443e-bb72-c1c8907950d0	premium	mobile
9f9feac3-c609-4713-8f68-7b47a72220f9	04bf7ca3-7163-443e-bb72-c1c8907950d0	ultra	mobile
d6ac4c24-caf1-4d26-b085-f8ac9487b1fa	09baca34-fa9b-4c7c-a172-e66584bfc0f4	basic	stationary
84d450f0-4433-4c2b-8aba-2f2ef72f5e35	09baca34-fa9b-4c7c-a172-e66584bfc0f4	premium	stationary
22bd725d-fa28-43ab-a058-eb02a3333238	09baca34-fa9b-4c7c-a172-e66584bfc0f4	ultra	stationary
25164396-303c-45d4-ba62-e2cda6cf7c36	a689b5b1-22af-422f-ad72-7f468e637c7e	basic	stationary
3214667b-d56e-4330-8f5f-2213fa36c97b	a689b5b1-22af-422f-ad72-7f468e637c7e	premium	stationary
a8ed4944-d264-4eae-8890-9913ae0a8d88	a689b5b1-22af-422f-ad72-7f468e637c7e	ultra	stationary
1424042a-da88-49d5-8f77-962c91effcd6	dbf5fe69-3316-43ab-b97e-eacd1d7a24bf	basic	stationary
14fb996c-911f-493b-97cf-6c2d2e790800	dbf5fe69-3316-43ab-b97e-eacd1d7a24bf	premium	stationary
11bb6a7b-4c81-4b88-aff3-215a72c108dc	dbf5fe69-3316-43ab-b97e-eacd1d7a24bf	ultra	stationary
0e7b90d0-2a06-43bf-9170-b7f4073be95b	feafc6f0-d0fc-42b6-b137-67d0e7b262bd	basic	stationary
b85b3b7b-8e6d-4863-ac0c-6c538b680dba	feafc6f0-d0fc-42b6-b137-67d0e7b262bd	premium	stationary
d9a8f4ab-b98b-43c8-8343-9fbd38378ee6	feafc6f0-d0fc-42b6-b137-67d0e7b262bd	ultra	stationary
87e56f5e-e495-4635-b6eb-0336f15d90b8	04bf7ca3-7163-443e-bb72-c1c8907950d0	basic	stationary
0adc160c-71e4-4cec-90e9-573916d72419	04bf7ca3-7163-443e-bb72-c1c8907950d0	premium	stationary
d7e29b58-cec6-4a4c-92f8-1eb8782f7bda	04bf7ca3-7163-443e-bb72-c1c8907950d0	ultra	stationary
\.


--
-- Data for Name: products; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.products (id, name, price, product_type) FROM stdin;
00e94756-1231-44aa-9d3e-665a4b26aadd	Lenovo ThinkPad T14s	1050.00	laptop
7b1d1dfc-37d3-47f0-b674-537bf6251e53	Lenovo ThinkPad T16 Gen4	1850.00	laptop
1920f61c-324f-4394-90ef-06824da53ca0	Amazon Basics Sitz-Steh-Schreibtisch elektrisch	115.00	desk
69feb6ce-46dd-416e-9609-143682f21433	FlexiSpot Höhenverstellbarer Schreibtisch Q3	270.00	desk
fc55a6ea-3a5a-45a3-b307-2f844147503b	Yaasa Desk Pro Höhenverstellbarer Schreibtisch	660.00	desk
d48b8232-8a89-42a7-b8c2-66f5913839e2	Lenovo C24d-20	229.00	monitor
33335893-90a7-4da2-883c-7a363effa39e	Lenovo ThinkVision P27Q-40	399.00	monitor
a3d863e3-53ef-4a6d-987c-60067ce03357	Lenovo ThinkVision T27UD-40	489.00	monitor
992a6c56-2c83-47c5-b9a9-5a28932337e9	Lenovo ThinkVision T27UD-40	489.00	monitor
70a32933-9c5f-4c86-8752-b96da53c89b2	IKEA MARKUS Drehstuhl	160.00	chair
361807b0-308b-4856-9e41-e86b8fb725ca	SIHOO Doro S300	700.00	chair
a6939d8b-9bde-4cc6-bccc-9858fce44f9c	Herman Miller Embody	1450.00	chair
d86dd0b6-3c43-405e-b282-8583d0897518	Lenovo ThinkPad E14 Gen7	720.00	laptop
2a2ccc14-99a4-4806-8894-ca83045b0781	ThinkPad Essential Funkmaus	16.00	mouse
bffb32eb-6498-433e-bc9f-9480a48ce462	ThinkPad kompakte Funkmaus mit USB-C-Empfänger	30.00	mouse
6d04d10e-cebe-4087-8faf-9c4eeefc1be1	IdeaCentre AIO i Gen9	699.00	workstation
b5e84ccb-a1f6-4e35-972b-f2af8fd03dd8	IdeaCentre AIO Gen 10	899.00	workstation
7442ca46-b5ca-4446-9829-4c6321ef2d90	Yoga AIO 9i Gen 10	2499.00	workstation
235cc53b-2afe-4f91-9659-21cf926e36bb	Lenovo Legion M600s Qi Gaming-Funkmaus	99.00	mouse
dcc784ed-bb4c-4b8c-a745-9e41433284df	Lenovo Essential USB Tastatur	24.00	keyboard
c9263a73-7622-4e03-b8f2-c489f86e25a2	Lenovo Professional wiederaufladbare Funktastatur	75.00	keyboard
be3923cb-a269-487e-bba7-e93f334bc4e2	Lenovo QHD-Webcam	99.00	webcam
8cb86222-596e-4cea-82cc-47c560a11352	Ergonomische Tastatur R-Go Split Break	120.00	keyboard
9d308540-fe0a-4136-b380-32853b653754	Lenovo 4K Pro Webcam	169.00	webcam
1f6b7678-7187-42c8-9519-2cf883ce82bd	ThinkPad Universal USB-C Dock	195.00	docking_station
8f9207ab-78a0-488c-8642-49e3fa711f1c	ThinkPad USB4 Smart Dock 5500	360.00	docking_station
e768f283-f448-4a3c-8369-410c98876344	ThinkPad Thunderbolt 5 Smart Dock 7500	450.00	docking_station
cd27224f-3934-4b7f-a721-7b5a68b76544	Kabelpaket Basic	23.17	cable
337398d7-fc7e-4ab6-93ec-2dd3f1755e35	Kabelpaket Premium	37.00	cable
09949847-54d3-4187-b186-4f3ba7662b5f	Kabelpaket Ultra	121.00	cable
\.


--
-- Data for Name: webcams; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.webcams (id, fps, resolution, dfov_adjustable, connection_style, description) FROM stdin;
be3923cb-a269-487e-bba7-e93f334bc4e2	30	2K HD-Auflösung	t	USB-C	Autofokus und Auto-Framing
9d308540-fe0a-4136-b380-32853b653754	30	4K HD-Auflösung	t	USB-C	Autofokus und Auto-Framing
\.


--
-- Data for Name: workstations; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.workstations (id, processor, operating_system, memory, power_usage, disc_memory, screen_size, resolution_height, resolution_width, refresh_rate, graphics_card, camera) FROM stdin;
6d04d10e-cebe-4087-8faf-9c4eeefc1be1	Intel® U300 Prozessor	Windows 11	8 GB DDR5-5200MT/s	30.000	256 GB SSD M.2 2280 PCIe 4.0 TLC	23.800	1920	1080	100	integrated graphics	5MP-RGB
b5e84ccb-a1f6-4e35-972b-f2af8fd03dd8	AMD Ryzen™ 5 220 Prozessor	Windows 11	16 GB DDR5-5600MT/s	40.000	512 GB SSD M.2 2280 PCIe 4.0 QL	27.000	1920	1080	100	integrated graphics	5MP-IR
7442ca46-b5ca-4446-9829-4c6321ef2d90	Intel® Core™ Ultra 7 258V Prozessor	Windows 11	32 GB LPDDR5X-8533MHz	70.000	1 TB SSD M.2 2280 PCIe 4.0 TLC	31.500	3840	2160	60	NVIDIA® GeForce RTX™ 4050 6GB	5MP-IR
\.


--
-- Name: alembic_version alembic_version_pkc; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.alembic_version
    ADD CONSTRAINT alembic_version_pkc PRIMARY KEY (version_num);


--
-- Name: cables cables_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.cables
    ADD CONSTRAINT cables_pkey PRIMARY KEY (id);


--
-- Name: chairs chairs_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.chairs
    ADD CONSTRAINT chairs_pkey PRIMARY KEY (id);


--
-- Name: departments departments_name_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.departments
    ADD CONSTRAINT departments_name_key UNIQUE (name);


--
-- Name: departments departments_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.departments
    ADD CONSTRAINT departments_pkey PRIMARY KEY (id);


--
-- Name: desks desks_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.desks
    ADD CONSTRAINT desks_pkey PRIMARY KEY (id);


--
-- Name: docking_stations docking_stations_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.docking_stations
    ADD CONSTRAINT docking_stations_pkey PRIMARY KEY (id);


--
-- Name: keyboards keyboards_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.keyboards
    ADD CONSTRAINT keyboards_pkey PRIMARY KEY (id);


--
-- Name: laptops laptops_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.laptops
    ADD CONSTRAINT laptops_pkey PRIMARY KEY (id);


--
-- Name: monitors monitors_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.monitors
    ADD CONSTRAINT monitors_pkey PRIMARY KEY (id);


--
-- Name: mouses mouses_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.mouses
    ADD CONSTRAINT mouses_pkey PRIMARY KEY (id);


--
-- Name: package_items package_items_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.package_items
    ADD CONSTRAINT package_items_pkey PRIMARY KEY (id);


--
-- Name: packages packages_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.packages
    ADD CONSTRAINT packages_pkey PRIMARY KEY (id);


--
-- Name: products products_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.products
    ADD CONSTRAINT products_pkey PRIMARY KEY (id);


--
-- Name: package_items uq_package_items_unique; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.package_items
    ADD CONSTRAINT uq_package_items_unique UNIQUE (package_id, product_id);


--
-- Name: packages uq_packages_department_tier_usage_mode; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.packages
    ADD CONSTRAINT uq_packages_department_tier_usage_mode UNIQUE (department_id, tier, usage_mode);


--
-- Name: webcams webcams_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.webcams
    ADD CONSTRAINT webcams_pkey PRIMARY KEY (id);


--
-- Name: workstations workstations_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.workstations
    ADD CONSTRAINT workstations_pkey PRIMARY KEY (id);


--
-- Name: ix_products_product_type; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ix_products_product_type ON public.products USING btree (product_type);


--
-- Name: cables cables_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.cables
    ADD CONSTRAINT cables_id_fkey FOREIGN KEY (id) REFERENCES public.products(id) ON DELETE CASCADE;


--
-- Name: chairs chairs_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.chairs
    ADD CONSTRAINT chairs_id_fkey FOREIGN KEY (id) REFERENCES public.products(id) ON DELETE CASCADE;


--
-- Name: desks desks_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.desks
    ADD CONSTRAINT desks_id_fkey FOREIGN KEY (id) REFERENCES public.products(id) ON DELETE CASCADE;


--
-- Name: docking_stations docking_stations_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.docking_stations
    ADD CONSTRAINT docking_stations_id_fkey FOREIGN KEY (id) REFERENCES public.products(id) ON DELETE CASCADE;


--
-- Name: keyboards keyboards_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.keyboards
    ADD CONSTRAINT keyboards_id_fkey FOREIGN KEY (id) REFERENCES public.products(id) ON DELETE CASCADE;


--
-- Name: laptops laptops_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.laptops
    ADD CONSTRAINT laptops_id_fkey FOREIGN KEY (id) REFERENCES public.products(id) ON DELETE CASCADE;


--
-- Name: monitors monitors_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.monitors
    ADD CONSTRAINT monitors_id_fkey FOREIGN KEY (id) REFERENCES public.products(id) ON DELETE CASCADE;


--
-- Name: mouses mouses_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.mouses
    ADD CONSTRAINT mouses_id_fkey FOREIGN KEY (id) REFERENCES public.products(id) ON DELETE CASCADE;


--
-- Name: package_items package_items_package_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.package_items
    ADD CONSTRAINT package_items_package_id_fkey FOREIGN KEY (package_id) REFERENCES public.packages(id) ON DELETE CASCADE;


--
-- Name: package_items package_items_product_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.package_items
    ADD CONSTRAINT package_items_product_id_fkey FOREIGN KEY (product_id) REFERENCES public.products(id) ON DELETE RESTRICT;


--
-- Name: packages packages_department_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.packages
    ADD CONSTRAINT packages_department_id_fkey FOREIGN KEY (department_id) REFERENCES public.departments(id) ON DELETE CASCADE;


--
-- Name: webcams webcams_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.webcams
    ADD CONSTRAINT webcams_id_fkey FOREIGN KEY (id) REFERENCES public.products(id) ON DELETE CASCADE;


--
-- Name: workstations workstations_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.workstations
    ADD CONSTRAINT workstations_id_fkey FOREIGN KEY (id) REFERENCES public.products(id) ON DELETE CASCADE;


--
-- PostgreSQL database dump complete
--

\unrestrict BUNxYGYYI6jj6cSDlyciyXmjC53PBORGgIFPHM08BHe9Q39TFtVHdNOykhAOakf

