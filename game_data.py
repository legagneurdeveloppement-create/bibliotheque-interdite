"""
Le Secret de la Bibliothèque Interdite
Données du jeu — énigmes, indices, contenu narratif
"""

from dataclasses import dataclass, field
from typing import List, Dict


@dataclass
class ParisMap:
    id: str
    title: str
    year: int
    event: str
    description: str
    glyph: str


@dataclass
class LanguageFragment:
    id: str
    language: str
    flag: str
    original_text: str
    transliteration: str
    translation: str
    digit: int
    hint: str


@dataclass
class FoundersInitial:
    letter: str
    name: str
    role: str


@dataclass
class TruthItem:
    id: str
    name: str
    object: str
    icon: str
    birth_year: int
    role: str
    clue: str
    hidden_spot: str


@dataclass
class Hint:
    id: str
    act: str
    trigger: str
    text: str


# ──────────────────────────────────────────────────────────
# ACTE I — Les Codes des Lumières (Observation)
# ──────────────────────────────────────────────────────────
PARIS_MAPS: List[ParisMap] = [
    ParisMap(
        id="map-1715",
        title="La Ville du Roi-Soleil",
        year=1715,
        event="Mort de Louis XIV",
        description="Une carte montrant Paris centré sur Versailles, marquée d'un soleil couchant.",
        glyph="☉",
    ),
    ParisMap(
        id="map-1748",
        title="L'Esprit des Lois",
        year=1748,
        event="Publication de Montesquieu",
        description="Le quartier Saint-Sulpice est surligné, avec une balance gravée dans la marge.",
        glyph="⚖",
    ),
    ParisMap(
        id="map-1762",
        title="Le Contrat Social",
        year=1762,
        event="Œuvre de Rousseau",
        description="Une main tend un parchemin au-dessus de la Seine, signé 'J.J.R.'.",
        glyph="✍",
    ),
    ParisMap(
        id="map-1789",
        title="La Prise de la Bastille",
        year=1789,
        event="Révolution française",
        description="La forteresse est en flammes, entourée d'un cercle de sang sépia.",
        glyph="✺",
    ),
    ParisMap(
        id="map-1793",
        title="Le Régicide",
        year=1793,
        event="Exécution de Louis XVI",
        description="La place de la Révolution porte une marque noire, un triangle inversé.",
        glyph="▽",
    ),
    ParisMap(
        id="map-1799",
        title="Le 18 Brumaire",
        year=1799,
        event="Arrivée de Bonaparte au pouvoir",
        description="L'étoile d'un général est tracée au-dessus des Tuileries.",
        glyph="★",
    ),
]

ACT1_CORRECT_ORDER = [
    "map-1715",
    "map-1748",
    "map-1762",
    "map-1789",
    "map-1793",
    "map-1799",
]

CYRILLIC_MESSAGE = {
    "original": "ИЩИТЕ КЛЮЧ В ТРЁХ ЯЗЫКАХ, А ИСТИНУ — В ПОРЯДКЕ РОЖДЕНИЯ",
    "transliteration": "ISHCHITE KLYUCH V TRYOKH YAZYKAKH, A ISTINU — V PORYADKE ROZHDENIYA",
    "translation": "Cherchez la clé dans trois langues, et la vérité — dans l'ordre de naissance.",
    "hint": "Cet indice guidera l'Acte II (les trois langues) et l'Acte III (l'ordre de naissance).",
}


# ──────────────────────────────────────────────────────────
# ACTE II — Les Langues Oubliées (Cryptographie)
# ──────────────────────────────────────────────────────────
LANGUAGE_FRAGMENTS: List[LanguageFragment] = [
    LanguageFragment(
        id="frag-latin",
        language="Latin",
        flag="🏛️",
        original_text="TRES SUNT QUI TESTIMONIUM DANT",
        transliteration="Tres sunt qui testimonium dant",
        translation="Trois sont ceux qui témoignent",
        digit=3,
        hint="Le chiffre est caché dans le premier mot, traduit littéralement.",
    ),
    LanguageFragment(
        id="frag-greek",
        language="Ancien Grec",
        flag="🏛️",
        original_text="ΠΕΝΤΕ ΦΩΤΟΣ ΣΤΥΛΟΙ",
        transliteration="Pente phōtos styloi",
        translation="Cinq piliers de lumière",
        digit=5,
        hint="Le nombre de piliers mentionné dans la phrase.",
    ),
    LanguageFragment(
        id="frag-italian",
        language="Italien Renaissance",
        flag="🎭",
        original_text="SETTE SONO LE STELLE DELLA SERA",
        transliteration="Sette sono le stelle della sera",
        translation="Sept sont les étoiles du soir",
        digit=7,
        hint="Le nombre d'étoiles mentionné au début de la phrase.",
    ),
]

