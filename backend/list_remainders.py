import sqlite3, pathlib

db = pathlib.Path("reminders.db")
if not db.exists():
    print("⚠️ No reminders.db found.")
else:
    con = sqlite3.connect("reminders.db")
    cur = con.cursor()
    cur.execute("SELECT id, title, remind_at, done FROM reminders ORDER BY remind_at;")
    rows = cur.fetchall()
    if not rows:
        print("📭 No reminders scheduled.")
    else:
        print("🕒 Your Reminders:")
        for r in rows:
            print(f"ID={r[0]} | Title={r[1]} | Time={r[2]} | Done={bool(r[3])}")
    con.close()
