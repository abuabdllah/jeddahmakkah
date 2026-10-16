# -*- coding: utf-8 -*-
# ============================================================
#  إعدادات الموقع — عدّل هنا فقط ثم شغّل: python3 build.py
# ============================================================

SITE = {
    "name": "توصيل الحرمين",                 # اسم البراند (عربي)
    "name_en": "Haramain Transfer",           # اسم البراند (إنجليزي)
    "domain": "https://jeddahmakkah.com",     # بدون / في الآخر
    "phone": "966564612017",                  # للاتصال (صيغة دولية بدون +)
    "phone_display": "056 461 2017",
    "phone_title": "0564612017",              # الرقم اللي يظهر في التايتل (عربي)
    "phone_title_en": "+966 56 461 2017",     # الرقم في التايتل (إنجليزي)
    "whatsapp": "966564612017",               # رقم واتساب (صيغة دولية بدون +)
    "ga4_id": "",                             # مثال: G-XXXXXXX (اتركه فاضي لو مش جاهز)
    "gsc_verification": "",                   # كود التحقق من Search Console (اختياري)
    "updated": "2026-10-16",
}

# أنواع السيارات (الترتيب = ترتيب أعمدة جدول الأسعار)
# key, اسم عربي, وصف عربي, English name, English note
VEHICLES = [
    ("sedan",  "سيدان",              "حتى 4 ركاب و3 حقائب",   "Sedan",          "up to 4 passengers, 3 bags"),
    ("family", "عائلية (ستاريا/H1)", "حتى 7 ركاب مع الحقائب",  "Family (Staria/H1)", "up to 7 passengers with bags"),
    ("van",    "فان (هايس)",         "حتى 12 راكب",            "Van (HiAce)",    "up to 12 passengers"),
    ("gmc",    "GMC يوكن",           "حتى 7 ركاب — فئة فاخرة", "GMC Yukon",      "up to 7 passengers, premium"),
]

# المسارات والأسعار (تبدأ من — بالريال). ⚠️ أسعار مبدئية: راجعها مع المشغّل
ROUTES = {
    "airport_makkah": {"name": "مطار جدة ← مكة", "km": "حوالي 100 كم", "time": "60–90 دقيقة",
                       "name_en": "Jeddah Airport → Makkah", "km_en": "≈ 100 km", "time_en": "60–90 min",
                       "url": "/", "prices": {"sedan": 200, "family": 280, "van": 350, "gmc": 400}},
    "jeddah_makkah":  {"name": "جدة ← مكة", "km": "حوالي 80 كم", "time": "60–75 دقيقة",
                       "name_en": "Jeddah → Makkah", "km_en": "≈ 80 km", "time_en": "60–75 min",
                       "url": "/jeddah-to-makkah/", "prices": {"sedan": 180, "family": 250, "van": 330, "gmc": 380}},
    "makkah_airport": {"name": "مكة ← مطار جدة", "km": "حوالي 100 كم", "time": "60–90 دقيقة",
                       "name_en": "Makkah → Jeddah Airport", "km_en": "≈ 100 km", "time_en": "60–90 min",
                       "url": "/makkah-to-jeddah-airport/", "prices": {"sedan": 200, "family": 280, "van": 350, "gmc": 400}},
    "makkah_jeddah":  {"name": "مكة ← جدة", "km": "حوالي 80 كم", "time": "60–75 دقيقة",
                       "name_en": "Makkah → Jeddah", "km_en": "≈ 80 km", "time_en": "60–75 min",
                       "url": "/makkah-to-jeddah/", "prices": {"sedan": 180, "family": 250, "van": 330, "gmc": 380}},
    "airport_haram":  {"name": "مطار جدة ← الحرم", "km": "حوالي 100 كم", "time": "60–90 دقيقة",
                       "name_en": "Jeddah Airport → Haram", "km_en": "≈ 100 km", "time_en": "60–90 min",
                       "url": "/jeddah-airport-to-haram/", "prices": {"sedan": 200, "family": 280, "van": 350, "gmc": 400}},
    "makkah_madinah": {"name": "مكة ↔ المدينة المنورة", "km": "حوالي 450 كم", "time": "4:30–5 ساعات",
                       "name_en": "Makkah ↔ Madinah", "km_en": "≈ 450 km", "time_en": "4.5–5 hours",
                       "url": "/makkah-to-madinah/", "prices": {"sedan": 550, "family": 700, "van": 900, "gmc": 1000}},
    "makkah_taif":    {"name": "مكة ↔ الطائف", "km": "حوالي 90 كم", "time": "75–90 دقيقة",
                       "name_en": "Makkah ↔ Taif", "km_en": "≈ 90 km", "time_en": "75–90 min",
                       "url": "/makkah-to-taif/", "prices": {"sedan": 250, "family": 330, "van": 420, "gmc": 450}},
}
