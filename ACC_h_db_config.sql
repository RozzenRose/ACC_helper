--
-- PostgreSQL database dump
--

-- Dumped from database version 17.0 (Debian 17.0-1.pgdg120+1)
-- Dumped by pg_dump version 17.0 (Debian 17.0-1.pgdg120+1)

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
-- Data for Name: Cars; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public."Cars" (id, car_name) FROM stdin;
1	Porsche_922_GT3R
2	Ferrari_296_GT3
3	Lamborghini_Huracan_GT3_EVO_2
4	BMW_M4_GT3
5	McLaren_720s_EVO_GT3
6	Ford_Mustang_GT3
7	Aston_Martin_V8_Vantage
\.



--
-- Data for Name: Tracks; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public."Tracks" (id, track_name, turns, aproximate_flow, aproximate_time) FROM stdin;
2	Monza	11	\N	\N
3	Misano	16	\N	\N
1	Spa_Francorchamps	20	3.850	00:02:22
5	Watkins_Glen	11	\N	\N
6	Imola	19	\N	\N
4	Hungaroring	16	2.4	00:02:47
7	Mount_Panorama	23	\N	\N
\.

--
-- Data for Name: Info; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public."Info" (id, car_id, track_id, track_guide, setups) FROM stdin;
37	1	7	https://youtu.be/mCjVJYdhffA?si=_AZv7LRee-3pHhkt	+
38	2	7	https://youtu.be/m8Baypjgkpo?si=DvAultbCtFSd75PH	+
39	4	7	https://youtu.be/f0c2yUPuFKU?si=Fto0d-QecxUK2hv2	+
40	5	7	https://youtu.be/6EnbNyzPvcM?si=-DQi8wRRFTnrGMgq	+
42	3	7	https://youtu.be/9z06jDTN-4A?si=0h_s1lmXP1SPNHlC	+
1	1	1	https://www.youtube.com/watch?v=Ve7Qhx0lFzg&t=79s	+
2	1	2	https://youtu.be/aOG_eHcYpHY?si=6J07ekTzIKJhad46	+
3	1	3	https://youtu.be/_wln3lu1JPI?si=vtj3Gzf9H1DlHQvi	+
4	3	1	https://youtu.be/T8_UfrkVGzw?si=inMp3lcglfdNlZja	+
5	3	3	https://youtu.be/e4VFmcL0HEw?si=mSAlgiyCL_GXfyht	+
6	3	2	https://youtu.be/z16M0hfHd8k?si=W_iVgjI3CHV3iT-q	+
9	2	3	https://youtu.be/Ho6lnuBNLmw?si=mkdHZvXLd1zFw1Bm	+
10	1	4	https://www.youtube.com/watch?v=9tYS_2G2m_U&t=0s	+
11	3	4	https://www.youtube.com/watch?v=cuHUgfyrq-U&t=0s	+
12	2	4	https://www.youtube.com/watch?v=iLWapP7WEgw&t=0s	+
13	4	4	https://www.youtube.com/watch?v=4cVCUYbKu0Q&t=0s	+
15	4	2	https://www.youtube.com/watch?v=DLeLyDyV5kM	+
16	4	3	https://www.youtube.com/watch?v=8kOKNpZpGVg	+
36	2	6	https://youtu.be/pUCInJyil7A?si=nLns8mQsbALolg9B	+
17	5	4	https://www.youtube.com/watch?v=vhbFjlV6cnQ&t=0s	+
18	5	1	https://youtu.be/GHfX3yI7RTU?si=Gm15KWX3eV4U_ATL	+
19	5	3	https://youtu.be/fvaW7ES4MYU?si=O9WPiGwLxzVzl8ki	+
21	3	5	https://youtu.be/TN9gu4cP4V8?si=s2IaK4gbmzKDNefw	+
22	1	5	https://youtu.be/qbho7DEDDoQ?si=-zR8FKGylUj1W4FK	+
23	2	5	https://youtu.be/L_oWwny_7AA?si=DZV5OIoH-r7LD3_c	+
24	4	5	https://youtu.be/viXuT0mXaj4?si=EM7Y2Cs7EczS6rTY	+
25	5	5	https://youtu.be/cTmL9cQUWMQ?si=RGPcZ94mFK0AgBQT	+
26	6	2	https://youtu.be/BSYRskA6TBs?si=ZcyI5T55-qSJbelx	+
7	2	2	https://youtu.be/IEbgFQsmb-k?si=SFoskoARQfGx8YrA	+
31	6	6	https://www.youtube.com/watch?v=OiYAYk5vwsg	+
14	4	1	https://www.youtube.com/watch?v=KBhE1NfHhA8	+
20	5	2	https://www.youtube.com/watch?v=LyU0klBWY6Y	+
27	6	3	https://youtu.be/FZYc_Awb8ms?si=m4_GucxXtm0SWdS9	+
28	6	4	https://youtu.be/QQxHEa4vkq4?si=cuS7BHLBsLtlyS3b	+
30	6	5	https://www.youtube.com/watch?v=31cFnPg7H0M	+
29	6	1	https://youtu.be/3RhtDeyzlTw?si=HFO3DVrBhoA0rm-8	+
32	4	6	https://youtu.be/UmGRrJXO8cE?si=w0QYdX7kpww0Fwe7	+
33	1	6	https://www.youtube.com/watch?v=MFaMS_F4qT0	+
34	5	6	https://www.youtube.com/watch?v=xPUvVaE8uAI	+
35	3	6	https://youtu.be/9H87zFCyLj8?si=vMD9KmYuE_Ud4l_O	+
8	2	1	https://youtu.be/tVgEI5ohhw0?si=OZaSuo2MK4C4-W_u	+
41	6	7	https://youtu.be/tez0zsUKuMA?si=837kdpoEBhqjl4je	+
43	7	1	https://youtu.be/gKU21bGotOQ?si=22V_4_dyrZNgN62-	+
44	7	2	https://youtu.be/TkBYfC8fuOU?si=rdiW-xJPWDxKAmry	+
45	7	3	https://youtu.be/kIqQNIZWQRQ?si=j-1YvfwllqR9n2I6	+
46	7	4	https://youtu.be/bpOxvZeTBtE?si=8uImvQHgICIPDbMM	+
47	7	5	https://youtu.be/sJWNfj8X2c8?si=HRKdpNFjDonUOH-t	+
48	7	6	https://youtu.be/KtqAoe949CE?si=7Hm2WMzzxoO7DffB	+
49	7	7	https://youtu.be/JQ0gcTe3034?si=k-oZ-itl-dRWqlxk	+
\.

