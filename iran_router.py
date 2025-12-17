import streamlit as st
import pandas as pd
import requests
import pydeck as pdk
import math

# تنظیمات صفحه
st.set_page_config(page_title="مسیریاب پیشرفته ایران", page_icon="🚗", layout="wide")

# ==========================================
# 1. بانک اطلاعاتی جامع شهرهای ایران
# ==========================================
# این لیست شامل مختصات دقیق و اطلاعات شهرهای اصلی است
cities_db = {
    "تهران": {"lat": 35.6892, "lon": 51.3890, "desc": "پایتخت سیاسی و اقتصادی، پرجمعیت‌ترین شهر ایران."},
    "مشهد": {"lat": 36.2605, "lon": 59.6168, "desc": "پایتخت معنوی، دومین کلان‌شهر، میزبان حرم مطهر رضوی."},
    "اصفهان": {"lat": 32.6546, "lon": 51.6680, "desc": "نصف جهان، پایتخت فرهنگی و شاهکار معماری صفوی."},
    "شیراز": {"lat": 29.5918, "lon": 52.5837, "desc": "شهر شعر و ادب، پایتخت فرهنگی باستانی (تخت جمشید)."},
    "تبریز": {"lat": 38.0962, "lon": 46.2605, "desc": "شهر اولین‌ها، قطب صنعتی و اقتصادی شمال غرب."},
    "کرج": {"lat": 35.8400, "lon": 50.9391, "desc": "ایران کوچک، در دامنه البرز و نزدیک تهران."},
    "اهواز": {"lat": 31.3183, "lon": 48.6706, "desc": "شهر پل‌ها و کارون، مرکز نفت و صنعت خوزستان."},
    "قم": {"lat": 34.6399, "lon": 50.8759, "desc": "قطب مذهبی و علمی، دومین شهر زیارتی ایران."},
    "کرمانشاه": {"lat": 34.3142, "lon": 47.0650, "desc": "گهواره تمدن، دارای آثار بیستون و طاق بستان."},
    "ارومیه": {"lat": 37.5527, "lon": 45.0761, "desc": "پاریس ایران، مرکز آذربایجان غربی."},
    "رشت": {"lat": 37.2774, "lon": 49.5890, "desc": "شهر باران‌های نقره‌ای، مرکز گیلان و شهر خلاق خوراک."},
    "کرمان": {"lat": 30.2839, "lon": 57.0834, "desc": "دیار کریمان، دارای مجموعه گنجعلی‌خان."},
    "زاهدان": {"lat": 29.4963, "lon": 60.8629, "desc": "مرکز سیستان و بلوچستان، شهر وحدت."},
    "همدان": {"lat": 34.7982, "lon": 48.5146, "desc": "پایتخت تاریخ و تمدن، شهر هگمتانه و ابوعلی سینا."},
    "یزد": {"lat": 31.8974, "lon": 54.3569, "desc": "شهر بادگیرها، اولین شهر خشتی ثبت جهانی یونسکو."},
    "اردبیل": {"lat": 38.2498, "lon": 48.2933, "desc": "دیار سبلان، خاستگاه صفویه و چشمه‌های آب گرم."},
    "بندرعباس": {"lat": 27.1832, "lon": 56.2666, "desc": "پایتخت اقتصادی و بندری جنوب ایران."},
    "اراک": {"lat": 34.0954, "lon": 49.6909, "desc": "پایتخت صنعتی ایران."},
    "قزوین": {"lat": 36.2797, "lon": 50.0049, "desc": "پایتخت خوشنویسی، دارای آثار تاریخی صفوی."},
    "زنجان": {"lat": 36.6736, "lon": 48.4953, "desc": "شهر ملی ملیله و چاقو، میزبان گنبد سلطانیه."},
    "سنندج": {"lat": 35.3219, "lon": 46.9862, "desc": "شهر اصالت و موسیقی، مرکز کردستان."},
    "گرگان": {"lat": 36.8456, "lon": 54.4393, "desc": "شهر جنگل‌های هیرکانی و ناهارخوران."},
    "ساری": {"lat": 36.5659, "lon": 53.0586, "desc": "مرکز مازندران، شهری کهن و سرسبز."},
    "بوشهر": {"lat": 28.9220, "lon": 50.8331, "desc": "شبه‌جزیره کهن، پایتخت انرژی ایران."},
    "ایلام": {"lat": 33.6374, "lon": 46.4227, "desc": "عروس زاگرس."},
    "بیرجند": {"lat": 32.8663, "lon": 59.2211, "desc": "شهر کاج‌ها، مرکز خراسان جنوبی."},
    "چابهار": {"lat": 25.2919, "lon": 60.6430, "desc": "تنها بندر اقیانوسی ایران."},
    "کیش": {"lat": 26.5381, "lon": 53.9866, "desc": "مروارید خلیج فارس، منطقه آزاد تجاری."},
    "قشم": {"lat": 26.9581, "lon": 56.2706, "desc": "سرزمین عجایب هفتگانه، بزرگترین جزیره خلیج فارس."}
}

