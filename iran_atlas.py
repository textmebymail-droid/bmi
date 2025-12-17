import streamlit as st
import pandas as pd
import math

# تنظیمات صفحه
st.set_page_config(page_title="اطلس شهرهای ایران", page_icon="🗺️", layout="wide")

# ==========================================
# 1. بانک اطلاعاتی شهرها (دیتابیس داخلی)
# ==========================================
cities_data = {
    "تهران": {
        "lat": 35.6892, "lon": 51.3890,
        "pop": "۸,۶۹۳,۷۰۶ نفر",
        "area": "۷۳۰ کیلومتر مربع",
        "desc": "پایتخت ایران و پرجمعیت‌ترین شهر. دارای جاذبه‌هایی مثل برج آزادی، برج میلاد و کاخ گلستان. مرکز سیاسی و اقتصادی کشور."
    },
    "شیراز": {
        "lat": 29.5918, "lon": 52.5837,
        "pop": "۱,۵۶۵,۵۷۲ نفر",
        "area": "۲۴۰ کیلومتر مربع",
        "desc": "شهر شعر و ادب و گل. پایتخت ایران در دوران زندیه. میزبان حافظیه، سعدیه، تخت جمشید و باغ ارم."
    },
    "اصفهان": {
        "lat": 32.6546, "lon": 51.6680,
        "pop": "۱,۹۶۱,۰۰۰ نفر",
        "area": "۵۵۱ کیلومتر مربع",
        "desc": "نصف جهان. پایتخت دوران صفویه. مشهور به میدان نقش جهان، سی‌وسه پل و معماری بی‌نظیر اسلامی."
    },
    "مشهد": {
        "lat": 36.2605, "lon": 59.6168,
        "pop": "۳,۰۰۱,۱۸۴ نفر",
        "area": "۳۵۱ کیلومتر مربع",
        "desc": "پایتخت معنوی ایران. دومین شهر بزرگ کشور و میزبان حرم امام رضا (ع). دارای آرامگاه فردوسی در توس."
    },
    "تبریز": {
        "lat": 38.0962, "lon": 46.2605,
        "pop": "۱,۵۵۸,۶۹۳ نفر",
        "area": "۳۲۴ کیلومتر مربع",
        "desc": "شهر اولین‌ها. پایتخت فرش جهان. دارای بزرگترین بازار سرپوشیده جهان و مسجد کبود."
    },
    "یزد": {
        "lat": 31.8974, "lon": 54.3569,
        "pop": "۵۲۹,۶۷۳ نفر",
        "area": "۱۱۰ کیلومتر مربع",
        "desc": "شهر بادگیرها و عروس کویر. اولین شهر خشتی ثبت شده در میراث جهانی یونسکو. مرکز زرتشتیان ایران."
    }
}

# ==========================================
# 2. تابع محاسبه فاصله (فرمول ریاضی)
# ==========================================
def calculate_distance(lat1, lon1, lat2, lon2):
    # شعاع کره زمین (کیلومتر)
    R = 6371 
    
    # تبدیل درجه به رادیان
    phi1 = math.radians(lat1)
    phi2 = math.radians(lat2)
    delta_phi = math.radians(lat2 - lat1)
    delta_lambda = math.radians(lon2 - lon1)
    
    # فرمول Haversine
    a = math.sin(delta_phi / 2)**2 + \
        math.cos(phi1) * math.cos(phi2) * \
        math.sin(delta_lambda / 2)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    
    distance = R * c
    return round(distance) # گرد کردن عدد

# ==========================================
# 3. رابط کاربری (UI)
# ==========================================

st.title("🗺️ اطلس جامع شهرهای ایران")
st.write("اطلاعات جغرافیایی، تاریخی و محاسبه فاصله بین شهرها")
st.divider()

# انتخاب شهرها
col1, col2 = st.columns(2)
with col1:
    city1_name = st.selectbox("شهر مبدأ را انتخاب کنید:", list(cities_data.keys()), index=0)
with col2:
    city2_name = st.selectbox("شهر مقصد را انتخاب کنید:", list(cities_data.keys()), index=1)

# دکمه محاسبه
if st.button("محاسبه فاصله و نمایش اطلاعات"):
    
    # گرفتن اطلاعات شهرها از دیتابیس
    c1_info = cities_data[city1_name]
    c2_info = cities_data[city2_name]
    
    # محاسبه فاصله
    dist = calculate_distance(c1_info['lat'], c1_info['lon'], c2_info['lat'], c2_info['lon'])
    
    # نمایش فاصله
    st.success(f"📏 فاصله هوایی مستقیم بین **{city1_name}** و **{city2_name}** حدود **{dist} کیلومتر** است.")
    
    # نمایش نقشه
    # برای نقشه باید یک جدول (DataFrame) بسازیم که ستون‌های lat و lon داشته باشد
    map_data = pd.DataFrame([
        {'lat': c1_info['lat'], 'lon': c1_info['lon']},
        {'lat': c2_info['lat'], 'lon': c2_info['lon']}
    ])
    st.map(map_data, zoom=4)
    
    st.divider()
    
    # نمایش کارت‌های اطلاعاتی
    info_c1, info_c2 = st.columns(2)
    
    with info_c1:
        st.subheader(f"📍 درباره {city1_name}")
        st.image("https://upload.wikimedia.org/wikipedia/commons/thumb/c/ca/Iran_location_map.svg/200px-Iran_location_map.svg.png", width=100) # عکس نمادین نقشه
        st.metric("جمعیت", c1_info['pop'])
        st.metric("وسعت", c1_info['area'])
        st.info(c1_info['desc'])
        
    with info_c2:
        st.subheader(f"📍 درباره {city2_name}")
        st.image("https://upload.wikimedia.org/wikipedia/commons/thumb/c/ca/Iran_location_map.svg/200px-Iran_location_map.svg.png", width=100)
        st.metric("جمعیت", c2_info['pop'])
        st.metric("وسعت", c2_info['area'])
        st.info(c2_info['desc'])

else:
    st.info("برای مشاهده اطلاعات، دو شهر را انتخاب کرده و دکمه محاسبه را بزنید.")
