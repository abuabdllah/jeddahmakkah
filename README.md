# موقع توصيل الحرمين

## التعديل
1. افتح `config.py` وعدّل: اسم البراند، الدومين، رقم الجوال والواتساب، كود GA4، الأسعار.
2. المحتوى العربي في `content.py` والإنجليزي في `content_en.py` (كل صفحة: العنوان، الوصف، الأقسام، الأسئلة الشائعة).
3. شغّل `python3 build.py` → الموقع الجاهز يتولد في مجلد `public/`.

## الرفع على Netlify
- ارفع المجلد كله على GitHub واربطه بـ Netlify (الإعدادات في `netlify.toml`: publish = public).
- أو اسحب مجلد `public/` مباشرة على Netlify Drop.
- عدّل سطر الـ redirect في `netlify.toml` لو غيّرت الدومين.

## بعد الرفع
- Google Search Console: أضف الدومين وارفع `/sitemap.xml`.
- Google Business Profile واربطه بالموقع.
- GA4: أحداث `whatsapp_click` و`phone_click` و`generate_lead` شغالة تلقائياً بعد إضافة الـ ID.