FOUNDERS_INITIALS: List[FoundersInitial] = [
    FoundersInitial(letter="B", name="Balthazar", role="Archiviste"),
    FoundersInitial(letter="I", name="Ignace", role="Cryptographe"),
    FoundersInitial(letter="B", name="Béatrice", role="Cartographe"),
    FoundersInitial(letter="L", name="Lazare", role="Horloger"),
    FoundersInitial(letter="I", name="Isidore", role="Linguiste"),
    FoundersInitial(letter="O", name="Octave", role="Mécène"),
    FoundersInitial(letter="S", name="Séverine", role="Gardienne"),
]

# B.I.B.L.I.O.S. → la 4e lettre (L) est la 12e lettre de l'alphabet ; 1+2 = 2
REBUS_DIGIT = 2
REBUS_EXPLANATION = (
    "Les initiales des fondateurs forment B.I.B.L.I.O.S. — Bibliothèque de l'Aube Perdue. "
    "La quatrième lettre, L, est la 12ᵉ de l'alphabet. Sa somme digitale (1+2) donne le dernier chiffre : 2."
)

ACT2_COMBINATION = "3572"


# ──────────────────────────────────────────────────────────
# ACTE III — Le Chiffre de César (Cryptographie avancée)
# ──────────────────────────────────────────────────────────
# Chiffrement par décalage : chaque lettre est décalée de N positions.
# Pour décrypter, le joueur doit trouver le bon décalage (shift).

CAESAR_CIPHER = {
    # Message en clair : "L ETOILE DU NORD GUIDE LA VERITE"
    "plain_text": "L ETOILE DU NORD GUIDE LA VERITE",
    # Décalage (shift) : 7 — les 7 merveilles du monde antique
    "shift": 7,
    # Message chiffré (calculé automatiquement ci-dessous pour éviter les erreurs)
    # Message chiffré (calculé par la fonction _caesar_encrypt)
    "encrypted_text": "S LAVPSL KB UVYK NBPKL SH CLYPAL",
    # Indice pour trouver le décalage
    "shift_hint": (
        "Le décalage correspond au nombre de merveilles du monde antique. "
        "Combien y en avait-il ? (Indice : c'est un nombre entre 1 et 12.)"
    ),
    # Ce que le message révèle (indice pour l'Acte IV)
    "reveals": (
        "L'Étoile du Nord guide la vérité. Dans la Bibliothèque, "
        "cherchez le Carré de Polybe — les coordonnées y sont inscrites."
    ),
}


# ──────────────────────────────────────────────────────────
# ACTE IV — Le Carré de Polybe (Codage ancien)
# ──────────────────────────────────────────────────────────
# Grille 5×5 : chaque lettre est codée par ses coordonnées (ligne, colonne).
# I et J partagent la même case (convention standard).

POLYBIUS_SQUARE = {
    # Grille 5×5 (I/J confondus)
    "grid": [
        ["A", "B", "C", "D", "E"],
        ["F", "G", "H", "I/J", "K"],
        ["L", "M", "N", "O", "P"],
        ["Q", "R", "S", "T", "U"],
        ["V", "W", "X", "Y", "Z"],
    ],
    # Message encodé : coordonnées (ligne, colonne) séparées par des tirets
    # "SOLEIL" → S=(4,3), O=(3,4), L=(3,1), E=(1,5), I=(2,4), L=(3,1)
    "encoded_pairs": [
        (4, 3),  # S
        (3, 4),  # O
        (3, 1),  # L
        (1, 5),  # E
        (2, 4),  # I
        (3, 1),  # L
    ],
    "encoded_text": "43-34-31-15-24-31",
    # Mot décodé
    "decoded_word": "SOLEIL",
    # Indice
    "hint": (
        "Chaque paire de chiffres (ligne-colonne) pointe vers une lettre de la grille. "
        "Ainsi, 11 = A, 12 = B, 13 = C... Décodez la séquence pour révéler le mot."
    ),
    # Ce que le mot révèle (indice pour l'Acte V)
    "reveals": (
        "Le Soleil — symbole des Lumières — éclaire la vérité. "
        "Les sept objets cachés doivent être disposés sur le piédestal "
        "dans l'ordre de naissance des penseurs, du plus jeune au plus âgé."
    ),
}



