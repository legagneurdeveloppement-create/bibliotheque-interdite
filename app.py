"""
Le Secret de la Bibliothèque Interdite
Application web Flask — jeu d'évasion immersif

Lancement :
    pip install -r requirements.txt
    python app.py

Puis ouvrez http://localhost:5000 dans votre navigateur.
"""

import os
import time
import random
from datetime import datetime
from flask import (
    Flask, render_template, request, redirect, url_for,
    session, jsonify, flash
)

from game_data import (
    PARIS_MAPS, ACT1_CORRECT_ORDER, CYRILLIC_MESSAGE,
    LANGUAGE_FRAGMENTS, FOUNDERS_INITIALS, REBUS_EXPLANATION,
    ACT2_COMBINATION,
    CAESAR_CIPHER, POLYBIUS_SQUARE,
    TRUTH_ITEMS, ACT5_CORRECT_ORDER, HIDDEN_SPOTS,
    HINTS, GAME_CONFIG, NARRATION,
    get_hints_for_act, get_map_by_id, get_fragment_by_id,
    get_item_by_id, get_spot_by_id,
)

import os as _os
_tdir = _os.path.join(_os.path.dirname(_os.path.abspath(__file__)), 'templates')
_sdir = _os.path.join(_os.path.dirname(_os.path.abspath(__file__)), 'static')
app = Flask(__name__, template_folder=_tdir, static_folder=_sdir, static_url_path='/static')

from flask import send_from_directory as _sfd
@app.route('/static/<path:filename>')
def _serve_static(filename):
    return _sfd(_sdir, filename)
app.secret_key = os.environ.get(
    "SECRET_KEY",
    "bibliotheque-aube-perdue-secret-key-change-me-in-production",
)


# ──────────────────────────────────────────────────────────
# GESTION DE L'ÉTAT DE JEU (session)
# ──────────────────────────────────────────────────────────
def init_game_state():
    """Initialise l'état de jeu en session."""
    # Mélange initial des cartes pour l'acte 1
    shuffled = [m.id for m in PARIS_MAPS]
    random.shuffle(shuffled)

    session["game"] = {
        "current_act": "intro",
        "started": False,
        "start_time": None,       # timestamp Unix
        "time_remaining": GAME_CONFIG["total_time_seconds"],

        # Acte I
        "act1_order": shuffled,
        "act1_solved": False,
        "act1_cyrillic_revealed": False,

        # Acte II
        "act2_translated": [],
        "act2_combination": "",
        "act2_solved": False,
        "act2_rebus_revealed": False,

        # Acte III — Chiffre de César
        "act3_caesar_shift": 0,         # décalage choisi par le joueur (0-25)
        "act3_solved": False,
        "act3_message_revealed": False,

        # Acte IV — Carré de Polybe
        "act4_polybius_word": "",        # mot saisi par le joueur
        "act4_solved": False,
        "act4_revealed": False,

        # Acte V — Piédestal (anciennement Acte III)
        "act5_found_items": [],
        "act5_arrangement": [],
        "act5_solved": False,
        "act5_current_spot": None,

        # Stats
        "hints_used_by_act": {"act1": 0, "act2": 0, "act3": 0, "act4": 0, "act5": 0},
        "mistakes_count": 0,
    }
    session.modified = True


def get_state():
    """Récupère l'état de jeu, l'initialise si nécessaire."""
    if "game" not in session:
        init_game_state()
    return session["game"]


def update_state(**kwargs):
    """Met à jour l'état de jeu."""
    state = get_state()
    state.update(kwargs)
    session.modified = True


def reset_game():
    """Réinitialise complètement la partie."""
    init_game_state()


def get_elapsed_time():
    """Retourne le temps écoulé en secondes depuis le début."""
    state = get_state()
    if not state.get("start_time"):
        return 0
    return int(time.time() - state["start_time"])


def get_time_remaining():
    """Retourne le temps restant en secondes."""
    state = get_state()
    if not state.get("started"):
        return GAME_CONFIG["total_time_seconds"]
    elapsed = get_elapsed_time()
    remaining = GAME_CONFIG["total_time_seconds"] - elapsed
    return max(0, remaining)


