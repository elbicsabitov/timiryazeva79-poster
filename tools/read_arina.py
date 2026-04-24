"""Read chat with Arina (realtor) — find eOtinish instructions for Timiryazeva 79 poster.

Borrows Telethon auth from mama-helper (elbics's personal Telegram account, shared session).
Writes relevant messages to design-project/.claude-memory/arina_eotinish.txt.
"""
import asyncio
import os
import re
from pathlib import Path
from datetime import timezone, timedelta
from telethon import TelegramClient

ALMATY_TZ = timezone(timedelta(hours=5))
DESIGN_ROOT = Path(__file__).parent.parent
OUT_DIR = DESIGN_ROOT / ".claude-memory"

# Borrow auth from mama-helper (user's single Telegram account)
MAMA_ROOT = DESIGN_ROOT.parent / "mama-helper"
SESSION_FILE = str(MAMA_ROOT / "data" / "telethon_session")
ENV_PATH = MAMA_ROOT / ".env"

for line in ENV_PATH.read_text(encoding="utf-8").splitlines():
    line = line.strip()
    if line and not line.startswith("#") and "=" in line:
        k, v = line.split("=", 1)
        os.environ.setdefault(k.strip(), v.strip())

API_ID = int(os.environ["TELETHON_API_ID"])
API_HASH = os.environ["TELETHON_API_HASH"]
PHONE = os.environ["TELETHON_PHONE"]

KEYWORDS = re.compile(
    r"eotinish|отиниш|akimat|акимат|эскиз|код город|design.?code|разреш|уведомл|"
    r"баннер|плакат|продаётс|продается|тимиряз|фасад|наружн|реклам",
    re.IGNORECASE,
)


async def main():
    client = TelegramClient(SESSION_FILE, API_ID, API_HASH)
    await client.start(phone=PHONE)

    target = None
    async for d in client.iter_dialogs(limit=1000):
        if not d.is_user or (d.entity and getattr(d.entity, "bot", False)):
            continue
        name = (d.name or "").lower()
        uname = ""
        if d.entity and getattr(d.entity, "username", None):
            uname = d.entity.username.lower()
        if "арин" in name or "arina" in name or "исхаков" in name or "ishakov" in uname:
            target = d
            print(f"FOUND: {d.name} (id={d.id}, @{uname or 'none'})")
            break

    if not target:
        print("Arina not found in first 1000 dialogs")
        await client.disconnect()
        return

    all_msgs = []
    matched_msgs = []
    async for m in client.iter_messages(target.id, limit=2000):
        text = m.text or ""
        who = "ME" if m.out else "ARINA"
        ts = m.date.astimezone(ALMATY_TZ).strftime("%Y-%m-%d %H:%M")
        entry = (ts, who, text, m.id)
        all_msgs.append(entry)
        if text and KEYWORDS.search(text):
            matched_msgs.append(entry)

    OUT_DIR.mkdir(exist_ok=True)
    out = OUT_DIR / "arina_eotinish.txt"

    lines = [f"=== Chat with {target.name} — total scanned: {len(all_msgs)} msgs ===",
             f"=== Matched by keywords (eOtinish/banner/permit/etc): {len(matched_msgs)} ===\n"]

    # Write matched messages with 2 neighbors of context
    by_id = {m[3]: i for i, m in enumerate(all_msgs)}
    included = set()
    for ts, who, text, mid in matched_msgs:
        idx = by_id[mid]
        for j in range(max(0, idx - 2), min(len(all_msgs), idx + 3)):
            included.add(j)

    sorted_idxs = sorted(included)
    prev_idx = None
    for idx in sorted_idxs:
        if prev_idx is not None and idx - prev_idx > 1:
            lines.append("\n... [gap] ...\n")
        ts, who, text, _ = all_msgs[idx]
        marker = "  >>> MATCH" if all_msgs[idx] in matched_msgs else ""
        lines.append(f"[{ts}] {who}:{marker}\n{text}\n" + "-" * 60)
        prev_idx = idx

    out.write_text("\n".join(lines), encoding="utf-8")
    print(f"Saved {len(matched_msgs)} matches (+context) -> {out}")

    await client.disconnect()


if __name__ == "__main__":
    asyncio.run(main())
