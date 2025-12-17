import streamlit as st

st.title("محاسبه‌گر BMI")

vazn = st.number_input("وزن خود را وارد کنید (کیلوگرم):")
ghad = st.number_input("قد خود را وارد کنید (متر):")

if st.button("محاسبه"):
    if ghad > 0:  # این خط چک می‌کند که قد صفر نباشد
        bmi = vazn / (ghad * ghad)
        st.write(f"شاخص توده بدنی شما: {bmi}")
    else:
        st.error("لطفاً قد خود را به درستی وارد کنید!")