def is_time_up():
    """Vérifie si le temps est écoulé."""
    return get_time_remaining() <= 0


# ──────────────────────────────────────────────────────────
# ROUTES
# ──────────────────────────────────────────────────────────

@app.route("/")
def index():
    """Page d'accueil / écran d'introduction."""
    state = get_state()

    # Vérifie si le temps est écoulé
    if state.get("started") and is_time_up():
        update_state(current_act="defeat")
        return redirect(url_for("defeat"))

    if state.get("started"):
        if state["current_act"] == "victory":
            return redirect(url_for("victory"))
        if state["current_act"] == "defeat":
            return redirect(url_for("defeat"))
        return redirect(url_for("act", act_id=state["current_act"]))

    return render_template("intro.html", narration=NARRATION["intro"])


@app.route("/start")
def start_game():
    """Démarre une nouvelle partie."""
    reset_game()
    update_state(
        started=True,
        current_act="act1",
        start_time=time.time(),
    )
    return redirect(url_for("act", act_id="act1"))


@app.route("/reset")
def reset():
    """Réinitialise la partie et retourne à l'intro."""
    reset_game()
    return redirect(url_for("index"))


@app.route("/act/<act_id>")
def act(act_id):
    """Affiche l'acte donné."""
    state = get_state()

    # Vérifie le temps
    if state.get("started") and is_time_up():
        update_state(current_act="defeat")
        return redirect(url_for("defeat"))

    # Vérifie que l'acte est accessible
    valid_acts = ["act1", "act2", "act3", "act4", "act5"]
    if act_id not in valid_acts:
        return redirect(url_for("index"))

    # Vérifie la progression (ne peut pas sauter un acte non résolu)
    if act_id == "act2" and not state.get("act1_solved"):
        flash("Vous devez d'abord résoudre l'Acte I.", "warning")
        return redirect(url_for("act", act_id="act1"))
    if act_id == "act3" and not state.get("act2_solved"):
        flash("Vous devez d'abord résoudre l'Acte II.", "warning")
        return redirect(url_for("act", act_id="act2"))
    if act_id == "act4" and not state.get("act3_solved"):
        flash("Vous devez d'abord résoudre l'Acte III.", "warning")
        return redirect(url_for("act", act_id="act3"))
    if act_id == "act5" and not state.get("act4_solved"):
        flash("Vous devez d'abord résoudre l'Acte IV.", "warning")
        return redirect(url_for("act", act_id="act4"))

    update_state(current_act=act_id)

    time_remaining = get_time_remaining()
    hints_used = state["hints_used_by_act"].get(act_id, 0)
    act_hints = get_hints_for_act(act_id)
    visible_hints = act_hints[:hints_used + 1] if hints_used > 0 else []

    context = {
        "state": state,
        "time_remaining": time_remaining,
        "time_remaining_str": format_time(time_remaining),
        "hints_used": hints_used,
        "visible_hints": visible_hints,
        "max_hints": GAME_CONFIG["max_hints_per_act"],
        "narration": NARRATION,
    }

    if act_id == "act1":
        context["maps"] = [get_map_by_id(mid) for mid in state["act1_order"]]
        context["cyrillic"] = CYRILLIC_MESSAGE
        return render_template("act1.html", **context)
    elif act_id == "act2":
        context["fragments"] = LANGUAGE_FRAGMENTS
        context["founders"] = FOUNDERS_INITIALS
        context["rebus_explanation"] = REBUS_EXPLANATION
        context["combination_length"] = len(state["act2_combination"])
        return render_template("act2.html", **context)
    elif act_id == "act3":
        # Acte III — Chiffre de César
        context["caesar"] = CAESAR_CIPHER
        context["current_shift"] = state.get("act3_caesar_shift", 0)
        context["decrypted"] = caesar_decrypt(
            CAESAR_CIPHER["encrypted_text"], context["current_shift"]
        )
        return render_template("act3.html", **context)
    elif act_id == "act4":
        # Acte IV — Carré de Polybe
        context["polybius"] = POLYBIUS_SQUARE
        context["user_word"] = state.get("act4_polybius_word", "")
        return render_template("act4.html", **context)
    elif act_id == "act5":
        # Acte V — Piédestal
        context["items"] = TRUTH_ITEMS
        context["spots"] = HIDDEN_SPOTS
        context["arrangement_items"] = [
            get_item_by_id(iid) for iid in state["act5_arrangement"]
        ]
        context["remaining_items"] = [
            i for i in TRUTH_ITEMS
            if i.id in state["act5_found_items"]
            and i.id not in state["act5_arrangement"]
        ]
        context["current_spot_item"] = None
        if state.get("act5_current_spot"):
            spot = get_spot_by_id(state["act5_current_spot"])
            context["current_spot_item"] = get_item_by_id(spot["item"])
            context["current_spot"] = spot
        return render_template("act5.html", **context)

    return redirect(url_for("index"))


