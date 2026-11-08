# Kundalik Yordamchi

Vue 3/Vite frontend va Django REST Framework backend’dan iborat kundalik yordamchi ilova.

## Render: backend

1. GitHub repository’ni Render’ga ulang va `render.yaml` Blueprint’ni deploy qiling.
2. Blueprint backend papkasida backend service va PostgreSQL bazasini yaratadi. SECRET_KEY Render tomonidan yaratiladi; CORS_ALLOWED_ORIGINS qiymatiga production Netlify domenining aniq HTTPS manzilini (masalan, https://sayt-nomi.netlify.app) kiriting, localhost emas. Mavjud Render service uchun sync: false qiymat Blueprint sync orqali yangilanmaydi; uni Render Dashboard'da sozlang.
3. Backend deploy bo‘lgach, Render service URL’ini yozib oling. API manzili shu URL’ning oxiriga `/api` qo‘shish orqali hosil bo‘ladi.
4. Netlify site URL’i chiqqach, Render service’ning `CORS_ALLOWED_ORIGINS` qiymatiga uni kiriting. Bir nechta origin vergul bilan ajratiladi; masalan: `https://site-name.netlify.app,https://example.uz`.
5. AI yordamchidan foydalanish uchun Render’da `AI_PROVIDER` va `AI_API_KEY` ni, ixtiyoriy ravishda `AI_MODEL` va `AI_API_BASE_URL` ni sozlang.

## Netlify: frontend

1. Shu GitHub repository’dan Netlify site yarating. Root’dagi `netlify.toml` `frontend/` base directory, `npm run build` build command va `dist` publish directory’ni belgilaydi.
2. Netlify site environment variables’ga `VITE_API_BASE_URL` qo‘shing. Qiymat Render service’ning to‘liq origin’i bo‘lsin, `/api` qo‘shmang; masalan: `https://kundalik-yordamchimm.onrender.com`.
3. Deploy qiling. `netlify.toml` dagi SPA redirect frontend yo‘llarini `index.html` ga qayta yo‘naltiradi.

Frontend’dagi `VITE_API_BASE_URL` build vaqtida o‘qiladi. Uni o‘zgartirgandan keyin Netlify’da qayta deploy qiling. Backend’da CORS origin’larini yangilagandan keyin Render service’ni redeploy/restart qiling.

## Mahalliy ishga tushirish

Backend uchun `backend/requirements.txt` dagi paketlarni o‘rnating va `backend/` ichida `python manage.py migrate`, `python manage.py seed_services`, `python manage.py runserver` ni bajaring. Frontend uchun `frontend/` ichida `npm install` va `npm run dev` ni ishga tushiring. Lokal Vite origin’lari CORS’da standart holatda ruxsat etilgan.
