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

def process_file(filepath, lang_name, lang_code):
    print(f"\nProcessing {filepath} ({lang_name})...")
    with open(filepath, "r", encoding="utf-8") as f:
        data = json.load(f)

    missing = [e for e in data if not e.get("definition")]
    if not missing:
        print("  All entries already have definitions!")
        return

    print(f"  {len(missing)} entries missing definitions")

    batch_size = 50
    for start in range(0, len(missing), batch_size):
        batch = missing[start:start + batch_size]
        words = [e["word"] for e in batch]
        batch_num = start // batch_size + 1
        total = (len(missing) - 1) // batch_size + 1

        prompt = f"""For each {lang_name} word, provide:
1. A short definition in Spanish
2. The part of speech (sustantivo, verbo, adjetivo, adverbio, preposici\u00f3n, etc.)
3. Phonetic pronunciation in IPA

Return ONLY valid JSON like this:
{{
  "word1": {{"definition": "Definici\u00f3n corta en espa\u00f1ol.", "pos": "sustantivo", "phonetic": "/ipa/"}},
  "word2": {{"definition": "Definici\u00f3n corta en espa\u00f1ol.", "pos": "verbo", "phonetic": "/ipa/"}}
}}

Words:
{chr(10).join(words)}"""

        print(f"  Batch {batch_num}/{total} ({len(batch)} words)...")
        result = call_gemini(prompt)

        if result is None:
            print("    Failed, retrying...")
            result = call_gemini(prompt)

        if result:
            updated = 0
            for e in batch:
                w = e["word"]
                info = result.get(w) or result.get(w.lower())
                if info and isinstance(info, dict):
                    if info.get("definition"): e["definition"] = info["definition"]; updated += 1
                    if info.get("pos"): e["part_of_speech"] = info["pos"]
                    if info.get("phonetic"): e["phonetic"] = info["phonetic"]
            with open(filepath, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
            print(f"    Updated {updated} entries")

    missing_after = [e["word"] for e in data if not e.get("definition")]
    print(f"  Done! Remaining without definition: {len(missing_after)}")

if __name__ == "__main__":
    for fp, ln, lc in [
        ("data/german_vocab.json", "German", "de"),
        ("data/french_vocab.json", "French", "fr"),
    ]:
        process_file(fp, ln, lc)
