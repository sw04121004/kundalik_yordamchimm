const CBU_RATES_URL = 'https://cbu.uz/uz/arkhiv-kursov-valyut/json/'

export async function fetchOfficialCurrencyRates() {
  const response = await fetch(CBU_RATES_URL, { cache: 'no-store' })
  if (!response.ok) throw new Error('Markaziy bank kurslarini olib bo‘lmadi.')

  const rows = await response.json()
  if (!Array.isArray(rows) || rows.length === 0) {
    throw new Error('Markaziy bank kurslar ro‘yxatini qaytarmadi.')
  }

  const rates = rows.map((row) => {
    const nominal = Number(row.Nominal)
    const rate = Number(String(row.Rate).replace(',', '.'))
    if (!row.Ccy || !Number.isFinite(nominal) || nominal <= 0 || !Number.isFinite(rate)) return null
    return {
      code: row.Ccy,
      name: row.CcyNm_UZ || row.CcyNm_EN || row.Ccy,
      rate: rate / nominal,
      date: row.Date,
      change: Number(String(row.Diff || 0).replace(',', '.')) / nominal,
    }
  }).filter(Boolean)

  if (!rates.length) throw new Error('Kurslar formatini o‘qib bo‘lmadi.')
  return [
    { code: 'UZS', name: 'O‘zbekiston so‘mi', rate: 1, date: rows[0].Date, change: 0 },
    ...rates,
  ]
}
