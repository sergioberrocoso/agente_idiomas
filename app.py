import json
import os
from flask import Flask, jsonify, render_template, request
from agent.language_tutor import LanguageTutorAgent
from services.dictionary_service import DictionaryService
from services.ai_tutor_service import AITutorService

app = Flask(__name__)

agents = {}
dictionary = DictionaryService()
tutor = AITutorService()

LANG_CONFIG = {
    "en": {
        "agent": lambda: LanguageTutorAgent(language="English"),
        "vocab_file": "data/core_vocab_500.json",
        "ngsl_file": "data/NGSL_1.2_lemmatized_for_teaching.csv",
        "missions_file": "data/missions.json",
        "extra_vocab_file": "data/extra_vocab.json",
    },
    "de": {
        "agent": lambda: LanguageTutorAgent(language="German"),
        "vocab_file": "data/german_vocab.json",
        "ngsl_file": None,
        "missions_file": "data/missions_de.json",
        "extra_vocab_file": "data/extra_vocab_de.json",
    },
    "fr": {
        "agent": lambda: LanguageTutorAgent(language="French"),
        "vocab_file": "data/french_vocab.json",
        "ngsl_file": None,
        "missions_file": "data/missions_fr.json",
        "extra_vocab_file": "data/extra_vocab_fr.json",
    },
}


def get_agent(lang):
    lang = (lang or "en").lower()
    if lang not in agents:
        cfg = LANG_CONFIG[lang] if lang in LANG_CONFIG else LANG_CONFIG["en"]
        agent = cfg["agent"]()
        if os.path.exists(cfg["vocab_file"]):
            agent.load_core_vocab(cfg["vocab_file"])
        if cfg["ngsl_file"] and os.path.exists(cfg["ngsl_file"]):
            agent.load_ngsl_vocab(cfg["ngsl_file"])
        if os.path.exists(cfg["missions_file"]):
            agent.load_missions(cfg["missions_file"])
        agents[lang] = agent
    return agents[lang]


def load_extra_vocab(mission_id, lang):
    cfg = LANG_CONFIG.get(lang, LANG_CONFIG["en"])
    path = cfg["extra_vocab_file"]
    if not os.path.exists(path):
        return []
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)
    return data.get(mission_id, [])


def save_extra_vocab(mission_id, entries, lang):
    cfg = LANG_CONFIG.get(lang, LANG_CONFIG["en"])
    path = cfg["extra_vocab_file"]
    data = {}
    if os.path.exists(path):
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
    data[mission_id] = entries
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)


def get_lang():
    return request.args.get("lang", "en")


@app.route("/")
def index():
    lang = get_lang()
    agent = get_agent(lang)
    return render_template("index.html", missions=agent.missions, lang=lang)


@app.route("/api/vocab")
def all_vocab():
    lang = get_lang()
    agent = get_agent(lang)
    vocab = list(agent.core_vocab)
    extra = load_extra_vocab("__all__", lang)
    existing_words = {w["word"] for w in vocab}
    for entry in extra:
        if entry["word"] not in existing_words:
            vocab.append(entry)
            existing_words.add(entry["word"])
    return jsonify(vocab)


@app.route("/api/vocab/<mission_id>")
def vocab_by_mission(mission_id):
    lang = get_lang()
    agent = get_agent(lang)
    try:
        agent.select_mission(mission_id)
        vocab = agent.get_mission_vocabulary()
        extra = load_extra_vocab(mission_id, lang)
        existing_words = {w["word"] for w in vocab}
        for entry in extra:
            if entry["word"] not in existing_words:
                vocab.append(entry)
                existing_words.add(entry["word"])
        return jsonify(vocab)
    except (ValueError, KeyError) as e:
        return jsonify({"error": str(e)}), 404


@app.route("/api/define/<word>")
def define_word(word):
    lang = get_lang()
    result = dictionary.fetch_definition(word, language=lang)
    return jsonify(result)


@app.route("/api/grammar")
def grammar_rules():
    lang = get_lang()
    agent = get_agent(lang)
    return jsonify(agent.get_grammar_rules())


@app.route("/api/vocab/add", methods=["POST"])
def add_vocab():
    data = request.get_json()
    if not data or not data.get("word"):
        return jsonify({"error": "No word provided"}), 400
    word = data["word"].strip().lower()
    mission_id = data.get("mission_id", "__all__")
    lang = data.get("lang", "en")
    agent = get_agent(lang)
    extra = load_extra_vocab(mission_id, lang)
    if any(w["word"] == word for w in extra):
        return jsonify({"status": "exists"})
    definition = dictionary.fetch_definition(word, language=lang)
    entry = {
        "word": word,
        "definition": definition.get("definition", ""),
        "spanish": definition.get("spanish", ""),
        "phonetic": definition.get("phonetic", ""),
        "example": definition.get("example", ""),
        "part_of_speech": definition.get("part_of_speech", ""),
        "tags": ["user-added"]
    }
    extra.append(entry)
    save_extra_vocab(mission_id, extra, lang)
    return jsonify({"status": "added", "entry": entry})


@app.route("/api/missions")
def missions():
    lang = get_lang()
    agent = get_agent(lang)
    return jsonify(agent.missions)


@app.route("/api/mission/<mission_id>/content")
def mission_content(mission_id):
    lang = get_lang()
    agent = get_agent(lang)
    try:
        return jsonify(agent.get_mission_content(mission_id))
    except (ValueError, KeyError) as e:
        return jsonify({"error": str(e)}), 404


@app.route("/api/tutor/chat", methods=["POST"])
def tutor_chat():
    data = request.get_json()
    if not data:
        return jsonify({"error": "No data"}), 400
    message = data.get("message", "")
    mission_id = data.get("mission_id", "")
    history = data.get("history", [])
    lang = data.get("lang", "en")
    agent = get_agent(lang)

    mission_name = ""
    mission_vocab = []
    if mission_id:
        try:
            content = agent.get_mission_content(mission_id)
            mission_name = content["mission"]["name"]
            mission_vocab = [w["word"] for w in content["vocabulary"]]
        except Exception:
            pass

    result = tutor.chat(message, mission_name=mission_name, mission_vocab=mission_vocab, history=history, language=lang)
    return jsonify(result)


@app.route("/api/tutor/status")
def tutor_status():
    return jsonify({"available": tutor.is_available()})


if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True, port=5000)