def caesar_decrypt(text, shift):
    """Déchiffre un texte avec un décalage donné (César)."""
    result = []
    for char in text:
        if char.isalpha():
            base = ord("A") if char.isupper() else ord("a")
            # Pour décrypter : on recule de 'shift' positions
            decrypted = chr((ord(char) - base - shift) % 26 + base)
            result.append(decrypted)
        else:
            result.append(char)
    return "".join(result)


@app.route("/victory")
def victory():
    """Écran de victoire."""
    state = get_state()
    if not state.get("act5_solved"):
        return redirect(url_for("index"))

    time_remaining = get_time_remaining()
    elapsed = GAME_CONFIG["total_time_seconds"] - time_remaining
    hints_used = sum(state["hints_used_by_act"].values())

    # Score
    time_bonus = round((time_remaining / (75 * 60)) * 400)
    hint_penalty = hints_used * 30
    mistake_penalty = state["mistakes_count"] * 20
    score = max(0, 600 + time_bonus - hint_penalty - mistake_penalty)

    if score >= 900:
        rank = "Archiviste Légendaire"
    elif score >= 750:
        rank = "Gardien de l'Aube"
    elif score >= 600:
        rank = "Chercheur Éclairé"
    else:
        rank = "Apprenti Curieux"

    return render_template(
        "victory.html",
        narration=NARRATION["victory"],
        elapsed_str=format_time(elapsed),
        hints_used=hints_used,
        mistakes=state["mistakes_count"],
        score=score,
        rank=rank,
    )


@app.route("/defeat")
def defeat():
    """Écran de défaite."""
    state = get_state()
    hints_used = sum(state["hints_used_by_act"].values())
    return render_template(
        "defeat.html",
        narration=NARRATION["defeat"],
        hints_used=hints_used,
        mistakes=state["mistakes_count"],
    )


# ──────────────────────────────────────────────────────────
# ACTIONS DE JEU — ACTE I
# ──────────────────────────────────────────────────────────
@app.route("/act1/move", methods=["POST"])
def act1_move():
    """Déplace une carte vers le haut ou le bas."""
    state = get_state()
    if state.get("act1_solved"):
        return redirect(url_for("act", act_id="act1"))

    map_id = request.form.get("map_id")
    direction = request.form.get("direction")  # "up" ou "down"

    order = state["act1_order"]
    try:
        idx = order.index(map_id)
    except ValueError:
        return redirect(url_for("act", act_id="act1"))

    if direction == "up" and idx > 0:
        order[idx], order[idx - 1] = order[idx - 1], order[idx]
    elif direction == "down" and idx < len(order) - 1:
        order[idx], order[idx + 1] = order[idx + 1], order[idx]

    update_state(act1_order=order)
    return redirect(url_for("act", act_id="act1"))


@app.route("/act1/shuffle")
def act1_shuffle():
    """Mélange les cartes."""
    state = get_state()
    if state.get("act1_solved"):
        return redirect(url_for("act", act_id="act1"))
    shuffled = [m.id for m in PARIS_MAPS]
    random.shuffle(shuffled)
    update_state(act1_order=shuffled)
    return redirect(url_for("act", act_id="act1"))


