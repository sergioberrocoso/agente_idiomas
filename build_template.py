import json

# Read Jinja header (only the L dict + lc setter, up to 96 lines)
with open('templates/index.html', 'r', encoding='utf-8') as f:
    lines = f.readlines()
# Keep only the Jinja header (before <style>) â€” first encounter of '<style' stops
header_lines = []
for line in lines:
    if '<style' in line:
        break
    header_lines.append(line)
header = ''.join(header_lines)

css = """* { margin: 0; padding: 0; box-sizing: border-box; }
body {
    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
    background: #1a1a2e;
    color: #eee;
    min-height: 100vh;
    display: flex;
    flex-direction: column;
    align-items: center;
}
.header {
    width: 100%;
    padding: 1rem 2rem;
    background: #16213e;
    display: flex;
    justify-content: space-between;
    align-items: center;
    flex-wrap: wrap;
    gap: 1rem;
}
.header h1 { font-size: 1.3rem; color: #e94560; }
.controls { display: flex; gap: 0.75rem; align-items: center; flex-wrap: wrap; }
.controls select, .controls button {
    padding: 0.5rem 1rem;
    border: 1px solid #0f3460;
    border-radius: 8px;
    background: #0f3460;
    color: #eee;
    font-size: 0.9rem;
    cursor: pointer;
}
.controls select:focus { outline: none; border-color: #e94560; }
.controls button { background: #e94560; border-color: #e94560; font-weight: 600; }
.controls button:hover { background: #d63851; }
.controls .count { font-size: 0.85rem; color: #aaa; }
.tabs {
    display: flex;
    gap: 0;
    width: 100%;
    max-width: 600px;
    margin: 1rem auto 0;
    border-bottom: 2px solid #0f3460;
}
.tabs button {
    flex: 1;
    padding: 0.7rem 1rem;
    border: none;
    background: transparent;
    color: #888;
    font-size: 0.95rem;
    cursor: pointer;
    transition: all 0.2s;
    border-bottom: 2px solid transparent;
    margin-bottom: -2px;
}
.tabs button:hover { color: #eee; }
.tabs button.active { color: #e94560; border-bottom-color: #e94560; }
.tab-content { display: none; width: 100%; max-width: 600px; padding: 1rem; }
.tab-content.active { display: block; }
.card-container {
    flex: 1;
    display: flex;
    align-items: center;
    justify-content: center;
    width: 100%;
    padding: 1.5rem;
    perspective: 1200px;
}
.card-wrapper {
    width: 100%;
    max-width: 520px;
    min-height: 360px;
    cursor: pointer;
    position: relative;
}
.card {
    width: 100%;
    min-height: 360px;
    position: relative;
    transform-style: preserve-3d;
    transition: transform 0.5s ease;
    border-radius: 16px;
}
.card.flipped { transform: rotateY(180deg); }
.card-face {
    position: absolute;
    width: 100%;
    min-height: 360px;
    backface-visibility: hidden;
    border-radius: 16px;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    padding: 2rem;
    text-align: center;
    background: #16213e;
    border: 1px solid #0f3460;
    box-shadow: 0 8px 32px rgba(0,0,0,0.4);
}
.card-face.back {
    transform: rotateY(180deg);
    background: #0f3460;
    gap: 0.5rem;
    justify-content: flex-start;
    padding-top: 2rem;
}
.card-face .word { font-size: 2.5rem; font-weight: 700; color: #fff; }
.card-face .hint { font-size: 0.85rem; color: #888; margin-top: 1rem; }
.back .label { font-size: 0.75rem; color: #e94560; text-transform: uppercase; letter-spacing: 1px; margin-bottom: 0.2rem; }
.back .value { font-size: 0.95rem; color: #ddd; line-height: 1.5; }
.back .section { width: 100%; margin: 0.3rem 0; padding: 0 0.5rem; }
.back .placeholder { color: #666; font-style: italic; }
.back .pos { font-size: 0.8rem; color: #e94560; background: rgba(233,69,96,0.15); padding: 0.15rem 0.6rem; border-radius: 4px; display: inline-block; margin-top: 0.3rem; }
.nav-bar {
    display: flex;
    align-items: center;
    gap: 1.5rem;
    padding: 0.5rem 0 1rem;
}
.nav-bar button {
    background: none;
    border: 1px solid #0f3460;
    color: #eee;
    padding: 0.5rem 1.2rem;
    border-radius: 8px;
    font-size: 0.95rem;
    cursor: pointer;
}
.nav-bar button:hover { background: #0f3460; }
.nav-bar .progress { font-size: 0.9rem; color: #aaa; }
.nav-bar button:disabled { opacity: 0.3; cursor: default; }
.dialogue-box {
    background: #16213e;
    border: 1px solid #0f3460;
    border-radius: 12px;
    padding: 1.2rem;
    margin-bottom: 0.8rem;
}
.exercise-card {
    background: #16213e;
    border: 1px solid #0f3460;
    border-radius: 12px;
    padding: 1.2rem;
    margin-bottom: 1rem;
}
.exercise-sentence {
    font-size: 1.1rem;
    color: #fff;
    margin-bottom: 1rem;
    line-height: 1.6;
}
.exercise-sentence .blank { color: #e94560; font-weight: 700; }
.exercise-input-row {
    display: flex;
    gap: 0.5rem;
    margin-bottom: 0.8rem;
}
.exercise-input-row input {
    flex: 1;
    padding: 0.6rem 1rem;
    border: 1px solid #0f3460;
    border-radius: 8px;
    background: #0f3460;
    color: #eee;
    font-size: 1rem;
    outline: none;
}
.exercise-input-row input:focus { border-color: #e94560; }
.exercise-input-row input.correct { border-color: #4caf50; }
.exercise-input-row input.wrong { border-color: #f44336; }
.exercise-input-row button {
    padding: 0.6rem 1.2rem;
    border: none;
    border-radius: 8px;
    background: #e94560;
    color: #fff;
    font-weight: 600;
    cursor: pointer;
    white-space: nowrap;
}
.exercise-input-row button:hover { background: #d63851; }
.exercise-feedback {
    padding: 0.8rem;
    border-radius: 8px;
    font-size: 0.9rem;
    line-height: 1.5;
}
.exercise-feedback.correct { background: rgba(76,175,80,0.15); color: #a5d6a7; }
.exercise-feedback.wrong { background: rgba(244,67,54,0.15); color: #ef9a9a; }
.exercise-feedback .fb-title { font-weight: 700; margin-bottom: 0.3rem; }
.exercise-feedback .fb-hint { color: #ffcc02; margin: 0.3rem 0; }
.exercise-feedback .fb-example { color: #90caf9; font-style: italic; }
.exercise-index {
    font-size: 0.8rem;
    color: #888;
    margin-bottom: 0.5rem;
}
.stats { font-size: 0.8rem; color: #555; padding-bottom: 1rem; }
.empty-state { text-align: center; padding: 2rem; color: #888; }
.tutor-input-row { display: flex; gap: 0.5rem; }
.tutor-input-row input {
    flex: 1; padding: 0.7rem 1rem; border: 1px solid #0f3460; border-radius: 8px;
    background: #0f3460; color: #eee; font-size: 1rem; outline: none;
}
.tutor-input-row input:focus { border-color: #e94560; }
.tutor-input-row button {
    padding: 0.7rem 1.5rem; border: none; border-radius: 8px;
    background: #e94560; color: #fff; font-weight: 600; cursor: pointer;
}
.tutor-input-row button:hover { background: #d63851; }
.tutor-input-row button:disabled { opacity: 0.5; cursor: default; }
.chat-msg { margin-bottom: 1rem; }
.chat-msg .sender { font-size: 0.75rem; color: #e94560; font-weight: 600; margin-bottom: 0.2rem; }
.chat-msg .sender.student { color: #4fc3f7; }
.chat-msg .bubble {
    padding: 0.8rem 1rem; border-radius: 12px; background: #16213e;
    border: 1px solid #0f3460; line-height: 1.5; font-size: 0.95rem;
    max-width: 90%;
}
.chat-msg.student .bubble { background: #0f3460; border-color: #1a4a7a; }
.chat-correction {
    margin-top: 0.5rem; padding: 0.6rem 0.8rem; border-radius: 8px;
    background: rgba(255,152,0,0.12); border: 1px solid rgba(255,152,0,0.3); font-size: 0.85rem;
}
.chat-correction .label { color: #ffa726; font-weight: 600; margin-bottom: 0.3rem; }
.chat-correction .text { color: #ffcc80; }
.chat-alternatives { margin-top: 0.4rem; color: #90caf9; font-size: 0.85rem; }
.chat-alternatives .label { color: #64b5f6; font-weight: 600; }
.typing-indicator { color: #888; font-style: italic; padding: 0.5rem 0; }
.mic-active { border-color: #f44336 !important; background: rgba(244,67,54,0.15) !important; animation: pulse 1s infinite; }
.speak-tutor-btn { background:none; border:none; color:#90caf9; cursor:pointer; font-size:0.85rem; margin-left:0.5rem; }
.speak-tutor-btn:hover { color:#e94560; }
@keyframes pulse { 0% { opacity:0.6; } 50% { opacity:1; } 100% { opacity:0.6; } }
.speaker-btn {
    background: none;
    border: 1px solid #e94560;
    color: #e94560;
    width: 40px;
    height: 40px;
    border-radius: 50%;
    font-size: 1.2rem;
    cursor: pointer;
    display: inline-flex;
    align-items: center;
    justify-content: center;
    transition: all 0.2s;
}
.speaker-btn:hover { background: #e94560; color: #fff; }
.word-row { display: flex; align-items: center; gap: 0.8rem; }"""

