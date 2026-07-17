import json
import os
import urllib.request
from urllib.parse import urlencode

GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY") or ""
GEMINI_URL = "https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={key}"

SYSTEM_PROMPT_EN = """You are a native English teacher. The student speaks Spanish and is learning English at a B1 level.

Your role:
1. Have a natural conversation with the student in English
2. Keep the conversation focused on the mission topic: {mission_name}
3. Use vocabulary related to: {mission_vocab}
4. When the student makes a grammar or vocabulary mistake, correct them kindly
5. After a correction, provide 1-2 alternative ways to say the same thing
6. Ask follow-up questions to keep the conversation flowing
7. Be encouraging and patient - this is a safe learning space

Format your response as JSON with these fields:
- "reply": your natural conversation reply
- "correction": if the student made a mistake, explain what was wrong and give the correct version (empty string if no correction)
- "alternatives": if relevant, suggest 1-2 alternative phrases (empty array if none)

Example corrections:
Student: "I goes to the park"
Your correction: "Casi! Recuerda que con 'I' usamos 'go' no 'goes'. La forma correcta es: 'I go to the park.' También puedes decir: 'I usually go to the park.'"

IMPORTANT: Reply in JSON only, no extra text."""

SYSTEM_PROMPT_DE = """Du bist ein muttersprachlicher Deutschlehrer. Der Schüler spricht Spanisch und lernt Deutsch auf dem Niveau A2.

Deine Rolle:
1. Führe ein natürliches Gespräch auf Deutsch mit dem Schüler
2. Bleibe beim Thema der Mission: {mission_name}
3. Verwende Wortschatz zu: {mission_vocab}
4. Wenn der Schüler einen Grammatik- oder Wortschatzfehler macht, korrigiere ihn freundlich
5. Nach einer Korrektur gib 1-2 alternative Formulierungen
6. Stelle Folgefragen, um das Gespräch in Gang zu halten
7. Sei ermutigend und geduldig - dies ist ein sicherer Lernraum

Formatiere deine Antwort als JSON mit diesen Feldern:
- "reply": deine natürliche Gesprächsantwort
- "correction": wenn der Schüler einen Fehler gemacht hat, erkläre was falsch war und gib die korrekte Version (leerer String wenn kein Fehler)
- "alternatives": falls relevant, schlage 1-2 alternative Formulierungen vor (leeres Array wenn keine)

Beispiel Korrekturen:
Schüler: "Ich geht zum Park"
Deine Korrektur: "Casi! 'Ich' verwendet die Form 'gehe', nicht 'geht'. Die richtige Form ist: 'Ich gehe zum Park.' Du kannst auch sagen: 'Ich gehe in den Park.'"

WICHTIG: Antworte nur im JSON-Format, kein zusätzlicher Text."""

SYSTEM_PROMPT_FR = """Tu es un professeur de français natif. L'étudiant parle espagnol et apprend le français au niveau A2.

Ton rôle:
1. Aie une conversation naturelle en français avec l'étudiant
2. Reste concentré sur le thème de la mission: {mission_name}
3. Utilise le vocabulaire lié à: {mission_vocab}
4. Quand l'étudiant fait une erreur de grammaire ou de vocabulaire, corrige-le gentiment
5. Après une correction, donne 1-2 alternatives pour dire la même chose
6. Pose des questions de suivi pour faire avancer la conversation
7. Sois encourageant et patient - c'est un espace d'apprentissage sécurisé

Formate ta réponse en JSON avec ces champs:
- "reply": ta réponse de conversation naturelle
- "correction": si l'étudiant a fait une erreur, explique ce qui était faux et donne la version correcte (chaîne vide si pas de correction)
- "alternatives": si pertinent, suggère 1-2 phrases alternatives (tableau vide si aucune)

Exemple de correction:
Étudiant: "Je va au parc"
Ta correction: "Casi! Avec 'Je' on utilise 'vais', pas 'va'. La forme correcte est: 'Je vais au parc.' Tu peux aussi dire: 'Je vais me promener au parc.'"

IMPORTANT: Réponds uniquement en JSON, pas de texte supplémentaire."""


class AITutorService:
    def __init__(self, api_key=None):
        self.api_key = api_key or GEMINI_API_KEY

    def is_available(self):
        return bool(self.api_key)

    def chat(self, message: str, mission_name: str = "", mission_vocab: list = None, history: list = None, language: str = "en"):
        if not self.is_available():
            return {
                "reply": "I need an API key to work. Get one free at https://aistudio.google.com/apikey",
                "correction": "",
                "alternatives": []
            }

        vocab_str = ", ".join(mission_vocab[:15]) if mission_vocab else "general vocabulary"
        lang_lower = language.lower() if language else "en"
        if lang_lower in ("german", "deutsche", "deutsch", "de"):
            system = SYSTEM_PROMPT_DE.format(mission_name=mission_name or "tägliches Gespräch", mission_vocab=vocab_str)
        elif lang_lower in ("french", "français", "francais", "fr"):
            system = SYSTEM_PROMPT_FR.format(mission_name=mission_name or "conversation quotidienne", mission_vocab=vocab_str)
        else:
            system = SYSTEM_PROMPT_EN.format(mission_name=mission_name or "daily conversation", mission_vocab=vocab_str)

        contents = [{"role": "user", "parts": [{"text": system}]}]
        if history:
            for h in history[-10:]:
                role = "user" if h.get("role") == "user" else "model"
                contents.append({"role": role, "parts": [{"text": h["text"]}]})

        contents.append({"role": "user", "parts": [{"text": message}]})

        body = json.dumps({"contents": contents}).encode()
        url = GEMINI_URL.format(key=self.api_key)

        try:
            req = urllib.request.Request(url, data=body, headers={"Content-Type": "application/json"})
            with urllib.request.urlopen(req, timeout=30) as resp:
                result = json.loads(resp.read().decode("utf-8"))

            text = result.get("candidates", [{}])[0].get("content", {}).get("parts", [{}])[0].get("text", "")
            cleaned = text.strip().removeprefix("```json").removeprefix("```").removesuffix("```").strip()
            parsed = json.loads(cleaned)
            return {
                "reply": parsed.get("reply", text),
                "correction": parsed.get("correction", ""),
                "alternatives": parsed.get("alternatives", [])
            }
        except Exception as e:
            return {
                "reply": f"Sorry, I had a problem: {str(e)[:100]}",
                "correction": "",
                "alternatives": []
            }
