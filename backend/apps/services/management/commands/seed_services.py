from django.core.management.base import BaseCommand

from apps.services.models import Category, Service

CATEGORIES = [
    {
        "name": "Hisob-kitob",
        "slug": "hisob-kitob",
        "icon": "🧮",
        "order": 1,
        "services": [
            {
                "name": "Foiz hisoblagich",
                "slug": "foiz-hisoblagich",
                "description": "Sondan foizni tez va aniq hisoblang",
                "icon": "🧮",
                "route": "/tools/percent",
            },
            {
                "name": "Oddiy kalkulyator",
                "slug": "oddiy-kalkulyator",
                "description": "Qo‘shish, ayirish, ko‘paytirish, bo‘lish",
                "icon": "➗",
                "route": "/tools/calculator",
            },
            {
                "name": "O‘rtacha qiymat hisoblagich",
                "slug": "ortacha-qiymat",
                "description": "Sonlar ro‘yxatining o‘rtachasini toping",
                "icon": "📊",
                "route": "/tools/average",
            },
            {
                "name": "Tana massa indeksi (BMI)",
                "slug": "bmi-hisoblagich",
                "description": "Bo‘y va vaznga qarab BMI’ni aniqlang",
                "icon": "⚕️",
                "route": "/tools/bmi",
            },
        ],
    },
    {
        "name": "Konvertorlar",
        "slug": "konvertorlar",
        "icon": "🔄",
        "order": 2,
        "services": [
            {
                "name": "Uzunlik konvertori",
                "slug": "uzunlik-konvertori",
                "description": "Metr, kilometr, milya va boshqalar",
                "icon": "📏",
                "route": "/tools/length",
            },
            {
                "name": "Og‘irlik konvertori",
                "slug": "ogirlik-konvertori",
                "description": "Kilogramm, gramm, funt va boshqalar",
                "icon": "⚖️",
                "route": "/tools/weight",
            },
            {
                "name": "Harorat konvertori",
                "slug": "harorat-konvertori",
                "description": "Selsiy, Farengeyt, Kelvin",
                "icon": "🌡️",
                "route": "/tools/temperature",
            },
            {
                "name": "Valyuta konvertori",
                "slug": "valyuta-konvertori",
                "description": "So‘m, dollar, yevro va boshqa valyutalar (taxminiy kurs)",
                "icon": "💱",
                "route": "/tools/currency",
            },
        ],
    },
    {
        "name": "Sana va vaqt",
        "slug": "sana-va-vaqt",
        "icon": "📅",
        "order": 3,
        "services": [
            {
                "name": "Sana farqi",
                "slug": "sana-farqi",
                "description": "Ikki sana orasidagi kun/oy/yil farqi",
                "icon": "📅",
                "route": "/tools/date-diff",
            },
            {
                "name": "Kun hisoblagich",
                "slug": "kun-hisoblagich",
                "description": "Sanaga kun qo‘shish yoki ayirish",
                "icon": "⏱️",
                "route": "/tools/day-counter",
            },
        ],
    },
    {
        "name": "Matn",
        "slug": "matn",
        "icon": "📝",
        "order": 4,
        "services": [
            {
                "name": "So‘z va belgi sanagich",
                "slug": "soz-belgi-sanagich",
                "description": "Matndagi so‘z, belgi va qatorlar sonini bilib oling",
                "icon": "🔤",
                "route": "/tools/text-counter",
            },
            {
                "name": "Katta/kichik harf o‘zgartirish",
                "slug": "harf-ozgartirish",
                "description": "Matnni turli registrga o‘zgartiring",
                "icon": "🔡",
                "route": "/tools/case-converter",
            },
            {
                "name": "Kirill & Lotin Tarjimon",
                "slug": "transliterator",
                "description": "Matnlarni alifbolar orasida ogirish va AI orqali tarjima",
                "icon": "🔄",
                "route": "/tools/transliterator",
            },
            {
                "name": "Matnni tozalash",
                "slug": "matnni-tozalash",
                "description": "Ortiqcha bo‘shliq va qatorlarni tozalang",
                "icon": "🧹",
                "route": "/tools/text-cleaner",
            },
        ],
    },
    {
        "name": "Generatorlar",
        "slug": "generatorlar",
        "icon": "🔐",
        "order": 5,
        "services": [
            {
                "name": "Kuchli parol generatori",
                "slug": "parol-generatori",
                "description": "Xavfsiz va murakkab parol yarating",
                "icon": "🔐",
                "route": "/tools/password-generator",
            },
            {
                "name": "Random son generatori",
                "slug": "random-son-generatori",
                "description": "Berilgan oraliqda tasodifiy son yarating",
                "icon": "🎲",
                "route": "/tools/random-number",
            },
            {
                "name": "QR-kod generatori",
                "slug": "qr-kod-generatori",
                "description": "Matn yoki havoladan QR-kod yarating",
                "icon": "🔳",
                "route": "/tools/qr-code",
            },
        ],
    },
    {
        "name": "Rasm",
        "slug": "rasm",
        "icon": "🖼️",
        "order": 6,
        "services": [
            {
                "name": "Rasm o‘lchamini o‘zgartirish",
                "slug": "rasm-olchamini-ozgartirish",
                "description": "Rasm o‘lchami, formati va hajmini o‘zgartiring",
                "icon": "🖼️",
                "route": "/tools/image-resizer",
            },
            {
                "name": "Fonni o'chirish",
                "slug": "fonni-ochirish",
                "description": "Rasm orqa fonini shaffof (PNG) qilish",
                "icon": "✂️",
                "route": "/tools/image-bg-remove",
            },
            {
                "name": "Rasmni aylantirish",
                "slug": "rasmni-aylantirish",
                "description": "90°, 180° burish va ko'zgu kabi akslantirish",
                "icon": "🔃",
                "route": "/tools/image-rotate",
            },
            {
                "name": "Rasm filtrlari",
                "slug": "rasm-filtrlari",
                "description": "Qora-oq, retro, yorqinlik va kontrast effektlari",
                "icon": "🎨",
                "route": "/tools/image-filters",
            },
        ],
    },
    {
        "name": "Oshxona",
        "slug": "oshxona",
        "icon": "🍳",
        "order": 7,
        "services": [
            {
                "name": "Oshxona AI",
                "slug": "oshxona-ai",
                "description": "Retseptlar va ovqatlanish bo'yicha maslahatlar",
                "icon": "🍳",
                "route": "/kitchen",
            },
        ],
    },
    {
        "name": "Uy",
        "slug": "uy",
        "icon": "🏠",
        "order": 8,
        "services": [
            {
                "name": "Uy AI",
                "slug": "uy-ai",
                "description": "Uyni toza saqlash va boshqarish yordamchisi",
                "icon": "🏠",
                "route": "/home-services",
            },
        ],
    },
    {
        "name": "Vaqt va Unumdorlik",
        "slug": "vaqt-unumdorlik",
        "icon": "⏱️",
        "order": 9,
        "services": [
            {
                "name": "Pomodoro taymer",
                "slug": "pomodoro",
                "description": "Fokuslanib ishlash uchun Pomodoro taymer",
                "icon": "🍅",
                "route": "/tools/pomodoro",
            },
            {
                "name": "Sekundomer va Taymer",
                "slug": "vaqt-trekeri",
                "description": "Kunlik vazifalarga ketgan vaqtni o'lchash",
                "icon": "⏱️",
                "route": "/tools/time-tracker",
            },
            {
                "name": "Odatlar taqvimi",
                "slug": "odatlar-taqvimi",
                "description": "Yangi foydali odatlarni shakllantirish",
                "icon": "✅",
                "route": "/tools/habit-tracker",
            },
            {
                "name": "Maqsadlar doskasi",
                "slug": "maqsadlar-doskasi",
                "description": "Katta maqsadlarni rejalashtirish va monitoring",
                "icon": "🎯",
                "route": "/tools/goal-board",
            },
        ],
    },
    {
        "name": "O'qish",
        "slug": "oqish",
        "icon": "📚",
        "order": 10,
        "services": [
            {
                "name": "O'qish AI",
                "slug": "oqish-ai",
                "description": "Lug'at, testlar va o'qish bo'yicha yordam",
                "icon": "📚",
                "route": "/study",
            },
        ],
    },
    {
        "name": "Hujjatlar",
        "slug": "hujjatlar",
        "icon": "📄",
        "order": 11,
        "services": [
            {
                "name": "Hujjat AI",
                "slug": "hujjat-ai",
                "description": "Hujjatlarni o'qish, tahrirlash va tarjima qilish",
                "icon": "📄",
                "route": "/document",
            },
        ],
    },
    {
        "name": "Moliya",
        "slug": "moliya",
        "icon": "💰",
        "order": 12,
        "services": [
            {
                "name": "Mening pulim",
                "slug": "mening-pulim",
                "description": "Xarajatlarni va byudjetni hisoblash",
                "icon": "💰",
                "route": "/finance",
            },
            {
                "name": "Kredit kalkulyatori",
                "slug": "kredit-kalkulyatori",
                "description": "Kredit oylik to'lovlarini hisoblash",
                "icon": "🏦",
                "route": "/tools/loan-calculator",
            },
            {
                "name": "Oylik maosh hisoblagich",
                "slug": "oylik-hisoblagich",
                "description": "Soliq va ushlanmalarni hisoblash",
                "icon": "💵",
                "route": "/tools/salary-calc",
            },
            {
                "name": "Omonat va Depozit",
                "slug": "omonat-depozit",
                "description": "Omonatdan keladigan foiz daromadini hisoblash",
                "icon": "📈",
                "route": "/tools/deposit-calculator",
            },
        ],
    },
    {
        "name": "Aqlli hisob-kitoblar",
        "slug": "aqlli-hisob-kitob",
        "icon": "🧠",
        "order": 13,
        "services": [
            {
                "name": "Hisoblab ber",
                "slug": "hisoblab-ber",
                "description": "Matnli va murakkab aqlli universal hisoblagich",
                "icon": "🧠",
                "route": "/tools/universal-calc",
            },
            {
                "name": "7-11 sinf kalkulyatori",
                "slug": "maktab-kalkulyatori",
                "description": "Geometriya, algebra formulalari bilan yechuvchi kalkulyator",
                "icon": "📏",
                "route": "/tools/math-calc",
            },
        ],
    },
]


class Command(BaseCommand):
    help = "Seed initial categories and services for Qulay"

    def handle(self, *args, **options):
        for cat_index, cat_data in enumerate(CATEGORIES, start=1):
            services = cat_data.pop("services")
            category, _ = Category.objects.update_or_create(
                slug=cat_data["slug"], defaults=cat_data
            )
            for svc_index, svc_data in enumerate(services, start=1):
                svc_data["order"] = svc_index
                Service.objects.update_or_create(
                    slug=svc_data["slug"], defaults={**svc_data, "category": category}
                )
            cat_data["services"] = services

        self.stdout.write(self.style.SUCCESS("Qulay: kategoriyalar va xizmatlar muvaffaqiyatli yuklandi."))
