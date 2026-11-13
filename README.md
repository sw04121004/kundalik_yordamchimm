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

## Environment variables

Backend variables (values intentionally omitted):

- `SECRET_KEY` (required in production)
- `DEBUG` (set to `False` in production)
- `DATABASE_URL` (required in production; local development may use SQLite)
- `ALLOWED_HOSTS`
- `CORS_ALLOWED_ORIGINS`
- `CSRF_TRUSTED_ORIGINS` (if Django CSRF-protected browser flows are used)
- `AI_PROVIDER` (`openai` or `anthropic`)
- `AI_API_KEY` (optional; AI replies require a configured provider key)
- `AI_MODEL` (optional)
- `AI_API_BASE_URL` (optional)
- `OPEN_METEO_API_KEY` (optional; enables the commercial Open-Meteo host)
- `EMAIL_HOST`, `EMAIL_PORT`, `EMAIL_HOST_USER`, `EMAIL_HOST_PASSWORD`, `EMAIL_USE_TLS`, `DEFAULT_FROM_EMAIL` (SMTP settings required for password reset email)

Frontend build variable: `VITE_API_BASE_URL` (backend origin only, without `/api`).

## Deploy steps

1. Copy `backend/.env.example` to `backend/.env`, set local values, install `backend/requirements.txt`, then run `python manage.py migrate`, `python manage.py seed_services`, and `python manage.py runserver` from `backend/`.
2. From `frontend/`, install dependencies with `npm ci`, set `VITE_API_BASE_URL` in `.env.local`, and run `npm run dev`. Run `npm run build` before publishing.
3. For Render, connect the repository and use `render.yaml`; set production secrets and the exact Netlify origin in Render environment settings. Never commit `.env` files.
4. For Netlify, use `netlify.toml`; set `VITE_API_BASE_URL` to the Render origin and trigger a fresh build after changing it.
5. After deployment verify `/health/`, login, and service pages. The service worker caches only static shell files and does not intercept `/api/` requests.

Backend uchun `backend/requirements.txt` dagi paketlarni o‘rnating va `backend/` ichida `python manage.py migrate`, `python manage.py seed_services`, `python manage.py runserver` ni bajaring. Frontend uchun `frontend/` ichida `npm install` va `npm run dev` ni ishga tushiring. Lokal Vite origin’lari CORS’da standart holatda ruxsat etilgan.
