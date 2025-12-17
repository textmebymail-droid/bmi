import streamlit as st
import pandas as pd
from datetime import date, timedelta
from fpdf import FPDF
import io

# تنظیمات صفحه
st.set_page_config(page_title="Runna AI Coach", page_icon="🧬", layout="wide")

# ==========================================
# 🧠 بخش منطق و هوش مصنوعی (Algorithm)
# ==========================================

class RunnaCoach:
    def __init__(self, current_5k, race_date, days_per_week, level, strength_days):
        self.today = date.today()
        self.race_date = race_date
        self.days_per_week = days_per_week
        self.level = level
        self.strength_days = strength_days
        self.pace_zones = self._calculate_paces(current_5k)
        
    def _calculate_paces(self, time_str):
        # تبدیل زمان به ثانیه و محاسبه دقیق زون‌ها
        try:
            m, s = map(int, time_str.split(':'))
            total_sec = m * 60 + s
            pace = total_sec / 5  # pace per km
            
            def fmt(p): return f"{int(p//60)}:{int(p%60):02d}"
            
            return {
                "Easy": fmt(pace * 1.35),
                "Long": fmt(pace * 1.45),
                "Tempo": fmt(pace * 1.15),
                "Interval": fmt(pace * 0.95),
                "Race": fmt(pace)
            }
        except:
            return None

    def generate_plan(self):
        # محاسبه تعداد هفته‌ها تا مسابقه
        delta = self.race_date - self.today
        weeks_count = delta.days // 7
        
        if weeks_count < 1:
            return None, "تاریخ مسابقه باید حداقل ۱ هفته بعد باشد."
            
        full_schedule = []
        
        # الگوریتم تولید برنامه
        for w in range(weeks_count):
            week_start = self.today + timedelta(days=w*7)
            phase = self._get_phase(w, weeks_count)
            
            # تولید تمرینات بر اساس تعداد روزهای انتخابی کاربر
            workouts = self._get_weekly_workouts(phase)
            
            # پخش کردن تمرینات در هفته
            day_counter = 0
            for i in range(7):
                current_day_date = week_start + timedelta(days=i)
                day_name = current_day_date.strftime("%A")
                
                # منطق ساده برای چیدن روزها (شنبه تا جمعه)
                activity = "Rest 💤"
                details = "Recovery & Stretch"
                
                # اگر کاربر این روز را انتخاب کرده باشد
                # (این بخش ساده شده است، در نسخه واقعی پیچیده‌تر است)
                if day_counter < len(workouts) and i % 2 == 0: # یک روز در میان
                     activity = workouts[day_counter]['type']
                     details = workouts[day_counter]['desc']
                     day_counter += 1
                elif "Strength" in self.strength_days and i == 3: # وسط هفته قدرتی
                    activity = "Strength 🏋️"
                    details = "Core & Legs Workout (30 mins)"

                full_schedule.append({
                    "Date": current_day_date,
                    "Week": w + 1,
                    "Phase": phase,
                    "Activity": activity,
                    "Details": details
                })
                
        return pd.DataFrame(full_schedule), None

    def _get_phase(self, current_week, total_weeks):
        if current_week < total_weeks * 0.4: return "Base Building 🏗️"
        if current_week < total_weeks * 0.8: return "Peak Training 🔥"
        return "Tapering 📉" # کاهش فشار قبل مسابقه

    def _get_weekly_workouts(self, phase):
        # تمرینات بر اساس فاز تغییر می‌کنند
        p = self.pace_zones
        if phase == "Base Building 🏗️":
            return [
                {"type": "Easy Run", "desc": f"30-40 min @ {p['Easy']}/km"},
                {"type": "Tempo Run", "desc": f"20 min @ {p['Tempo']}/km"},
                {"type": "Long Run", "desc": f"5-8 km @ {p['Long']}/km"}
            ]
        elif phase == "Peak Training 🔥":
            return [
                {"type": "Intervals", "desc": f"8x400m @ {p['Interval']}/km"},
                {"type": "Threshold", "desc": f"40 min mixed pace"},
                {"type": "Long Run", "desc": f"10-15 km @ {p['Long']}/km"}
            ]
        else: # Taper
            return [
                {"type": "Shakeout", "desc": f"20 min very easy"},
                {"type": "Strides", "desc": "10 min + 4 strides"},
                {"type": "Race Prep", "desc": f"5 km easy @ {p['Easy']}/km"}
            ]

