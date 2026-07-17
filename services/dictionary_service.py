import json
import os
import time
from pathlib import Path
from urllib.parse import urlencode
from urllib.request import urlopen, Request
from urllib.error import HTTPError, URLError

CACHE_PATH = Path("data/definitions_cache.json")
DICT_API_URL_EN = "https://api.dictionaryapi.dev/api/v2/entries/en/{word}"
DICT_API_URL_DE = "https://api.dictionaryapi.dev/api/v2/entries/de/{word}"
DICT_API_URL_FR = "https://api.dictionaryapi.dev/api/v2/entries/fr/{word}"
DEEPL_API_KEY = os.environ.get("DEEPL_API_KEY") or ""


class DictionaryService:
    def __init__(self):
        self.cache = {}
        self._load_cache()

    def _load_cache(self):
        if CACHE_PATH.exists():
            with open(CACHE_PATH, "r", encoding="utf-8") as f:
                self.cache = json.load(f)

    def _save_cache(self):
        CACHE_PATH.parent.mkdir(parents=True, exist_ok=True)
        with open(CACHE_PATH, "w", encoding="utf-8") as f:
            json.dump(self.cache, f, indent=2, ensure_ascii=False)

    def _fetch_translation(self, word: str, source: str = "EN", target: str = "ES") -> str:
        try:
            body = urlencode({"text": word, "source_lang": source, "target_lang": target}).encode()
            req = Request(
                "https://api-free.deepl.com/v2/translate",
                data=body,
                headers={
                    "Authorization": f"DeepL-Auth-Key {DEEPL_API_KEY}",
                    "Content-Type": "application/x-www-form-urlencoded"
                }
            )
            with urlopen(req, timeout=10) as resp:
                result = json.loads(resp.read().decode("utf-8"))
            return result.get("translations", [{}])[0].get("text", "")
        except Exception:
            return ""

    def fetch_definition(self, word: str, retries=2, language: str = "en"):
        word_lower = word.lower().strip()
        if word_lower in self.cache:
            return self.cache[word_lower]

        result = {"definition": "", "example": "", "part_of_speech": ""}
        lang_lower = language.lower() if language else "en"
        is_de = lang_lower in ("german", "deutsche", "deutsch", "de")
        is_fr = lang_lower in ("french", "français", "francais", "fr")
        if is_fr:
            dict_url = DICT_API_URL_FR
        elif is_de:
            dict_url = DICT_API_URL_DE
        else:
            dict_url = DICT_API_URL_EN

        for attempt in range(retries):
            try:
                req = Request(dict_url.format(word=word_lower), headers={"User-Agent": "LanguageTutor/1.0"})
                with urlopen(req, timeout=10) as resp:
                    data = json.loads(resp.read().decode("utf-8"))
                if data and isinstance(data, list):
                    entry = data[0]
                    phonetic = entry.get("phonetic", "")
                    if not phonetic:
                        for p in entry.get("phonetics", []):
                            if p.get("text"):
                                phonetic = p["text"]
                                break
                    result["phonetic"] = phonetic
                    meaning = entry["meanings"][0]
                    def_data = meaning["definitions"][0]
                    result["definition"] = def_data.get("definition", "")
                    result["example"] = def_data.get("example", "")
                    result["part_of_speech"] = meaning.get("partOfSpeech", "")
                break
            except (HTTPError, URLError, ValueError, json.JSONDecodeError, IndexError, KeyError):
                if attempt < retries - 1:
                    time.sleep(1)

        source_lang = "FR" if is_fr else ("DE" if is_de else "EN")
        translation = self._fetch_translation(word_lower, source=source_lang)
        if translation:
            result["spanish"] = translation

        self.cache[word_lower] = result
        self._save_cache()
        return result
