import os, re, sys

# Simple deep scan for hard‑coded Uzbek text in Vue/JS files

def is_uzbek_literal(line: str) -> bool:
    # Detect Cyrillic characters (common in Uzbek) or Uzbek Latin letters with special chars
    if re.search(r"[\u0400-\u04FF]", line):
        return True
    # Detect Uzbek Latin words that are likely not translated (e.g., "Chiqish", "Qayta", "Saqlash")
    uz_words = [
        "Chiqish",
        "Kirish",
        "Ro'yhat",
        "Parol",
        "Saqlash",
        "Qayta",
        "Xatolik",
        "Muvaffaqiyat",
        "Qidiruv",
        "Moslamalar",
        "Profil",
    ]
    for w in uz_words:
        if w in line:
            return True
    return False

def line_ignored(line: str) -> bool:
    # If the line already uses translation function, ignore
    return bool(re.search(r"\b(t|\$t|useToolText)\s*\(", line))

def scan_file(filepath: str):
    with open(filepath, "r", encoding="utf-8", errors="ignore") as f:
        for i, line in enumerate(f, start=1):
            if is_uzbek_literal(line) and not line_ignored(line):
                print(f"{filepath}:{i}: {line.strip()}")

def main():
    root = os.getcwd()
    for dirpath, _, filenames in os.walk(root):
        for name in filenames:
            if name.endswith(('.vue', '.js', '.ts')):
                filepath = os.path.join(dirpath, name)
                scan_file(filepath)

if __name__ == "__main__":
    main()