@app.route("/act1/verify", methods=["POST"])
def act1_verify():
    """Vérifie l'alignement des cartes."""
    state = get_state()
    order = state["act1_order"]

    correct = (
        len(order) == len(ACT1_CORRECT_ORDER)
        and all(order[i] == ACT1_CORRECT_ORDER[i] for i in range(len(order)))
    )

    if correct:
        update_state(act1_solved=True, act1_cyrillic_revealed=True)
        flash("Le mécanisme résonne... Un compartiment secret s'ouvre dans le pupitre.", "success")
    else:
        mistakes = state["mistakes_count"] + 1
        update_state(mistakes_count=mistakes)
        flash("L'alignement est incorrect. Les cartes ne racontent pas encore la bonne histoire.", "error")

    return redirect(url_for("act", act_id="act1"))


# ──────────────────────────────────────────────────────────
# ACTIONS DE JEU — ACTE II
# ──────────────────────────────────────────────────────────
@app.route("/act2/translate/<frag_id>")
def act2_translate(frag_id):
    """Traduit un fragment."""
    state = get_state()
    if frag_id not in [f.id for f in LANGUAGE_FRAGMENTS]:
        return redirect(url_for("act", act_id="act2"))

    translated = state["act2_translated"]
    if frag_id not in translated:
        translated.append(frag_id)
        update_state(act2_translated=translated)

    return redirect(url_for("act", act_id="act2"))


@app.route("/act2/rebus")
def act2_rebus():
    """Déchiffre le rébus."""
    update_state(act2_rebus_revealed=True)
    return redirect(url_for("act", act_id="act2"))


@app.route("/act2/verify", methods=["POST"])
def act2_verify():
    """Vérifie la combinaison du cadenas."""
    state = get_state()

    # Lit les 4 chiffres individuels directement (sans dépendre du JS)
    combination = ""
    for i in range(4):
        combination += request.form.get(f"combo{i}", "").strip()[:1]

    # Fallback : si le champ caché "combination" existe et est rempli
    if not combination:
        combination = request.form.get("combination", "").strip()[:4]

    if combination == ACT2_COMBINATION:
        update_state(act2_solved=True, act2_combination=combination)
        flash("La boîte s'ouvre dans un déclic satisfaisant...", "success")
    else:
        mistakes = state["mistakes_count"] + 1
        state["mistakes_count"] = mistakes
        state["act2_combination"] = combination
        session.modified = True
        flash(f"Combinaison incorrecte : '{combination}'. Le mécanisme résiste.", "error")

    return redirect(url_for("act", act_id="act2"))


@app.route("/act2/combination", methods=["POST"])
def act2_set_combination():
    """Met à jour la combinaison saisie (sans vérifier)."""
    state = get_state()
    combination = request.form.get("combination", "").strip()[:4]
    state["act2_combination"] = combination
    session.modified = True
    return redirect(url_for("act", act_id="act2"))


# ──────────────────────────────────────────────────────────
# ACTIONS DE JEU — ACTE III (Chiffre de César)
# ──────────────────────────────────────────────────────────
@app.route("/act3/set_shift", methods=["POST"])
def act3_set_shift():
    """Met à jour le décalage choisi par le joueur."""
    state = get_state()
    if state.get("act3_solved"):
        return redirect(url_for("act", act_id="act3"))
    try:
        shift = int(request.form.get("shift", 0))
        shift = max(0, min(25, shift))
    except (TypeError, ValueError):
        shift = 0
    state["act3_caesar_shift"] = shift
    session.modified = True
    return redirect(url_for("act", act_id="act3") + "#caesar")


@app.route("/act3/verify", methods=["POST"])
def act3_verify():
    """Vérifie si le décalage choisi est correct."""
    state = get_state()
    shift = state.get("act3_caesar_shift", 0)

    if shift == CAESAR_CIPHER["shift"]:
        update_state(act3_solved=True, act3_message_revealed=True)
        flash("Le message se dévoile ! Le décalage était correct.", "success")
    else:
        mistakes = state["mistakes_count"] + 1
        state["mistakes_count"] = mistakes
        session.modified = True
        flash(f"Décalage {shift} : le message reste incompréhensible. Cherchez encore.", "error")

    return redirect(url_for("act", act_id="act3") + "#caesar")


