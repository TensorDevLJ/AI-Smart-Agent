import os, requests
def get_latest_news():
    api_key = os.environ.get("NEWSAPI_KEY")
    if not api_key:
        return "ℹ️ News API key not found. Set NEWSAPI_KEY in environment to enable news."
    url = f"https://newsapi.org/v2/top-headlines?country=in&pageSize=5&apiKey={api_key}"
    try:
        r = requests.get(url, timeout=10)
        j = r.json()
        if "articles" in j:
            titles = [a.get("title","").strip() for a in j["articles"][:5]]
            return "🗞️ Top headlines:\n" + "\n".join(f"- {t}" for t in titles)
        return "⚠️ Couldn't fetch news."
    except Exception as e:
        return f"⚠️ News fetch failed: {e}"
