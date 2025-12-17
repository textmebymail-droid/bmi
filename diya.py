import streamlit as st
import pandas as pd

# تنظیمات صفحه و راست‌چین کردن متون
st.set_page_config(page_title="محاسبه‌گر تخصصی دیه و ارش", page_icon="⚖️", layout="wide")

# استایل CSS برای راست‌چین کردن کامل (RTL)
st.markdown("""
<style>
    .stApp {
        direction: rtl;
        text-align: right;
        font-family: "Vazir", "Tahoma", sans-serif;
    }
    .stSelectbox, .stNumberInput, .stTextInput {
        direction: rtl;
    }
    /* تنظیم فونت و سایز تیترها */
    h1, h2, h3 {
        text-align: right;
        font-family: "B Nazanin", sans-serif;
    }
    /* جدول‌ها */
    .dataframe {
        text-align: right !important;
        direction: rtl !important;
    }
</style>
""", unsafe_allow_html=True)

# ==========================================
# 📚 بانک اطلاعاتی قوانین (ماده ۷۰۹ ق.م.ا)
# ==========================================
def get_injury_types():
    return {
        "حارصه (خراشیدگی پوست بدون خونریزی)": 0.5,
        "دامیه (جراحت سطحی با خونریزی)": 2.0,
        "متلاحمه (جراحت عمیق در گوشت)": 3.0,
        "سمحاق (جراحت که به پرده استخوان برسد)": 4.0,
        "موضحه (جراحت که استخوان را آشکار کند)": 5.0,
        "هاشمه (شکستگی استخوان)": 10.0,
        "منقله (جابجایی استخوان)": 15.0,
        "جائفه (جراحت نفوذی به حفرات بدن)": 33.33,
        "سایر / ارش (تعیین دستی درصد)": 0.0
    }

# ==========================================
# 🧮 بخش محاسبات
# ==========================================

st.title("⚖️ سامانه دستیار پزشکی قانونی")
st.caption("محاسبه دیه مقدر و ارش بر اساس نرخ روز دیه کامل")

# --- سایدبار: تنظیمات پایه ---
with st.sidebar:
    st.header("⚙️ تنظیمات نرخ دیه")
    
    # نرخ دیه سال ۱۴۰۳ (پیش‌فرض ۱ میلیارد و ۲۰۰ میلیون تومان)
    base_diya_amount = st.number_input(
        "نرخ دیه کامل سال (به تومان):", 
        value=1200000000, 
        step=50000000,
        format="%d"
    )
    
    month_type = st.radio("نوع ماه:", ["ماه عادی", "ماه حرام (تغلیظ)"])
    
    if month_type == "ماه حرام (تغلیظ)":
        st.info("نکته: تغلیظ دیه (افزودن یک‌سوم) معمولاً فقط در موارد فوت (قتل) اعمال می‌شود، نه جراحات ساده.")
        # اگر بخواهید تغلیظ را اعمال کنید:
        # base_diya_amount = base_diya_amount + (base_diya_amount / 3)

    st.divider()
    st.write("👨‍⚕️ کاربر: دکتر (متخصص پزشکی قانونی)")

# --- بخش اصلی: ورود اطلاعات پرونده ---
col1, col2 = st.columns(2)
with col1:
    case_number = st.text_input("شماره پرونده / کلاسه:", "1403/...")
with col2:
    patient_name = st.text_input("نام مصدوم:", "")

st.divider()

# --- انتخاب صدمات ---
st.subheader("📝 لیست صدمات وارده")

if 'injuries' not in st.session_state:
    st.session_state.injuries = []

# فرم افزودن صدمه جدید
with st.expander("افزودن صدمه جدید", expanded=True):
    c1, c2, c3 = st.columns([3, 2, 1])
    
    injury_dict = get_injury_types()
    
    with c1:
        selected_injury = st.selectbox("نوع جراحت (عنوان فقهی/پزشکی):", list(injury_dict.keys()))
    
    with c2:
        # اگر گزینه "سایر/ارش" انتخاب شد، کاربر درصد را دستی وارد کند
        if selected_injury == "سایر / ارش (تعیین دستی درصد)":
            percent = st.number_input("درصد ارش تعیین شده:", min_value=0.0, max_value=100.0, step=0.1, value=1.0)
        else:
            percent = injury_dict[selected_injury]
            st.info(f"درصد قانونی: {percent}%")
            
    with c3:
        count = st.number_input("تعداد:", min_value=1, value=1)

    add_btn = st.button("➕ ثبت صدمه در لیست")

    if add_btn:
        amount = (base_diya_amount * percent / 100) * count
        st.session_state.injuries.append({
            "عنوان": selected_injury.split(" (")[0], # فقط نام اصلی
            "درصد": percent,
            "تعداد": count,
            "مبلغ کل (تومان)": int(amount)
        })
        st.success("اضافه شد!")

# --- نمایش جدول محاسبات ---
if st.session_state.injuries:
    st.write("---")
    df = pd.DataFrame(st.session_state.injuries)
    
    # فرمت کردن اعداد جدول برای نمایش بهتر
    df_display = df.copy()
    df_display["مبلغ کل (تومان)"] = df["مبلغ کل (تومان)"].apply(lambda x: f"{x:,.0f}")
    
    st.table(df_display)
    
    # جمع کل
    total_amount = sum(item["مبلغ کل (تومان)"] for item in st.session_state.injuries)
    total_percent = sum(item["درصد"] * item["تعداد"] for item in st.session_state.injuries)
    
    st.info(f"💰 **جمع کل دیه و ارش تعیین شده:** {total_amount:,.0f} تومان")
    st.caption(f"مجموع درصدی از دیه کامل: {total_percent}%")
    
    # دکمه پاک کردن لیست
    if st.button("🗑️ پاک کردن لیست و شروع مجدد"):
        st.session_state.injuries = []
        st.rerun()

else:
    st.warning("هنوز صدمه‌ای ثبت نشده است.")

# --- فوتر ---
st.markdown("---")
st.caption("⚠️ سلب مسئولیت: این برنامه صرفاً جهت کمک به محاسبات است و جایگزین حکم نهایی مقام قضایی نمی‌باشد.")