# ──────────────────────────────────────────────────────────
# ACTIONS DE JEU — ACTE IV (Carré de Polybe)
# ──────────────────────────────────────────────────────────
@app.route("/act4/set_word", methods=["POST"])
def act4_set_word():
    """Met à jour le mot saisi par le joueur."""
    state = get_state()
    if state.get("act4_solved"):
        return redirect(url_for("act", act_id="act4"))
    word = request.form.get("polybius_word", "").strip().upper()[:10]
    state["act4_polybius_word"] = word
    session.modified = True
    return redirect(url_for("act", act_id="act4") + "#polybius")


@app.route("/act4/verify", methods=["POST"])
def act4_verify():
    """Vérifie le mot décodé."""
    state = get_state()

    # Lit le mot directement depuis le formulaire (sans dépendre de la session)
    word = request.form.get("polybius_word", "").strip().upper()[:10]
    # Ne garde que les lettres A-Z
    word = "".join(c for c in word if c.isalpha())

    # Sauvegarde aussi en session (pour l'affichage)
    state["act4_polybius_word"] = word
    session.modified = True

    if word == POLYBIUS_SQUARE["decoded_word"]:
        update_state(act4_solved=True, act4_revealed=True)
        flash("Le mot se dévoile : SOLEIL ! La voie des Lumières s'éclaire.", "success")
    else:
        mistakes = state["mistakes_count"] + 1
        state["mistakes_count"] = mistakes
        session.modified = True
        flash(f"« {word} » n'est pas le bon mot. Vérifiez les coordonnées.", "error")

    return redirect(url_for("act", act_id="act4") + "#polybius")


# ──────────────────────────────────────────────────────────
# ACTIONS DE JEU — ACTE V (Piédestal, anciennement Acte III)
# ──────────────────────────────────────────────────────────
@app.route("/act5/search/<spot_id>")
def act5_search(spot_id):
    """Fouille un emplacement."""
    state = get_state()
    try:
        spot = get_spot_by_id(spot_id)
    except ValueError:
        return redirect(url_for("act", act_id="act5"))

    update_state(act5_current_spot=spot_id)
    return redirect(url_for("act", act_id="act5"))


@app.route("/act5/take", methods=["POST"])
def act5_take():
    """Récupère l'objet trouvé."""
    state = get_state()
    spot_id = state.get("act5_current_spot")
    if not spot_id:
        return redirect(url_for("act", act_id="act5"))

    spot = get_spot_by_id(spot_id)
    item_id = spot["item"]

    # Crée une NOUVELLE liste (pas de mutation en place)
    found = list(state.get("act5_found_items", []))
    if item_id not in found:
        found.append(item_id)
        update_state(act5_found_items=found, act5_current_spot=None)
        item = get_item_by_id(item_id)
        flash(f"Objet récupéré ! {item.object} — lié à {item.name}.", "success")
    else:
        update_state(act5_current_spot=None)

    return redirect(url_for("act", act_id="act5"))


@app.route("/act5/close_search")
def act5_close_search():
    """Ferme la modal de fouille sans récupérer."""
    update_state(act5_current_spot=None)
    return redirect(url_for("act", act_id="act5"))


@app.route("/act5/place/<item_id>")
def act5_place(item_id):
    """Place un objet sur le piédestal."""
    state = get_state()
    # Crée une NOUVELLE liste (pas de mutation en place) pour que Flask détecte le changement
    arrangement = list(state.get("act5_arrangement", []))

    if item_id not in arrangement and len(arrangement) < 7:
        if item_id in state.get("act5_found_items", []):
            arrangement.append(item_id)
            update_state(act5_arrangement=arrangement)

    return redirect(url_for("act", act_id="act5") + "#pedestal")


@app.route("/act5/remove/<item_id>")
def act5_remove(item_id):
    """Retire un objet du piédestal."""
    state = get_state()
    arrangement = [i for i in state.get("act5_arrangement", []) if i != item_id]
    update_state(act5_arrangement=arrangement)
    return redirect(url_for("act", act_id="act5") + "#pedestal")


