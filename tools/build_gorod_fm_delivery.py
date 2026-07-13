# -*- coding: utf-8 -*-
"""Собрать поставку «Города ФМ»: 2 standalone-версии + README + zip.

Почему README ГЕНЕРИРУЕТСЯ, а не написан руками
───────────────────────────────────────────────
13.07.2026 архив уехал в Saved с README, который врал: там было «карусель 6 станций РМГ»
и «ждём частоту Города», хотя станции к тому моменту были уже свои и цифровые, а частот
у них нет. Сами сборки были верные — врал сопроводительный текст. Классика: рукописный
дубль данных отстаёт от данных.

Лечим не проверкой, а устранением дубля: список станций README берёт ИЗ СОБРАННОГО ФАЙЛА.
Соврать про станции он теперь не может — их неоткуда взять, кроме сборки.
Поверх стоит гейт на чужие бренды: если они всплывут в станциях — падаем.

Запуск:  python tools/build_gorod_fm_delivery.py [YYYY-MM-DD]
"""
from __future__ import annotations

import io
import os
import re
import shutil
import sys
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DESIGNS = ROOT / "designs"
BUILT = DESIGNS / "gorod-fm-standalone.html"

# бренды соседних станций холдинга: их в продукте «Города» быть не должно (owner 13.07)
FOREIGN_BRANDS = ("Русское Радио", "ХИТ FM", "DFM", "MAXIMUM", "Monte Carlo", "Авторадио")


def stations_from_build(built: str) -> list[str]:
    """Достать НАЗВАНИЯ станций из собранного файла — единственный источник правды."""
    names = re.findall(r"\{id:'[a-z]+',\s*name:'([^']+)'", built)
    return [n.strip() for n in names]


def readme_text(stations: list[str]) -> str:
    lines = " · ".join(stations)
    return (
        "Город ФМ — главная (standalone)\r\n"
        "\r\n"
        "Два файла, оба самодостаточные: открыть двойным кликом, интернет не нужен,\r\n"
        "все картинки зашиты внутрь файла.\r\n"
        "\r\n"
        "  gorod-fm-standalone.html         — версия с монограммами (плейсхолдеры)\r\n"
        "  gorod-fm-images-standalone.html  — та же витрина, заполненная тематическими фото\r\n"
        "\r\n"
        "Что на главной:\r\n"
        f"  • карусель цифровых станций: {lines}.\r\n"
        "    Центральная = та, что играет сейчас (♥ / пауза / далее). Частот FM нет — каналы цифровые.\r\n"
        "  • живой плеер снизу (LIVE, без перемотки)\r\n"
        "  • витрина: друзья, жанры, подборки, редакция, новинки, чарты, коллекции,\r\n"
        "    исполнители, программы — у каждой карточки ♥ и ＋\r\n"
        "  • поиск: клавиша / или Ctrl+K\r\n"
        "  • справа — ИИ-ДИДЖЕЙ станции: рассказывает про то, что играет, каждые ~10 секунд.\r\n"
        "    Переключи станцию — сменится диджей. Спросить его можно прямо в поле.\r\n"
        "    Второй режим композера — «Мой диджей», собран из вашего вкуса.\r\n"
        "  • мобильный вид — просто сузить окно (<768px)\r\n"
        "\r\n"
        "Контент демонстрационный, реплики диджея сценарные.\r\n"
        "От клиента нужны: логотип «Города», арт каналов и ссылки на живые потоки.\r\n"
    )


def main() -> int:
    date = sys.argv[1] if len(sys.argv) > 1 else "2026-07-13"
    out = ROOT / "deliverables" / date
    out.mkdir(parents=True, exist_ok=True)

    if not BUILT.exists():
        print(f"FAIL: нет {BUILT} — сначала собери standalone", file=sys.stderr)
        return 1
    built = io.open(BUILT, encoding="utf-8", newline="").read()

    # гейты: без них поставка не имеет права уехать
    if "GOROD-OFFLINE" not in built:
        print("FAIL: в сборке нет офлайн-перехватчика — картинки 404-нутся у клиента", file=sys.stderr)
        return 1
    if "GOROD_OFFLINE_RESOLVE" not in built:
        print("FAIL: в сборке нет резолвера в источнике — карусель успеет сходить на диск", file=sys.stderr)
        return 1

    stations = stations_from_build(built)
    if not stations:
        print("FAIL: не смог прочитать станции из сборки — README врал бы вслепую", file=sys.stderr)
        return 1
    leaked = [b for b in FOREIGN_BRANDS if any(b in s for s in stations)]
    if leaked:
        print(f"FAIL: в станциях чужие бренды: {leaked} — owner просил только свои цифровые", file=sys.stderr)
        return 1

    plain = out / "gorod-fm-standalone.html"
    shutil.copyfile(BUILT, plain)

    # версия с фото: тот же флаг, что и у dev-варианта — ПОСЛЕ перехватчика, ДО app-скриптов
    nl = "\r\n" if "\r\n" in built else "\n"
    flag = ('<script>window.GOROD_PHOTOS = true; /* photos variant - thematic art instead of monograms */'
            '</script>' + nl)
    i = built.index("  <style>")
    photos = out / "gorod-fm-images-standalone.html"
    io.open(photos, "w", encoding="utf-8", newline="").write(built[:i] + flag + built[i:])

    readme = out / "README-Gorod-FM.txt"
    io.open(readme, "w", encoding="utf-8-sig", newline="").write(readme_text(stations))

    zip_path = out / f"gorod-fm-standalone-{date}.zip"
    with zipfile.ZipFile(zip_path, "w", compression=zipfile.ZIP_DEFLATED, compresslevel=9) as z:
        for p in (plain, photos, readme):
            z.write(p, p.name)

    print(f"станции из сборки ({len(stations)}): " + " | ".join(stations))
    for p in (plain, photos, readme, zip_path):
        print("%9d bytes  %s" % (os.path.getsize(p), p.name))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
