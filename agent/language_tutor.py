import json
from pathlib import Path

class LanguageTutorAgent:
    def __init__(self, language="English"):
        self.language = language
        self.core_vocab = []
        self.missions = []
        self.current_mission = None


    # -----------------------------
    # CARGA DE DATOS
    # -----------------------------
    def load_core_vocab(self, filepath: str):
        path = Path(filepath)
        if not path.exists():
            raise FileNotFoundError(f"El archivo de vocabulario no existe: {filepath}")

        with open(path, "r", encoding="utf-8") as f:
            self.core_vocab = json.load(f)

    GERMAN_TAG_KEYWORDS = {
        "animals": {"hund", "katze", "vogel", "fisch", "pferd", "schaf", "tier", "bär", "löwe", "tiger", "elefant", "affe", "hase", "maus", "fuchs", "wolf", "schlange", "schildkröte", "delfin", "hai", "insekt", "käfer", "flügel", "schwanz", "pfote", "fell", "schnabel"},
        "actions": {"laufen", "essen", "trinken", "lesen", "schreiben", "sprechen", "gehen", "nehmen", "geben", "machen", "sagen", "arbeiten", "lernen", "studieren", "sitzen", "stehen", "kaufen", "verkaufen", "bezahlen", "kochen", "putzen", "waschen", "fahren", "fliegen", "schwimmen", "springen", "singen", "tanzen", "malen", "bauen", "öffnen", "schließen", "finden", "halten", "bringen", "senden", "zeigen", "rufen", "beginnen", "enden", "versuchen", "brauchen", "wollen", "mögen", "lieben", "hassen", "glauben", "denken", "wissen", "verstehen", "erinnern", "vergessen", "wählen", "helfen", "können", "müssen", "dürfen", "sollen", "bewegen", "schneiden", "werfen", "fangen", "folgen", "ändern", "leben", "sterben", "lächeln", "weinen", "lachen", "klettern", "verstecken", "teilen", "ausgeben", "sparen", "verpassen", "gewinnen", "verlieren", "kämpfen", "besuchen", "treffen", "verlassen", "ankommen", "warten", "erwarten", "vorbereiten", "planen", "berichten", "erklären", "beschreiben", "diskutieren", "vorschlagen", "anbieten", "akzeptieren", "zustimmen", "ablehnen", "beweisen", "schützen", "vermeiden", "fortsetzen", "bleiben", "werden", "einschließen", "enthalten"},
        "food": {"essen", "trinken", "restaurant", "speisekarte", "frühstück", "mittagessen", "abendessen", "mahlzeit", "obst", "gemüse", "fleisch", "fisch", "brot", "reis", "nudeln", "suppe", "salat", "kuchen", "schokolade", "zucker", "salz", "pfeffer", "milch", "wasser", "saft", "kaffee", "tee", "bier", "wein", "teller", "tasse", "glas", "flasche", "messer", "gabel", "löffel", "kochen", "backen", "braten", "schmecken", "hungrig", "durstig", "käse", "butter", "ei", "hähnchen", "schwein", "soße", "nachtisch", "kartoffel", "tomate", "zwiebel", "knoblauch", "apfel", "banane", "orange", "traube", "erdbeere", "zitrone", "mais", "bohne", "nuss", "honig", "öl", "sahne", "snack", "küche", "rezept", "zutat", "mehl", "joghurt", "müsli", "nudel", "sandwich"},
        "travel": {"reise", "reisen", "flughafen", "hotel", "flug", "reise", "urlaub", "besuchen", "tour", "karte", "fahrkarte", "pass", "tasche", "koffer", "zug", "bus", "auto", "taxi", "fahrrad", "schiff", "flugzeug", "fahren", "fliegen", "ankommen", "abfahren", "buchen", "reservieren", "reiseführer", "tourist", "ausland", "land", "stadt", "dorf", "strand", "berg", "museum", "station", "hafen", "straße", "richtung", "norden", "süden", "osten", "westen", "gepäck", "abenteuer", "ziel", "passagier", "pilot", "fahrer", "abflug", "ankunft", "plan", "verspätung", "stornieren"},
        "phone": {"anruf", "telefon", "handy", "nachricht", "sms", "klingeln", "antworten", "auflegen", "wählen", "leitung", "mailbox", "kontakt", "nummer", "besetzt", "signal", "empfang", "lautsprecher", "stumm", "warten", "weiterleiten", "rückruf", "verpasst", "dringend", "erreichbar"},
        "email": {"email", "mail", "send", "senden", "bekommen", "schreiben", "posteingang", "anhängen", "weiterleiten", "antworten", "spam", "entwurf", "betreff", "cc", "bcc", "anhang", "ordner", "löschen", "archivieren", "signatur", "adresse", "verfassen", "erinnerung", "filter", "label", "faden", "empfänger", "absender", "postfach", "ausgang"},
        "hotel": {"hotel", "zimmer", "buchen", "reservieren", "rezeption", "reservierung", "suite", "einzelzimmer", "doppelzimmer", "check-in", "check-out", "lobby", "page", "zimmermädchen", "minibar", "zimmerservice", "handtuch", "kissen", "decke", "schlüsselkarte", "balkon", "wäscherei", "wlan", "frühstück", "inbegriffen", "gebühr", "kaution", "stornierung"},
        "shopping": {"kaufen", "verkaufen", "preis", "kosten", "bezahlen", "bar", "karte", "quittung", "rückgabe", "umtausch", "größe", "farbe", "marke", "rabatt", "angebot", "handeln", "kassenbon", "wechselgeld", "theke", "kassierer", "einkaufswagen", "korb", "regal", "vorrat", "verfügbar", "kasse", "lieferung"},
        "directions": {"geradeaus", "links", "rechts", "abbiegen", "ecke", "kreuzung", "ampel", "straße", "weg", "karte", "navigation", "richtung", "norden", "süden", "osten", "westen", "neben", "gegenüber", "zwischen", "hinter", "vor", "ende", "block", "viertel", "zentrum"},
        "sports": {"sport", "spiel", "mannschaft", "tor", "schiedsrichter", "trainer", "trainieren", "spieler", "fan", "stadion", "feld", "ball", "punkt", "sieg", "niederlage", "meisterschaft", "turnier", "liga", "laufen", "schwimmen", "radfahren", "turnen", "yoga", "fit", "übung"},
        "exercise": {"sport", "trainieren", "übung", "fitness", "studio", "laufen", "joggen", "schwimmen", "radfahren", "dehnen", "aufwärmen", "gewicht", "hantel", "wiederholen", "satz", "pause", "schweiß", "ausdauer", "kraft", "bewegung", "fit", "gesund"},
        "work": {"arbeit", "arbeiten", "büro", "job", "beruf", "kollege", "chef", "aufgabe", "projekt", "frist", "besprechung", "meeting", "termin", "formular", "bericht", "präsentation", "kunde", "lieferung", "bestellung", "rechnung", "gehalt", "bewerbung", "vertrag", "abteilung", "team", "aufgabe"},
    }

    FRENCH_TAG_KEYWORDS = {
        "animals": {"chat", "chien", "oiseau", "poisson", "cheval", "vache", "cochon", "mouton", "canard", "poule", "animal", "ours", "lion", "tigre", "elephant", "singe", "lapin", "souris", "renard", "loup", "chevre", "grenouille", "tortue", "dauphin", "requin", "insecte", "aile", "queue", "patte", "fourrure", "bec", "plume"},
        "actions": {"manger", "boire", "courir", "marcher", "nager", "sauter", "dormir", "lire", "ecrire", "parler", "dire", "aller", "venir", "prendre", "donner", "faire", "voir", "regarder", "ecouter", "acheter", "vendre", "payer", "cuisiner", "nettoyer", "laver", "conduire", "voler", "chanter", "danser", "construire", "ouvrir", "fermer", "trouver", "garder", "tenir", "apporter", "montrer", "appeler", "commencer", "finir", "essayer", "vouloir", "aimer", "pouvoir", "devoir", "savoir", "comprendre", "oublier", "choisir", "aider", "utiliser", "bouger", "couper", "lancer", "attraper", "suivre", "changer", "vivre", "sourire", "pleurer", "rire", "partager", "gagner", "perdre", "visiter", "rencontrer", "quitter", "arriver", "attendre", "preparer", "continuer", "rester", "devenir"},
        "food": {"manger", "boire", "restaurant", "menu", "petit-dejeuner", "dejeuner", "diner", "repas", "fruit", "legume", "viande", "poisson", "pain", "riz", "pates", "soupe", "salade", "gateau", "chocolat", "sucre", "sel", "poivre", "lait", "eau", "jus", "cafe", "the", "biere", "vin", "assiette", "tasse", "verre", "bouteille", "couteau", "fourchette", "cuillere", "cuire", "griller", "gouter", "faim", "soif", "fromage", "beurre", "oeuf", "poulet", "boeuf", "porc", "sauce", "dessert", "pomme", "tomate", "oignon", "ail", "banane", "orange", "raisin", "fraise", "citron", "noix", "miel", "huile", "creme", "snack", "cuisine", "recette", "ingredient", "farine", "yaourt", "cereale", "nouille", "sandwich", "pizza", "burger"},
        "travel": {"voyage", "voyager", "aeroport", "hotel", "vol", "vacances", "visite", "tour", "carte", "billet", "passeport", "sac", "valise", "train", "bus", "voiture", "taxi", "velo", "bateau", "avion", "conduire", "voler", "arriver", "partir", "reserver", "guide", "touriste", "etranger", "pays", "ville", "village", "plage", "montagne", "musee", "gare", "port", "rue", "direction", "nord", "sud", "est", "ouest", "bagage", "souvenir", "aventure", "destination", "passager", "pilote", "chauffeur", "depart", "arrivee", "horaire", "retard", "annuler"},
        "phone": {"appel", "telephone", "portable", "message", "sms", "sonner", "repondre", "raccrocher", "composer", "ligne", "messagerie", "contact", "numero", "occupe", "signal", "reception", "haut-parleur", "silencieux", "attendre", "transferer", "rappeler", "manque", "urgent", "joignable"},
        "email": {"email", "courriel", "envoyer", "recevoir", "ecrire", "boite", "joindre", "transferer", "repondre", "spam", "brouillon", "objet", "cc", "cci", "piece-jointe", "dossier", "supprimer", "archiver", "signature", "adresse", "composer", "rappel", "filtre", "etiquette", "fil", "destinataire", "expediteur"},
        "hotel": {"hotel", "chambre", "reserver", "reception", "reservation", "suite", "simple", "double", "enregistrement", "hall", "bagagiste", "femme-de-chambre", "minibar", "service-d-etage", "serviette", "oreiller", "couverture", "carte", "balcon", "linge", "wifi", "petit-dejeuner", "inclus", "frais", "caution", "annulation"},
        "shopping": {"acheter", "vendre", "prix", "couter", "payer", "especes", "carte", "recu", "remboursement", "echange", "taille", "couleur", "marque", "rabais", "solde", "marchander", "ticket", "monnaie", "comptoir", "caissier", "chariot", "panier", "rayon", "stock", "disponible", "caisse", "livraison"},
        "directions": {"tout-droit", "gauche", "droite", "tourner", "coin", "carrefour", "feu", "rue", "chemin", "carte", "navigation", "direction", "nord", "sud", "est", "ouest", "a-cote", "en-face", "entre", "derriere", "devant", "bout", "pate-de-maisons", "quartier", "centre"},
        "sports": {"sport", "jeu", "equipe", "but", "arbitre", "entraineur", "entrainer", "joueur", "fan", "stade", "terrain", "balle", "point", "victoire", "defaite", "championnat", "tournoi", "ligue", "courir", "nager", "velo", "gymnastique", "yoga", "forme", "exercice"},
        "exercise": {"sport", "entrainer", "exercice", "fitness", "salle", "courir", "jogging", "nager", "velo", "etirer", "echauffer", "poids", "haltere", "repetition", "serie", "pause", "sueur", "endurance", "force", "mouvement", "forme", "sain"},
        "work": {"travail", "travailler", "bureau", "emploi", "profession", "collegue", "chef", "tache", "projet", "delai", "reunion", "rendez-vous", "formulaire", "rapport", "presentation", "client", "livraison", "commande", "facture", "salaire", "candidature", "contrat", "departement", "equipe", "mission"},
    }

    TAG_KEYWORDS = {
        "animals": {"dog", "cat", "bird", "fish", "horse", "cow", "pig", "sheep", "duck", "chicken", "pet", "animal", "bear", "lion", "tiger", "elephant", "monkey", "rabbit", "mouse", "rat", "fox", "wolf", "goat", "donkey", "hen", "goose", "frog", "turtle", "shark", "whale", "dolphin", "insect", "bug", "snake", "lizard", "wing", "tail", "paw", "fur", "feather", "beak"},
        "actions": {"run", "eat", "walk", "play", "sleep", "drink", "read", "write", "speak", "talk", "listen", "go", "come", "take", "give", "make", "do", "say", "get", "see", "look", "watch", "hear", "ask", "answer", "work", "study", "learn", "teach", "sit", "stand", "buy", "sell", "pay", "cook", "clean", "wash", "drive", "fly", "swim", "jump", "sing", "dance", "draw", "paint", "build", "break", "open", "close", "turn", "put", "set", "find", "keep", "hold", "carry", "bring", "send", "show", "tell", "call", "start", "stop", "finish", "try", "need", "want", "like", "love", "hate", "hope", "wish", "believe", "think", "know", "understand", "remember", "forget", "choose", "decide", "help", "let", "allow", "can", "use", "move", "cut", "push", "pull", "throw", "catch", "follow", "lead", "change", "grow", "live", "die", "smile", "cry", "laugh", "shout", "whisper", "climb", "hide", "share", "spend", "save", "miss", "win", "lose", "fight", "visit", "join", "meet", "leave", "arrive", "pick", "drop", "wait", "expect", "prepare", "plan", "report", "explain", "describe", "discuss", "suggest", "offer", "refuse", "accept", "agree", "disagree", "argue", "prove", "protect", "prevent", "avoid", "continue", "remain", "exist", "appear", "seem", "become", "include", "contain", "consist", "involve", "represent", "indicate", "reveal", "announce", "declare", "claim", "admit", "deny", "confirm", "guarantee", "warn", "recommend", "introduce", "produce", "create", "design", "develop", "improve", "reduce", "increase", "expand", "extend", "limit", "control", "manage", "organize", "arrange", "collect", "gather", "spread", "divide", "separate", "combine", "connect", "compare", "contrast", "distinguish", "identify", "recognize", "consider", "evaluate", "analyze", "examine", "investigate", "define", "calculate", "measure", "test", "practice", "train", "exercise"},
        "food": {"food", "eat", "drink", "restaurant", "menu", "breakfast", "lunch", "dinner", "meal", "fruit", "vegetable", "meat", "fish", "bread", "rice", "pasta", "soup", "salad", "cake", "cookie", "chocolate", "sugar", "salt", "pepper", "milk", "water", "juice", "coffee", "tea", "beer", "wine", "plate", "cup", "glass", "bottle", "knife", "fork", "spoon", "cook", "bake", "boil", "fry", "taste", "hungry", "thirsty", "cheese", "butter", "egg", "chicken", "beef", "pork", "sauce", "dessert", "potato", "tomato", "onion", "garlic", "apple", "banana", "orange", "grape", "strawberry", "lemon", "corn", "bean", "nut", "honey", "oil", "cream", "snack", "kitchen", "oven", "stove", "microwave", "refrigerator", "freezer", "recipe", "ingredient", "flour", "yogurt", "cereal", "noodle", "sandwich", "pizza", "burger", "grill", "roast", "steam", "stir", "mix", "pour", "slice", "peel", "chop"},
        "travel": {"travel", "airport", "hotel", "flight", "trip", "vacation", "holiday", "visit", "tour", "map", "ticket", "passport", "bag", "suitcase", "train", "bus", "car", "taxi", "bike", "boat", "ship", "plane", "drive", "fly", "ride", "arrive", "leave", "depart", "book", "reserve", "guide", "tourist", "abroad", "foreign", "country", "city", "town", "village", "beach", "mountain", "museum", "hostel", "station", "port", "highway", "road", "street", "avenue", "route", "direction", "north", "south", "east", "west", "accommodation", "luggage", "souvenir", "adventure", "journey", "destination", "passenger", "crew", "pilot", "driver", "boarding", "departure", "arrival", "schedule", "delay", "cancel", "reservation", "sightseeing", "landmark", "downtown", "suburb", "coast", "island", "desert", "forest", "lake", "river"},
        "phone": {"call", "phone", "mobile", "message", "text", "ring", "answer", "hang", "dial", "line", "voicemail", "cell", "contact", "number", "busy", "signal", "reception", "speaker", "mute", "hold", "transfer", "callback", "missed", "urgent", "available", "reachable", "forward", "redial", "vibrate", "silent"},
        "email": {"email", "send", "receive", "write", "inbox", "attach", "forward", "reply", "spam", "draft", "subject", "cc", "bcc", "attachment", "folder", "delete", "archive", "signature", "address", "compose", "schedule", "reminder", "newsletter", "filter", "label", "thread", "recipient", "sender", "mailbox", "outbox"},
        "hotel": {"hotel", "room", "book", "reserve", "reception", "reservation", "suite", "single", "double", "checkin", "checkout", "lobby", "bellboy", "maid", "minibar", "roomservice", "towels", "pillow", "blanket", "keycard", "balcony", "amenities", "laundry", "wifi", "breakfast", "included", "extra", "charge", "deposit", "cancellation"},
        "shopping": {"buy", "sell", "price", "cost", "pay", "cash", "card", "receipt", "refund", "exchange", "size", "color", "brand", "discount", "sale", "offer", "bargain", "receipt", "change", "counter", "cashier", "cart", "basket", "aisle", "shelf", "stock", "available", "checkout", "return", "warranty", "delivery"},
        "directions": {"left", "right", "straight", "corner", "block", "cross", "follow", "sign", "traffic", "light", "pedestrian", "crosswalk", "sidewalk", "bridge", "tunnel", "intersection", "roundabout", "highway", "exit", "entrance", "north", "south", "east", "west", "direction", "route", "path", "way", "distance", "kilometer", "mile", "block", "avenue", "boulevard"},
        "work": {"job", "office", "meeting", "deadline", "boss", "colleague", "project", "report", "task", "schedule", "salary", "hire", "fire", "promotion", "interview", "resume", "contract", "shift", "overtime", "team", "manager", "employee", "employer", "training", "policy", "goal", "performance", "review", "budget", "invoice", "supplier", "client", "customer", "sales", "marketing", "production", "quality", "delivery", "order", "shipment"},
        "sports": {"football", "soccer", "match", "team", "player", "score", "goal", "win", "lose", "fan", "league", "championship", "tournament", "stadium", "coach", "referee", "penalty", "foul", "corner", "kick", "pass", "shoot", "defense", "offense", "midfield", "goalkeeper", "substitute", "bench", "injury", "half", "overtime", "final", "cup", "medal", "competition", "practice", "training"},
        "exercise": {"gym", "workout", "lift", "train", "muscle", "stretch", "cardio", "fitness", "health", "diet", "protein", "yoga", "pilates", "squat", "pushup", "pullup", "plank", "dumbbell", "barbell", "treadmill", "stationary", "bicycle", "rowing", "machine", "warmup", "cooldown", "repetition", "set", "routine", "personal", "trainer", "gym", "exercise", "active", "sweat", "endurance", "strength", "flexibility", "balance", "calories", "heart", "rate"}
    }

    def load_ngsl_vocab(self, filepath: str):
        path = Path(filepath)
        if not path.exists():
            raise FileNotFoundError(f"El archivo NGSL no existe: {filepath}")

        with open(path, "r", encoding="utf-8") as f:
            existing_words = {w["word"] for w in self.core_vocab}
            for line in f:
                line = line.strip()
                if not line or line.startswith("##"):
                    continue
                parts = [p.strip() for p in line.split(",")]
                headword = parts[0]
                if headword in existing_words:
                    continue
                forms = parts[1:] if len(parts) > 1 else []
                tags = []
                for tag, keywords in self.TAG_KEYWORDS.items():
                    if headword.lower() in keywords:
                        tags.append(tag)
                self.core_vocab.append({
                    "word": headword,
                    "forms": forms,
                    "tags": tags
                })

    def load_missions(self, filepath: str):
        path = Path(filepath)
        if not path.exists():
            raise FileNotFoundError(f"El archivo de misiones no existe: {filepath}")

        with open(path, "r", encoding="utf-8") as f:
            self.missions = json.load(f)

    # -----------------------------
    # SELECCIÓN DE MISIÓN
    # -----------------------------
    def select_mission(self, mission_id: str):
        for mission in self.missions:
            if mission["id"] == mission_id:
                self.current_mission = mission
                return mission
        raise ValueError(f"Misión no encontrada: {mission_id}")

    def get_mission_vocabulary(self):
        if not self.current_mission:
            raise ValueError("No hay misión seleccionada.")

        specific = self.current_mission.get("vocabulary_words")
        if specific:
            word_set = {w.lower() for w in specific}
            return [w for w in self.core_vocab if w["word"].lower() in word_set]

        tags = self.current_mission.get("vocabulary_tags", [])
        filtered = [w for w in self.core_vocab if any(tag in w["tags"] for tag in tags)]
        return filtered

    # -----------------------------
    # PLANTILLAS DE DIÁLOGO
    # -----------------------------
    # -----------------------------
    # PLANTILLAS DE EJERCICIOS POR TAG
    # -----------------------------
    EXERCISE_TEMPLATES_BY_TAG = {
        "animals": [
            {"sentence": "My ____ is very friendly.", "hint": "Mascota común"},
            {"sentence": "The ____ is sleeping on the sofa.", "hint": "Animal doméstico"},
            {"sentence": "I saw a ____ at the park yesterday.", "hint": "Animal que ves en la naturaleza"},
            {"sentence": "The ____ has beautiful feathers.", "hint": "Animal que vuela", "valid_answers": ["bird"]},
            {"sentence": "A ____ lives in water and can swim.", "hint": "Animal acuático", "valid_answers": ["fish"]},
        ],
        "actions": [
            {"sentence": "I like to ____ in the morning.", "hint": "Acción al despertar"},
            {"sentence": "She ____ English every day to improve.", "hint": "Presente simple: practicar un idioma", "valid_answers": ["practice"]},
            {"sentence": "Could you ____ me the salt, please?", "hint": "Pasar algo a alguien", "valid_answers": ["pass"]},
            {"sentence": "I am looking ____ my keys. Have you seen them?", "hint": "Preposición: buscar algo", "valid_answers": ["for"]},
            {"sentence": "She is ____ for a new job at the moment.", "hint": "Verbo presente continuo: buscar", "valid_answers": ["looking"]},
            {"sentence": "I am interested ____ learning new languages.", "hint": "Preposición después de interested", "valid_answers": ["in"]},
            {"sentence": "I need to ____ my password to log in.", "hint": "Recordar de nuevo", "valid_answers": ["remember"]},
            {"sentence": "Please ____ your name on the form.", "hint": "Poner información por escrito", "valid_answers": ["write"]},
            {"sentence": "Can you ____ me a favor?", "hint": "Pedir ayuda", "valid_answers": ["do"]},
            {"sentence": "I need to ____ a decision before Friday.", "hint": "Tomar una decisión", "valid_answers": ["make"]},
        ],
        "food": [
            {"sentence": "I need to buy some ____ at the supermarket.", "hint": "Comida que compras", "valid_answers": ["bread", "rice", "cheese", "fruit", "vegetable", "meat", "fish", "milk"]},
            {"sentence": "Would you like some ____ for dinner?", "hint": "Alimento para la cena", "valid_answers": ["bread", "rice", "cheese", "pasta", "chicken", "fish", "soup", "salad"]},
            {"sentence": "I always have ____ for breakfast.", "hint": "Comida de la mañana", "valid_answers": ["bread", "milk", "cheese", "fruit", "egg", "juice", "cereal"]},
            {"sentence": "Please pass me the ____, it's next to the bread.", "hint": "Producto lácteo", "valid_answers": ["cheese", "milk", "butter", "yogurt"]},
            {"sentence": "This ____ tastes delicious!", "hint": "Cualquier plato de comida"},
            {"sentence": "I'll have a glass of ____, please.", "hint": "Bebida común", "valid_answers": ["water", "juice", "milk", "coffee", "tea"]},
            {"sentence": "Can you ____ the vegetables for the salad?", "hint": "Cortar en trozos pequeños", "valid_answers": ["chop"]},
            {"sentence": "We need to ____ the chicken for 30 minutes.", "hint": "Cocinar en el horno", "valid_answers": ["bake", "roast"]},
        ],
        "travel": [
            {"sentence": "I went to the ____ last summer.", "hint": "Lugar de vacaciones", "valid_answers": ["beach", "island", "coast", "mountain", "city", "country"]},
            {"sentence": "We need to ____ a hotel before our trip.", "hint": "Acción antes de viajar", "valid_answers": ["book", "reserve"]},
            {"sentence": "They arrived ____ the airport on time.", "hint": "Preposición: llegar a un lugar", "valid_answers": ["at"]},
            {"sentence": "I am thinking ____ taking a vacation.", "hint": "Preposición: pensar en", "valid_answers": ["about"]},
            {"sentence": "The ____ was delayed due to bad weather.", "hint": "Avión programado", "valid_answers": ["flight", "plane"]},
            {"sentence": "I packed my ____ the night before the trip.", "hint": "Maleta para el viaje", "valid_answers": ["suitcase", "bag", "luggage"]},
            {"sentence": "The ____ from the hotel had a beautiful view.", "hint": "Habitación del hotel", "valid_answers": ["room"]},
        ],
        "hotel": [
            {"sentence": "I would like to ____ a room for two nights.", "hint": "Apartar una habitación", "valid_answers": ["book", "reserve"]},
            {"sentence": "The ____ at this hotel is very professional.", "hint": "Personal de bienvenida", "valid_answers": ["reception", "staff"]},
            {"sentence": "____ is included with the room rate.", "hint": "Comida de la mañana", "valid_answers": ["breakfast"]},
            {"sentence": "Please ____ at least two hours before departure.", "hint": "Registrarse en el aeropuerto u hotel", "valid_answers": ["check"]},
            {"sentence": "The hotel offers a ____ service for laundry.", "hint": "Recogida y entrega", "valid_answers": ["pickup", "delivery"]},
            {"sentence": "We stayed in a ____ room with two beds.", "hint": "Tipo de habitación para dos camas", "valid_answers": ["double", "twin"]},
        ],
        "directions": [
            {"sentence": "Go straight ____ the traffic lights.", "hint": "Preposición: hasta", "valid_answers": ["to"]},
            {"sentence": "Turn ____ at the next corner.", "hint": "Opuesto de derecha", "valid_answers": ["left"]},
            {"sentence": "The bank is ____ the supermarket.", "hint": "Preposición: al lado de", "valid_answers": ["near", "next"]},
            {"sentence": "Can you tell me where the ____ is?", "hint": "Punto de referencia"},
            {"sentence": "Walk two ____ and then turn right.", "hint": "Tramo de calle entre dos calles", "valid_answers": ["blocks"]},
            {"sentence": "The museum is on the ____ side of the street.", "hint": "Opuesto de izquierda", "valid_answers": ["right"]},
        ],
        "shopping": [
            {"sentence": "How much does this ____ cost?", "hint": "Lo que pagas en la tienda"},
            {"sentence": "Can I ____ by credit card?", "hint": "Dar dinero por algo", "valid_answers": ["pay"]},
            {"sentence": "Could I have the ____, please?", "hint": "Comprobante de pago", "valid_answers": ["receipt"]},
            {"sentence": "Is this ____ on sale this week?", "hint": "Artículo que quieres comprar"},
            {"sentence": "I need a ____ for these groceries.", "hint": "Carrito de compras", "valid_answers": ["cart", "basket"]},
            {"sentence": "The ____ gave me my change.", "hint": "Persona que cobra", "valid_answers": ["cashier"]},
        ],
        "phone": [
            {"sentence": "I will ____ you as soon as I arrive.", "hint": "Llamar por teléfono", "valid_answers": ["call"]},
            {"sentence": "He is ____ on the phone right now.", "hint": "Verbo para hablar con alguien", "valid_answers": ["speaking", "talking"]},
            {"sentence": "Could you ____ me your phone number?", "hint": "Dar información a alguien", "valid_answers": ["give", "tell"]},
            {"sentence": "Please ____ the line, I'll transfer you.", "hint": "Esperar sin colgar", "valid_answers": ["hold"]},
            {"sentence": "I missed your ____, I'll call you back.", "hint": "Llamada telefónica", "valid_answers": ["call"]},
            {"sentence": "Can you ____ a message for her?", "hint": "Anotar un mensaje", "valid_answers": ["take"]},
        ],
        "email": [
            {"sentence": "Please ____ me the report by email.", "hint": "Enviar un archivo", "valid_answers": ["send"]},
            {"sentence": "I will ____ the documents to you.", "hint": "Pegar un archivo al correo", "valid_answers": ["attach"]},
            {"sentence": "I look forward ____ hearing from you soon.", "hint": "Preposición en emails formales", "valid_answers": ["to"]},
            {"sentence": "Please ____ the email before sending it.", "hint": "Leer para buscar errores", "valid_answers": ["check", "review", "read"]},
            {"sentence": "I'll ____ to your message as soon as possible.", "hint": "Responder un correo", "valid_answers": ["reply"]},
        ],
        "work": [
            {"sentence": "The ____ for this project is next Friday.", "hint": "Fecha límite", "valid_answers": ["deadline"]},
            {"sentence": "We have a ____ every Monday morning.", "hint": "Reunión de trabajo", "valid_answers": ["meeting"]},
            {"sentence": "He is responsible ____ training new staff.", "hint": "Preposición después de responsible", "valid_answers": ["for"]},
            {"sentence": "She is good ____ solving problems.", "hint": "Preposición después de good", "valid_answers": ["at"]},
            {"sentence": "Please ____ the form and send it back.", "hint": "Llenar un documento", "valid_answers": ["complete", "fill"]},
            {"sentence": "We need to ____ the order before Friday.", "hint": "Procesar un pedido", "valid_answers": ["process", "complete", "fill"]},
            {"sentence": "I ____ that we should change suppliers.", "hint": "Opinar o proponer algo", "valid_answers": ["think", "believe", "suggest"]},
            {"sentence": "The delivery will ____ on Monday morning.", "hint": "Llegar a destino", "valid_answers": ["arrive"]},
            {"sentence": "The ____ checked the products for defects.", "hint": "Persona que revisa calidad", "valid_answers": ["inspector", "quality", "manager"]},
            {"sentence": "Please ____ the machine before using it.", "hint": "Poner en funcionamiento", "valid_answers": ["operate", "start"]},
        ],
        "sports": [
            {"sentence": "The ____ scored a goal in the first half.", "hint": "Jugador que anota", "valid_answers": ["player", "forward", "striker"]},
            {"sentence": "They won the ____ last season.", "hint": "Campeonato", "valid_answers": ["championship", "league", "cup", "tournament"]},
            {"sentence": "The ____ blew his whistle for a foul.", "hint": "Árbitro en inglés", "valid_answers": ["referee"]},
            {"sentence": "He ____ the ball to his teammate.", "hint": "Enviar el balón a otro jugador", "valid_answers": ["passed", "kicked", "threw"]},
            {"sentence": "The ____ between the two teams was exciting.", "hint": "Partido deportivo", "valid_answers": ["match", "game"]},
            {"sentence": "The ____ cheered when their team scored.", "hint": "Aficionados en el estadio", "valid_answers": ["fans", "crowd"]},
        ],
        "exercise": [
            {"sentence": "I ____ weights at the gym three times a week.", "hint": "Levantar pesas", "valid_answers": ["lift"]},
            {"sentence": "You should ____ before working out.", "hint": "Preparar los músculos", "valid_answers": ["stretch"]},
            {"sentence": "She runs on the ____ for twenty minutes.", "hint": "Máquina para correr", "valid_answers": ["treadmill"]},
            {"sentence": "I do ____ every morning to stay fit.", "hint": "Actividad física general", "valid_answers": ["exercise", "workout"]},
            {"sentence": "Drink plenty of ____ when you exercise.", "hint": "Líquido vital", "valid_answers": ["water"]},
            {"sentence": "Take a ____ between sets to recover.", "hint": "Pausa para descansar", "valid_answers": ["rest", "break"]},
        ]
    }

    # -----------------------------
    # PLANTILLAS DE EJERCICIOS EN ALEMÁN
    # -----------------------------
    EXERCISE_TEMPLATES_BY_TAG_DE = {
        "animals": [
            {"sentence": "Mein ____ ist sehr freundlich.", "hint": "Mascota común"},
            {"sentence": "Die ____ schläft auf dem Sofa.", "hint": "Animal doméstico"},
            {"sentence": "Ich habe gestern einen ____ im Park gesehen.", "hint": "Animal en la naturaleza"},
            {"sentence": "Der ____ hat schöne Federn.", "hint": "Animal que vuela", "valid_answers": ["Vogel"]},
            {"sentence": "Ein ____ lebt im Wasser und kann schwimmen.", "hint": "Animal acuático", "valid_answers": ["Fisch"]},
        ],
        "actions": [
            {"sentence": "Ich ____ jeden Morgen um sechs Uhr auf.", "hint": "Verbo separable: aufstehen"},
            {"sentence": "Er ____ Deutsch, um sich zu verbessern.", "hint": "Presente: üben"},
            {"sentence": "Kannst du mir bitte das Salz ____?", "hint": "Dar algo a alguien", "valid_answers": ["geben", "reichen"]},
            {"sentence": "Ich ____ meine Schlüssel. Hast du sie gesehen?", "hint": "Buscar", "valid_answers": ["suche"]},
            {"sentence": "Sie ____ sich auf die Prüfung vor.", "hint": "Prepararse", "valid_answers": ["bereitet"]},
            {"sentence": "Ich muss mein Passwort ____.", "hint": "Recordar", "valid_answers": ["merken", "wiederholen"]},
            {"sentence": "Bitte ____ deinen Namen auf das Formular.", "hint": "Escribir", "valid_answers": ["schreiben"]},
            {"sentence": "Kannst du mir einen Gefallen ____?", "hint": "Hacer un favor", "valid_answers": ["tun"]},
            {"sentence": "Ich muss eine Entscheidung ____.", "hint": "Tomar", "valid_answers": ["treffen"]},
        ],
        "food": [
            {"sentence": "Ich muss ____ im Supermarkt kaufen.", "hint": "Comida que compras", "valid_answers": ["Brot", "Käse", "Obst", "Gemüse", "Fleisch", "Fisch", "Milch"]},
            {"sentence": "Möchtest du etwas ____ zum Abendessen?", "hint": "Comida para la cena", "valid_answers": ["Brot", "Käse", "Reis", "Fisch", "Suppe", "Salat"]},
            {"sentence": "Ich trinke gern ____ zum Frühstück.", "hint": "Bebida", "valid_answers": ["Milch", "Kaffee", "Tee", "Saft", "Wasser"]},
            {"sentence": "Dieses ____ schmeckt ausgezeichnet!", "hint": "Cualquier plato"},
            {"sentence": "Ich möchte ein Glas ____, bitte.", "hint": "Bebida común", "valid_answers": ["Wasser", "Saft", "Milch", "Kaffee", "Tee"]},
            {"sentence": "Kannst du das Gemüse für den Salat ____?", "hint": "Cortar", "valid_answers": ["schneiden"]},
        ],
        "travel": [
            {"sentence": "Ich bin letzten Sommer ans ____ gefahren.", "hint": "Lugar de vacaciones", "valid_answers": ["Meer", "Strand", "Insel", "Berg"]},
            {"sentence": "Wir müssen ein Hotel für unsere Reise ____.", "hint": "Reservar", "valid_answers": ["buchen", "reservieren"]},
            {"sentence": "Sie sind pünktlich am Flughafen ____.", "hint": "Llegar", "valid_answers": ["angekommen"]},
            {"sentence": "Der ____ hatte Verspätung wegen des Wetters.", "hint": "Avión programado", "valid_answers": ["Flug"]},
            {"sentence": "Ich habe meinen ____ am Abend vor der Reise gepackt.", "hint": "Maleta", "valid_answers": ["Koffer", "Tasche"]},
        ],
        "hotel": [
            {"sentence": "Ich möchte ein Zimmer für zwei Nächte ____.", "hint": "Reservar", "valid_answers": ["buchen", "reservieren"]},
            {"sentence": "Die ____ in diesem Hotel ist sehr professionell.", "hint": "Recepción", "valid_answers": ["Rezeption"]},
            {"sentence": "____ ist im Zimmerpreis inbegriffen.", "hint": "Desayuno", "valid_answers": ["Frühstück"]},
            {"sentence": "Bitte ____ Sie mindestens zwei Stunden vor Abflug.", "hint": "Check-in", "valid_answers": ["checken"]},
            {"sentence": "Das Hotel bietet einen ____-Service für die Wäsche an.", "hint": "Recogida", "valid_answers": ["Hol", "Bring"]},
        ],
        "directions": [
            {"sentence": "Gehen Sie ____ bis zur Ampel.", "hint": "Recto", "valid_answers": ["geradeaus"]},
            {"sentence": "Biegen Sie an der nächsten Ecke ____ ab.", "hint": "Izquierda", "valid_answers": ["links"]},
            {"sentence": "Die Bank ist ____ dem Supermarkt.", "hint": "Al lado de", "valid_answers": ["neben"]},
            {"sentence": "Können Sie mir sagen, wo der ____ ist?", "hint": "Punto de referencia"},
            {"sentence": "Gehen Sie zwei ____ und dann rechts.", "hint": "Manzanas", "valid_answers": ["Straßen"]},
        ],
        "shopping": [
            {"sentence": "Wie viel ____ dieser Artikel?", "hint": "Costar", "valid_answers": ["kostet"]},
            {"sentence": "Kann ich mit Karte ____?", "hint": "Pagar", "valid_answers": ["bezahlen"]},
            {"sentence": "Kann ich die ____ bekommen, bitte?", "hint": "Recibo", "valid_answers": ["Quittung"]},
            {"sentence": "Ist dieser ____ diese Woche im Angebot?", "hint": "Artículo"},
            {"sentence": "Ich brauche einen ____ für die Einkäufe.", "hint": "Carrito", "valid_answers": ["Wagen", "Korb"]},
            {"sentence": "Der ____ hat mir das Wechselgeld gegeben.", "hint": "Cajero", "valid_answers": ["Kassierer"]},
        ],
        "phone": [
            {"sentence": "Ich ____ dich an, sobald ich ankomme.", "hint": "Llamar", "valid_answers": ["rufe"]},
            {"sentence": "Er ____ gerade am Telefon.", "hint": "Hablar", "valid_answers": ["spricht"]},
            {"sentence": "Kannst du mir deine Telefonnummer ____?", "hint": "Dar", "valid_answers": ["geben"]},
            {"sentence": "Bitte ____ Sie die Leitung, ich verbinde Sie.", "hint": "Esperar", "valid_answers": ["halten"]},
            {"sentence": "Ich habe deinen ____ verpasst.", "hint": "Llamada", "valid_answers": ["Anruf"]},
            {"sentence": "Kannst du eine ____ für sie aufnehmen?", "hint": "Mensaje", "valid_answers": ["Nachricht"]},
        ],
        "email": [
            {"sentence": "Bitte ____ Sie mir den Bericht per E-Mail.", "hint": "Enviar", "valid_answers": ["senden", "schicken"]},
            {"sentence": "Ich werde die Dokumente an die E-Mail ____.", "hint": "Adjuntar", "valid_answers": ["anhängen"]},
            {"sentence": "Bitte ____ Sie die E-Mail vor dem Senden.", "hint": "Revisar", "valid_answers": ["prüfen", "kontrollieren"]},
            {"sentence": "Ich ____ auf Ihre Nachricht so bald wie möglich.", "hint": "Responder", "valid_answers": ["antworte"]},
        ],
        "work": [
            {"sentence": "Die ____ für dieses Projekt ist nächsten Freitag.", "hint": "Fecha límite", "valid_answers": ["Frist"]},
            {"sentence": "Wir haben jeden Montagmorgen eine ____.", "hint": "Reunión", "valid_answers": ["Besprechung"]},
            {"sentence": "Bitte ____ Sie das Formular aus und senden Sie es zurück.", "hint": "Llenar", "valid_answers": ["füllen"]},
            {"sentence": "Wir müssen die Bestellung vor Freitag ____.", "hint": "Procesar", "valid_answers": ["bearbeiten"]},
            {"sentence": "Die Lieferung wird am Montagmorgen ____.", "hint": "Llegar", "valid_answers": ["ankommen"]},
            {"sentence": "Bitte ____ Sie die Maschine vor der Benutzung.", "hint": "Operar", "valid_answers": ["bedienen"]},
        ],
        "sports": [
            {"sentence": "Der ____ hat ein Tor in der ersten Hälfte geschossen.", "hint": "Jugador", "valid_answers": ["Spieler"]},
            {"sentence": "Sie haben die ____ letzte Saison gewonnen.", "hint": "Campeonato", "valid_answers": ["Meisterschaft"]},
            {"sentence": "Der ____ hat wegen eines Fouls gepfiffen.", "hint": "Árbitro", "valid_answers": ["Schiedsrichter"]},
            {"sentence": "Er ____ den Ball zu seinem Mitspieler.", "hint": "Pasar", "valid_answers": ["passt"]},
            {"sentence": "Das ____ zwischen den beiden Teams war spannend.", "hint": "Partido", "valid_answers": ["Spiel"]},
            {"sentence": "Die ____ jubelten, als ihr Team ein Tor schoss.", "hint": "Aficionados", "valid_answers": ["Fans"]},
        ],
        "exercise": [
            {"sentence": "Ich ____ Gewichte im Fitnessstudio.", "hint": "Levantar", "valid_answers": ["hebe"]},
            {"sentence": "Du solltest dich vor dem Training ____.", "hint": "Estirar", "valid_answers": ["dehnen"]},
            {"sentence": "Sie läuft zwanzig Minuten auf dem ____.", "hint": "Cinta de correr", "valid_answers": ["Laufband"]},
            {"sentence": "Ich mache jeden Morgen ____, um fit zu bleiben.", "hint": "Ejercicio general", "valid_answers": ["Sport", "Übungen"]},
            {"sentence": "Trinke viel ____, wenn du Sport machst.", "hint": "Agua", "valid_answers": ["Wasser"]},
            {"sentence": "Mach eine ____ zwischen den Sätzen.", "hint": "Pausa", "valid_answers": ["Pause"]},
        ]
    }

    EXERCISE_TEMPLATES_BY_TAG_FR = {
        "animals": [
            {"sentence": "Mon ____ est tres gentil.", "hint": "Animal de compagnie"},
            {"sentence": "Le ____ dort sur le canape.", "hint": "Animal domestique"},
            {"sentence": "J'ai vu un ____ au parc hier.", "hint": "Animal dans la nature"},
            {"sentence": "Le ____ a de belles plumes.", "hint": "Animal qui vole", "valid_answers": ["oiseau"]},
            {"sentence": "Un ____ vit dans l'eau et peut nager.", "hint": "Animal aquatique", "valid_answers": ["poisson"]},
        ],
        "actions": [
            {"sentence": "Je ____ de l'eau tous les matins.", "hint": "Action au reveil", "valid_answers": ["bois"]},
            {"sentence": "Elle ____ le francais tous les jours pour s'ameliorer.", "hint": "Present: pratiquer une langue", "valid_answers": ["pratique"]},
            {"sentence": "Pourrais-tu me ____ le sel, s'il te plait?", "hint": "Passer quelque chose", "valid_answers": ["passer", "donner"]},
            {"sentence": "Je ____ mes cles. Les as-tu vues?", "hint": "Chercher", "valid_answers": ["cherche"]},
            {"sentence": "Elle ____ un nouveau travail en ce moment.", "hint": "Present continu: chercher", "valid_answers": ["cherche"]},
            {"sentence": "Je m'interesse ____ apprendre de nouvelles langues.", "hint": "Preposition apres interesser", "valid_answers": ["a"]},
            {"sentence": "Je dois ____ mon mot de passe pour me connecter.", "hint": "Se souvenir de nouveau", "valid_answers": ["retenir", "rappeler"]},
            {"sentence": "Veuillez ____ votre nom sur le formulaire.", "hint": "Mettre par ecrit", "valid_answers": ["ecrire"]},
            {"sentence": "Peux-tu me ____ un service?", "hint": "Demander de l'aide", "valid_answers": ["rendre"]},
            {"sentence": "Je dois ____ une decision avant vendredi.", "hint": "Prendre une decision", "valid_answers": ["prendre"]},
        ],
        "food": [
            {"sentence": "Je dois acheter du ____ au supermarche.", "hint": "Nourriture a acheter", "valid_answers": ["pain", "fromage", "fruit", "legume", "viande", "poisson", "lait"]},
            {"sentence": "Veux-tu du ____ pour le diner?", "hint": "Aliment pour le diner", "valid_answers": ["pain", "fromage", "riz", "poulet", "poisson", "soupe", "salade"]},
            {"sentence": "Je prends toujours du ____ au petit-dejeuner.", "hint": "Nourriture du matin", "valid_answers": ["pain", "lait", "fromage", "fruit", "oeuf", "jus", "cafe"]},
            {"sentence": "Passe-moi le ____, s'il te plait.", "hint": "Produit laitier", "valid_answers": ["fromage", "lait", "beurre", "yaourt"]},
            {"sentence": "Ce ____ est delicieux!", "hint": "N'importe quel plat"},
            {"sentence": "Je vais prendre un verre d'____, s'il vous plait.", "hint": "Boisson courante", "valid_answers": ["eau", "jus", "lait", "cafe", "the"]},
            {"sentence": "Peux-tu ____ les legumes pour la salade?", "hint": "Couper en petits morceaux", "valid_answers": ["couper"]},
            {"sentence": "Nous devons ____ le poulet pendant 30 minutes.", "hint": "Cuire au four", "valid_answers": ["cuire", "rotir"]},
        ],
        "travel": [
            {"sentence": "Je suis alle(e) a la ____ l'ete dernier.", "hint": "Lieu de vacances", "valid_answers": ["plage", "montagne", "ville", "campagne"]},
            {"sentence": "Nous devons ____ un hotel avant notre voyage.", "hint": "Action avant de voyager", "valid_answers": ["reserver", "booker"]},
            {"sentence": "Ils sont arrives ____ l'aeroport a l'heure.", "hint": "Preposition: arriver dans un lieu", "valid_answers": ["a"]},
            {"sentence": "Le ____ a ete retarde a cause du mauvais temps.", "hint": "Avion programme", "valid_answers": ["vol", "avion"]},
            {"sentence": "J'ai fait ma ____ la veille du voyage.", "hint": "Valise pour le voyage", "valid_answers": ["valise", "bagage"]},
            {"sentence": "La ____ de l'hotel avait une belle vue.", "hint": "Chambre d'hotel", "valid_answers": ["chambre"]},
        ],
        "hotel": [
            {"sentence": "Je voudrais ____ une chambre pour deux nuits.", "hint": "Reserver une chambre", "valid_answers": ["reserver", "booker"]},
            {"sentence": "La ____ de cet hotel est tres professionnelle.", "hint": "Personnel d'accueil", "valid_answers": ["reception", "accueil"]},
            {"sentence": "Le ____ est inclus dans le prix de la chambre.", "hint": "Repas du matin", "valid_answers": ["petit-dejeuner"]},
            {"sentence": "Veuillez ____ au moins deux heures avant le depart.", "hint": "S'enregistrer a l'aeroport ou a l'hotel", "valid_answers": ["vous-enregistrer", "checker"]},
            {"sentence": "L'hotel propose un service de ____ pour le linge.", "hint": "Enlevement et livraison", "valid_answers": ["blanchisserie", "nettoyage"]},
            {"sentence": "Nous avons sejourne dans une chambre ____ avec deux lits.", "hint": "Type de chambre pour deux lits", "valid_answers": ["double", "twin"]},
        ],
        "directions": [
            {"sentence": "Allez tout droit ____ aux feux.", "hint": "Preposition: jusqu'a", "valid_answers": ["jusqu"]},
            {"sentence": "Tournez ____ au prochain coin.", "hint": "Oppose de droite", "valid_answers": ["a-gauche", "gauche"]},
            {"sentence": "La banque est ____ du supermarche.", "hint": "A cote de", "valid_answers": ["a-cote", "pres"]},
            {"sentence": "Pouvez-vous me dire ou se trouve ____?", "hint": "Point de repere"},
            {"sentence": "Marchez deux ____ et puis tournez a droite.", "hint": "Troncon de rue entre deux rues", "valid_answers": ["rues", "pates-de-maisons"]},
            {"sentence": "Le musee est sur le ____ de la rue.", "hint": "Cote oppose a gauche", "valid_answers": ["droit", "cote-droit"]},
        ],
        "shopping": [
            {"sentence": "Combien coute cet ____?", "hint": "Ce que vous payez au magasin"},
            {"sentence": "Puis-je ____ par carte de credit?", "hint": "Donner de l'argent pour quelque chose", "valid_answers": ["payer"]},
            {"sentence": "Pourrais-je avoir le ____, s'il vous plait?", "hint": "Preuve de paiement", "valid_answers": ["recu", "ticket"]},
            {"sentence": "Est-ce que cet ____ est en solde cette semaine?", "hint": "Article que vous voulez acheter"},
            {"sentence": "J'ai besoin d'un ____ pour ces courses.", "hint": "Caddie de courses", "valid_answers": ["chariot", "panier"]},
            {"sentence": "Le ____ m'a rendu la monnaie.", "hint": "Personne qui encaisse", "valid_answers": ["caissier", "caissiere"]},
        ],
        "phone": [
            {"sentence": "Je te ____ des que j'arrive.", "hint": "Appeler par telephone", "valid_answers": ["appelle"]},
            {"sentence": "Il est en train de ____ au telephone.", "hint": "Parler avec quelqu'un", "valid_answers": ["parler"]},
            {"sentence": "Pourrais-tu me ____ ton numero de telephone?", "hint": "Donner des informations", "valid_answers": ["donner"]},
            {"sentence": "Veuillez ____ la ligne, je vous transfere.", "hint": "Attendre sans raccrocher", "valid_answers": ["garder"]},
            {"sentence": "J'ai rate ton ____, je te rappelle.", "hint": "Appel telephonique", "valid_answers": ["appel"]},
            {"sentence": "Peux-tu ____ un message pour elle?", "hint": "Noter un message", "valid_answers": ["prendre", "laisser"]},
        ],
        "email": [
            {"sentence": "Veuillez me ____ le rapport par email.", "hint": "Envoyer un fichier", "valid_answers": ["envoyer"]},
            {"sentence": "Je vais ____ les documents au courriel.", "hint": "Attacher un fichier", "valid_answers": ["joindre", "attacher"]},
            {"sentence": "Veuillez ____ l'email avant de l'envoyer.", "hint": "Relire pour trouver des erreurs", "valid_answers": ["verifier", "relire"]},
            {"sentence": "Je ____ a votre message des que possible.", "hint": "Repondre a un courriel", "valid_answers": ["repondrai"]},
        ],
        "work": [
            {"sentence": "Le ____ pour ce projet est vendredi prochain.", "hint": "Date limite", "valid_answers": ["delai"]},
            {"sentence": "Nous avons une ____ tous les lundis matin.", "hint": "Reunion de travail", "valid_answers": ["reunion"]},
            {"sentence": "Il est responsable ____ la formation du personnel.", "hint": "Preposition apres responsable", "valid_answers": ["de"]},
            {"sentence": "Veuillez ____ le formulaire et le renvoyer.", "hint": "Remplir un document", "valid_answers": ["remplir", "completer"]},
            {"sentence": "Nous devons ____ la commande avant vendredi.", "hint": "Traiter une commande", "valid_answers": ["traiter", "preparer"]},
            {"sentence": "La livraison ____ lundi matin.", "hint": "Arriver a destination", "valid_answers": ["arrivera"]},
        ],
        "sports": [
            {"sentence": "Le ____ a marque un but en premiere mi-temps.", "hint": "Joueur qui marque", "valid_answers": ["joueur"]},
            {"sentence": "Ils ont gagne le ____ la saison derniere.", "hint": "Championnat", "valid_answers": ["championnat", "tournoi", "trophee"]},
            {"sentence": "L'____ a siffle pour une faute.", "hint": "Arbitre", "valid_answers": ["arbitre"]},
            {"sentence": "Il ____ la balle a son coequipier.", "hint": "Envoyer le ballon a un autre joueur", "valid_answers": ["passe"]},
            {"sentence": "Le ____ entre les deux equipes etait passionnant.", "hint": "Match sportif", "valid_answers": ["match", "jeu"]},
            {"sentence": "Les ____ ont acclame quand leur equipe a marque.", "hint": "Supporters dans le stade", "valid_answers": ["supporters", "fans"]},
        ],
        "exercise": [
            {"sentence": "Je ____ des poids a la salle de sport trois fois par semaine.", "hint": "Soulever des poids", "valid_answers": ["souleve"]},
            {"sentence": "Tu devrais ____ avant de faire de l'exercice.", "hint": "Preparer les muscles", "valid_answers": ["t-etirer", "etirer"]},
            {"sentence": "Elle court sur le ____ pendant vingt minutes.", "hint": "Machine pour courir", "valid_answers": ["tapis-de-course"]},
            {"sentence": "Je fais du ____ tous les matins pour rester en forme.", "hint": "Activite physique generale", "valid_answers": ["sport", "exercice"]},
            {"sentence": "Bois beaucoup d'____ quand tu fais du sport.", "hint": "Liquide vital", "valid_answers": ["eau"]},
            {"sentence": "Fais une ____ entre les series pour recuperer.", "hint": "Pause pour se reposer", "valid_answers": ["pause", "paus"]},
        ]
    }

    # -----------------------------
    # REGLAS GRAMATICALES (EN)
    # -----------------------------
    GRAMMAR_RULES = [
        {
            "id": "present_simple",
            "title": "Present Simple",
            "description": "Se usa para hechos generales, rutinas y hábitos.",
            "formula": "Sujeto + verbo (base form) / He/She/It + verbo+s",
            "negative": "Sujeto + don't/doesn't + verbo",
            "question": "Do/Does + sujeto + verbo?",
            "examples": ["I walk to work every day.", "She reads the news in the morning.", "They don't like coffee.", "Does he play tennis?"],
            "exercises": [
                {"sentence": "She ____ (go) to the gym every morning.", "answer": "goes", "hint": "He/She/It añade -s"},
                {"sentence": "They ____ (not/like) spicy food.", "answer": "don't like", "hint": "Negativo con don't"},
                {"sentence": "____ he ____ (work) on Sundays?", "answer": "Does work", "hint": "Pregunta con does"},
                {"sentence": "I always ____ (drink) coffee at breakfast.", "answer": "drink", "hint": "I usa el verbo sin cambios"},
                {"sentence": "My sister ____ (study) at the library every day.", "answer": "studies", "hint": "Verbo terminado en -y cambia a -ies"},
            ]
        },
        {
            "id": "present_continuous",
            "title": "Present Continuous",
            "description": "Se usa para acciones que están ocurriendo ahora mismo o planes futuros cercanos.",
            "formula": "Sujeto + am/is/are + verbo+ing",
            "negative": "Sujeto + am/is/are + not + verbo+ing",
            "question": "Am/Is/Are + sujeto + verbo+ing?",
            "examples": ["I am reading a book right now.", "She is working on a project.", "They are not coming to the party.", "Are you listening to me?"],
            "exercises": [
                {"sentence": "She ____ (read) a book right now.", "answer": "is reading", "hint": "Present continuous con she"},
                {"sentence": "They ____ (play) football at the moment.", "answer": "are playing", "hint": "Present continuous con they"},
                {"sentence": "I ____ (not/watch) TV right now.", "answer": "am not watching", "hint": "Negativo con I"},
                {"sentence": "____ you ____ (wait) for the bus?", "answer": "Are waiting", "hint": "Pregunta con you"},
                {"sentence": "He ____ (study) for his exam this week.", "answer": "is studying", "hint": "Plan cercano con he"},
            ]
        },
        {
            "id": "past_simple",
            "title": "Past Simple",
            "description": "Se usa para acciones completadas en el pasado.",
            "formula": "Sujeto + verbo en pasado (regular: -ed / irregular)",
            "negative": "Sujeto + didn't + verbo (base form)",
            "question": "Did + sujeto + verbo (base form)?",
            "examples": ["I visited my grandmother yesterday.", "She went to the cinema last night.", "They didn't finish the project.", "Did you see the movie?"],
            "exercises": [
                {"sentence": "She ____ (visit) her grandmother yesterday.", "answer": "visited", "hint": "Pasado regular añade -ed"},
                {"sentence": "They ____ (go) to the beach last weekend.", "answer": "went", "hint": "Go es irregular → went"},
                {"sentence": "I ____ (not/eat) breakfast this morning.", "answer": "didn't eat", "hint": "Negativo con didn't + verbo base"},
                {"sentence": "____ you ____ (see) the match last night?", "answer": "Did see", "hint": "Pregunta con did + verbo base"},
                {"sentence": "He ____ (buy) a new car last month.", "answer": "bought", "hint": "Buy es irregular → bought"},
            ]
        },
        {
            "id": "future_will",
            "title": "Future with Will",
            "description": "Se usa para predicciones, decisiones espontáneas y promesas.",
            "formula": "Sujeto + will + verbo (base form)",
            "negative": "Sujeto + will not (won't) + verbo",
            "question": "Will + sujeto + verbo?",
            "examples": ["I will call you tomorrow.", "She won't be late.", "Will they come to the party?", "It will rain later."],
            "exercises": [
                {"sentence": "I ____ (call) you when I arrive.", "answer": "will call", "hint": "Promesa con will"},
                {"sentence": "She ____ (not/be) late for the meeting.", "answer": "won't be", "hint": "Negativo: will not = won't"},
                {"sentence": "____ they ____ (come) to the party?", "answer": "Will come", "hint": "Pregunta con will"},
                {"sentence": "It ____ (rain) tomorrow according to the forecast.", "answer": "will rain", "hint": "Predicción con will"},
            ]
        },
        {
            "id": "going_to",
            "title": "Going to (Futuro)",
            "description": "Se usa para planes e intenciones futuras, y para predicciones con evidencia.",
            "formula": "Sujeto + am/is/are + going to + verbo",
            "negative": "Sujeto + am/is/are + not + going to + verbo",
            "question": "Am/Is/Are + sujeto + going to + verbo?",
            "examples": ["I am going to travel to Spain next year.", "She is going to start a new job.", "They are not going to buy a house.", "Are you going to study tonight?"],
            "exercises": [
                {"sentence": "I ____ (travel) to London next summer.", "answer": "am going to travel", "hint": "Plan futuro con going to"},
                {"sentence": "She ____ (start) a new course next month.", "answer": "is going to start", "hint": "Intención futura con she"},
                {"sentence": "They ____ (not/buy) a new car this year.", "answer": "are not going to buy", "hint": "Negativo con going to"},
                {"sentence": "____ you ____ (study) for the exam?", "answer": "Are going to study", "hint": "Pregunta con going to"},
            ]
        },
        {
            "id": "present_perfect",
            "title": "Present Perfect",
            "description": "Conecta el pasado con el presente. Se usa para experiencias, cambios y acciones que continúan.",
            "formula": "Sujeto + have/has + participio pasado",
            "negative": "Sujeto + haven't/hasn't + participio pasado",
            "question": "Have/Has + sujeto + participio pasado?",
            "examples": ["I have visited Paris three times.", "She has never tried sushi.", "They haven't finished yet.", "Have you ever seen that movie?"],
            "exercises": [
                {"sentence": "I ____ (visit) Paris three times.", "answer": "have visited", "hint": "Experiencia con have + participio"},
                {"sentence": "She ____ (never/try) sushi before.", "answer": "has never tried", "hint": "Negativo con has + never"},
                {"sentence": "They ____ (not/finish) the project yet.", "answer": "haven't finished", "hint": "Negativo con haven't"},
                {"sentence": "____ you ever ____ (see) that film?", "answer": "Have seen", "hint": "Pregunta de experiencia"},
            ]
        },
        {
            "id": "comparatives",
            "title": "Comparativos y Superlativos",
            "description": "Se usan para comparar personas, cosas o lugares.",
            "formula": "Comparativo: adj+er / more + adj + than | Superlativo: the adj+est / the most + adj",
            "examples": ["My house is bigger than yours.", "She is the tallest girl in class.", "This book is more interesting than that one.", "He is the most intelligent student."],
            "exercises": [
                {"sentence": "My house is ____ (big) than yours.", "answer": "bigger", "hint": "Adjetivo corto: big → bigger"},
                {"sentence": "She is the ____ (tall) girl in the class.", "answer": "tallest", "hint": "Superlativo de tall"},
                {"sentence": "This book is ____ (interesting) than that one.", "answer": "more interesting", "hint": "Adjetivo largo: more + adjetivo"},
                {"sentence": "He is the ____ (intelligent) student in the school.", "answer": "most intelligent", "hint": "Superlativo de adjetivo largo"},
            ]
        },
        {
            "id": "conditionals",
            "title": "First Conditional",
            "description": "Se usa para situaciones reales o probables en el futuro.",
            "formula": "If + sujeto + present simple, sujeto + will + verbo",
            "examples": ["If it rains, I will stay home.", "If you study, you will pass the exam.", "She will be happy if she gets the job.", "If they invite me, I will go."],
            "exercises": [
                {"sentence": "If it ____ (rain), I will stay home.", "answer": "rains", "hint": "After 'if' usamos present simple"},
                {"sentence": "If you study, you ____ (pass) the exam.", "answer": "will pass", "hint": "Resultado con will"},
                {"sentence": "She ____ (be) happy if she gets the job.", "answer": "will be", "hint": "Resultado futuro con will be"},
                {"sentence": "If they invite me, I ____ (go) to the party.", "answer": "will go", "hint": "Respuesta futura con will"},
            ]
        },
    ]

    # -----------------------------
    # REGLAS GRAMATICALES (DE)
    # -----------------------------
    GRAMMAR_RULES_DE = [
        {
            "id": "de_articles",
            "title": "Artículos (der/die/das)",
            "description": "En alemán, los sustantivos tienen género gramatical: masculino (der), femenino (die), neutro (das). No hay reglas fijas, hay que aprender el artículo con cada sustantivo.",
            "formula": "der → masculino (der Mann) | die → femenino (die Frau) | das → neutro (das Kind)",
            "examples": ["der Tisch (mesa, masc.)", "die Lampe (lámpara, fem.)", "das Buch (libro, neutro)", "der Hund, die Katze, das Haus"],
            "exercises": [
                {"sentence": "____ Hund ist sehr brav.", "answer": "Der", "hint": "Hund es masculino"},
                {"sentence": "____ Katze schläft auf dem Sofa.", "answer": "Die", "hint": "Katze es femenino"},
                {"sentence": "____ Kind spielt im Garten.", "answer": "Das", "hint": "Kind es neutro"},
                {"sentence": "____ Tisch ist aus Holz.", "answer": "Der", "hint": "Tisch es masculino"},
                {"sentence": "____ Sonne scheint heute.", "answer": "Die", "hint": "Sonne es femenino"},
                {"sentence": "____ Wasser ist kalt.", "answer": "Das", "hint": "Wasser es neutro"},
            ]
        },
        {
            "id": "de_present",
            "title": "Presente (Präsens)",
            "description": "Se usa para acciones presentes, habituales y hechos generales. Los verbos regulares siguen un patrón fijo de conjugación.",
            "formula": "ich -e / du -st / er/sie/es -t / wir -en / ihr -t / sie/Sie -en",
            "examples": ["Ich lerne Deutsch. (Yo aprendo alemán)", "Du spielst Fußball. (Juegas fútbol)", "Er wohnt in Berlin. (Él vive en Berlín)", "Wir arbeiten heute. (Nosotros trabajamos hoy)"],
            "exercises": [
                {"sentence": "Ich ____ (lernen) Deutsch.", "answer": "lerne", "hint": "ich → -e"},
                {"sentence": "Du ____ (spielen) Fußball.", "answer": "spielst", "hint": "du → -st"},
                {"sentence": "Er ____ (wohnen) in Berlin.", "answer": "wohnt", "hint": "er/sie/es → -t"},
                {"sentence": "Wir ____ (arbeiten) heute.", "answer": "arbeiten", "hint": "wir → -en"},
                {"sentence": "Ihr ____ (kommen) aus Deutschland.", "answer": "kommt", "hint": "ihr → -t"},
                {"sentence": "Sie ____ (trinken) Kaffee.", "answer": "trinken", "hint": "sie/Sie → -en"},
            ]
        },
        {
            "id": "de_perfekt",
            "title": "Pasado (Perfekt)",
            "description": "Se usa para hablar del pasado, especialmente en conversación. Se forma con haben/sein + participio pasado (ge- + raíz + -t/-en).",
            "formula": "haben/sein (conjugado) + Partizip II (ge-...-t / ge-...-en)",
            "examples": ["Ich habe gelernt. (He aprendido)", "Er ist gegangen. (Él se ha ido)", "Wir haben gegessen. (Hemos comido)", "Sie ist gefahren. (Ella ha conducido)"],
            "exercises": [
                {"sentence": "Ich ____ gelernt. (haben)", "answer": "habe", "hint": "haber + lernen → gelernt"},
                {"sentence": "Er ____ nach Berlin gefahren. (sein)", "answer": "ist", "hint": "fahren usa sein"},
                {"sentence": "Wir ____ Pizza gegessen.", "answer": "haben", "hint": "haben + essen → gegessen"},
                {"sentence": "Sie ____ schon angekommen.", "answer": "ist", "hint": "ankommen usa sein"},
                {"sentence": "Ich ____ meine Hausaufgaben gemacht.", "answer": "habe", "hint": "haben + machen → gemacht"},
            ]
        },
        {
            "id": "de_separable",
            "title": "Verbos Separables",
            "description": "Muchos verbos alemanes tienen un prefijo separable (an-, auf-, ein-, aus-, mit-, etc.). En presente, el prefijo va al final de la oración.",
            "formula": "Prefijo separable + verbo conjugado ... prefijo",
            "examples": ["Ich stehe um 7 Uhr auf. (Me levanto)", "Er ruft mich an. (Él me llama)", "Wir kaufen im Supermarkt ein. (Compramos)", "Sie kommt um 8 Uhr an. (Ella llega)"],
            "exercises": [
                {"sentence": "Ich ____ um 7 Uhr ____. (aufstehen)", "answer": "stehe auf", "hint": "aufstehen → ich stehe ... auf"},
                {"sentence": "Er ____ mich ____. (anrufen)", "answer": "ruft an", "hint": "anrufen → er ruft ... an"},
                {"sentence": "Wir ____ im Supermarkt ____. (einkaufen)", "answer": "kaufen ein", "hint": "einkaufen → wir kaufen ... ein"},
                {"sentence": "Der Zug ____ um 8 Uhr ____. (ankommen)", "answer": "kommt an", "hint": "ankommen → er kommt ... an"},
            ]
        },
        {
            "id": "de_modal",
            "title": "Verbos Modales",
            "description": "Los verbos modales (können, müssen, dürfen, wollen, sollen) cambian la vocal en singular y van seguidos de otro verbo en infinitivo al final.",
            "formula": "Modal conjugado + ... + infinitivo",
            "examples": ["Ich kann Deutsch sprechen. (Puedo hablar)", "Du musst jetzt gehen. (Debes irte)", "Er will Arzt werden. (Quiere ser médico)", "Wir dürfen hier nicht rauchen. (No podemos fumar aquí)"],
            "exercises": [
                {"sentence": "Ich ____ Deutsch sprechen. (können)", "answer": "kann", "hint": "können → ich kann"},
                {"sentence": "Du ____ jetzt gehen. (müssen)", "answer": "musst", "hint": "müssen → du musst"},
                {"sentence": "Er ____ Arzt werden. (wollen)", "answer": "will", "hint": "wollen → er will"},
                {"sentence": "Wir ____ hier parken. (dürfen)", "answer": "dürfen", "hint": "dürfen → wir dürfen"},
                {"sentence": "Ihr ____ das Fenster öffnen. (sollen)", "answer": "sollt", "hint": "sollen → ihr sollt"},
            ]
        },
        {
            "id": "de_cases",
            "title": "Casos (Nominativ, Akkusativ, Dativ)",
            "description": "El alemán tiene cuatro casos. El Nominativ es el sujeto, el Akkusativ el objeto directo, y el Dativ el objeto indirecto.",
            "formula": "Nom: der/die/das | Akk: den/die/das | Dat: dem/der/dem",
            "examples": ["Der Mann sieht den Hund. (Nom → Akk)", "Ich gebe dem Kind das Buch. (Dat → Akk)", "Die Frau hilft der Frau. (Nom → Dat)", "Sie kauft den Tisch. (Akk)"],
            "exercises": [
                {"sentence": "____ Mann sieht ____ Hund. (der, der)", "answer": "Der den", "hint": "Sujeto Nom → Objeto Akk"},
                {"sentence": "Ich gebe ____ Kind ____ Buch. (das, das)", "answer": "dem das", "hint": "Objeto indirecto Dat → Objeto directo Akk"},
                {"sentence": "Sie hilft ____ Frau. (die)", "answer": "der", "hint": "helfen requiere Dativ"},
            ]
        },
        {
            "id": "de_word_order",
            "title": "Orden de Palabras",
            "description": "En oraciones principales, el verbo conjugado va en segunda posición. En subordinadas con 'weil' o 'dass', el verbo va al final.",
            "formula": "Principal: Sujeto + Verbo + ... | Subordinada: ... + weil/dass + Sujeto + ... + Verbo",
            "examples": ["Ich lerne Deutsch, weil ich in Berlin wohne.", "Er sagt, dass er morgen kommt.", "Heute gehe ich ins Kino. (Verbo en 2ª posición)", "Weil es regnet, bleibe ich zu Hause."],
            "exercises": [
                {"sentence": "Heute ____ ich ins Kino. (gehen)", "answer": "gehe", "hint": "Verbo en 2ª posición tras adverbio"},
                {"sentence": "Ich lerne Deutsch, weil ich in Berlin ____. (wohnen)", "answer": "wohne", "hint": "Verbo al final con weil"},
                {"sentence": "Er sagt, dass er morgen ____. (kommen)", "answer": "kommt", "hint": "Verbo al final con dass"},
            ]
        },
        {
            "id": "de_possessive",
            "title": "Artículos Posesivos",
            "description": "Indican pertenencia: mein (mi), dein (tu), sein (su de él), ihr (su de ella), unser (nuestro), euer (vuestro), ihr (su de ellos), Ihr (su de Ud.).",
            "formula": "mein/dein/sein/ihr/unser/euer/Ihr + sustantivo",
            "examples": ["Mein Bruder heißt Max.", "Deine Schwester ist nett.", "Sein Auto ist neu.", "Ihre Wohnung ist groß.", "Unser Haus ist alt."],
            "exercises": [
                {"sentence": "____ Bruder heißt Max. (mi)", "answer": "Mein", "hint": "Mein = mi (masculino)"},
                {"sentence": "____ Schwester ist nett. (tu)", "answer": "Deine", "hint": "Deine = tu (femenino)"},
                {"sentence": "____ Auto ist neu. (su de él)", "answer": "Sein", "hint": "Sein = su (neutro)"},
                {"sentence": "____ Haus ist alt. (nuestro)", "answer": "Unser", "hint": "Unser = nuestro (neutro)"},
            ]
        },
    ]

    GRAMMAR_RULES_FR = [
        {
            "id": "fr_articles",
            "title": "Articles definis (le/la/les)",
            "description": "En francais, les noms ont un genre: masculin (le) ou feminin (la). Le pluriel est (les) pour les deux genres.",
            "formula": "le + nom masculin (le chat) | la + nom feminin (la table) | les + nom pluriel (les chats / les tables)",
            "examples": ["le chien est dans le jardin", "la maison est grande", "les enfants jouent dehors", "le livre est sur la table"],
            "exercises": [
                {"sentence": "____ chat est noir.", "answer": "Le", "hint": "chat est masculin"},
                {"sentence": "____ maison est grande.", "answer": "La", "hint": "maison est feminin"},
                {"sentence": "____ enfants jouent dans le parc.", "answer": "Les", "hint": "enfants est pluriel"},
                {"sentence": "____ table est en bois.", "answer": "La", "hint": "table est feminin"},
                {"sentence": "____ soleil brille aujourd'hui.", "answer": "Le", "hint": "soleil est masculin"},
            ]
        },
        {
            "id": "fr_er_verbs",
            "title": "Present des verbes en -er",
            "description": "Les verbes reguliers du premier groupe (-er) suivent un modele de conjugaison fixe au present.",
            "formula": "je -e / tu -es / il/elle -e / nous -ons / vous -ez / ils/elles -ent",
            "examples": ["Je parle francais.", "Tu parles anglais.", "Il parle italien.", "Nous parlons ensemble.", "Vous parlez trop.", "Ils parlent vite."],
            "exercises": [
                {"sentence": "Je ____ (parler) francais.", "answer": "parle", "hint": "je \u2192 -e"},
                {"sentence": "Tu ____ (parler) anglais.", "answer": "parles", "hint": "tu \u2192 -es"},
                {"sentence": "Il ____ (manger) une pomme.", "answer": "mange", "hint": "il/elle \u2192 -e"},
                {"sentence": "Nous ____ (chanter) une chanson.", "answer": "chantons", "hint": "nous \u2192 -ons"},
                {"sentence": "Vous ____ (danser) bien.", "answer": "dansez", "hint": "vous \u2192 -ez"},
                {"sentence": "Ils ____ (jouer) au football.", "answer": "jouent", "hint": "ils/elles \u2192 -ent"},
            ]
        },
        {
            "id": "fr_etre_avoir",
            "title": "Verbes etre et avoir au present",
            "description": "Etre et avoir sont les verbes les plus importants et les plus irreguliers du francais. Ils servent aussi d'auxiliaires pour les temps composes.",
            "formula": "Etre: je suis, tu es, il/elle est, nous sommes, vous etes, ils/elles sont | Avoir: j'ai, tu as, il/elle a, nous avons, vous avez, ils/elles ont",
            "examples": ["Je suis etudiant.", "Tu es fatigue.", "Elle est heureuse.", "J'ai un chat.", "Tu as raison.", "Ils ont une voiture."],
            "exercises": [
                {"sentence": "Je ____ etudiant.", "answer": "suis", "hint": "etre \u2192 je suis"},
                {"sentence": "Tu ____ tres gentil.", "answer": "es", "hint": "etre \u2192 tu es"},
                {"sentence": "Elle ____ professeur.", "answer": "est", "hint": "etre \u2192 elle est"},
                {"sentence": "Nous ____ dans la cuisine.", "answer": "sommes", "hint": "etre \u2192 nous sommes"},
                {"sentence": "J'____ un frere et une soeur.", "answer": "ai", "hint": "avoir \u2192 j'ai"},
                {"sentence": "Ils ____ une grande maison.", "answer": "ont", "hint": "avoir \u2192 ils ont"},
            ]
        },
        {
            "id": "fr_passe_compose",
            "title": "Passe compose",
            "description": "Le passe compose exprime une action passee et terminee. Il se forme avec l'auxiliaire avoir ou etre au present + le participe passe du verbe.",
            "formula": "avoir/etre (present) + participe passe (participe en -e, -i, -u, etc.)",
            "examples": ["J'ai mange une pomme.", "Elle est allee a Paris.", "Nous avons fini le travail.", "Ils sont partis hier.", "Tu as vu le film?"],
            "exercises": [
                {"sentence": "J'____ (manger) une pomme.", "answer": "ai mange", "hint": "avoir + participe passe"},
                {"sentence": "Elle ____ (aller) a Paris.", "answer": "est allee", "hint": "aller utilise etre"},
                {"sentence": "Nous ____ (finir) le travail.", "answer": "avons fini", "hint": "avoir + finir \u2192 fini"},
                {"sentence": "Ils ____ (partir) hier soir.", "answer": "sont partis", "hint": "partir utilise etre"},
                {"sentence": "Tu ____ (voir) ce film?", "answer": "as vu", "hint": "avoir + voir \u2192 vu"},
            ]
        },
        {
            "id": "fr_possessifs",
            "title": "Adjectifs possessifs (mon/ma/mes, ton/ta/tes, etc.)",
            "description": "Les adjectifs possessifs indiquent la possession. Ils s'accordent avec le nom possede, pas avec le possesseur.",
            "formula": "mon/ma/mes (mon livre, ma table, mes amis) | ton/ta/tes | son/sa/ses | notre/nos | votre/vos | leur/leurs",
            "examples": ["Mon frere s'appelle Pierre.", "Ma soeur est gentille.", "Tes amis sont sympas.", "Notre maison est grande.", "Leur chien est mignon."],
            "exercises": [
                {"sentence": "____ frere s'appelle Pierre. (mon)", "answer": "Mon", "hint": "frere est masculin"},
                {"sentence": "____ soeur est gentille. (ma)", "answer": "Ma", "hint": "soeur est feminin"},
                {"sentence": "____ amis sont sympas. (tes)", "answer": "Tes", "hint": "amis est pluriel"},
                {"sentence": "____ maison est grande. (notre)", "answer": "Notre", "hint": "maison est feminin singulier"},
                {"sentence": "____ chien est mignon. (leur)", "answer": "Leur", "hint": "leur + singulier"},
            ]
        },
        {
            "id": "fr_adjectifs",
            "title": "Accord des adjectifs",
            "description": "En francais, les adjectifs s'accordent en genre (masculin/feminin) et en nombre (singulier/pluriel) avec le nom qu'ils qualifient.",
            "formula": "Masculin \u2192 base (petit) | Feminin \u2192 base + e (petite) | Pluriel \u2192 base + s (petits / petites)",
            "examples": ["Un petit chat (masc.sg.)", "Une petite chatte (fem.sg.)", "Des petits chats (masc.pl.)", "Des petites chattes (fem.pl.)"],
            "exercises": [
                {"sentence": "Un ____ chat. (petit)", "answer": "petit", "hint": "chat est masculin singulier"},
                {"sentence": "Une ____ chatte. (petit)", "answer": "petite", "hint": "chatte est feminin singulier \u2192 ajoute -e"},
                {"sentence": "Des ____ chats. (petit)", "answer": "petits", "hint": "pluriel \u2192 ajoute -s"},
                {"sentence": "Une voiture ____ (rouge)", "answer": "rouge", "hint": "rouge ne change pas au feminin"},
                {"sentence": "Des fleurs ____ (joli)", "answer": "jolies", "hint": "feminin pluriel \u2192 -es"},
            ]
        },
        {
            "id": "fr_negation",
            "title": "Negation (ne...pas)",
            "description": "Pour former la negation en francais, on encadre le verbe conjugue avec 'ne' devant et 'pas' derriere.",
            "formula": "Sujet + ne + verbe + pas + complement",
            "examples": ["Je ne parle pas anglais.", "Il n'aime pas le cafe.", "Nous ne travaillons pas le dimanche.", "Elles ne sont pas la."],
            "exercises": [
                {"sentence": "Je ____ parle ____ anglais.", "answer": "ne pas", "hint": "ne ... pas encadre le verbe"},
                {"sentence": "Il ____ aime ____ le cafe.", "answer": "n' pas", "hint": "ne devient n' devant une voyelle"},
                {"sentence": "Nous ____ travaillons ____ le dimanche.", "answer": "ne pas", "hint": "ne ... pas autour du verbe"},
                {"sentence": "Elles ____ sont ____ venues.", "answer": "ne pas", "hint": "ne ... pas avec etre"},
            ]
        },
        {
            "id": "fr_futur_proche",
            "title": "Futur proche (aller + infinitif)",
            "description": "Le futur proche exprime une action qui va se produire dans un avenir immediat. Il se forme avec le verbe 'aller' conjugue + l'infinitif.",
            "formula": "aller (present) + infinitif",
            "examples": ["Je vais manger.", "Tu vas voyager.", "Il va arriver bientot.", "Nous allons etudier.", "Ils vont venir."],
            "exercises": [
                {"sentence": "Je ____ (aller) manger.", "answer": "vais", "hint": "aller \u2192 je vais + infinitif"},
                {"sentence": "Tu ____ (aller) voyager.", "answer": "vas", "hint": "aller \u2192 tu vas + infinitif"},
                {"sentence": "Il ____ (aller) arriver bientot.", "answer": "va", "hint": "aller \u2192 il va + infinitif"},
                {"sentence": "Nous ____ (aller) etudier.", "answer": "allons", "hint": "aller \u2192 nous allons + infinitif"},
                {"sentence": "Ils ____ (aller) venir demain.", "answer": "vont", "hint": "aller \u2192 ils vont + infinitif"},
            ]
        },
        {
            "id": "fr_comparatifs",
            "title": "Comparatifs (plus...que, moins...que, aussi...que)",
            "description": "Les comparatifs permettent de comparer des personnes, des choses ou des actions. On utilise 'plus...que' (superiorite), 'moins...que' (inferiorite), 'aussi...que' (egalite).",
            "formula": "plus + adjectif + que (superiorite) | moins + adjectif + que (inferiorite) | aussi + adjectif + que (egalite)",
            "examples": ["Marie est plus grande que Luc.", "Ce livre est moins interessant que l'autre.", "Il est aussi fort que son frere.", "Elle court plus vite que moi."],
            "exercises": [
                {"sentence": "Marie est ____ grande ____ Luc.", "answer": "plus que", "hint": "superiorite: plus...que"},
                {"sentence": "Ce livre est ____ interessant ____ l'autre.", "answer": "moins que", "hint": "inferiorite: moins...que"},
                {"sentence": "Il est ____ fort ____ son frere.", "answer": "aussi que", "hint": "egalite: aussi...que"},
                {"sentence": "Elle court ____ vite ____ moi.", "answer": "plus que", "hint": "adverbe + plus...que"},
            ]
        },
        {
            "id": "fr_pronoms_toniques",
            "title": "Pronoms toniques (moi, toi, lui, elle, nous, vous, eux, elles)",
            "description": "Les pronoms toniques (ou pronoms disjoints) s'utilisent apres une preposition, pour insister, ou dans des reponses sans verbe.",
            "formula": "moi (je) | toi (tu) | lui (il) | elle (elle) | nous (nous) | vous (vous) | eux (ils) | elles (elles)",
            "examples": ["Moi, je parle francais.", "Viens avec moi.", "Ce livre est pour toi.", "Elle est plus grande que lui.", "Eux, ils sont partis."],
            "exercises": [
                {"sentence": "____, je parle francais. (insistance sur je)", "answer": "Moi", "hint": "pronom tonique pour je"},
                {"sentence": "Viens avec ____.", "answer": "moi", "hint": "apres la preposition avec"},
                {"sentence": "Ce cadeau est pour ____. (tu)", "answer": "toi", "hint": "apres la preposition pour"},
                {"sentence": "Elle est plus grande que ____. (il)", "answer": "lui", "hint": "apres que dans une comparaison"},
                {"sentence": "____, ils sont deja arrives. (ils)", "answer": "Eux", "hint": "pronom tonique pour ils"},
            ]
        },
    ]

    def _is_de(self):
        return self.language and self.language.lower() in ("german", "deutsche", "deutsch", "de")

    def _is_fr(self):
        return self.language and self.language.lower() in ("french", "fran\u00e7ais", "francais", "fr")

    def get_grammar_rules(self):
        if self._is_de():
            return list(self.GRAMMAR_RULES_DE)
        if self._is_fr():
            return list(self.GRAMMAR_RULES_FR)
        return list(self.GRAMMAR_RULES)

    def _pick_word(self, vocab_words, tag=None, exclude=None, valid_answers=None):
        if valid_answers:
            candidates = [w["word"] for w in vocab_words if tag in w["tags"] and w["word"] in valid_answers]
            if not candidates:
                candidates = [a for a in valid_answers if a not in (exclude or [])]
            if not candidates:
                candidates = [w["word"] for w in vocab_words if tag in w["tags"]]
        elif tag:
            candidates = [w["word"] for w in vocab_words if tag in w["tags"]]
        else:
            candidates = [w["word"] for w in vocab_words]
        if exclude:
            candidates = [w for w in candidates if w not in exclude]
        return candidates[0] if candidates else ""

    def _pick_words_for_tag(self, vocab_words, tag, count=3, exclude=None):
        candidates = [w for w in vocab_words if tag in w.get("tags", [])]
        if exclude:
            candidates = [w for w in candidates if w["word"] != exclude]
        return [w["word"] for w in candidates[:count]]

    def analyze_description(self, description: str):
        detected_tags = []
        desc_lower = description.lower()
        if self._is_de():
            keywords_dict = self.GERMAN_TAG_KEYWORDS
        elif self._is_fr():
            keywords_dict = self.FRENCH_TAG_KEYWORDS
        else:
            keywords_dict = self.TAG_KEYWORDS
        for tag, keywords in keywords_dict.items():
            if any(word in desc_lower for word in keywords):
                detected_tags.append(tag)
        return detected_tags

    def generate_exercises(self, tags: list):
        vocab_words = self.get_mission_vocabulary() if self.current_mission else []
        exercises = []
        used_answers = set()
        max_per_tag = 3

        if self._is_de():
            templates_by_tag = self.EXERCISE_TEMPLATES_BY_TAG_DE
        elif self._is_fr():
            templates_by_tag = self.EXERCISE_TEMPLATES_BY_TAG_FR
        else:
            templates_by_tag = self.EXERCISE_TEMPLATES_BY_TAG

        for tag in tags:
            templates = templates_by_tag.get(tag, [])
            tag_count = 0
            for tmpl in templates:
                if tag_count >= max_per_tag:
                    break
                word = self._pick_word(vocab_words, tag, exclude=used_answers, valid_answers=tmpl.get("valid_answers"))
                if not word:
                    continue
                used_answers.add(word)
                tag_count += 1
                alt_words = self._pick_words_for_tag(vocab_words, tag, count=3, exclude=word)
                if not alt_words and tmpl.get("valid_answers"):
                    alt_words = [a for a in tmpl["valid_answers"] if a != word][:3]
                exercises.append({
                    "id": f"ex_{len(exercises) + 1}",
                    "type": "fill_blank",
                    "sentence": tmpl["sentence"],
                    "answer": word,
                    "hint": tmpl["hint"],
                    "sentence_with_answer": tmpl["sentence"].replace("____", word),
                    "alternatives": alt_words,
                })

        if not exercises:
            exercises.append({
                "id": "ex_fallback",
                "type": "fill_blank",
                "sentence": "I want to ____ English.",
                "answer": "learn",
                "hint": "Acción que haces en una escuela",
                "sentence_with_answer": "I want to learn English.",
                "alternatives": ["study", "practice", "speak"],
            })

        return exercises

    def create_open_mission(self, description: str, mission_id: str):
        tags = self.analyze_description(description)

        new_mission = {
            "id": mission_id,
            "name": description,
            "goal": description,
            "vocabulary_tags": tags,
            "exercises": self.generate_exercises(tags)
        }

        self.missions.append(new_mission)
        self.current_mission = new_mission
        return new_mission

    def get_mission_content(self, mission_id: str):
        self.select_mission(mission_id)
        tags = self.current_mission.get("vocabulary_tags", [])
        name = self.current_mission.get("name", "")
        exercises = self.current_mission.get("exercises") or self.generate_exercises(tags)
        return {
            "mission": self.current_mission,
            "vocabulary": self.get_mission_vocabulary(),
            "exercises": exercises,
        }

    # -----------------------------
    # FLASHCARDS
    # -----------------------------
    def generate_flashcards(self):
        if not self.current_mission:
            raise ValueError("No hay misión seleccionada para generar flashcards.")

        vocab = self.get_mission_vocabulary()
        flashcards = []

        for item in vocab:
            word = item["word"]
            forms = item.get("forms", [])
            tags = item.get("tags", [])

            back = {
                "definition": f"Definition of '{word}' (placeholder)",
                "example": f"Example sentence using '{word}' (placeholder)",
                "translation": f"Traducción de '{word}' (placeholder)"
            }
            if forms:
                back["forms"] = ", ".join(forms)
            if tags:
                back["tags"] = ", ".join(tags)

            flashcards.append({"front": word, "back": back})

        return flashcards
