# -*- coding: utf-8 -*-
"""ГЕЙТ: standalone обязан рендериться ОФЛАЙН, без папки assets/ рядом.

Зачем этот файл существует
──────────────────────────
13.07.2026 мы едва не отправили клиенту сборку, в которой половина картинок 404-ится, как
только файл вынут из designs/. Баг прожил незамеченным целую сессию по одной причине:
проверяли standalone ИЗ designs/, где соседняя папка assets/ молча резолвит относительные
пути. Прибор врал, потому что стоял не в той комнате.

Инвариант, который нарушался МОЛЧА:
    в собранном файле не должно остаться НИ ОДНОГО пути к файловой системе,
    по которому рантайм может пойти за картинкой.

Статический инлайнер ловит только ЛИТЕРАЛЬНЫЕ `assets/...` . Но часть путей склеивается в
рантайме (`ASSET + d.img`, `B + pool[i]`, `'library-artist-' + f + '.png'`) — их он не видит.
Для них билд инжектит карту `assets/... -> data:` + перехватчик. Эта проверка сверяет, что
карта ПОКРЫВАЕТ всё, что рантайм способен склеить. Если нет — билд падает.

Запуск:
    python tools/check_standalone_offline.py            # проверить текущую сборку
    python tools/check_standalone_offline.py --selftest # НЕГАТИВНЫЙ КОНТРОЛЬ (см. ниже)

НЕГАТИВНЫЙ КОНТРОЛЬ (обязателен — судья, который не умеет падать, бесполезен):
  --selftest прогоняет проверку по ИСТОРИЧЕСКИ СЛОМАННОЙ сборке (git 1f4da4a — та самая,
  что чуть не уехала клиенту) и по сборке с искусственно выбитой записью карты. Оба прогона
  ОБЯЗАНЫ упасть. Если хоть один проходит — проверке верить нельзя, и selftest сам падает.
"""
from __future__ import annotations

import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DESIGNS = ROOT / "designs"
SOURCE = DESIGNS / "gorod-fm.html"
BUILT = DESIGNS / "gorod-fm-standalone.html"

IMG_EXT = r"(?:png|jpg|jpeg|webp|avif|gif|svg)"

# та самая сборка, которую мы чуть не отправили клиенту (до починки инлайна)
BROKEN_REF = "1f4da4a:designs/gorod-fm-standalone.html"


def _map_keys(built: str) -> set[str]:
    """Ключи карты рантайм-ассетов, которую инжектит билд (assets/... -> data:)."""
    return set(re.findall(r'"(assets/[^"]+?)":"data:', built))


def _strip_injection(built: str) -> str:
    """Вырезать инжект перехватчика.

    Внутри него `assets/...` встречаются ЗАКОННО: это ключи карты (`"assets/x.png":"data:..."`)
    и пояснительные комментарии. Без этого выреза проверка принимала бы собственную карту
    за «неинлайненные ссылки» и падала на исправной сборке — то есть врала бы в другую сторону.
    """
    i = built.find("GOROD-OFFLINE")
    if i < 0:
        return built                                   # инжекта нет (старая сборка) — резать нечего
    start = built.rfind("<script>", 0, i)
    end = built.find("</script>", i)
    if start < 0 or end < 0:
        return built
    return built[:start] + built[end + len("</script>"):]


def _literal_refs(text: str) -> set[str]:
    """Литеральные ссылки на ассеты с расширением: assets/x/y.png"""
    return set(re.findall(r"assets/[A-Za-z0-9/_.\-]+\." + IMG_EXT, text, re.IGNORECASE))


def _runtime_producible(src: str) -> set[str]:
    """Пути, которые исходник СПОСОБЕН склеить в рантайме (то, чего инлайнер не видит).

    Две семьи, обе реально встречаются в gorod-fm.html:
      • база + голое имя:  var ASSET='assets/gorod-fm/'; ... ASSET + d.img,  где d.img='genre-pop.jpg'
      • база + префикс + токен:  'assets/gorod-fm/library-artist-' + a.f + '.png',  где a.f='alsu'
    """
    produced: set[str] = set()

    # базы: литерал 'assets/<dir>/' (заканчивается слэшем, без расширения)
    bases = set(re.findall(r"['\"](assets/[A-Za-z0-9_\-]+/)['\"]", src))
    # голые имена файлов в кавычках: 'genre-pop.jpg' (без слэша)
    bare = set(re.findall(r"['\"]([A-Za-z0-9._\-]+\." + IMG_EXT + r")['\"]", src, re.IGNORECASE))
    for b in bases:
        for name in bare:
            if (DESIGNS / b / name).exists():
                produced.add(b + name)

    # префиксные конкатенации: литерал 'assets/<dir>/<prefix>' БЕЗ расширения (не база)
    partials = set(re.findall(r"['\"(](assets/[A-Za-z0-9_\-]+/[A-Za-z0-9_\-]+-)['\"+]", src))
    for p in partials:
        d = DESIGNS / Path(p).parent
        stem = Path(p).name
        if not d.is_dir():
            continue
        for f in d.iterdir():
            if not f.is_file():
                continue
            if not f.name.startswith(stem):
                continue
            token = f.stem[len(stem):]
            # берём только те файлы, чей ТОКЕН реально встречается в исходнике как значение данных
            if re.search(r"['\"]" + re.escape(token) + r"['\"]", src):
                produced.add("assets/" + f.parent.name + "/" + f.name)

    return produced


