import streamlit as st
import pandas as pd
import datetime
from fpdf import FPDF
import base64

# تنظیمات صفحه
st.set_page_config(page_title="Pro Run Coach", page_icon="🏃‍♂️", layout="wide")

# ==========================================
# 🧠 بخش محاسبات (Logic)
# ==========================================

def calculate_zones(age):
    max_hr = 220 - age
    return {
        "Zone 1 (Warm up)": f"{int(max_hr * 0.50)} - {int(max_hr * 0.60)} bpm",
        "Zone 2 (Easy)": f"{int(max_hr * 0.60)} - {int(max_hr * 0.70)} bpm",
        "Zone 3 (Aerobic)": f"{int(max_hr * 0.70)} - {int(max_hr * 0.80)} bpm",
        "Zone 4 (Threshold)": f"{int(max_hr * 0.80)} - {int(max_hr * 0.90)} bpm",
        "Zone 5 (Max)": f"{int(max_hr * 0.90)} - {int(max_hr * 1.00)} bpm",
    }

def calculate_paces(current_5k_str):
    try:
        parts = current_5k_str.split(':')
        total_sec = int(parts[0]) * 60 + int(parts[1])
        pace = total_sec / 5
        
        def fmt(p):
            mins = int(p // 60)
            secs = int(p % 60)
            return f"{mins}:{secs:02d}"

        return {
            "Easy": fmt(pace * 1.25),   # Runna style easy
            "Tempo": fmt(pace * 1.08),
            "Interval": fmt(pace * 0.92),
            "Long": fmt(pace * 1.35),
            "Race": fmt(pace)
        }
    except:
        return None

def generate_ics_file(plan_df, start_date):
    """تولید فایل برای گوگل کلندر"""
    ics_content = "BEGIN:VCALENDAR\nVERSION:2.0\nPRODID:-//RunnaClone//RunPlan//EN\n"
    
    for index, row in plan_df.iterrows():
        if row['نوع تمرین'] == "Rest":
            continue
            
        # محاسبه تاریخ هر تمرین
        day_offset = index  # فرض ساده: هر سطر یک روز است
        event_date = start_date + datetime.timedelta(days=day_offset)
        date_str = event_date.strftime("%Y%m%d")
        
        ics_content += "BEGIN:VEVENT\n"
        ics_content += f"DTSTART;VALUE=DATE:{date_str}\n"
        ics_content += f"SUMMARY:🏃 {row['نوع تمرین']} - {row['مسافت/زمان']}\n"
        ics_content += f"DESCRIPTION:{row['جزئیات تمرین']}\n"
        ics_content += "END:VEVENT\n"
        
    ics_content += "END:VCALENDAR"
    return ics_content

def create_pdf(plan_df, user_info, paces, zones):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    
    # عنوان
    pdf.set_font("Arial", 'B', 16)
    pdf.cell(200, 10, txt="Running Training Plan", ln=1, align='C')
    
    # مشخصات
    pdf.set_font("Arial", size=10)
    pdf.cell(200, 10, txt=f"Athlete: {user_info['name']} | Goal: {user_info['goal']}", ln=1, align='L')
    
    # سرعت‌ها
    pdf.ln(5)
    pdf.set_font("Arial", 'B', 12)
    pdf.cell(200, 10, txt="Your Training Paces:", ln=1)
    pdf.set_font("Arial", size=10)
    for k, v in paces.items():
        pdf.cell(40, 10, txt=f"{k}: {v}/km", border=1)
    pdf.ln(15)

    # زون‌ها
    pdf.set_font("Arial", 'B', 12)
    pdf.cell(200, 10, txt="Heart Rate Zones:", ln=1)
    pdf.set_font("Arial", size=10)
    for k, v in zones.items():
        pdf.cell(0, 8, txt=f"{k}: {v}", ln=1)
    pdf.ln(10)

    # جدول برنامه
    pdf.set_font("Arial", 'B', 12)
    pdf.cell(200, 10, txt="Weekly Schedule:", ln=1)
    pdf.set_font("Arial", size=8)
    
    # هدر جدول
    pdf.cell(30, 8, "Day", 1)
    pdf.cell(40, 8, "Type", 1)
    pdf.cell(120, 8, "Details", 1)
    pdf.ln()
    
    for index, row in plan_df.iterrows():
        details = row['جزئیات تمرین'].encode('latin-1', 'replace').decode('latin-1') # رفع مشکل فونت ساده
        pdf.cell(30, 8, str(row['روز']), 1)
        pdf.cell(40, 8, str(row['نوع تمرین']), 1)
        pdf.cell(120, 8, str(details), 1)
        pdf.ln()
        
    return pdf.output(dest='S').encode('latin-1')

# ==========================================
# 📱 رابط کاربری (UI)
# ==========================================

st.title("🏃‍♂️ Runna Pro Clone")
st.markdown("برنامه تمرینی حرفه‌ای با قابلیت خروجی **PDF** و **Google Calendar**")

# --- سایدبار: مشخصات فردی ---
with st.sidebar:
    st.header("پروفایل دونده")
    name = st.text_input("نام:", "Runner")
    age = st.number_input("سن:", min_value=15, max_value=90, value=30)
    weight = st.number_input("وزن (kg):", value=70)
    
    st.divider()
    st.header("تنظیمات برنامه")
    goal = st.selectbox("هدف:", ["5K Beginner", "10K Intermediate", "Half Marathon Pro"])
    record_5k = st.text_input("رکورد ۵ کیلومتر فعلی:", "25:00")
    start_date = st.date_input("تاریخ شروع برنامه:", datetime.date.today())
    
    st.info("⚠️ نکته: برای خروجی تقویم، تاریخ شروع را دقیق تنظیم کنید.")

# --- محاسبات ---
paces = calculate_paces(record_5k)
zones = calculate_zones(age)

if paces:
    # 1. نمایش زون‌های ضربان قلب و سرعت‌ها
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("💓 زون‌های قلبی شما")
        st.caption("برای نتیجه‌گیری حرفه‌ای، در زون مشخص شده بدوید.")
        st.table(pd.DataFrame(list(zones.items()), columns=["Zone", "Heart Rate"]))
        
    with col2:
        st.subheader("⚡ سرعت‌های تمرینی")
        st.caption("دقیقه بر کیلومتر")
        # نمایش متریک‌ها
        c1, c2 = st.columns(2)
        c1.metric("Easy Pace", paces['Easy'])
        c1.metric("Tempo Pace", paces['Tempo'])
        c2.metric("Interval Pace", paces['Interval'])
        c2.metric("Long Run", paces['Long'])

    st.divider()

    # 2. تولید دیتای برنامه (نمونه ۴ هفته‌ای فشرده برای نمایش)
    st.subheader(f"📅 برنامه تمرینی: {goal}")
    
    # ساخت دیتای هوشمند بر اساس انتخاب
    days = ["Saturday", "Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]
    
    # الگوی ساده برنامه (می‌تواند بسیار پیچیده‌تر شود)
    if "5K" in goal:
        workouts = [
            ("Rest", "-", "Recovery Day"),
            ("Easy Run", "30 min", f"Run at {paces['Easy']}. Keep HR in Zone 2."),
            ("Intervals", "3km Total", f"1km Warmup, 5x400m @ {paces['Interval']}, 1km Cooldown"),
            ("Rest", "-", "Recovery / Yoga"),
            ("Easy Run", "30 min", f"Steady run at {paces['Easy']}."),
            ("Rest", "-", "Rest Day"),
            ("Long Run", "5 km", f"Long slow distance at {paces['Long']}.")
        ]
    elif "10K" in goal:
        workouts = [
            ("Rest", "-", "Recovery"),
            ("Easy Run", "40 min", f"Zone 2 run at {paces['Easy']}."),
            ("Tempo", "40 min", f"10min Warmup, 20min @ {paces['Tempo']}, 10min Cool"),
            ("Easy Run", "30 min", f"Recovery run."),
            ("Intervals", "5km Total", f"1km Warmup, 6x800m @ {paces['Interval']}, 1km Cooldown"),
            ("Rest", "-", "Active Recovery"),
            ("Long Run", "10 km", f"Endurance run at {paces['Long']}.")
        ]
    else: # Half Marathon
        workouts = [
            ("Rest", "-", "Recovery"),
            ("Easy Run", "50 min", f"Zone 2 steady state."),
            ("Speed", "8km Total", f"2km Warmup, 10x400m Hills, 2km Cooldown"),
            ("Easy Run", "40 min", f"Recovery run."),
            ("Tempo", "60 min", f"15min Warmup, 30min @ {paces['Tempo']}, 15min Cool"),
            ("Rest", "-", "Yoga / Stretch"),
            ("Long Run", "16 km", f"Big run! Keep pace at {paces['Long']}.")
        ]

    # تبدیل لیست به دیتافریم
    plan_data = []
    for i, day in enumerate(days):
        plan_data.append({
            "روز": day,
            "نوع تمرین": workouts[i][0],
            "مسافت/زمان": workouts[i][1],
            "جزئیات تمرین": workouts[i][2]
        })
    
    df_plan = pd.DataFrame(plan_data)
    st.table(df_plan)
    
    # --- بخش دانلودها ---
    st.subheader("📥 دانلود برنامه")
    d_col1, d_col2 = st.columns(2)
    
    # دانلود فایل تقویم (ICS)
    ics_text = generate_ics_file(df_plan, start_date)
    d_col1.download_button(
        label="📅 افزودن به تقویم (Google/Apple)",
        data=ics_text,
        file_name="runna_plan.ics",
        mime="text/calendar"
    )
    
    # دانلود PDF
    # نکته: برای PDF ساده لاتین استفاده شده تا در سرور مشکل فونت نداشته باشد
    user_info = {"name": name, "goal": goal}
    pdf_bytes = create_pdf(df_plan, user_info, paces, zones)
    d_col2.download_button(
        label="📄 دانلود فایل PDF",
        data=bytes(pdf_bytes),
        file_name="training_plan.pdf",
        mime="application/pdf"
    )

else:
    st.error("لطفاً فرمت زمان را چک کنید (مثال: 24:30)")