--
-- Data for Name: workers; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.workers (id, username) FROM stdin;
\.


--
-- Name: Cars_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public."Cars_id_seq"', 1, false);


--
-- Name: Info_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public."Info_id_seq"', 1, true);


--
-- Name: Tracks_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public."Tracks_id_seq"', 1, false);


--
-- Name: workers_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.workers_id_seq', 1, false);


--
-- Name: Cars Cars_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."Cars"
    ADD CONSTRAINT "Cars_pkey" PRIMARY KEY (id);


--
-- Name: Info Info_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."Info"
    ADD CONSTRAINT "Info_pkey" PRIMARY KEY (id);


--
-- Name: Tracks Tracks_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."Tracks"
    ADD CONSTRAINT "Tracks_pkey" PRIMARY KEY (id);


--
-- Name: Users Users_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."Users"
    ADD CONSTRAINT "Users_pkey" PRIMARY KEY (user_id);


--
-- Name: workers workers_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.workers
    ADD CONSTRAINT workers_pkey PRIMARY KEY (id);


--
-- Name: Info Info_car_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."Info"
    ADD CONSTRAINT "Info_car_id_fkey" FOREIGN KEY (car_id) REFERENCES public."Cars"(id);


--
-- Name: Info Info_track_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."Info"
    ADD CONSTRAINT "Info_track_id_fkey" FOREIGN KEY (track_id) REFERENCES public."Tracks"(id);


--
-- PostgreSQL database dump complete
--