def check(built: str, src: str, label: str = "") -> list[str]:
    """Вернуть список нарушений. Пустой список = сборка работает офлайн."""
    problems: list[str] = []

    if "GOROD-OFFLINE" not in built:
        problems.append("нет перехватчика рантайм-ассетов (GOROD-OFFLINE) — рантайм-пути пойдут на диск")
    if "GOROD_OFFLINE_RESOLVE" not in built:
        problems.append(
            "нет резолвера в источнике (GOROD_OFFLINE_RESOLVE) — карточки строятся через innerHTML, "
            "и парсер стартует загрузку <img src> РАНЬШЕ перехватчика: мёртвый запрос + ошибка в консоли"
        )

    # 1) литералы должны быть инлайнены статически — вне инжекта их остаться не должно
    for ref in sorted(_literal_refs(_strip_injection(built))):
        problems.append(f"литеральная ссылка осталась НЕ инлайненной: {ref}")

    # 2) всё, что рантайм способен склеить, обязано быть в карте
    amap = _map_keys(built)
    for path in sorted(_runtime_producible(src)):
        if path not in amap:
            problems.append(f"рантайм склеит путь, которого НЕТ в карте → 404 офлайн: {path}")

    if label and problems:
        problems.insert(0, f"[{label}]")
    return problems


def _report(problems: list[str], where: str) -> int:
    if not problems:
        print(f"OK: {where} — офлайн-целостность подтверждена (карта покрывает все рантайм-пути)")
        return 0
    print(f"FAIL: {where} — сборка НЕ работает офлайн ({len(problems)} нарушений):", file=sys.stderr)
    for p in problems[:25]:
        print("   - " + p, file=sys.stderr)
    if len(problems) > 25:
        print(f"   … и ещё {len(problems) - 25}", file=sys.stderr)
    print("\n   Проверять standalone ТОЛЬКО из папки БЕЗ соседней assets/ — из designs/ пути\n"
          "   резолвятся и маскируют дыру (так она и дожила до отправки клиенту).", file=sys.stderr)
    return 1


def selftest() -> int:
    """Судья обязан уметь падать. Два негативных контроля; оба ДОЛЖНЫ упасть."""
    src = SOURCE.read_text(encoding="utf-8")
    ok = True

    # НК-1: исторически сломанная сборка (та, что чуть не уехала клиенту)
    try:
        broken = subprocess.run(["git", "show", BROKEN_REF], cwd=ROOT, capture_output=True,
                                text=True, encoding="utf-8", check=True).stdout
    except Exception as e:                                    # noqa: BLE001
        print(f"SELFTEST: не смог достать {BROKEN_REF} из git ({e}) — НК-1 пропущен", file=sys.stderr)
        broken = None
    if broken:
        if check(broken, src):
            print("NK-1 PASS: проверка ПАДАЕТ на исторически сломанной сборке (1f4da4a)")
        else:
            print("NK-1 FAIL: проверка ПРОШЛА на заведомо сломанной сборке — ЕЙ ВЕРИТЬ НЕЛЬЗЯ", file=sys.stderr)
            ok = False

    # НК-2: выбиваем одну запись из карты живой сборки — проверка обязана это заметить
    built = BUILT.read_text(encoding="utf-8")
    keys = sorted(_map_keys(built))
    if not keys:
        print("NK-2 FAIL: в сборке пустая карта — нечего выбивать", file=sys.stderr)
        ok = False
    else:
        victim = keys[0]
        holed = re.sub(r'"' + re.escape(victim) + r'":"data:[^"]*",?', "", built, count=1)
        if check(holed, src):
            print(f"NK-2 PASS: проверка ПАДАЕТ, когда из карты выбита запись ({victim})")
        else:
            print(f"NK-2 FAIL: выбил {victim} из карты — проверка НЕ заметила. ЕЙ ВЕРИТЬ НЕЛЬЗЯ", file=sys.stderr)
            ok = False

    if not ok:
        return 1
    # и только теперь — что живая сборка проходит
    return _report(check(built, src), "designs/gorod-fm-standalone.html")


def main() -> int:
    if "--selftest" in sys.argv:
        return selftest()
    if not BUILT.exists():
        print(f"FAIL: нет {BUILT} — сначала собери standalone", file=sys.stderr)
        return 1
    return _report(check(BUILT.read_text(encoding="utf-8"), SOURCE.read_text(encoding="utf-8")),
                   "designs/gorod-fm-standalone.html")


if __name__ == "__main__":
    raise SystemExit(main())
