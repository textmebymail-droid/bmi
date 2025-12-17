{\rtf1\ansi\ansicpg1252\cocoartf2822
\cocoatextscaling0\cocoaplatform0{\fonttbl\f0\fswiss\fcharset0 Helvetica;}
{\colortbl;\red255\green255\blue255;}
{\*\expandedcolortbl;;}
\margl1440\margr1440\vieww11520\viewh8400\viewkind0
\pard\tx720\tx1440\tx2160\tx2880\tx3600\tx4320\tx5040\tx5760\tx6480\tx7200\tx7920\tx8640\pardirnatural\partightenfactor0

\f0\fs24 \cf0 import streamlit as st\
\
st.title("\uc0\u1605 \u1581 \u1575 \u1587 \u1576 \u1607 \u8204 \u1711 \u1585  BMI")\
\
vazn = st.number_input("\uc0\u1608 \u1586 \u1606  \u1582 \u1608 \u1583  \u1585 \u1575  \u1608 \u1575 \u1585 \u1583  \u1705 \u1606 \u1740 \u1583  (\u1705 \u1740 \u1604 \u1608 \u1711 \u1585 \u1605 ):")\
ghad = st.number_input("\uc0\u1602 \u1583  \u1582 \u1608 \u1583  \u1585 \u1575  \u1608 \u1575 \u1585 \u1583  \u1705 \u1606 \u1740 \u1583  (\u1605 \u1578 \u1585 ):")\
\
if st.button("\uc0\u1605 \u1581 \u1575 \u1587 \u1576 \u1607 "):\
    bmi = vazn / (ghad * ghad)\
    st.write(f"\uc0\u1588 \u1575 \u1582 \u1589  \u1578 \u1608 \u1583 \u1607  \u1576 \u1583 \u1606 \u1740  \u1588 \u1605 \u1575 : \{bmi\}")}