# ──────────────────────────────────────────────────────────
# ACTE V — Le Protocole de Vérité (Interdépendance)
# ──────────────────────────────────────────────────────────
TRUTH_ITEMS: List[TruthItem] = [
    TruthItem(
        id="item-voltaire", name="Voltaire", object="Plume d'oie", icon="🪶",
        birth_year=1694, role="Le Philosophe des Lumières",
        clue="Sa plume acérée pourfendit l'obscurantisme.",
        hidden_spot="Dans l'encrier du pupitre central",
    ),
    TruthItem(
        id="item-rousseau", name="Rousseau", object="Boussole", icon="🧭",
        birth_year=1712, role="Le Penseur Solitaire",
        clue="Il marcha seul, cherchant le nord moral.",
        hidden_spot="Au pied du globe terrestre",
    ),
    TruthItem(
        id="item-diderot", name="Diderot", object="Livre relié", icon="📕",
        birth_year=1713, role="L'Encyclopédiste",
        clue="Il rassembla tout le savoir en un seul ouvrage.",
        hidden_spot="Dans l'étagère du fond, troisième rayon",
    ),
    TruthItem(
        id="item-montesquieu", name="Montesquieu", object="Balance de justice", icon="⚖️",
        birth_year=1689, role="Le Légiste",
        clue="Il pesa les pouvoirs pour les équilibrer.",
        hidden_spot="Sur la cheminée, derrière le cadran",
    ),
    TruthItem(
        id="item-condorcet", name="Condorcet", object="Pièce de monnaie", icon="🪙",
        birth_year=1743, role="Le Mathématicien",
        clue="Il calcula le progrès et frappa des idées en monnaie.",
        hidden_spot="Dans le tiroir secret du pupitre",
    ),
    TruthItem(
        id="item-beaumarchais", name="Beaumarchais", object="Masque de théâtre", icon="🎭",
        birth_year=1732, role="Le Dramaturge",
        clue="Sous le masque du Barbier, il fit rire les rois.",
        hidden_spot="Accroché au mur, derrière un portrait",
    ),
    TruthItem(
        id="item-chatelet", name="Émilie du Châtelet", object="Verre de cristal", icon="🍷",
        birth_year=1706, role="La Savante",
        clue="Elle traduisit Newton et fit briller la lumière dans le cristal.",
        hidden_spot="Dans le cabinet vitré à droite",
    ),
]

# Ordre correct : du plus jeune au plus âgé
ACT5_CORRECT_ORDER = [
    "item-condorcet",    # 1743
    "item-beaumarchais", # 1732
    "item-diderot",      # 1713
    "item-rousseau",     # 1712
    "item-chatelet",     # 1706
    "item-voltaire",     # 1694
    "item-montesquieu",  # 1689
]

# Hotspots cachés dans la salle
HIDDEN_SPOTS = [
    {"id": "spot-desk", "label": "Pupitre central", "x": 50, "y": 35, "item": "item-voltaire"},
    {"id": "spot-globe", "label": "Globe terrestre", "x": 22, "y": 55, "item": "item-rousseau"},
    {"id": "spot-shelf", "label": "Étagère du fond", "x": 78, "y": 45, "item": "item-diderot"},
    {"id": "spot-fireplace", "label": "Cheminée", "x": 30, "y": 75, "item": "item-montesquieu"},
    {"id": "spot-drawer", "label": "Tiroir secret", "x": 60, "y": 60, "item": "item-condorcet"},
    {"id": "spot-wall", "label": "Mur / Portrait", "x": 15, "y": 30, "item": "item-beaumarchais"},
    {"id": "spot-cabinet", "label": "Cabinet vitré", "x": 85, "y": 70, "item": "item-chatelet"},
]


