"""Read chat 'обучение' — find discussion of a kinolog (dog handler) website.

Borrows Telethon auth from mama-helper (shared personal Telegram account).
Writes relevant messages to design-project/.claude-memory/obuchenie_kinolog.txt (gitignored).
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
    r"сайт|лендинг|landing|web|веб|страниц|structure|структур|"
    r"кинолог|dog.?trainer|дресс|послушани|щенок|щенк|порода|"
    r"дизайн|макет|прототип|figma|фигма|"
    r"услуг|прайс|цен|тариф|отзыв|testim|"
    r"курс|программ|занят|тренировк|консульт",
    re.IGNORECASE,
)


async def find_chat(client, needle: str):
    """Find a dialog by name substring, case-insensitive. Works for groups/channels/users."""
    needle = needle.lower()
    matches = []
    async for d in client.iter_dialogs(limit=2000):
        name = (d.name or "").lower()
        uname = ""
        if d.entity and getattr(d.entity, "username", None):
            uname = d.entity.username.lower()
        if needle in name or needle in uname:
            matches.append(d)
    return matches


async def main():
    client = TelegramClient(SESSION_FILE, API_ID, API_HASH)
    await client.start(phone=PHONE)

    candidates = await find_chat(client, "обучение")
    candidates += await find_chat(client, "kinolog")
    candidates += await find_chat(client, "кинолог")

    seen = set()
    unique = []
    for d in candidates:
        if d.id not in seen:
            seen.add(d.id)
            unique.append(d)

    print(f"Found {len(unique)} candidate chats:")
    for d in unique:
        kind = "USER" if d.is_user else ("GROUP" if d.is_group else ("CHANNEL" if d.is_channel else "?"))
        print(f"  [{kind}] id={d.id} name={d.name!r}")

    if not unique:
        print("No matches. Dumping first 50 dialogs for inspection:")
        async for d in client.iter_dialogs(limit=50):
            print(f"  id={d.id} name={d.name!r}")
        await client.disconnect()
        return

    OUT_DIR.mkdir(exist_ok=True)
    out = OUT_DIR / "obuchenie_kinolog.txt"
    lines = []

    for target in unique:
        all_msgs = []
        matched_msgs = []
        async for m in client.iter_messages(target.id, limit=3000):
            text = m.text or ""
            who = "ME" if m.out else (getattr(m.sender, "first_name", None) or f"id{m.sender_id}")
            ts = m.date.astimezone(ALMATY_TZ).strftime("%Y-%m-%d %H:%M")
            entry = (ts, who, text, m.id)
            all_msgs.append(entry)
            if text and KEYWORDS.search(text):
                matched_msgs.append(entry)

        lines.append(f"\n{'='*72}")
        lines.append(f"Chat: {target.name} (id={target.id})")
        lines.append(f"Scanned: {len(all_msgs)} msgs — matched: {len(matched_msgs)}")
        lines.append(f"{'='*72}\n")

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
    print(f"\nSaved -> {out} ({out.stat().st_size} bytes)")

    await client.disconnect()


if __name__ == "__main__":
    asyncio.run(main())
