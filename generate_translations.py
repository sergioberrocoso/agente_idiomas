import json
import os
import urllib.request
import sys

GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")
GEMINI_URL = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-3.1-flash-lite:generateContent?key={GEMINI_API_KEY}"

LANG_NAMES = {"de": "German", "fr": "French"}

def call_gemini(prompt):
    body = json.dumps({"contents": [{"parts": [{"text": prompt}]}]}).encode()
    req = urllib.request.Request(GEMINI_URL, data=body, headers={"Content-Type": "application/json"})
    try:
        with urllib.request.urlopen(req, timeout=60) as resp:
            result = json.loads(resp.read().decode("utf-8"))
        text = result.get("candidates", [{}])[0].get("content", {}).get("parts", [{}])[0].get("text", "")
        cleaned = text.strip().removeprefix("```json").removeprefix("```").removesuffix("```").strip()
        return json.loads(cleaned)
    except Exception as e:
        print(f"  Error: {e}")
        return None

def process_file(filepath, lang_code):
    print(f"\nProcessing {filepath} ({LANG_NAMES.get(lang_code, lang_code)})...")
    with open(filepath, "r", encoding="utf-8") as f:
        data = json.load(f)
    
    missing = [entry for entry in data if not entry.get("translation")]
    if not missing:
        print("  All entries already have translations!")
        return
    
    print(f"  {len(missing)} entries missing translations")
    
    batch_size = 100
    total_updated = 0
    
    for start in range(0, len(missing), batch_size):
        batch = missing[start:start + batch_size]
        words = [entry["word"] for entry in batch]
        
        lang_name = LANG_NAMES.get(lang_code, lang_code)
        prompt = f"""Given these {lang_name} words, give the Spanish translation for each. Return ONLY valid JSON like this:
{{{chr(34)}word1{chr(34)}: {chr(34)}translation1{chr(34)}, {chr(34)}word2{chr(34)}: {chr(34)}translation2{chr(34)}, ...}}

Words:
{chr(10).join(words)}"""
        
        print(f"  Batch {start//batch_size + 1}/{(len(missing)-1)//batch_size + 1}: {len(batch)} words...")
        result = call_gemini(prompt)
        
        if result is None:
            print("  Failed, retrying once...")
            result = call_gemini(prompt)
        
        if result:
            batch_updated = 0
            for entry in batch:
                word_lower = entry["word"].lower()
                # Try exact match first, then lowercase
                trans = result.get(entry["word"]) or result.get(word_lower) or ""
                if trans:
                    entry["translation"] = trans
                    batch_updated += 1
            total_updated += batch_updated
            print(f"    Updated {batch_updated} translations")
            
            # Save periodically
            with open(filepath, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
        else:
            print(f"    Failed after retry")
    
    print(f"  Done! Total updated: {total_updated}")

if __name__ == "__main__":
    filepath = sys.argv[1] if len(sys.argv) > 1 else None
    if filepath:
        lang_code = "de" if "german" in filepath.lower() else "fr" if "french" in filepath.lower() else "en"
        process_file(filepath, lang_code)
    else:
        for fp, lc in [("data/german_vocab.json", "de"), ("data/french_vocab.json", "fr")]:
            process_file(fp, lc)