html_body = """</style>
</head>
<body>
<div class="header">
    <h1>Language Tutor</h1>
    <div class="controls">
        <select id="lang-select" onchange="switchLanguage(this.value)">
            <option value="en" {{ 'selected' if lang == 'en' else '' }}>English</option>
            <option value="de" {{ 'selected' if lang == 'de' else '' }}>Deutsch</option>
            <option value="fr" {{ 'selected' if lang == 'fr' else '' }}>Fran\u00e7ais</option>
        </select>
        <select id="mission-select">
            <option value="__all__">{{ lc.all_vocab }}</option>
            {% for m in missions %}
            <option value="{{ m.id }}">{{ m.name }}</option>
            {% endfor %}
        </select>
        <span class="count" id="vocab-count">0 {{ lc.words }}</span>
        <button id="shuffle-btn">{{ lc.shuffle }}</button>
    </div>
</div>

<div class="tabs">
    <button class="active" data-tab="cards" onclick="switchTab('cards')">{{ lc.tab_cards }}</button>
    <button data-tab="exercises" onclick="switchTab('exercises')">{{ lc.tab_exercises }}</button>
    <button data-tab="grammar" onclick="switchTab('grammar')">{{ lc.tab_grammar }}</button>
    <button data-tab="tutor" onclick="switchTab('tutor')">{{ lc.tab_tutor }}</button>
    <button data-tab="notes" onclick="switchTab('notes')">{{ lc.tab_notes }}</button>
</div>

<div id="tab-cards" class="tab-content active">
    <div class="card-container">
        <div class="card-wrapper" id="card-wrapper">
            <div class="card" id="card" onclick="flipCard()">
                <div class="card-face front">
                    <div class="word-row">
                        <div class="word" id="front-word"></div>
                        <button class="speaker-btn" id="speaker-btn" onclick="event.stopPropagation(); speakWord()" title="Escuchar pronunciaci\u00f3n">&#x1F50A;</button>
                    </div>
                    <div class="hint" id="card-hint">{{ lc.card_hint }}</div>
                </div>
                <div class="card-face back" id="back-face">
                <div class="section">
                    <div class="label">Definici\u00f3n</div>
                    <div class="value" id="back-def"></div>
                </div>
                <div class="section" id="phonetic-section" style="display:none">
                    <div class="label">Pronunciaci\u00f3n</div>
                    <div class="value" id="back-phonetic"></div>
                </div>
                <div class="section" id="example-section" style="display:none">
                        <div class="label">Ejemplo</div>
                        <div class="value" id="back-example"></div>
                    </div>
                    <div class="section" id="forms-section" style="display:none">
                        <div class="label">Formas</div>
                        <div class="value" id="back-forms"></div>
                    </div>
                    <div class="section" id="tags-section" style="display:none">
                        <div class="label">Tags</div>
                        <div class="value" id="back-tags"></div>
                    </div>
                    <div class="section" id="spanish-section" style="display:none">
                        <div class="label">Espa\u00f1ol</div>
                        <div class="value" id="back-spanish"></div>
                    </div>
                </div>
            </div>
        </div>
    </div>
    <div class="nav-bar">
        <button id="prev-btn" onclick="prevCard()">{{ lc.anterior }}</button>
        <span class="progress" id="progress">0 / 0</span>
        <button id="next-btn" onclick="nextCard()">{{ lc.siguiente }}</button>
    </div>
</div>

<div id="tab-exercises" class="tab-content">
    <div id="exercises-container"><div class="empty-state">{{ lc.ex_empty }}</div></div>
</div>

<div id="tab-tutor" class="tab-content">
    <div id="tutor-container">
        <div class="empty-state" id="tutor-welcome">
            <p style="margin-bottom:1rem">{{ lc.tutor_welcome1 }} {{ lc.tutor_lang }}.</p>
            <p style="font-size:0.85rem;color:#888">{{ lc.tutor_welcome2 }}</p>
        </div>
        <div id="tutor-chat" style="display:none;margin-bottom:1rem"></div>
        <div class="tutor-input-row" id="tutor-input-row" style="display:none">
            <input type="text" id="tutor-input" placeholder="{{ lc.tutor_ph }}" onkeydown="if(event.key==='Enter')sendTutorMessage()">
            <button id="tutor-mic-btn" onclick="startVoiceInput()" title="{{ lc.mic_title }}" style="background:none;border:1px solid #0f3460;color:#eee;font-size:1.2rem">&#x1F3A4;</button>
            <button onclick="sendTutorMessage()">{{ lc.tutor_send }}</button>
        </div>
        <div id="tutor-setup" style="text-align:center;padding:1rem">
            <button onclick="startTutorChat()" style="padding:0.8rem 2rem;border:none;border-radius:8px;background:#e94560;color:#fff;font-weight:600;font-size:1rem;cursor:pointer">{{ lc.tutor_start }}</button>
        </div>
    </div>
</div>

<div id="tab-notes" class="tab-content">
    <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:1rem">
        <h2 style="font-size:1.1rem;color:#e94560">{{ lc.notes_title }}</h2>
        <button onclick="clearNotes()" style="padding:0.4rem 1rem;border:1px solid #f44336;border-radius:8px;background:transparent;color:#f44336;font-size:0.85rem;cursor:pointer">{{ lc.notes_clear }}</button>
    </div>
    <div id="notes-container"><div class="empty-state">{{ lc.notes_empty }}</div></div>
</div>

<div id="tab-grammar" class="tab-content">
    <div style="margin-bottom:1rem">
        <input type="text" id="grammar-search" placeholder="{{ lc.grammar_ph }}" oninput="filterGrammarRules()" style="width:100%;padding:0.7rem 1rem;border:1px solid #0f3460;border-radius:8px;background:#0f3460;color:#eee;font-size:0.95rem;outline:none">
    </div>
    <div id="grammar-rules-list"></div>
    <div id="grammar-exercise-area" style="display:none">
        <button onclick="backToGrammarRules()" style="padding:0.4rem 1rem;border:1px solid #0f3460;border-radius:8px;background:transparent;color:#eee;font-size:0.85rem;cursor:pointer;margin-bottom:1rem">&larr; {{ lc.grammar_back }}</button>
        <div id="grammar-exercise-content"></div>
    </div>
</div>

<div class="stats" id="stats"></div>
"""

