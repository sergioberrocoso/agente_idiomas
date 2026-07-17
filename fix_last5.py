import json

de = json.load(open("data/german_vocab.json", encoding="utf-8"))

fixes = {
    "auf jeden/keinen Fal": {"definition": "En cualquier caso / de ninguna manera", "part_of_speech": "expresi\u00f3n", "phonetic": "/a\u028af \u02c8je\u02d0d\u0259n \u02c8fal/"},
    "da(r) (Bsp. darauf": {"definition": "Ah\u00ed (ej. sobre eso)", "part_of_speech": "adverbio", "phonetic": "/da\u02d0\u0251\u032f/"},
    "Geburts-(jahr": {"definition": "A\u00f1o de nacimiento", "part_of_speech": "sustantivo", "phonetic": "/\u0261\u0259\u02c8b\u028a\u0281tsja\u02d0\u0251\u032f/"},
    "wer (wen": {"definition": "Qui\u00e9n", "part_of_speech": "pronombre", "phonetic": "/ve\u02d0\u0251\u032f/"},
    "zur\u00fcck- (fahren": {"definition": "Volver (conducir de vuelta)", "part_of_speech": "verbo", "phonetic": "/ts\u028a\u02c8\u0281\u028fkza\u02d0\u032f\u0259n/"},
}

for e in de:
    if not e.get("definition") and e["word"] in fixes:
        e["definition"] = fixes[e["word"]]["definition"]
        e["part_of_speech"] = fixes[e["word"]]["part_of_speech"]
        e["phonetic"] = fixes[e["word"]]["phonetic"]

with open("data/german_vocab.json", "w", encoding="utf-8") as f:
    json.dump(de, f, indent=2, ensure_ascii=False)

still = sum(1 for e in de if not e.get("definition"))
print(f"Remaining without definition: {still}")