# ==========================================
# 2. توابع کمکی (مسیریابی و جستجو)
# ==========================================

def get_coordinates_from_name(city_name):
    """جستجوی نام شهر در اینترنت (اگر در لیست نبود)"""
    try:
        url = "https://nominatim.openstreetmap.org/search"
        headers = {'User-Agent': 'IranRouterApp/1.0'}
        params = {'q': f"{city_name}, Iran", 'format': 'json', 'limit': 1}
        response = requests.get(url, params=params, headers=headers, timeout=5)
        data = response.json()
        if data:
            return float(data[0]['lat']), float(data[0]['lon']), f"پیدا شده در نقشه: {data[0]['display_name']}"
    except:
        return None
    return None

def get_driving_route(lat1, lon1, lat2, lon2):
    """دریافت مسیر رانندگی از سرویس OSRM"""
    # سرویس رایگان مسیریابی (توجه: ممکن است گاهی کند باشد)
    url = f"http://router.project-osrm.org/route/v1/driving/{lon1},{lat1};{lon2},{lat2}?overview=full&geometries=geojson"
    try:
        r = requests.get(url, timeout=5)
        if r.status_code == 200:
            data = r.json()
            if data['code'] == 'Ok':
                route = data['routes'][0]
                distance_km = route['distance'] / 1000
                duration_min = route['duration'] / 60
                # استخراج مختصات مسیر برای رسم روی نقشه
                path_coords = route['geometry']['coordinates'] # فرمت: [lon, lat]
                return distance_km, duration_min, path_coords
    except:
        pass
    return None, None, None

def haversine(lat1, lon1, lat2, lon2):
    """محاسبه فاصله هوایی (زمانی که سرویس مسیریابی قطع است)"""
    R = 6371
    phi1, phi2 = math.radians(lat1), math.radians(lat2)
    dphi = math.radians(lat2 - lat1)
    dlambda = math.radians(lon2 - lon1)
    a = math.sin(dphi/2)**2 + math.cos(phi1)*math.cos(phi2) * math.sin(dlambda/2)**2
    return R * 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))

# ==========================================
# 3. رابط کاربری (UI)
# ==========================================

st.title("🚗 مسیریاب هوشمند و اطلس ایران")
st.markdown("محاسبه فاصله **زمینی (رانندگی)**، زمان سفر و نمایش مسیر روی نقشه")
st.divider()

# --- انتخاب مبدا و مقصد ---
col1, col2 = st.columns(2)

def city_selector(label, key):
    # لیست شهرها + گزینه تایپ دستی
    options = list(cities_db.keys()) + ["📍 وارد کردن نام شهر دیگر..."]
    selection = st.selectbox(label, options, key=f"sel_{key}")
    
    selected_lat, selected_lon, selected_desc = None, None, None
    city_final_name = selection
    
    if selection == "📍 وارد کردن نام شهر دیگر...":
        manual_name = st.text_input(f"نام شهر {key} را بنویسید:", key=f"txt_{key}")
        if manual_name:
            city_final_name = manual_name
            # جستجو در دیتابیس خودمان ابتدا
            if manual_name in cities_db:
                info = cities_db[manual_name]
                selected_lat, selected_lon = info['lat'], info['lon']
                selected_desc = info['desc']
            else:
                # جستجو در اینترنت
                with st.spinner(f"در حال جستجوی مختصات '{manual_name}'..."):
                    res = get_coordinates_from_name(manual_name)
                    if res:
                        selected_lat, selected_lon, found_desc = res
                        selected_desc = found_desc
                    else:
                        st.error(f"مختصات '{manual_name}' پیدا نشد. لطفا نام را دقیق‌تر بنویسید.")
    else:
        info = cities_db[selection]
        selected_lat, selected_lon = info['lat'], info['lon']
        selected_desc = info['desc']
        
    return city_final_name, selected_lat, selected_lon, selected_desc