# ──────────────────────────────────────────────────────────
# INDICES DU MAÎTRE DU JEU
# ──────────────────────────────────────────────────────────
HINTS: List[Hint] = [
    # Acte I
    Hint("h-a1-1", "act1", "first",
         "Les dates inscrites sur les cartes racontent l'histoire de la pensée française. Commencez par le plus ancien."),
    Hint("h-a1-2", "act1", "stuck",
         "La mort du Roi-Soleil ouvre le siècle des Lumières. Montesquieu suit, puis Rousseau, et enfin la Révolution."),
    Hint("h-a1-3", "act1", "final",
         "L'ordre est : 1715 → 1748 → 1762 → 1789 → 1793 → 1799. Le message cyrillique se révélera alors."),
    # Acte II
    Hint("h-a2-1", "act2", "first",
         "Chaque fragment contient un nombre écrit en toutes lettres. Traduisez littéralement, sans interpréter."),
    Hint("h-a2-2", "act2", "stuck",
         "Tres = 3, Pente = 5, Sette = 7. Le quatrième chiffre se cache dans le rébus : observez les initiales."),
    Hint("h-a2-3", "act2", "final",
         "Les fondateurs : Balthazar, Ignace, Béatrice, Lazare, Isidore, Octave, Séverine. Le 4e, Lazare (L), est la 12ᵉ lettre ; 1+2 = 2. Combinaison : 3572."),
    # Acte III — César
    Hint("h-a3-1", "act3", "first",
         "Il s'agit d'un chiffrement par décalage : chaque lettre a été avancée de N positions dans l'alphabet. Trouvez N."),
    Hint("h-a3-2", "act3", "stuck",
         "Le décalage correspond aux 7 merveilles du monde antique. Ajustez le curseur sur 7 pour décrypter le message."),
    Hint("h-a3-3", "act3", "final",
         "Le décalage est 7. Le message décrypté dit : 'L'Étoile du Nord guide la vérité'. Cela mène au Carré de Polybe."),
    # Acte IV — Polybe
    Hint("h-a4-1", "act4", "first",
         "Chaque paire de chiffres indique la ligne puis la colonne de la lettre dans la grille 5×5."),
    Hint("h-a4-2", "act4", "stuck",
         "43 = ligne 4, colonne 3 = S. 34 = ligne 3, colonne 4 = O. Continuez ainsi pour chaque paire."),
    Hint("h-a4-3", "act4", "final",
         "Les paires décodent en : S-O-L-E-I-L, soit le mot 'SOLEIL'. Ce symbole des Lumières confirme l'ordre final."),
    # Acte V — Piédestal
    Hint("h-a5-1", "act5", "first",
         "Chaque objet est lié à un personnage par sa fonction. La plume va au polémiste, le masque au dramaturge."),
    Hint("h-a5-2", "act5", "stuck",
         "Le message cyrillique disait : 'la vérité — dans l'ordre de naissance'. Du plus jeune au plus âgé."),
    Hint("h-a5-3", "act5", "final",
         "L'ordre exact : Condorcet (1743) → Beaumarchais (1732) → Diderot (1713) → Rousseau (1712) → Émilie (1706) → Voltaire (1694) → Montesquieu (1689)."),
]


# ──────────────────────────────────────────────────────────
# CONFIGURATION GLOBALE
# ──────────────────────────────────────────────────────────
GAME_CONFIG = {
    "total_time_seconds": 75 * 60,  # 75 minutes
    "max_hints_per_act": 3,
}

