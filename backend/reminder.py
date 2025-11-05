import sqlite3
import pathlib
import datetime
import re
import os

# Optional Google Calendar sync
try:
    from google_sync import add_to_google_calendar
    GOOGLE_SYNC = True
except ImportError:
    GOOGLE_SYNC = False

# Use absolute DB path inside backend folder
BASE_DIR = pathlib.Path(__file__).parent.resolve()
DB_PATH = BASE_DIR / "reminders.db"

def _get_conn():
    return sqlite3.connect(str(DB_PATH), timeout=10)

def ensure_table():
    con = _get_conn()
    cur = con.cursor()
    cur.execute("""
    CREATE TABLE IF NOT EXISTS reminders (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT NOT NULL,
        remind_at TEXT NOT NULL,
        done INTEGER DEFAULT 0
    )
    """)
    con.commit()
    con.close()

ensure_table()


# -------------------------------------------------------------------------
# ⏰ TIME PARSER
# -------------------------------------------------------------------------
def _parse_time_from_text(text: str) -> str:
    now = datetime.datetime.now()
    m = re.search(r"(\d{1,2}:\d{2})", text)
    if m:
        hhmm = m.group(1)
        try:
            t = datetime.time.fromisoformat(hhmm)
            dt = datetime.datetime.combine(now.date(), t)
            return dt.isoformat()
        except Exception:
            pass

    m2 = re.search(r"(\d{1,2})(?:\s*)(am|pm)", text)
    if m2:
        hour = int(m2.group(1))
        ampm = m2.group(2).lower()
        if ampm == "pm" and hour != 12:
            hour += 12
        if ampm == "am" and hour == 12:
            hour = 0
        dt = now.replace(hour=hour, minute=0, second=0, microsecond=0)
        return dt.isoformat()

    if "tomorrow" in text:
        dt = (now + datetime.timedelta(days=1)).replace(hour=18, minute=0, second=0, microsecond=0)
        return dt.isoformat()
    return now.replace(hour=18, minute=0, second=0, microsecond=0).isoformat()


# -------------------------------------------------------------------------
# 📝 ADD REMINDER
# -------------------------------------------------------------------------
def add_reminder(text: str) -> str:
    ensure_table()
    t = text.strip()
    t = re.sub(r'(?i)^remind me to\s*', '', t)
    if " at " in t:
        title_part, _ = t.rsplit(" at ", 1)
        title = title_part.strip()
    else:
        title = t if len(t) < 60 else t[:60].strip()
    remind_at = _parse_time_from_text(text.lower())

    con = _get_conn()
    cur = con.cursor()
    cur.execute(
        "INSERT INTO reminders (title, remind_at, done) VALUES (?, ?, ?)",
        (title, remind_at, 0)
    )
    con.commit()
    con.close()

    if GOOGLE_SYNC:
        try:
            add_to_google_calendar(title, remind_at)
        except Exception as e:
            print("⚠️ Google Calendar sync failed:", e)

    return f"✅ Reminder set for '{title}' at {remind_at}"


# -------------------------------------------------------------------------
# 📋 LIST REMINDERS
# -------------------------------------------------------------------------
def list_reminders():
    ensure_table()
    con = _get_conn()
    cur = con.cursor()
    cur.execute("SELECT id, title, remind_at, done FROM reminders ORDER BY remind_at;")
    rows = cur.fetchall()
    con.close()
    return rows


# -------------------------------------------------------------------------
# 🗑️ DELETE REMINDER
# -------------------------------------------------------------------------
def delete_reminder(identifier: str) -> str:
    ensure_table()
    con = _get_conn()
    cur = con.cursor()
    if identifier.isdigit():
        cur.execute("DELETE FROM reminders WHERE id=?", (int(identifier),))
    else:
        cur.execute("DELETE FROM reminders WHERE title LIKE ?", (f"%{identifier}%",))
    count = cur.rowcount
    con.commit()
    con.close()
    if count > 0:
        return f"🗑️ Deleted {count} reminder(s) matching '{identifier}'."
    return f"⚠️ No reminders found for '{identifier}'."