with col1:
    st.subheader("مبدأ")
    name1, lat1, lon1, desc1 = city_selector("انتخاب مبدأ:", "origin")

with col2:
    st.subheader("مقصد")
    name2, lat2, lon2, desc2 = city_selector("انتخاب مقصد:", "dest")

# --- دکمه محاسبه ---
if st.button("محاسبه مسیر و نمایش نقشه", type="primary"):
    if lat1 and lat2:
        with st.spinner('در حال محاسبه مسیر جاده‌ای...'):
            dist_km, time_min, path_geo = get_driving_route(lat1, lon1, lat2, lon2)
            
            # --- نمایش نتایج ---
            st.write("---")
            res_col1, res_col2, res_col3 = st.columns(3)
            
            if dist_km:
                # اگر مسیر جاده‌ای پیدا شد
                hours = int(time_min // 60)
                minutes = int(time_min % 60)
                res_col1.metric("مسافت جاده‌ای", f"{int(dist_km):,} کیلومتر")
                res_col2.metric("زمان تقریبی (بدون ترافیک)", f"{hours} ساعت و {minutes} دقیقه")
                res_col3.success("✅ مسیر جاده‌ای پیدا شد")
                
                # آماده‌سازی مسیر برای نقشه
                map_path_data = [{"path": path_geo, "name": "Route", "color": [0, 128, 255]}]
            else:
                # حالت اضطراری (فاصله مستقیم)
                direct_dist = haversine(lat1, lon1, lat2, lon2)
                res_col1.metric("فاصله هوایی (مستقیم)", f"{int(direct_dist):,} کیلومتر")
                res_col2.warning("سرویس جاده‌ای پاسخ نداد")
                res_col3.info("نمایش خط مستقیم")
                # مسیر مستقیم برای نقشه
                map_path_data = [{"path": [[lon1, lat1], [lon2, lat2]], "name": "Direct", "color": [255, 0, 0]}]

            # --- رسم نقشه پیشرفته (PyDeck) ---
            view_state = pdk.ViewState(
                latitude=(lat1 + lat2) / 2,
                longitude=(lon1 + lon2) / 2,
                zoom=5,
                pitch=0
            )
            
            # لایه مسیر (خط)
            layer_path = pdk.Layer(
                "PathLayer",
                map_path_data,
                get_path="path",
                get_color="color",
                width_scale=20,
                width_min_pixels=4,
                pickable=True
            )
            
            # لایه شهرها (نقطه)
            points_data = [
                {"name": name1, "coords": [lon1, lat1], "color": [0, 200, 0]}, # سبز
                {"name": name2, "coords": [lon2, lat2], "color": [200, 0, 0]}  # قرمز
            ]
            layer_points = pdk.Layer(
                "ScatterplotLayer",
                points_data,
                get_position="coords",
                get_color="color",
                get_radius=15000, # شعاع نقطه
                pickable=True
            )
            
            # نمایش نقشه
            st.pydeck_chart(pdk.Deck(
                map_style="mapbox://styles/mapbox/light-v9", # یا استایل ساده
                initial_view_state=view_state,
                layers=[layer_path, layer_points],
                tooltip={"text": "{name}"}
            ))
            
            # --- اطلاعات شهرها ---
            st.write("---")
            c1, c2 = st.columns(2)
            with c1:
                st.info(f"**درباره {name1}:**\n{desc1 or 'اطلاعاتی در دسترس نیست.'}")
            with c2:
                st.info(f"**درباره {name2}:**\n{desc2 or 'اطلاعاتی در دسترس نیست.'}")

    else:
        st.error("لطفاً مبدأ و مقصد را مشخص کنید.")
