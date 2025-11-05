import os
import requests
import textwrap

# Load provider from .env
USE = os.environ.get("USE_PROVIDER", "HUGGINGFACE").upper().strip()


def llm_reply(prompt: str) -> str:
    """
    Unified LLM client supporting GROQ and HUGGINGFACE.
    Select provider using USE_PROVIDER in .env
    """

    # ---------------- GROQ PROVIDER ----------------
        # ---------------- GROQ ----------------
    if USE == "GROQ":
        key = os.environ.get("GROQ_API_KEY")
        if not key:
            return "⚠️ Groq key not found. Set GROQ_API_KEY in .env to enable Groq."

        try:
            import requests, json
            headers = {
                "Authorization": f"Bearer {key}",
                "Content-Type": "application/json"
            }

            # ✅ Updated models (as of Nov 2025)
            model_list = ["llama-3.1-70b-versatile", "llama-3.1-8b-instant"]
            model = model_list[0]

            for m in model_list:
                payload = {
                    "model": m,
                    "messages": [
                        {"role": "system", "content": "You are a helpful AI assistant."},
                        {"role": "user", "content": prompt}
                    ],
                    "temperature": 0.7,
                    "max_tokens": 512
                }

                r = requests.post("https://api.groq.com/openai/v1/chat/completions",
                                  headers=headers, json=payload, timeout=30)
                data = r.json()

                # If model works — return result
                if "choices" in data and len(data["choices"]) > 0:
                    print(f"🧠 Groq model: {m}")
                    return data["choices"][0]["message"]["content"].strip()

                # If model decommissioned, try next
                if "error" in data and "decommissioned" in data["error"]["message"].lower():
                    print(f"⚠️ {m} is decommissioned, trying next model...")
                    continue

                # Other error? stop.
                if "error" in data:
                    return f"⚠️ Groq error: {data['error']['message']}"

            return "⚠️ All Groq models failed or deprecated."

        except Exception as e:
            import traceback
            traceback.print_exc()
            return f"⚠️ Groq request failed: {e}"


    # ---------------- HUGGINGFACE PROVIDER ----------------
    if USE == "HUGGINGFACE":
        key = os.environ.get("HUGGINGFACE_API_KEY")
        if not key:
            return ("ℹ️ No external LLM provider configured. "
                    "To enable cloud LLMs set HUGGINGFACE_API_KEY or GROQ_API_KEY.\n"
                    "Fallback: try asking simple factual questions or enable a provider.")

        try:
            headers = {"Authorization": f"Bearer {key}"}

            # ✅ Default open-source model on Hugging Face
            api_url = "https://api-inference.huggingface.co/models/mistralai/Mistral-7B-Instruct-v0.2"
            payload = {"inputs": prompt, "options": {"wait_for_model": True}}

            r = requests.post(api_url, headers=headers, json=payload, timeout=30)
            jr = r.json()

            if isinstance(jr, dict) and "error" in jr:
                return f"⚠️ HuggingFace model error: {jr['error']}"
            if isinstance(jr, list) and len(jr) and "generated_text" in jr[0]:
                return jr[0]["generated_text"]

            return str(jr)

        except Exception as e:
            return f"⚠️ HuggingFace request failed: {e}"

    # ---------------- FALLBACK ----------------
    return "⚠️ No valid LLM provider selected. Set USE_PROVIDER=GROQ or HUGGINGFACE in .env"
