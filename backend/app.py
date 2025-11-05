from dotenv import load_dotenv
load_dotenv()
import os
print("✅ Environment variables loaded")
print("COHERE_API_KEY:", os.environ.get("COHERE_API_KEY"))

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import threading, time, sqlite3
from datetime import datetime

# Local imports
from reminder import add_reminder, list_reminders, delete_reminder
from web_search import search_web
from news_fetcher import get_latest_news
from fun_facts import get_random_fact
from llm_client import llm_reply

app = FastAPI(title="Smart Agent API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

class AskRequest(BaseModel):
    message: str


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/ask")
async def ask(req: AskRequest):
    text = req.message.strip().lower()

    # ---------------- Reminder Commands ----------------
    if text.startswith("remind me") or "remind me" in text:
        resp = add_reminder(text)
        return {"reply": resp}

    if "show reminders" in text or "list reminders" in text:
        rows = list_reminders()
        if not rows:
            return {"reply": "📭 You have no reminders set."}
        msg = "🕒 Your Reminders:\n" + "\n".join(
            [f"ID={r[0]} | Title={r[1]} | Time={r[2]} | Done={bool(r[3])}" for r in rows]
        )
        return {"reply": msg}

    if "delete reminder" in text or "cancel reminder" in text:
        parts = text.split()
        if parts[-1].isdigit():
            identifier = parts[-1]
        else:
            identifier = text.replace("delete reminder", "").replace("cancel reminder", "").strip()
        resp = delete_reminder(identifier)
        return {"reply": resp}

    # ---------------- Web Search ----------------
    if text.startswith("search ") or text.startswith("what ") or "search" in text:
        resp = search_web(req.message)
        return {"reply": resp}

    # ---------------- News ----------------
    if "news" in text or "happening" in text:
        resp = get_latest_news()
        return {"reply": resp}

    # ---------------- Fun Facts ----------------
    if "bored" in text or "i feel bored" in text or "fun" in text:
        resp = get_random_fact()
        return {"reply": resp}

    # ---------------- LLM Reply (Fallback) ----------------
    resp = llm_reply(req.message)
    return {"reply": resp}


# -------------------------------------------------------------------------
# 🕐 Background thread to trigger reminders
# -------------------------------------------------------------------------
def reminder_watcher():
    while True:
        try:
            rows = list_reminders()
            now = datetime.now().replace(second=0, microsecond=0)
            for r in rows:
                remind_time = datetime.fromisoformat(r[2])
                if remind_time <= now and not r[3]:
                    print(f"🔔 Reminder: {r[1]} (ID={r[0]})")
                    # mark done so it doesn’t trigger again
                    con = sqlite3.connect("reminders.db")
                    cur = con.cursor()
                    cur.execute("UPDATE reminders SET done=1 WHERE id=?", (r[0],))
                    con.commit()
                    con.close()
        except Exception as e:
            print("⚠️ Reminder watcher error:", e)
        time.sleep(60)  # check every minute


# Start the watcher when the backend starts
threading.Thread(target=reminder_watcher, daemon=True).start()

print("✅ Smart Agent backend running with reminders, notifications & chat features!")
