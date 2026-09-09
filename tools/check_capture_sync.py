# -*- coding: utf-8 -*-
"""Гейт фигма-рельсы (v2.17, 09.09): designs/capture.html обязан быть ТЕКУЩИМ
showcase-aggregator.html + ровно два инъекта (capture.js после </style>,
query→localStorage перед <script>). Молчаливый инвариант: устаревший capture.html
тихо льёт в фигму СТАРЫЕ экраны — фреймы заменяются, никто не замечает.

Запуск (перед любым капчером):   python3 tools/check_capture_sync.py
Негативный контроль:             python3 tools/check_capture_sync.py --self-test
  (подсовывает capture.html, собранный из ПРЕДЫДУЩЕГО коммита, и обязан УПАСТЬ).
Код выхода 0 = синхронно, 1 = рассинхрон / инъекты не на месте, 2 = селфтест не упал.
"""
from __future__ import annotations

import subprocess
import sys
from pathlib import Path

# cp1251-консоль Windows роняет print с кириллицей/юникодом — печатаем в utf-8 с заменой
try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / "designs" / "showcase-aggregator.html"
CAP = ROOT / "designs" / "capture.html"
INJECT_JS = '<script src="https://mcp.figma.com/mcp/html-to-design/capture.js"></script>'
INJECT_LS = [
    "<script>",
    "(function(){ try { var q = new URLSearchParams(location.search);",
    "  ['route','style','detail','ctab'].forEach(function(k){ if (q.get(k)) localStorage.setItem('showcase.'+k, q.get(k)); }); } catch (e) {} })();",
    "</script>",
]


def strip_injects(cap_lines: list[str]) -> tuple[list[str], list[str]]:
    """Возвращает (строки без инъектов, список проблем)."""
    problems: list[str] = []
    out = list(cap_lines)
    js_idx = [i for i, l in enumerate(out) if l.strip() == INJECT_JS]
    if len(js_idx) != 1:
        problems.append(f"capture.js inject: найдено {len(js_idx)}, ожидалось 1")
    else:
        i = js_idx[0]
        if i == 0 or out[i - 1].strip() != "</style>":
            problems.append("capture.js inject стоит не сразу после </style>")
        del out[i]
    ls_idx = [i for i in range(len(out) - 3) if [l.strip() for l in out[i:i + 4]] == [l.strip() for l in INJECT_LS]]
    if len(ls_idx) != 1:
        problems.append(f"query→localStorage inject: найдено {len(ls_idx)}, ожидалось 1")
    else:
        i = ls_idx[0]
        if i + 4 >= len(out) or out[i + 4].strip() != "<script>":
            problems.append("query→localStorage inject стоит не перед основным <script>")
        del out[i:i + 4]
    return out, problems


def compare(src_text: str, cap_text: str) -> list[str]:
    src = src_text.split("\n")
    stripped, problems = strip_injects(cap_text.split("\n"))
    if stripped != src:
        n = sum(1 for a, b in zip(stripped, src) if a != b) + abs(len(stripped) - len(src))
        problems.append(f"capture.html != showcase-aggregator.html: {n} строк расходятся (пересобери capture.html из текущего HTML)")
    return problems


def main() -> int:
    if not CAP.exists():
        print("FAIL: designs/capture.html отсутствует — рельса не собрана")
        return 1
    if "--self-test" in sys.argv:
        # негативный контроль: capture.html из предыдущего коммита должен НЕ пройти
        # предыдущая версия САМОГО файла (не HEAD~1 — docs-коммиты файл не меняют)
        log = subprocess.run(["git", "log", "--format=%H", "-n", "2", "--", "designs/showcase-aggregator.html"], capture_output=True, text=True, encoding="utf-8", cwd=ROOT)
        hashes = [h for h in log.stdout.split() if h]
        if len(hashes) < 2:
            print("SELF-TEST SKIP: нет предыдущей версии файла в истории")
            return 0
        old = subprocess.run(["git", "show", f"{hashes[1]}:designs/showcase-aggregator.html"], capture_output=True, text=True, encoding="utf-8", cwd=ROOT)
        if old.returncode != 0:
            print("SELF-TEST SKIP: не читается предыдущая версия")
            return 0
        lines = old.stdout.split("\n")
        style_end = [i for i, l in enumerate(lines) if l.strip() == "</style>"]
        script_start = [i for i, l in enumerate(lines) if l.strip() == "<script>"]
        if len(style_end) != 1 or len(script_start) != 1:
            print("SELF-TEST SKIP: у старой версии не один </style>/<script>")
            return 0
        lines[script_start[0]:script_start[0]] = INJECT_LS
        lines[style_end[0] + 1:style_end[0] + 1] = [INJECT_JS]
        problems = compare(SRC.read_text(encoding="utf-8"), "\n".join(lines))
        if problems:
            print("SELF-TEST OK: устаревший capture.html ПОЙМАН —", problems[-1])
            return 0
        print("SELF-TEST FAIL: устаревший capture.html прошёл проверку — гейт слепой")
        return 2
    problems = compare(SRC.read_text(encoding="utf-8"), CAP.read_text(encoding="utf-8"))
    if problems:
        for p in problems:
            print("FAIL:", p)
        return 1
    print("OK: capture.html = текущий showcase-aggregator.html + 2 инъекта")
    return 0


if __name__ == "__main__":
    sys.exit(main())