@app.route("/act5/clear_all")
def act5_clear_all():
    """Retire tous les objets du piédestal d'un coup."""
    update_state(act5_arrangement=[])
    return redirect(url_for("act", act_id="act5") + "#pedestal")


@app.route("/act5/move", methods=["POST"])
def act5_move():
    """Déplace un objet sur le piédestal (haut/bas)."""
    state = get_state()
    item_id = request.form.get("item_id")
    direction = request.form.get("direction")

    arrangement = list(state.get("act5_arrangement", []))
    try:
        idx = arrangement.index(item_id)
    except ValueError:
        return redirect(url_for("act", act_id="act5") + "#pedestal")

    if direction == "up" and idx > 0:
        arrangement[idx], arrangement[idx - 1] = arrangement[idx - 1], arrangement[idx]
    elif direction == "down" and idx < len(arrangement) - 1:
        arrangement[idx], arrangement[idx + 1] = arrangement[idx + 1], arrangement[idx]

    update_state(act5_arrangement=arrangement)
    return redirect(url_for("act", act_id="act5") + "#pedestal")


@app.route("/act5/verify", methods=["POST"])
def act5_verify():
    """Vérifie l'arrangement final sur le piédestal."""
    state = get_state()
    arrangement = state["act5_arrangement"]

    correct = (
        len(arrangement) == len(ACT5_CORRECT_ORDER)
        and all(arrangement[i] == ACT5_CORRECT_ORDER[i] for i in range(len(arrangement)))
    )

    if correct:
        update_state(act5_solved=True, current_act="victory")
        return redirect(url_for("victory"))
    else:
        mistakes = state["mistakes_count"] + 1
        state["mistakes_count"] = mistakes
        session.modified = True
        flash("L'arrangement est incorrect. Le piédestal reste inerte. Réétudiez l'ordre.", "error")
        return redirect(url_for("act", act_id="act5") + "#pedestal")


# ──────────────────────────────────────────────────────────
# INDICES
# ──────────────────────────────────────────────────────────
@app.route("/hint/<act_id>")
def reveal_hint(act_id):
    """Révèle l'indice suivant pour un acte."""
    state = get_state()
    act_hints = get_hints_for_act(act_id)
    current_count = state["hints_used_by_act"].get(act_id, 0)

    if current_count < len(act_hints):
        state["hints_used_by_act"][act_id] = current_count + 1
        session.modified = True
        flash("Le Maître du Jeu murmure... Un nouvel indice vous parvient.", "info")

    return redirect(url_for("act", act_id=act_id))


# ──────────────────────────────────────────────────────────
# API — TIMER (pour mise à jour temps réel côté client)
# ──────────────────────────────────────────────────────────
@app.route("/api/time")
def api_time():
    """Retourne le temps restant en JSON (pour le JS côté client)."""
    state = get_state()
    if not state.get("started"):
        return jsonify({"time_remaining": GAME_CONFIG["total_time_seconds"], "started": False})

    remaining = get_time_remaining()
    if remaining <= 0:
        return jsonify({"time_remaining": 0, "started": True, "defeat": True})

    return jsonify({
        "time_remaining": remaining,
        "started": True,
        "defeat": False,
        "time_str": format_time(remaining),
    })


# ──────────────────────────────────────────────────────────
# UTILITAIRES
# ──────────────────────────────────────────────────────────
def format_time(seconds):
    """Formate des secondes en MM:SS."""
    minutes = seconds // 60
    secs = seconds % 60
    return f"{minutes:02d}:{secs:02d}"


@app.template_filter("format_time")
def format_time_filter(seconds):
    return format_time(seconds)


@app.context_processor
def inject_globals():
    """Injecte des variables globales dans tous les templates."""
    return {
        "current_year": datetime.now().year,
        "game_config": GAME_CONFIG,
    }


# ──────────────────────────────────────────────────────────
# LANCEMENT
# ──────────────────────────────────────────────────────────
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    print(f"\n  🗝️  Le Secret de la Bibliothèque Interdite")
    print(f"  📜 Ouvrez http://localhost:{port} dans votre navigateur\n")
    app.run(host="0.0.0.0", port=port, debug=True)
