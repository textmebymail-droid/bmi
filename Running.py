
import streamlit as st
import pandas as pd

st.set_page_config(page_title="Runna Plan", page_icon="🏃")

st.title("🏃‍♂️ مربی هوشمند دویدن")
st.write("برنامه تمرینی اختصاصی شما")

# --- توابع محاسباتی ---
def seconds_to_min_sec(seconds):
    mins = int(seconds // 60)
    secs = int(seconds % 60)
    return f"{mins}:{secs:02d}"

def calculate_paces(current_5k_str):
    try:
        parts = current_5k_str.split(':')
        total_sec = int(parts[0]) * 60 + int(parts[1])
        pace = total_sec / 5
        return {
            "Easy": seconds_to_min_sec(pace * 1.30),
            "Tempo": seconds_to_min_sec(pace * 1.10),
            "Interval": seconds_to_min_sec(pace * 0.95),
            "Race": seconds_to_min_sec(pace)
        }
    except:
        return None

# --- ورودی‌ها ---
col1, col2 = st.columns(2)
with col1:
    goal = st.selectbox("هدف شما:", ["5K", "10K", "Half Marathon"])
with col2:
    record = st.text_input("رکورد ۵ کیلومتر فعلی:", "25:00")

# --- نمایش نتایج ---
paces = calculate_paces(record)

if paces:
    st.divider()
    st.subheader("سرعت‌های تمرینی شما (دقیقه بر کیلومتر)")
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("آرام (Easy)", paces['Easy'])
    c2.metric("تمپو (Tempo)", paces['Tempo'])
    c3.metric("سرعتی (Interval)", paces['Interval'])
    c4.metric("مسابقه", paces['Race'])
    
    st.divider()
    st.subheader(f"📅 برنامه پیشنهادی هفته اول ({goal})")
    
    # دیتای برنامه
    if goal == "5K":
        data = {"روز": ["شنبه", "یکشنبه", "دوشنبه", "سه‌شنبه", "چهارشنبه", "پنج‌شنبه", "جمعه"],
                "تمرین": ["استراحت", "30 دقیقه آرام", "اینتروال 400متر", "استراحت", "30 دقیقه آرام", "استراحت", "5km طولانی"]}
    elif goal == "10K":
        data = {"روز": ["شنبه", "یکشنبه", "دوشنبه", "سه‌شنبه", "چهارشنبه", "پنج‌شنبه", "جمعه"],
                "تمرین": ["استراحت", "40 دقیقه آرام", "تمپو 20 دقیقه", "استراحت", "40 دقیقه آرام", "استراحت", "8km طولانی"]}
    else:
        data = {"روز": ["شنبه", "یکشنبه", "دوشنبه", "سه‌شنبه", "چهارشنبه", "پنج‌شنبه", "جمعه"],
                "تمرین": ["استراحت", "50 دقیقه آرام", "اینتروال 800متر", "40 دقیقه آرام", "تمپو 30 دقیقه", "استراحت", "12km طولانی"]}
    
    df = pd.DataFrame(data)
    st.table(df)
else:
    st.error("لطفاً زمان را درست وارد کنید (مثلاً 25:00)")