NARRATION = {
    "intro": [
        "Vous êtes un groupe de passionnés, de chercheurs excentriques, réunis par une légende murmurée.",
        "La Bibliothèque de l'Aube Perdue détiendrait les archives d'un groupe de penseurs dissidents du XVIIIᵉ siècle, échappés à l'Inquisition savante.",
        "Vous avez réussi l'accès à une salle de lecture souterraine, scellée depuis deux siècles. Au centre, un pupitre massif, surmonté d'un livre étrangement ouvert...",
        "Votre objectif : récupérer le Protocole de Vérité avant que les gardiens — ou le temps — ne vous rattrapent.",
        "Trouvez les sept clés. Découvrez la vérité. Échappez à la Bibliothèque.",
    ],
    "act1_start": "La salle est remplie de cartes anciennes, de globes et de manuscrits éparpillés. Certaines cartes portent des marques ésotériques. Alignez-les selon l'ordre historique.",
    "act1_end": "Le mécanisme résonne. Un compartiment secret s'ouvre dans le pupitre, révélant un parchemin couvert de caractères cyrilliques. Le message est clair : la clé est dans les trois langues, et la vérité dans l'ordre de naissance.",
    "act2_start": "Le message de l'Acte I pointe vers une boîte verrouillée. Un mécanisme à quatre chiffres protège son contenu. Autour, des fragments de textes en latin, grec ancien et italien Renaissance. Un rébus orne le couvercle.",
    "act2_end": "La boîte s'ouvre dans un déclic satisfaisant. À l'intérieur, non pas la réponse, mais une feuille de notes mentionnant sept noms et sept objets dispersés dans la salle. Au fond, un second parchemin caché révèle un texte incompréhensible…",
    "act3_start": "Au fond de la boîte, un parchemin caché révèle un texte incompréhensible : des lettres décalées, semblant n'avoir aucun sens. Il s'agit d'un chiffre de César — un codage ancien par décalage. Trouvez le bon décalage pour révéler le message.",
    "act3_end": "Le décalage de 7 révèle le message : « L'Étoile du Nord guide la vérité. » Ce n'est pas une indication astronomique, mais un renvoi au Carré de Polybe — un système de coordonnées que les fondateurs utilisaient pour coder leurs secrets les plus précieux.",
    "act4_start": "Le message décrypté pointe vers le Carré de Polybe : une grille 5×5 où chaque lettre est désignée par ses coordonnées (ligne, colonne). Une séquence de paires numériques est inscrite sur la paroi. Décodez-la pour révéler le mot caché.",
    "act4_end": "Le mot se dévoile : SOLEIL. Symbole des Lumières, il confirme la voie à suivre — les sept objets cachés dans la salle doivent être disposés selon l'ordre de naissance des penseurs, du plus jeune au plus âgé.",
    "act5_start": "Sept objets sont cachés dans la salle. Sept noms y correspondent. Retrouvez-les, associez-les, puis disposez-les sur le piédestal dans l'ordre révélé par le message cyrillique : du plus jeune au plus âgé.",
    "act5_end": "L'arrangement final s'achève. Un grondement sourd ébranle la salle. Le piédestal s'illumine d'une lueur dorée. Le Protocole de Vérité se dévoile enfin...",
    "victory": "Vous avez réussi. Le Protocole de Vérité repose entre vos mains. Les esprits dissidents du XVIIIᵉ siècle peuvent enfin reposer, leur héritage préservé. Vous quittez la Bibliothèque de l'Aube Perdue, marqués à jamais par ses secrets.",
    "defeat": "Le temps a coulé comme le sable. Les gardiens ont repris leurs droits. La Bibliothèque se referme sur ses secrets... pour cette fois. Mais la légende, elle, perdurera.",
}


def get_hints_for_act(act: str) -> List[Hint]:
    """Retourne les indices disponibles pour un acte donné."""
    return [h for h in HINTS if h.act == act]


def get_map_by_id(map_id: str) -> ParisMap:
    for m in PARIS_MAPS:
        if m.id == map_id:
            return m
    raise ValueError(f"Carte inconnue: {map_id}")


def get_fragment_by_id(frag_id: str) -> LanguageFragment:
    for f in LANGUAGE_FRAGMENTS:
        if f.id == frag_id:
            return f
    raise ValueError(f"Fragment inconnu: {frag_id}")


def get_item_by_id(item_id: str) -> TruthItem:
    for i in TRUTH_ITEMS:
        if i.id == item_id:
            return i
    raise ValueError(f"Objet inconnu: {item_id}")


def get_spot_by_id(spot_id: str) -> Dict:
    for s in HIDDEN_SPOTS:
        if s["id"] == spot_id:
            return s
    raise ValueError(f"Emplacement inconnu: {spot_id}")
