import requests
from bs4 import BeautifulSoup
import html

def search_web(query):
    try:
        url = "https://duckduckgo.com/html/"
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0 Safari/537.36"
        }
        res = requests.post(url, data={"q": query}, headers=headers, timeout=10)
        soup = BeautifulSoup(res.text, "html.parser")
        
        # Try snippets first
        results = soup.select(".result__snippet")[:5]
        if not results:
            # Try titles if no snippets
            results = soup.select(".result__a")[:5]

        snippets = []
        for r in results:
            txt = r.get_text(separator=" ", strip=True)
            txt = html.unescape(txt)
            if txt:
                snippets.append(txt)

        if snippets:
            return "🔍 Here are top results:\n" + "\n".join(f"- {s}" for s in snippets)
        return "⚠️ I couldn’t find reliable info right now. Try asking later."
    except Exception as e:
        return f"⚠️ Search failed: {e}"