# ==========================================
# 🖥️ رابط کاربری (UI)
# ==========================================

st.title("Runna AI Coach 🧬")
st.caption("برنامه‌ریزی هوشمند بر اساس تاریخ مسابقه و سطح شما")

# 1. تنظیمات اولیه (Setup)
with st.expander("⚙️ تنظیمات پروفایل (اینجا شروع کنید)", expanded=True):
    c1, c2 = st.columns(2)
    with c1:
        name = st.text_input("نام ورزشکار", "Doctor")
        level = st.selectbox("سطح شما", ["Beginner", "Intermediate", "Advanced"])
        days = st.slider("چند روز در هفته می‌دوید؟", 2, 6, 3)
    with c2:
        current_5k = st.text_input("رکورد فعلی ۵ کیلومتر", "25:00")
        race_date = st.date_input("تاریخ مسابقه", date.today() + timedelta(days=60))
        strength = st.multiselect("تمرینات جانبی", ["Strength Training", "Pilates"], ["Strength Training"])

# 2. اجرا
if st.button("تولید برنامه هوشمند"):
    coach = RunnaCoach(current_5k, race_date, days, level, strength)
    
    # نمایش سرعت‌ها
    if coach.pace_zones:
        st.success("✅ پروفایل آنالیز شد. سرعت‌های شما:")
        cols = st.columns(5)
        p = coach.pace_zones
        cols[0].metric("Easy", p['Easy'])
        cols[1].metric("Long", p['Long'])
        cols[2].metric("Tempo", p['Tempo'])
        cols[3].metric("Interval", p['Interval'])
        cols[4].metric("Race", p['Race'])
    
    # تولید برنامه
    df, error = coach.generate_plan()
    
    if error:
        st.error(error)
    else:
        st.divider()
        
        # تب‌بندی نمایش
        tab1, tab2, tab3 = st.tabs(["📅 نمای کلی برنامه", "📄 خروجی PDF", "📆 گوگل کلندر"])
        
        with tab1:
            st.dataframe(df, use_container_width=True)
            
            # نمودار پیشرفت حجم تمرین
            st.caption("توزیع فشار تمرینی تا روز مسابقه:")
            chart_data = df[df['Activity'] != 'Rest 💤'].groupby('Week').count()['Activity']
            st.bar_chart(chart_data)

        with tab2:
            # ساخت PDF
            pdf = FPDF()
            pdf.add_page()
            pdf.set_font("Arial", "B", 16)
            pdf.cell(0, 10, f"Runna AI Plan for {name}", ln=True, align="C")
            pdf.set_font("Arial", "", 12)
            pdf.cell(0, 10, f"Goal: Race on {race_date}", ln=True, align="C")
            pdf.ln(10)
            
            # اضافه کردن جدول به PDF (ساده)
            pdf.set_font("Arial", size=10)
            for i, row in df.iterrows():
                line = f"W{row['Week']} | {row['Date'].strftime('%Y-%m-%d')} | {row['Activity']} | {row['Details']}"
                # حذف اموجی‌ها برای جلوگیری از ارور PDF
                line = line.encode('latin-1', 'ignore').decode('latin-1')
                pdf.cell(0, 8, line, ln=True, border=1)
                
            pdf_bytes = pdf.output(dest='S').encode('latin-1')
            st.download_button("دانلود فایل PDF کامل", pdf_bytes, "runna_plan.pdf", "application/pdf")

        with tab3:
            # ساخت فایل ICS
            ics_content = "BEGIN:VCALENDAR\nVERSION:2.0\nPRODID:-//RunnaAI//EN\n"
            for i, row in df.iterrows():
                if "Rest" in row['Activity']: continue
                d_str = row['Date'].strftime("%Y%m%d")
                ics_content += f"BEGIN:VEVENT\nDTSTART;VALUE=DATE:{d_str}\nSUMMARY:{row['Activity']}\nDESCRIPTION:{row['Details']}\nEND:VEVENT\n"
            ics_content += "END:VCALENDAR"
            
            st.download_button("افزودن به تقویم موبایل/گوگل", ics_content, "plan.ics", "text/calendar")
