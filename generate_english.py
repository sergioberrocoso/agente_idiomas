import json
import os
import urllib.request
import sys

GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")
if not GEMINI_API_KEY:
    print("ERROR: GEMINI_API_KEY env var required")
    sys.exit(1)

GEMINI_URL = "https://generativelanguage.googleapis.com/v1beta/models/gemini-3.1-flash-lite:generateContent?key=" + GEMINI_API_KEY

def call_gemini(prompt):
    body = json.dumps({"contents": [{"parts": [{"text": prompt}]}]}).encode()
    req = urllib.request.Request(GEMINI_URL, data=body, headers={"Content-Type": "application/json"})
    try:
        with urllib.request.urlopen(req, timeout=90) as resp:
            result = json.loads(resp.read().decode("utf-8"))
        text = result["candidates"][0]["content"]["parts"][0]["text"]
        text = text.strip()
        for p in ["```json", "```"]:
            if text.startswith(p): text = text[len(p):]
        if text.endswith("```"): text = text[:-3]
        return json.loads(text.strip())
    except Exception as e:
        print(f"  Error: {e}")
        return None

print("Loading English vocab...")
sys.path.insert(0, ".")
from agent.language_tutor import LanguageTutorAgent
from app import LANG_CONFIG

cfg = LANG_CONFIG["en"]
agent = cfg["agent"]()
if os.path.exists(cfg["vocab_file"]):
    agent.load_core_vocab(cfg["vocab_file"])
if cfg["ngsl_file"] and os.path.exists(cfg["ngsl_file"]):
    agent.load_ngsl_vocab(cfg["ngsl_file"])

vocab = agent.core_vocab
print(f"Total English entries: {len(vocab)}")

# Separate entries with/without needed data
todo = [e for e in vocab if not e.get("translation") and not e.get("sentence")]
print(f"Entries needing data: {len(todo)}")

batch_size = 80
for start in range(0, len(todo), batch_size):
    batch = todo[start:start + batch_size]
    words = [e["word"] for e in batch]
    batch_num = start // batch_size + 1
    total_batches = (len(todo) - 1) // batch_size + 1

    prompt = f"""For each English word, give its Spanish translation AND an example sentence in English.

Return ONLY valid JSON like this:
{{
  "word1": {{"es": "translation1", "en": "Example sentence using word1."}},
  "word2": {{"es": "translation2", "en": "Example sentence using word2."}}
}}

Words:
{chr(10).join(words)}"""

    print(f"Batch {batch_num}/{total_batches} ({len(batch)} words)...")
    result = call_gemini(prompt)

    if result is None:
        print("  Failed, retrying...")
        result = call_gemini(prompt)

    if result:
        updated = 0
        for e in batch:
            w = e["word"]
            data = result.get(w) or result.get(w.lower())
            if data and isinstance(data, dict):
                if data.get("es"): e["translation"] = data["es"]; updated += 1
                if data.get("en"): e["sentence"] = data["en"]
            elif data and isinstance(data, str):
                e["translation"] = data
                updated += 1
        # Save checkpoint
        out = {"source": "core_vocab_500 + NGSL", "entries": vocab}
        with open("data/english_vocab.json", "w", encoding="utf-8") as f:
            json.dump(out, f, indent=2, ensure_ascii=False)
        print(f"  Updated {updated} translations")

# Final save
out = {"source": "core_vocab_500 + NGSL", "entries": vocab}
with open("data/english_vocab.json", "w", encoding="utf-8") as f:
    json.dump(out, f, indent=2, ensure_ascii=False)

missing = [e["word"] for e in vocab if not e.get("translation")]
print(f"\nDone! Missing translations: {len(missing)}")
if missing:
    print(f"Missing: {missing[:20]}...")
