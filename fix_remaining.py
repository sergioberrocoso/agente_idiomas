import json, os, urllib.request

key = os.environ.get("GEMINI_API_KEY")

de = json.load(open("data/german_vocab.json", encoding="utf-8"))
remaining = [e for e in de if not e.get("definition")]
if not remaining:
    print("All German entries have definitions")
    exit()

words = [e["word"] for e in remaining]
print(f"Remaining German words without definition: {len(words)}")

prompt = """For each German word, give definition in Spanish, part of speech, and IPA phonetics.
Return ONLY valid JSON: {"word": {"definition": "...", "pos": "...", "phonetic": "/ipa/"}}

Words:
""" + "\n".join(words)

url = "https://generativelanguage.googleapis.com/v1beta/models/gemini-3.1-flash-lite:generateContent?key=" + key
body = json.dumps({"contents": [{"parts": [{"text": prompt}]}]}).encode()
req = urllib.request.Request(url, data=body, headers={"Content-Type": "application/json"})
with urllib.request.urlopen(req, timeout=90) as resp:
    result = json.loads(resp.read().decode("utf-8"))

text = result["candidates"][0]["content"]["parts"][0]["text"]
text = text.strip()
for p in ["```json", "```"]:
    if text.startswith(p): text = text[len(p):]
if text.endswith("```"): text = text[:-3]
text = text.strip()

parsed = json.loads(text)
for e in de:
    if not e.get("definition"):
        w = e["word"]
        info = parsed.get(w) or parsed.get(w.lower())
        if info:
            if info.get("definition"): e["definition"] = info["definition"]
            if info.get("pos"): e["part_of_speech"] = info["pos"]
            if info.get("phonetic"): e["phonetic"] = info["phonetic"]

with open("data/german_vocab.json", "w", encoding="utf-8") as f:
    json.dump(de, f, indent=2, ensure_ascii=False)

still = sum(1 for e in de if not e.get("definition"))
print(f"Remaining without definition: {still}")
