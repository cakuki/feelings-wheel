#!/usr/bin/env python3
"""Language content for the feelings wheel. Add a language by adding an entry to
LANGUAGES; the geometry/layout code stays language-agnostic.

The 6 core emotions share one PALETTE (index aligns with each language's `cores`
order). `core_font` is the uniform curved-label size for that language — sized so
its longest core word fills the wedge; verify with fit_check.js after editing.
"""

# Shared, in canonical order: Happy, Surprised, Angry, Scared, Sad, Calm.
PALETTE = ["#F4C430", "#E8833A", "#DB504A", "#9B6FB0", "#4F8FCB", "#56B27E"]

LANGUAGES = {
    "tr": {
        "name": "Türkçe",
        "core_font": 21,
        "cores": [
            ("Mutlu",   ["Neşeli", "Heyecanlı", "Gururlu", "Minnettar"]),
            ("Şaşkın",  ["Meraklı", "Hayran", "Kafası karışık", "Şok"]),
            ("Kızgın",  ["Sinirli", "Öfkeli", "Kıskanç", "Engellenmiş"]),
            ("Korkmuş", ["Endişeli", "Utangaç", "Tedirgin", "Panik"]),
            ("Üzgün",   ["Yalnız", "Hayal kırıklığı", "Çaresiz", "Özlemli"]),
            ("Sakin",   ["Huzurlu", "Rahat", "Güvende", "Memnun"]),
        ],
        "title": "Duygu Çarkı 🎡",
        "subtitle": "Bugün içinden hangi duygu geçiyor? Çarkta bul ve göster.",
        "center": ["Bugün", "nasıl", "hissediyorsun?"],
        "howto_title": "Nasıl kullanılır?",
        "howto_body": (
            "Ortadaki 6 ana duygudan sana en yakın olanı seç (örneğin "
            "<b>Mutlu</b>). Sonra o rengin dış halkasındaki daha ince "
            "duygulardan birini bul (örneğin <b>Minnettar</b> ya da "
            "<b>Heyecanlı</b>). Duygunun adını yüksek sesle söyle ve "
            "“Bu duyguyu ne zaman hissettim?” diye birlikte konuşun. "
            "Doğru ya da yanlış duygu yoktur — hepsi değerlidir. 💛"
        ),
        "cal_title": "Duygu Takvimim 📅",
        "cal_subtitle": "Her gün kendini nasıl hissettiysen o renkle daireyi boya.",
        "month_label": "Ay",
        "cal_note": (
            "Günün sonunda “Bugün en çok hangi duyguyu yaşadın?” diye sor ve o "
            "ana duygunun rengiyle boya. Hafta sonunda birlikte çarka bakıp konuşun."
        ),
    },
    "en": {
        "name": "English",
        "core_font": 20,
        "cores": [
            ("Happy",     ["Cheerful", "Excited", "Proud", "Grateful"]),
            ("Surprised", ["Curious", "Amazed", "Confused", "Shocked"]),
            ("Angry",     ["Annoyed", "Furious", "Jealous", "Frustrated"]),
            ("Scared",    ["Worried", "Shy", "Nervous", "Panicked"]),
            ("Sad",       ["Lonely", "Disappointed", "Helpless", "Wistful"]),
            ("Calm",      ["Peaceful", "Relaxed", "Safe", "Content"]),
        ],
        "title": "Feelings Wheel 🎡",
        "subtitle": "Which feeling is inside you today? Find it on the wheel and point to it.",
        "center": ["How do", "you feel", "today?"],
        "howto_title": "How to use it",
        "howto_body": (
            "Pick the core emotion in the middle that feels closest (e.g. "
            "<b>Happy</b>). Then find a more specific feeling in that color's "
            "outer ring (e.g. <b>Grateful</b> or <b>Excited</b>). Say the "
            "feeling out loud and talk together about “When did I feel this?” "
            "There is no right or wrong feeling — they all matter. 💛"
        ),
        "cal_title": "My Feelings Calendar 📅",
        "cal_subtitle": "Each day, color the circle with the feeling you had the most.",
        "month_label": "Month",
        "cal_note": (
            "At the end of the day, ask “Which feeling did you have most today?” "
            "and color it with that core emotion's color. At the weekend, look at "
            "the wheel together and talk about it."
        ),
    },
    "de": {
        "name": "Deutsch",
        "core_font": 17,
        "cores": [
            ("Glücklich",  ["Fröhlich", "Aufgeregt", "Stolz", "Dankbar"]),
            ("Überrascht", ["Neugierig", "Erstaunt", "Verwirrt", "Schockiert"]),
            ("Wütend",     ["Genervt", "Zornig", "Eifersüchtig", "Frustriert"]),
            ("Ängstlich",  ["Besorgt", "Schüchtern", "Nervös", "Panisch"]),
            ("Traurig",    ["Einsam", "Enttäuscht", "Hilflos", "Sehnsüchtig"]),
            ("Ruhig",      ["Friedlich", "Entspannt", "Geborgen", "Zufrieden"]),
        ],
        "title": "Gefühlsrad 🎡",
        "subtitle": "Welches Gefühl steckt heute in dir? Finde es im Rad und zeig darauf.",
        "center": ["Wie fühlst", "du dich", "heute?"],
        "howto_title": "So benutzt du es",
        "howto_body": (
            "Wähle in der Mitte das Grundgefühl, das am besten passt (z. B. "
            "<b>Glücklich</b>). Suche dann im äußeren Ring derselben Farbe ein "
            "genaueres Gefühl (z. B. <b>Dankbar</b> oder <b>Aufgeregt</b>). "
            "Sprich das Gefühl laut aus und redet zusammen darüber: „Wann habe "
            "ich das gefühlt?“ Es gibt kein richtiges oder falsches Gefühl — "
            "alle sind wichtig. 💛"
        ),
        "cal_title": "Mein Gefühlskalender 📅",
        "cal_subtitle": "Male jeden Tag den Kreis in der Farbe deines stärksten Gefühls an.",
        "month_label": "Monat",
        "cal_note": (
            "Frag am Ende des Tages: „Welches Gefühl hattest du heute am "
            "meisten?“ und male es in der Farbe dieses Grundgefühls aus. Schaut "
            "am Wochenende zusammen auf das Rad und redet darüber."
        ),
    },
}


def core_data(lang_code):
    """Return [(name, color, [feelings]), ...] for a language, with shared colors."""
    lang = LANGUAGES[lang_code]
    return [(name, PALETTE[i], feels) for i, (name, feels) in enumerate(lang["cores"])]