js = """
<script>
let currentLang = '{{ lang }}';
let vocab = [];
let missionId = '__all__';
let currentIndex = 0;
let isFlipped = false;
let grammarRules = [];
let exercisesData = [];

function switchLanguage(lang) {
    window.location = '/?lang=' + lang;
}

function apiUrl(path) {
    const sep = path.includes('?') ? '&' : '?';
    return path + sep + 'lang=' + currentLang;
}

const t = (en, de, fr) => currentLang === 'de' ? de : (currentLang === 'fr' ? fr : en);

const frontWord = document.getElementById('front-word');
const backDef = document.getElementById('back-def');
const backPhonetic = document.getElementById('back-phonetic');
const backExample = document.getElementById('back-example');
const backForms = document.getElementById('back-forms');
const backTags = document.getElementById('back-tags');
const backSpanish = document.getElementById('back-spanish');
const phoneticSection = document.getElementById('phonetic-section');
const exampleSection = document.getElementById('example-section');
const formsSection = document.getElementById('forms-section');
const tagsSection = document.getElementById('tags-section');
const spanishSection = document.getElementById('spanish-section');
const progress = document.getElementById('progress');
const vocabCount = document.getElementById('vocab-count');
const card = document.getElementById('card');
const defCache = {};

async function loadVocab(id) {
    missionId = id;
    const url = id === '__all__' ? apiUrl('/api/vocab') : apiUrl('/api/vocab/' + id);
    const res = await fetch(url);
    vocab = await res.json();
    currentIndex = 0;
    isFlipped = false;
    card.classList.remove('flipped');
    vocabCount.textContent = vocab.length + ' ' + t('palabras', 'W\u00f6rter', 'mots');
    document.getElementById('stats').textContent = '';
    if (vocab.length === 0) {
        frontWord.textContent = t('Sin vocabulario', 'Kein Wortschatz', 'Pas de vocabulaire');
        progress.textContent = '0 / 0';
        return;
    }
    showCard();
    if (id !== '__all__') {
        loadMissionContent(id);
    } else {
        document.getElementById('exercises-container').innerHTML = '<div class="empty-state">' + t('Selecciona una misi\u00f3n espec\u00edfica para ver los ejercicios', 'W\u00e4hle eine bestimmte Mission, um die \u00dcbungen zu sehen', 'S\u00e9lectionne une mission sp\u00e9cifique pour voir les exercices') + '</div>';
        exercisesData = [];
    }
}

async function loadMissionContent(id) {
    try {
        const res = await fetch(apiUrl('/api/mission/' + id + '/content'));
        const data = await res.json();
        exercisesData = data.exercises || [];
        renderExercises();
    } catch (e) {
        exercisesData = [];
        document.getElementById('exercises-container').innerHTML = '<div class="empty-state">' + t('Error al cargar ejercicios', 'Fehler beim Laden der \u00dcbungen', 'Erreur lors du chargement des exercices') + '</div>';
    }
}

function renderExercises() {
    const container = document.getElementById('exercises-container');
    if (!exercisesData || exercisesData.length === 0) {
        container.innerHTML = '<div class="empty-state">' + t('No hay ejercicios disponibles para esta misi\u00f3n', 'Keine \u00dcbungen f\u00fcr diese Mission verf\u00fcgbar', 'Aucun exercice disponible pour cette mission') + '</div>';
        return;
    }
    let html = '';
    exercisesData.forEach((ex, i) => {
        html += '<div class="exercise-card" id="ex-card-' + i + '">';
        html += '<div class="exercise-index">' + t('Ejercicio', '\u00dcbung', 'Exercice') + ' ' + (i + 1) + ' ' + t('de', 'von', 'sur') + ' ' + exercisesData.length + '</div>';
        html += '<div class="exercise-sentence">' + ex.sentence + '</div>';
        html += '<div class="exercise-input-row">';
        html += '<input type="text" id="ex-input-' + i + '" placeholder="' + t('Escribe tu respuesta...', 'Schreibe deine Antwort...', '\u00c9cris ta r\u00e9ponse...') + '" onkeydown="if(event.key===\\'Enter\\')checkAnswer(' + i + ')">';
        html += '<button onclick="checkAnswer(' + i + ')">' + t('Comprobar', 'Pr\u00fcfen', 'V\u00e9rifier') + '</button>';
        html += '</div>';
        html += '<div class="exercise-feedback" id="ex-feedback-' + i + '" style="display:none"></div>';
        html += '</div>';
    });
    container.innerHTML = html;
}

function checkAnswer(index) {
    const ex = exercisesData[index];
    const input = document.getElementById('ex-input-' + index);
    const feedback = document.getElementById('ex-feedback-' + index);
    const answer = input.value.trim().toLowerCase();
    const correct = ex.answer.toLowerCase();
    const alternatives = (ex.alternatives || []).map(function(a) { return a.toLowerCase(); });
    const isCorrect = answer === correct || alternatives.indexOf(answer) !== -1;
    input.classList.remove('correct', 'wrong');
    feedback.style.display = 'block';
    if (isCorrect) {
        input.classList.add('correct');
        feedback.className = 'exercise-feedback correct';
        feedback.innerHTML = '<div class="fb-title">' + t('Correcto!', 'Richtig!', 'Correct!') + '</div><div class="fb-example">' + (ex.sentence_with_answer || ex.sentence.replace('____', ex.answer)) + '</div>';
    } else {
        input.classList.add('wrong');
        feedback.className = 'exercise-feedback wrong';
        let html = '<div class="fb-title">' + t('Casi! La respuesta correcta es:', 'Fast! Die richtige Antwort ist:', 'Presque! La bonne r\u00e9ponse est:') + ' <strong>' + ex.answer + '</strong></div>';
        if (ex.hint) {
            html += '<div class="fb-hint">' + t('Pista:', 'Tipp:', 'Indice:') + ' ' + ex.hint + '</div>';
        }
        html += '<div class="fb-example">' + t('Ejemplo:', 'Beispiel:', 'Exemple:') + ' ' + (ex.sentence_with_answer || ex.sentence.replace('____', ex.answer)) + '</div>';
        feedback.innerHTML = html;
    }
}

function checkGrammarAnswer(index, ruleId) {
    const rules = JSON.parse(sessionStorage.getItem('grammar_rules') || '[]');
    const rule = rules.find(function(r) { return r.id === ruleId; });
    if (!rule) return;
    const ex = rule.exercises[index];
    const input = document.getElementById('gr-input-' + ruleId + '-' + index);
    const feedback = document.getElementById('gr-feedback-' + ruleId + '-' + index);
    const answer = input.value.trim().toLowerCase();
    const correct = ex.answer.toLowerCase();
    const isCorrect = answer === correct;
    input.classList.remove('correct', 'wrong');
    feedback.style.display = 'block';
    if (isCorrect) {
        input.classList.add('correct');
        feedback.className = 'exercise-feedback correct';
        feedback.innerHTML = '<div class="fb-title">' + t('Correcto!', 'Richtig!', 'Correct!') + '</div><div class="fb-example">' + ex.sentence.replace('____', ex.answer) + '</div>';
    } else {
        input.classList.add('wrong');
        feedback.className = 'exercise-feedback wrong';
        let html = '<div class="fb-title">' + t('Casi! Respuesta correcta:', 'Fast! Richtige Antwort:', 'Presque! Bonne r\u00e9ponse:') + ' <strong>' + ex.answer + '</strong></div>';
        if (ex.hint) html += '<div class="fb-hint">' + t('Pista:', 'Tipp:', 'Indice:') + ' ' + ex.hint + '</div>';
        html += '<div class="fb-example">' + ex.sentence.replace('____', ex.answer) + '</div>';
        feedback.innerHTML = html;
    }
}

async function loadGrammarRules() {
    try {
        const res = await fetch(apiUrl('/api/grammar'));
        const rules = await res.json();
        sessionStorage.setItem('grammar_rules', JSON.stringify(rules));
        renderGrammarRules(rules);
    } catch (e) {
        document.getElementById('grammar-rules-list').innerHTML = '<div class="empty-state">' + t('Error al cargar reglas gramaticales', 'Fehler beim Laden der Grammatikregeln', 'Erreur lors du chargement des r\u00e8gles de grammaire') + '</div>';
    }
}

function renderGrammarRules(rules) {
    const container = document.getElementById('grammar-rules-list');
    let html = '';
    for (const r of rules) {
        html += '<div class="dialogue-box" onclick="showGrammarRule(\\'' + r.id + '\\')" style="cursor:pointer">';
        html += '<div style="font-size:1rem;font-weight:600;color:#e94560">' + r.title + '</div>';
        html += '<div style="font-size:0.85rem;color:#aaa;margin-top:0.3rem">' + r.description + '</div>';
        html += '<div style="font-size:0.75rem;color:#888;margin-top:0.3rem">' + r.exercises.length + ' ' + t('ejercicios', '\u00dcbungen', 'exercices') + '</div>';
        html += '</div>';
    }
    container.innerHTML = html;
}

function filterGrammarRules() {
    const q = document.getElementById('grammar-search').value.toLowerCase();
    const rules = JSON.parse(sessionStorage.getItem('grammar_rules') || '[]');
    if (!q) { renderGrammarRules(rules); return; }
    const filtered = rules.filter(function(r) { return r.title.toLowerCase().includes(q) || r.description.toLowerCase().includes(q); });
    renderGrammarRules(filtered);
}

function showGrammarRule(ruleId) {
    const rules = JSON.parse(sessionStorage.getItem('grammar_rules') || '[]');
    const rule = rules.find(function(r) { return r.id === ruleId; });
    if (!rule) return;
    document.getElementById('grammar-rules-list').style.display = 'none';
    document.getElementById('grammar-search').style.display = 'none';
    const area = document.getElementById('grammar-exercise-area');
    area.style.display = 'block';
    area.innerHTML = '<button onclick="backToGrammarRules()" style="padding:0.4rem 1rem;border:1px solid #0f3460;border-radius:8px;background:transparent;color:#eee;font-size:0.85rem;cursor:pointer;margin-bottom:1rem">&larr; ' + t('Volver a reglas', 'Zur\u00fcck zu den Regeln', 'Retour aux r\u00e8gles') + '</button><div id="grammar-exercise-content"></div>';
    let html = '<div class="dialogue-box">';
    html += '<div style="font-size:1.2rem;font-weight:700;color:#e94560;margin-bottom:0.5rem">' + rule.title + '</div>';
    html += '<div style="font-size:0.9rem;color:#ddd;margin-bottom:0.5rem">' + rule.description + '</div>';
    html += '<div style="font-size:0.85rem;color:#ffa726;margin-bottom:0.5rem;background:rgba(255,167,38,0.1);padding:0.5rem;border-radius:6px"><strong>' + t('F\u00f3rmula', 'Formel', 'Formule') + ':</strong> ' + rule.formula + '</div>';
    if (rule.negative) {
        html += '<div style="font-size:0.85rem;color:#ffa726;margin-bottom:0.5rem;background:rgba(255,167,38,0.05);padding:0.5rem;border-radius:6px"><strong>' + t('Negativo', 'Negativ', 'N\u00e9gation') + ':</strong> ' + rule.negative + '</div>';
    }
    if (rule.question) {
        html += '<div style="font-size:0.85rem;color:#ffa726;margin-bottom:0.5rem;background:rgba(255,167,38,0.05);padding:0.5rem;border-radius:6px"><strong>' + t('Pregunta', 'Frage', 'Question') + ':</strong> ' + rule.question + '</div>';
    }
    html += '<div style="font-size:0.85rem;color:#90caf9;margin-bottom:0.5rem"><strong>' + t('Ejemplos', 'Beispiele', 'Exemples') + ':</strong></div>';
    html += '<ul style="font-size:0.85rem;color:#bbb;padding-left:1.2rem;margin-bottom:0.5rem">';
    for (const ex of rule.examples) {
        html += '<li>' + ex + '</li>';
    }
    html += '</ul></div>';
    html += '<div style="font-size:1rem;font-weight:600;color:#fff;margin:1rem 0 0.5rem">' + t('Ejercicios de', '\u00dcbungen zu', 'Exercices de') + ' ' + rule.title + '</div>';
    rule.exercises.forEach(function(ex, i) {
        html += '<div class="exercise-card">';
        html += '<div class="exercise-sentence">' + ex.sentence.replace('____', '<span class="blank">____</span>') + '</div>';
        html += '<div class="exercise-input-row">';
        html += '<input type="text" id="gr-input-' + ruleId + '-' + i + '" placeholder="' + t('Escribe la respuesta...', 'Schreibe die Antwort...', '\u00c9cris la r\u00e9ponse...') + '" onkeydown="if(event.key===\\'Enter\\')checkGrammarAnswer(' + i + ',\\'' + ruleId + '\\')">';
        html += '<button onclick="checkGrammarAnswer(' + i + ',\\'' + ruleId + '\\')">' + t('Comprobar', 'Pr\u00fcfen', 'V\u00e9rifier') + '</button>';
        html += '</div>';
        html += '<div class="exercise-feedback" id="gr-feedback-' + ruleId + '-' + i + '" style="display:none"></div>';
        html += '</div>';
    });
    document.getElementById('grammar-exercise-content').innerHTML = html;
    area.scrollIntoView({ behavior: 'smooth' });
}

function backToGrammarRules() {
    document.getElementById('grammar-rules-list').style.display = '';
    document.getElementById('grammar-search').style.display = '';
    const area = document.getElementById('grammar-exercise-area');
    area.style.display = 'none';
    area.innerHTML = '<button onclick="backToGrammarRules()" style="padding:0.4rem 1rem;border:1px solid #0f3460;border-radius:8px;background:transparent;color:#eee;font-size:0.85rem;cursor:pointer;margin-bottom:1rem">&larr; ' + t('Volver a reglas', 'Zur\u00fcck zu den Regeln', 'Retour aux r\u00e8gles') + '</button><div id="grammar-exercise-content"></div>';
}

function showCard() {
    if (vocab.length === 0) return;
    const item = vocab[currentIndex];
    const word = item.word || item.front || '?';
    frontWord.textContent = word;
    progress.textContent = (currentIndex + 1) + ' / ' + vocab.length;
    backDef.textContent = '';
    backPhonetic.textContent = '';
    backExample.textContent = '';
    backSpanish.textContent = '';
    exampleSection.style.display = 'none';
    phoneticSection.style.display = 'none';
    spanishSection.style.display = 'none';
    const forms = item.forms || (item.back && item.back.forms ? item.back.forms.split(', ') : []);
    const tags = item.tags || [];
    if (forms.length) {
        backForms.textContent = forms.join(', ');
        formsSection.style.display = '';
    } else {
        formsSection.style.display = 'none';
    }
    if (tags.length) {
        backTags.textContent = tags.join(', ');
        tagsSection.style.display = '';
    } else {
        tagsSection.style.display = 'none';
    }
    updateNavButtons();
}

async function flipCard() {
    if (vocab.length === 0) return;
    if (!isFlipped) {
        const item = vocab[currentIndex];
        const word = item.word || item.front || '?';
        await loadDefinition(word);
    }
    isFlipped = !isFlipped;
    card.classList.toggle('flipped', isFlipped);
}

async function loadDefinition(word) {
    if (defCache[word]) {
        applyDefinition(defCache[word]);
        return;
    }
    backDef.textContent = t('Cargando...', 'Laden...', 'Chargement...');
    try {
        const res = await fetch(apiUrl('/api/define/' + encodeURIComponent(word)));
        const data = await res.json();
        defCache[word] = data;
        applyDefinition(data);
    } catch (e) {
        backDef.textContent = t('Error al cargar definici\u00f3n', 'Fehler beim Laden der Definition', 'Erreur lors du chargement de la d\u00e9finition');
    }
}

function applyDefinition(data) {
    if (data.definition) {
        let html = data.definition;
        if (data.part_of_speech) {
            html += ' <span class="pos">' + data.part_of_speech + '</span>';
        }
        backDef.innerHTML = html;
    } else {
        backDef.textContent = t('(sin definici\u00f3n disponible)', '(keine Definition verf\u00fcgbar)', '(aucune d\u00e9finition disponible)');
    }
    if (data.example) {
        backExample.textContent = '\\u0022' + data.example + '\\u0022';
        exampleSection.style.display = '';
    } else {
        exampleSection.style.display = 'none';
    }
    if (data.spanish) {
        backSpanish.textContent = data.spanish;
        spanishSection.style.display = '';
    } else {
        spanishSection.style.display = 'none';
    }
    if (data.phonetic) {
        backPhonetic.textContent = data.phonetic;
        phoneticSection.style.display = '';
    } else {
        phoneticSection.style.display = 'none';
    }
}

function speakWord() {
    const word = frontWord.textContent;
    if (!word || (currentLang === 'de' ? word === 'Kein Wortschatz' : (currentLang === 'fr' ? word === 'Pas de vocabulaire' : word === 'Sin vocabulario'))) return;
    const utter = new SpeechSynthesisUtterance(word);
    utter.lang = currentLang === 'de' ? 'de-DE' : (currentLang === 'fr' ? 'fr-FR' : 'en-US');
    utter.rate = 0.9;
    speechSynthesis.cancel();
    speechSynthesis.speak(utter);
}

function nextCard() {
    if (currentIndex < vocab.length - 1) {
        isFlipped = false;
        card.classList.remove('flipped');
        currentIndex++;
        showCard();
    }
}

function prevCard() {
    if (currentIndex > 0) {
        isFlipped = false;
        card.classList.remove('flipped');
        currentIndex--;
        showCard();
    }
}

function updateNavButtons() {
    document.getElementById('prev-btn').disabled = currentIndex === 0;
    document.getElementById('next-btn').disabled = currentIndex === vocab.length - 1;
}

function switchTab(name) {
    document.querySelectorAll('.tabs button').forEach(b => b.classList.remove('active'));
    document.querySelectorAll('.tab-content').forEach(t => t.classList.remove('active'));
    document.querySelector('.tabs button[data-tab=\"'+name+'\"]').classList.add('active');
    document.getElementById('tab-'+name).classList.add('active');
}

document.getElementById('mission-select').addEventListener('change', function(e) {
    loadVocab(e.target.value);
});

document.getElementById('shuffle-btn').addEventListener('click', function() {
    for (let i = vocab.length - 1; i > 0; i--) {
        const j = Math.floor(Math.random() * (i + 1));
        [vocab[i], vocab[j]] = [vocab[j], vocab[i]];
    }
    currentIndex = 0;
    isFlipped = false;
    card.classList.remove('flipped');
    showCard();
});

document.addEventListener('keydown', function(e) {
    const tag = e.target.tagName;
    if (tag === 'INPUT' || tag === 'TEXTAREA') return;
    if (e.key === ' ' || e.key === 'Enter') { e.preventDefault(); flipCard(); }
    if (e.key === 'ArrowRight') nextCard();
    if (e.key === 'ArrowLeft') prevCard();
});

let tutorHistory = [];

function startTutorChat() {
    document.getElementById('tutor-welcome').style.display = 'none';
    document.getElementById('tutor-setup').style.display = 'none';
    document.getElementById('tutor-chat').style.display = 'block';
    document.getElementById('tutor-input-row').style.display = 'flex';
    tutorHistory = [];
    const greeting = currentLang === 'de'
        ? 'Hallo! Ich bin dein Deutschlehrer. Wor\u00fcber m\u00f6chtest du heute sprechen? Du kannst oben eine Mission ausw\u00e4hlen oder einfach ein freies Gespr\u00e4ch f\u00fchren.'
        : (currentLang === 'fr'
            ? 'Bonjour! Je suis ton professeur de fran\u00e7ais. De quoi veux-tu parler aujourd\\'hui? Tu peux choisir une mission ci-dessus ou simplement avoir une conversation libre.'
            : 'Hello! I am your English teacher. What would you like to talk about today? You can choose a mission above, or just have a free conversation.');
    addTutorMessage('tutor', greeting);
    document.getElementById('tutor-input').focus();
}

async function sendTutorMessage(voiceText) {
    const input = document.getElementById('tutor-input');
    const text = voiceText || input.value.trim();
    if (!text) return;
    input.value = '';
    addTutorMessage('student', text);
    showTyping();
    const btn = document.querySelector('.tutor-input-row button:last-child');
    btn.disabled = true;
    tutorHistory.push({ role: 'user', text: text });
    try {
        const res = await fetch('/api/tutor/chat', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ message: text, mission_id: missionId === '__all__' ? '' : missionId, history: tutorHistory.slice(0, -1), lang: currentLang })
        });
        const data = await res.json();
        hideTyping();
        addTutorMessage('tutor', data.reply, data.correction, data.alternatives);
        tutorHistory.push({ role: 'assistant', text: data.reply });
        if (data.correction || (data.alternatives && data.alternatives.length)) {
            const sel = document.getElementById('mission-select');
            const missionName = sel.value === '__all__' ? t('Conversaci\u00f3n libre', 'Freies Gespr\u00e4ch', 'Conversation libre') : sel.options[sel.selectedIndex].text;
            saveNote(data.correction, data.alternatives, missionName);
        }
        extractAndAddNewWords(data.reply, data.correction, data.alternatives);
        speakText(data.reply);
    } catch (e) {
        hideTyping();
        addTutorMessage('tutor', t('Sorry, I could not connect. Please try again.', 'Entschuldigung, ich konnte keine Verbindung herstellen. Bitte versuche es erneut.', 'D\u00e9sol\u00e9, je n\\'ai pas pu me connecter. Veuillez r\u00e9essayer.'), '', []);
    }
    btn.disabled = false;
    document.getElementById('tutor-input').focus();
}

function addTutorMessage(role, text, correction, alternatives) {
    const chat = document.getElementById('tutor-chat');
    const div = document.createElement('div');
    div.className = 'chat-msg ' + role;
    const senderClass = role === 'student' ? ' student' : '';
    let html = '<div class=\"sender' + senderClass + '\">' + (role === 'student' ? t('T\u00fa', 'Du', 'Toi') : t('Profesor', 'Lehrer', 'Professeur')) + '</div>';
    if (role === 'tutor') {
        html += '<div class=\"bubble\">' + text + ' <button class=\"speak-tutor-btn\" onclick=\"event.stopPropagation();speakText(this.parentElement.textContent)\" title=\"' + t('Escuchar', 'Anh\u00f6ren', '\u00c9couter') + '\">&#x1F50A;</button></div>';
    } else {
        html += '<div class=\"bubble\">' + text + '</div>';
    }
    if (correction) {
        html += '<div class=\"chat-correction\"><div class=\"label\">' + t('Correcci\u00f3n', 'Korrektur', 'Correction') + '</div><div class=\"text\">' + correction + '</div></div>';
    }
    if (alternatives && alternatives.length) {
        html += '<div class=\"chat-alternatives\"><span class=\"label\">' + t('Alternativas', 'Alternativen', 'Alternatives') + ': </span>' + alternatives.join(' | ') + '</div>';
    }
    div.innerHTML = html;
    chat.appendChild(div);
    chat.scrollTop = chat.scrollHeight;
}

function speakText(text) {
    const clean = text.replace(/<[^>]*>/g, '').replace(/[\\uD83D\\uDE0A\\uD83C\\uDFA4]/g, '').trim();
    if (!clean) return;
    const utter = new SpeechSynthesisUtterance(clean);
    utter.lang = currentLang === 'de' ? 'de-DE' : (currentLang === 'fr' ? 'fr-FR' : 'en-US');
    utter.rate = 0.9;
    speechSynthesis.cancel();
    speechSynthesis.speak(utter);
}

function startVoiceInput() {
    const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
    if (!SpeechRecognition) {
        alert('Speech recognition is not supported in your browser. Try Chrome.');
        return;
    }
    const recognition = new SpeechRecognition();
    recognition.lang = currentLang === 'de' ? 'de-DE' : (currentLang === 'fr' ? 'fr-FR' : 'en-US');
    recognition.interimResults = false;
    recognition.maxAlternatives = 1;
    const micBtn = document.getElementById('tutor-mic-btn');
    micBtn.classList.add('mic-active');
    micBtn.textContent = '\\u23FA';
    recognition.onresult = function(e) {
        const text = e.results[0][0].transcript;
        micBtn.classList.remove('mic-active');
        micBtn.textContent = '\\uD83C\\uDFA4';
        sendTutorMessage(text);
    };
    recognition.onerror = function() {
        micBtn.classList.remove('mic-active');
        micBtn.textContent = '\\uD83C\\uDFA4';
    };
    recognition.onend = function() {
        micBtn.classList.remove('mic-active');
        micBtn.textContent = '\\uD83C\\uDFA4';
    };
    recognition.start();
}

function saveNote(correction, alternatives, missionName) {
    if (!correction && (!alternatives || alternatives.length === 0)) return;
    const key = 'tutor_notes_' + currentLang;
    const notes = JSON.parse(localStorage.getItem(key) || '[]');
    notes.unshift({
        date: new Date().toLocaleString(),
        mission: missionName || t('Conversaci\u00f3n libre', 'Freies Gespr\u00e4ch', 'Conversation libre'),
        correction: correction || '',
        alternatives: alternatives || [],
        id: Date.now()
    });
    localStorage.setItem(key, JSON.stringify(notes));
    renderNotes();
}

function renderNotes() {
    const container = document.getElementById('notes-container');
    const key = 'tutor_notes_' + currentLang;
    const notes = JSON.parse(localStorage.getItem(key) || '[]');
    if (notes.length === 0) {
        container.innerHTML = '<div class="empty-state">' + t('A\u00fan no hay correcciones o sugerencias. Usa el Tutor IA para recibir feedback y se guardar\u00e1 aqu\u00ed.', 'Noch keine Korrekturen oder Vorschl\u00e4ge. Nutze den KI-Tutor, um Feedback zu erhalten - es wird hier gespeichert.', 'Pas encore de corrections ou suggestions. Utilise le Tuteur IA pour recevoir du feedback - il sera sauvegard\u00e9 ici.') + '</div>';
        return;
    }
    let html = '';
    for (const n of notes) {
        html += '<div class="dialogue-box" style="font-size:0.9rem">';
        html += '<div style="font-size:0.75rem;color:#888;margin-bottom:0.4rem">' + n.date + ' \u00b7 ' + n.mission + '</div>';
        if (n.correction) {
            html += '<div style="margin-bottom:0.3rem"><span style="color:#ffa726;font-weight:600">' + t('Correcci\u00f3n', 'Korrektur', 'Correction') + ':</span> <span style="color:#ffcc80">' + n.correction + '</span></div>';
        }
        if (n.alternatives && n.alternatives.length) {
            html += '<div><span style="color:#64b5f6;font-weight:600">' + t('Alternativas', 'Alternativen', 'Alternatives') + ':</span> <span style="color:#90caf9">' + n.alternatives.join(' \u00b7 ') + '</span></div>';
        }
        html += '</div>';
    }
    container.innerHTML = html;
}

const STOPWORDS = new Set([
    'the','a','an','and','or','but','in','on','at','to','for','of','with','by','from',
    'is','are','was','were','be','been','being','have','has','had','do','does','did',
    'will','would','could','should','may','might','can','shall','need','dare','ought',
    'i','you','he','she','it','we','they','me','him','her','us','them','my','your',
    'his','its','our','their','mine','yours','hers','ours','theirs','this','that',
    'these','those','what','which','who','whom','when','where','why','how','all',
    'each','every','both','few','more','most','some','any','no','not','only','own',
    'same','so','than','too','very','just','because','as','if','then','else','about',
    'up','out','over','after','before','between','under','again','further','once',
    'here','there','one','two','three','four','five','six','seven','eight','nine','ten',
    'am','don\\'t','can\\'t','won\\'t','doesn\\'t','isn\\'t','aren\\'t','wasn\\'t','weren\\'t',
    'hasn\\'t','haven\\'t','hadn\\'t','didn\\'t','couldn\\'t','wouldn\\'t','shouldn\\'t',
    'hello','hi','hey','yes','no','ok','okay','please','thanks','thank','sorry','goodbye',
    'bye','well','right','wrong','good','bad','like','just','also','really','quite',
    'much','many','some','thing','things','way','get','got','make','made','say','said',
    'go','went','come','came','take','took','see','saw','know','known','think','thought',
    'want','wanted','give','gave','tell','told','ask','asked','try','tried','use','used',
    'need','needed','find','found','let','keep','put','set','mean','meant','show','showed'
]);

const STOPWORDS_FR = new Set([
    'le','la','les','l\\'','un','une','des','du','de','d\\'','au','aux',
    'et','ou','mais','donc','car','ni','or',
    'je','tu','il','elle','nous','vous','ils','elles','on',
    'me','te','se','lui','leur',
    'j\\'','m\\'','t\\'','s\\'','c\\'','n\\'','qu\\'',
    'mon','ton','son','ma','ta','sa','mes','tes','ses','nos','vos','leurs',
    'ce','cet','cette','ces',
    'quel','quelle','quels','quelles',
    'suis','es','est','sommes','\u00eates','sont',
    'ai','as','a','avons','avez','ont',
    'dans','sur','avec','pour','par','chez','entre','sans','sous','vers','depuis',
    'pendant','avant','apr\u00e8s','devant','derri\u00e8re','contre',
    '\u00e0',
    'tr\u00e8s','bien','mal','mieux','pire',
    'pas','plus','moins','aussi','beaucoup','peu','trop','assez','tant','autant',
    'si','oui','non','puis','alors','enfin','ensuite','d\u00e9j\u00e0',
    'quand','comment','pourquoi','o\u00f9',
    'personne','rien','tout','tous','toute','toutes','chaque','certains','certaines',
    'quelque','quelques','plusieurs',
    'm\u00eame','m\u00eames','autre','autres',
    'ne','n\\'',
    'ici','l\u00e0','maintenant','aujourd\\'hui','hier','demain',
    'toujours','jamais','parfois','souvent',
    'dont','que','qui','quoi',
    'cependant','pourtant','n\u00e9anmoins','toutefois','d\\'ailleurs'
]);

const STOPWORDS_DE = new Set([
    'der','die','das','den','dem','des','ein','eine','einen','einem','eines','einer',
    'und','oder','aber','sondern','doch','denn','weil','dass','da','wenn','als',
    'wie','was','wer','wem','wen','wo','wohin','woher','warum','weshalb','deshalb',
    'nicht','kein','keine','keinen','keinem','keines','nein','ja','doch',
    'ich','du','er','sie','es','wir','ihr','sie','mir','dir','ihm','ihr','uns','euch',
    'mich','dich','sich','uns','euch','mein','dein','sein','ihr','unser','euer',
    'meine','deine','seine','ihre','unsere','eure','meinen','deinen','seinen',
    'ihren','unseren','euren','ist','sind','bin','bist','seid','war','waren',
    'wird','werden','wurde','w\u00fcrde','habe','hast','hat','haben','habt','hatte',
    'hatten','h\u00e4tte','h\u00e4tten','kann','kannst','k\u00f6nnen','konnte','konnten',
    'muss','musst','m\u00fcssen','musste','mussten','darf','darfst','d\u00fcrfen',
    'soll','sollst','sollen','sollte','sollten','will','willst','wollen',
    'wollte','wollten','mag','magst','m\u00f6gen','mochte','m\u00f6chte','m\u00f6chtest',
    'dieser','diese','dieses','diesen','diesem','jener','jene','jenes','jeden',
    'jede','jedes','man','frau','etwas','jemand','niemand','alle','viele',
    'einige','wenige','paar','anderer','andere','anderes','anderen','anderem',
    'ganz','gar','auch','immer','noch','schon','erst','bereits','eben','gerade',
    'sehr','ziemlich','fast','kaum','etwa','ungef\u00e4hr','genau','circa',
    'hier','da','dort','dahin','dorthin','her','hin','hinaus','herein',
    'heraus','hinein','oben','unten','links','rechts','vorn','hinten',
    'drinnen','drau\u00dfen','innen','au\u00dfen','heute','morgen',
    'gestern','jetzt','sofort','sp\u00e4ter','fr\u00fcher','immer','nie','niemals',
    'bitte','danke','vielen','dank','gern','gerne','wohl','vielleicht',
    'nat\u00fcrlich','sicher','sicherlich','allerdings','eigentlich','\u00fcberhaupt',
    'zwar','n\u00e4mlich','\u00fcbrigens','trotzdem','dennoch','jedoch',
    'au\u00dferdem','vor','hinter','neben','zwischen','\u00fcber','unter',
    'auf','an','in','aus','bei','mit','nach','seit','von','zu','durch','f\u00fcr',
    'gegen','ohne','um','ab','bis', 'hallo','tsch\u00fcss','servus','gott'
]);


function extractWordsFromText(text) {
    if (!text) return [];
    const words = text.toLowerCase().replace(/[^a-z\u00e0\u00e2\u00e4\u00e5\u00e6\u00e7\u00e8\u00e9\u00ea\u00eb\u00ee\u00ef\u00f4\u00f6\u00f9\u00fb\u00fc\u00e7\u0153\u00df\s'-]/g, ' ').split(/\\s+/);
    let stopwords;
    if (currentLang === 'de') stopwords = STOPWORDS_DE;
    else if (currentLang === 'fr') stopwords = STOPWORDS_FR;
    else stopwords = STOPWORDS;
    return [...new Set(words.filter(w => w.length > 2 && !stopwords.has(w)))];
}

function highlightNewWordsInChat(words) {
    const msgs = document.getElementById('tutor-chat').querySelectorAll('.chat-msg.tutor');
    const last = msgs[msgs.length - 1];
    if (!last) return;
    const bubble = last.querySelector('.bubble');
    if (!bubble) return;
    let html = bubble.innerHTML;
    for (const w of words) {
        const regex = new RegExp('\\\\b(' + w + ')\\\\b', 'gi');
        html = html.replace(regex, '<span style="color:#e94560;font-weight:600">$1</span>');
    }
    bubble.innerHTML = html;
}

async function extractAndAddNewWords(reply, correction, alternatives) {
    const raw = reply + ' ' + (correction || '') + ' ' + (alternatives || []).join(' ');
    const candidates = extractWordsFromText(raw);
    if (candidates.length === 0) return;
    const knownWords = new Set(vocab.map(v => (v.word || '').toLowerCase()));
    const newWords = candidates.filter(w => !knownWords.has(w));
    if (newWords.length === 0) return;
    const missionId = document.getElementById('mission-select').value;
    let added = 0;
    for (const word of newWords.slice(0, 5)) {
        try {
            const res = await fetch('/api/vocab/add', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ word, mission_id: missionId, lang: currentLang })
            });
            const data = await res.json();
            if (data.status === 'added') added++;
        } catch (e) {}
    }
    if (added > 0) {
        const updatedRes = await fetch(missionId === '__all__' ? apiUrl('/api/vocab') : apiUrl('/api/vocab/' + missionId));
        const updatedVocab = await updatedRes.json();
        vocab = updatedVocab;
        vocabCount.textContent = vocab.length + ' ' + t('palabras', 'W\u00f6rter', 'mots');
        highlightNewWordsInChat(newWords.slice(0, 5));
        const toast = document.createElement('div');
        toast.style.cssText = 'position:fixed;bottom:1rem;left:50%;transform:translateX(-50%);background:#4caf50;color:#fff;padding:0.6rem 1.2rem;border-radius:8px;font-size:0.85rem;z-index:999;box-shadow:0 4px 12px rgba(0,0,0,0.3);transition:opacity 0.5s';
        toast.textContent = added + ' ' + t('palabra(s) aÃ±adida(s) a las flashcards', 'Wort/WÃ¶rter zu den Karteikarten hinzugefÃ¼gt', 'mot(s) ajouté(s) aux flashcards');
        document.body.appendChild(toast);
        setTimeout(function() { toast.style.opacity = '0'; setTimeout(function() { toast.remove(); }, 500); }, 3000);
    }
}

function clearNotes() {
    if (!confirm(t('Borrar todas las notas?', 'Alle Notizen lÃ¶schen?', 'Effacer toutes les notes?'))) return;
    localStorage.setItem('tutor_notes_' + currentLang, '[]');
    renderNotes();
}

function showTyping() {
    const chat = document.getElementById('tutor-chat');
    const div = document.createElement('div');
    div.id = 'typing-indicator';
    div.className = 'typing-indicator';
    div.textContent = t('El profesor estÃ¡ escribiendo...', 'Der Lehrer schreibt...', 'Le professeur écrit...');
    chat.appendChild(div);
    chat.scrollTop = chat.scrollHeight;
}

function hideTyping() {
    const el = document.getElementById('typing-indicator');
    if (el) el.remove();
}

renderNotes();
loadGrammarRules();
loadVocab('__all__');
</script>
</body>
</html>"""

full = header + '\n<style>' + css + html_body + js

with open('templates/index.html', 'w', encoding='utf-8') as f:
    f.write(full)

print(f'Written {len(full)} bytes')

