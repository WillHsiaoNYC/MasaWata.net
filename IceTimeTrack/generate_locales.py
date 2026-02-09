#!/usr/bin/env python3
"""
Generate all 16 non-English locale JSON files for IceTimeTrack website.
FAQ items are extracted from the app's Localizable.xcstrings.
Website UI translations are embedded below.

Usage: python3 generate_locales.py
"""

import json
import os
import sys

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
LOCALES_DIR = os.path.join(SCRIPT_DIR, 'locales')

# Load en.json as template
with open(os.path.join(LOCALES_DIR, 'en.json'), 'r', encoding='utf-8') as f:
    EN_TEMPLATE = json.load(f)

# Load FAQ translations from extract_faq.py output
XCSTRINGS_PATH = os.path.join(
    SCRIPT_DIR, '..', '..', '..', 'IceTimeTrack',
    'Ice Time Track', 'Ice Time Track Phone', 'Localizable.xcstrings'
)

FAQ_QUESTIONS = [
    "How do I start tracking a session?",
    "What's the difference between Game, Practice, and Scrimmage?",
    "Do I need my iPhone with me during a game?",
    "What is a step?",
    "What is acceleration?",
    "What is rotation?",
    "How does the app know when I'm on the ice?",
    "How is on-ice/bench status triggered by motion?",
    "How do the advanced detection settings work?",
    "Why is there a delay when I stop skating?",
    "What is the movement buffer?",
    "What is the game log?",
    "Do I need to start a Game session to use the game log?",
    "Can I log a game result without starting a live tracking session on the Apple Watch?",
    "How do I log events on my Watch?",
    "How do I log events on my iPhone?",
    "What types of events can I log?",
    "What happens if I don't set a time for an event?",
    "Can I edit events after the session?",
    "How are Watch and iPhone events merged?",
    "What does detection sensitivity do?",
    "How do I adjust the buffer time?",
    "What are haptic alerts and how do I use them?",
    'What does "Auto-end session" do?',
    "If I change settings during an active session, do they take effect immediately?",
    "What are Advanced Settings?",
    "What data is saved to Apple Health?",
    "How do I enable/disable HealthKit integration?",
    "Why isn't my heart rate showing?",
    "How do sessions sync between Watch and iPhone?",
    "Why isn't my session showing on my iPhone?",
    "Can I delete a session?",
    "The app isn't detecting my shifts accurately",
    "The app stopped recording mid-game",
    "The Watch app is stuck on 'Sync Required'",
    "Why does the app need location access?",
    "Why does the app need motion & fitness access?",
    "Is my data shared with anyone?",
    "How do I enable location access if I accidentally denied it?",
]

# Build FAQ answer keys from en.json
FAQ_ANSWERS = [item['answer'] for item in EN_TEMPLATE['faq']['items']]


def get_faq_translations(xcstrings_data, lang):
    """Extract FAQ question/answer translations for a given language."""
    strings = xcstrings_data.get('strings', {})
    items = []
    for q_key, a_key in zip(FAQ_QUESTIONS, FAQ_ANSWERS):
        q_entry = strings.get(q_key, {})
        q_loc = q_entry.get('localizations', {}).get(lang, {})
        q_val = q_loc.get('stringUnit', {}).get('value', q_key)

        a_entry = strings.get(a_key, {})
        a_loc = a_entry.get('localizations', {}).get(lang, {})
        a_val = a_loc.get('stringUnit', {}).get('value', a_key)

        items.append({'question': q_val, 'answer': a_val})
    return items


# Website UI translations for all 16 non-English languages
UI_TRANSLATIONS = {
    "cs": {
        "appName": "Ice Time Track",
        "meta": {
            "title": "Ice Time Track - Automatická detekce střídání pro Apple Watch",
            "description": "Sledujte svůj čas na ledě automaticky s Apple Watch. Detekce střídání, záznam gólů a trestů, monitorování tepu a pohybu."
        },
        "nav": {"features": "Funkce", "howItWorks": "Jak to funguje", "screenshots": "Snímky", "faq": "FAQ", "cta": "Předobjednat", "ctaDownload": "Stáhnout"},
        "countdown": {"title": "Spuštění za", "promo": "1 rok za $6.99", "promoSub": "Časově omezená nabídka — nenechte si ujít", "days": "Dny", "hours": "Hodiny", "minutes": "Minuty", "seconds": "Sekundy", "date": "14. února 2026", "claimOffer": "Uplatnit nabídku", "launchSpecial": "Speciální nabídka", "offerEnds": "Nabídka končí 28. února 2026", "downloadNow": "Stáhnout nyní"},
        "hero": {"title": "Automatická detekce střídání<br>pro hokejisty", "description": "Zjistěte přesně, kolik času na ledě máte — bez dotyku hodinek. Sledujte góly, tresty a třetiny. Stačí spustit a hrát.", "preOrder": "Předobjednat nyní", "platforms": "K dispozici pro Apple Watch + iPhone · Spuštění 14. února 2026", "shiftDetection": "Detekce střídání", "goalTracking": "Sledování gólů", "penaltyLogging": "Záznam trestů", "gameAnalytics": "Herní analytika"},
        "features": {
            "title": "Funkce", "subtitle": "Vše potřebné pro sledování hry",
            "shiftDetection": {"title": "Automatická detekce střídání", "description": "Vstupte na led a vaše hodinky to vědí. Žádná tlačítka během hry — senzory automaticky rozpoznají bruslení vs. lavičku."},
            "eventTracking": {"title": "Sledování herních událostí", "description": "Zaznamenávejte góly, asistence a tresty přímo z zápěstí. Sledujte třetiny a uchovávejte kompletní záznam každého zápasu."},
            "healthMetrics": {"title": "Zdravotní metriky v reálném čase", "description": "Monitorujte tep, spálené kalorie a intenzitu pohybu v reálném čase. Podívejte se, jak tvrdě pracujete při každém střídání."},
            "analytics": {"title": "Analytika relací", "description": "Prohlédněte si celkový čas na ledě, počet střídání, průměrnou délku střídání a osobní rekordy."},
            "healthIntegration": {"title": "Integrace Apple Health", "description": "Relace se synchronizují do Apple Health jako hokejové tréninky. Přispívejte ke svým kroužkům aktivity."},
            "offline": {"title": "Funguje offline", "description": "Vaše hodinky zaznamenávají vše nezávisle. Na lavičce nepotřebujete iPhone — data se synchronizují automaticky po zápase."}
        },
        "howItWorks": {
            "title": "Jak to funguje", "subtitle": "Od rozcvičky po analýzu po zápase",
            "step1": {"number": "1", "title": "Před zápasem", "description": "Otevřete Ice Time Track na Apple Watch. Klepněte na Zápas, Trénink nebo Přátelák."},
            "step2": {"number": "2", "title": "Během zápasu", "description": "Vstupte na led a vaše hodinky to automaticky detekují. Zaznamenávejte góly a tresty klepnutím."},
            "step3": {"number": "3", "title": "Po zápase", "description": "Vaše relace se synchronizuje s iPhonem. Prohlédněte si čas na ledě, střídání, tep a herní události."}
        },
        "screenshots": {"title": "Podívejte se", "subtitle": "Navrženo pro hokejisty"},
        "testimonials": {
            "title": "Co říkají hráči", "subtitle": "Důvěřují nám hokejisté po celém světě",
            "review1": {"quote": "\"Konečně aplikace, která sleduje můj čas na ledě bez nutnosti cokoliv ťukat. Změna hry pro sledování střídání.\"", "author": "— Hockey Dad"},
            "review2": {"quote": "\"Miluju sledování tepu a statistik střídání po každém zápase. Pomáhá mi porozumět mé kondici.\"", "author": "— Beer League Player"},
            "review3": {"quote": "\"Automatická detekce je překvapivě přesná. Moje děti ji používají každý zápas.\"", "author": "— Youth Hockey Parent"}
        },
        "download": {"title": "Připraveni sledovat čas na ledě?", "description": "Stáhněte si Ice Time Track a začněte další relaci. Automatická detekce střídání, záznam herních událostí a zdravotní metriky — vše z vašeho zápěstí.", "preOrder": "Předobjednat nyní", "downloadNow": "Stáhnout nyní"},
        "footer": {"privacy": "Zásady ochrany osobních údajů", "terms": "Podmínky služby", "support": "Podpora", "copyright": "© 2026 MasaWata. Všechna práva vyhrazena."}
    },
    "da": {
        "appName": "Ice Time Track",
        "meta": {"title": "Ice Time Track - Automatisk skiftdetektering til Apple Watch", "description": "Spor din istid automatisk med Apple Watch. Detekter skift, log mål og straffe, overvåg puls og bevægelse."},
        "nav": {"features": "Funktioner", "howItWorks": "Sådan virker det", "screenshots": "Skærmbilleder", "faq": "FAQ", "cta": "Forudbestil", "ctaDownload": "Download"},
        "countdown": {"title": "Lancering om", "promo": "1 år for $6.99", "promoSub": "Tidsbegrænset tilbud — gå ikke glip af det", "days": "Dage", "hours": "Timer", "minutes": "Minutter", "seconds": "Sekunder", "date": "14. februar 2026", "claimOffer": "Indløs tilbud", "launchSpecial": "Lanceringsstilbud", "offerEnds": "Tilbud slutter 28. februar 2026", "downloadNow": "Download nu"},
        "hero": {"title": "Automatisk skiftdetektering<br>for hockeyspillere", "description": "Ved præcis, hvor meget istid du får — uden at trykke på dit ur. Spor mål, straffe og perioder. Start bare en session og spil.", "preOrder": "Forudbestil nu", "platforms": "Tilgængelig på Apple Watch + iPhone · Lancering 14. februar 2026", "shiftDetection": "Skiftdetektering", "goalTracking": "Målsporing", "penaltyLogging": "Straffelogning", "gameAnalytics": "Kampanalyse"},
        "features": {
            "title": "Funktioner", "subtitle": "Alt hvad du behøver for at spore din kamp",
            "shiftDetection": {"title": "Automatisk skiftdetektering", "description": "Træd på isen, og dit ur ved det. Ingen knapper at trykke under spil — sensorer registrerer skøjteløb vs. bænktid automatisk."},
            "eventTracking": {"title": "Kamphændelsesregistrering", "description": "Log mål, assists og straffe direkte fra dit håndled. Spor perioder og hold en komplet oversigt over hver kamp."},
            "healthMetrics": {"title": "Sundhedsdata i realtid", "description": "Overvåg puls, forbrændte kalorier og bevægelsesintensitet i realtid. Se hvor hårdt du arbejder hvert skift."},
            "analytics": {"title": "Sessionsanalyse", "description": "Gennemgå total istid, antal skift, gennemsnitlig skiftlængde og personlige rekorder."},
            "healthIntegration": {"title": "Apple Health-integration", "description": "Sessioner synkroniseres til Apple Health som hockeytræninger. Bidrag til dine aktivitetsringe."},
            "offline": {"title": "Virker offline", "description": "Dit ur registrerer alt uafhængigt. Ingen iPhone nødvendig på bænken — data synkroniseres automatisk efter kampen."}
        },
        "howItWorks": {
            "title": "Sådan virker det", "subtitle": "Fra opvarmning til analyse efter kampen",
            "step1": {"number": "1", "title": "Før kampen", "description": "Åbn Ice Time Track på dit Apple Watch. Tryk på Kamp, Træning eller Scrimmage."},
            "step2": {"number": "2", "title": "Under kampen", "description": "Træd på isen, og dit ur registrerer det automatisk. Log mål og straffe med et tryk."},
            "step3": {"number": "3", "title": "Efter kampen", "description": "Din session synkroniseres til din iPhone. Gennemgå istid, skift, puls og kamphændelser."}
        },
        "screenshots": {"title": "Se det i aktion", "subtitle": "Designet til hockeyspillere"},
        "testimonials": {
            "title": "Hvad spillere siger", "subtitle": "Betroet af hockeyspillere overalt",
            "review1": {"quote": "\"Endelig en app der sporer min istid uden at jeg skal trykke på noget. Game changer for at spore mine skift.\"", "author": "— Hockey Dad"},
            "review2": {"quote": "\"Elsker at se min puls og skiftstatistik efter hver kamp. Hjælper mig med at forstå min kondition.\"", "author": "— Beer League Player"},
            "review3": {"quote": "\"Den automatiske detektering er overraskende præcis. Mine børn bruger den til hver kamp nu.\"", "author": "— Youth Hockey Parent"}
        },
        "download": {"title": "Klar til at spore din istid?", "description": "Hent Ice Time Track og start din næste session. Automatisk skiftdetektering, kamphændelseslogning og sundhedsdata — alt fra dit håndled.", "preOrder": "Forudbestil nu", "downloadNow": "Download nu"},
        "footer": {"privacy": "Privatlivspolitik", "terms": "Servicevilkår", "support": "Support", "copyright": "© 2026 MasaWata. Alle rettigheder forbeholdes."}
    },
    "de": {
        "appName": "Ice Time Track",
        "meta": {"title": "Ice Time Track - Automatische Schichterkennung für Apple Watch", "description": "Verfolge deine Eiszeit automatisch mit der Apple Watch. Erkenne Schichten, protokolliere Tore und Strafen, überwache Herzfrequenz und Bewegung."},
        "nav": {"features": "Funktionen", "howItWorks": "So funktioniert's", "screenshots": "Screenshots", "faq": "FAQ", "cta": "Vorbestellen", "ctaDownload": "Laden"},
        "countdown": {"title": "Start in", "promo": "1 Jahr für $6,99", "promoSub": "Zeitlich begrenztes Angebot — nicht verpassen", "days": "Tage", "hours": "Stunden", "minutes": "Minuten", "seconds": "Sekunden", "date": "14. Februar 2026", "claimOffer": "Angebot einlösen", "launchSpecial": "Start-Spezial", "offerEnds": "Angebot endet am 28. Februar 2026", "downloadNow": "Jetzt laden"},
        "hero": {"title": "Automatische Schichterkennung<br>für Eishockeyspieler", "description": "Wisse genau, wie viel Eiszeit du bekommst — ohne deine Uhr zu berühren. Verfolge Tore, Strafen und Drittel. Starte einfach eine Sitzung und spiel.", "preOrder": "Jetzt vorbestellen", "platforms": "Verfügbar für Apple Watch + iPhone · Start am 14. Februar 2026", "shiftDetection": "Schichterkennung", "goalTracking": "Torverfolgung", "penaltyLogging": "Strafenprotokoll", "gameAnalytics": "Spielanalyse"},
        "features": {
            "title": "Funktionen", "subtitle": "Alles was du brauchst, um dein Spiel zu verfolgen",
            "shiftDetection": {"title": "Automatische Schichterkennung", "description": "Betritt das Eis und deine Uhr weiß es. Keine Tasten während des Spiels — Sensoren erkennen automatisch Schlittschuhlaufen vs. Bankzeit."},
            "eventTracking": {"title": "Spielereignis-Tracking", "description": "Protokolliere Tore, Assists und Strafen direkt vom Handgelenk. Verfolge Drittel und führe ein vollständiges Protokoll jedes Spiels."},
            "healthMetrics": {"title": "Live-Gesundheitsmetriken", "description": "Überwache Herzfrequenz, verbrannte Kalorien und Bewegungsintensität in Echtzeit."},
            "analytics": {"title": "Sitzungsanalyse", "description": "Überprüfe Gesamteiszeit, Schichtanzahl, durchschnittliche Schichtlänge und persönliche Rekorde."},
            "healthIntegration": {"title": "Apple Health Integration", "description": "Sitzungen werden als Eishockey-Workouts mit Apple Health synchronisiert."},
            "offline": {"title": "Funktioniert offline", "description": "Deine Uhr zeichnet alles unabhängig auf. Kein iPhone auf der Bank nötig — Daten synchronisieren sich automatisch nach dem Spiel."}
        },
        "howItWorks": {
            "title": "So funktioniert's", "subtitle": "Vom Aufwärmen bis zur Nachspielanalyse",
            "step1": {"number": "1", "title": "Vor dem Spiel", "description": "Öffne Ice Time Track auf deiner Apple Watch. Tippe auf Spiel, Training oder Scrimmage."},
            "step2": {"number": "2", "title": "Während des Spiels", "description": "Betritt das Eis und deine Uhr erkennt es automatisch. Protokolliere Tore und Strafen mit einem Tippen."},
            "step3": {"number": "3", "title": "Nach dem Spiel", "description": "Deine Sitzung synchronisiert sich mit deinem iPhone. Überprüfe Eiszeit, Schichten, Herzfrequenz und Spielereignisse."}
        },
        "screenshots": {"title": "In Aktion sehen", "subtitle": "Entwickelt für Eishockeyspieler"},
        "testimonials": {
            "title": "Was Spieler sagen", "subtitle": "Vertraut von Eishockeyspielern überall",
            "review1": {"quote": "\"Endlich eine App, die meine Eiszeit verfolgt, ohne dass ich etwas tippen muss. Game Changer für das Tracking meiner Schichten.\"", "author": "— Hockey Dad"},
            "review2": {"quote": "\"Liebe es, nach jedem Spiel meine Herzfrequenz und Schichtstatistiken zu sehen. Hilft mir, meine Kondition zu verstehen.\"", "author": "— Beer League Player"},
            "review3": {"quote": "\"Die automatische Erkennung ist erstaunlich genau. Meine Kinder nutzen sie jetzt bei jedem Spiel.\"", "author": "— Youth Hockey Parent"}
        },
        "download": {"title": "Bereit, deine Eiszeit zu verfolgen?", "description": "Hol dir Ice Time Track und starte deine nächste Sitzung. Automatische Schichterkennung, Spielereignis-Protokollierung und Gesundheitsmetriken — alles vom Handgelenk.", "preOrder": "Jetzt vorbestellen", "downloadNow": "Jetzt laden"},
        "footer": {"privacy": "Datenschutzrichtlinie", "terms": "Nutzungsbedingungen", "support": "Support", "copyright": "© 2026 MasaWata. Alle Rechte vorbehalten."}
    },
    "es": {
        "appName": "Ice Time Track",
        "meta": {"title": "Ice Time Track - Detección automática de turnos de hockey para Apple Watch", "description": "Registra tu tiempo en el hielo automáticamente con Apple Watch. Detecta turnos, registra goles y penalizaciones, monitorea ritmo cardíaco y movimiento."},
        "nav": {"features": "Funciones", "howItWorks": "Cómo funciona", "screenshots": "Capturas", "faq": "FAQ", "cta": "Pre-ordenar", "ctaDownload": "Descargar"},
        "countdown": {"title": "Lanzamiento en", "promo": "1 año por $6.99", "promoSub": "Oferta por tiempo limitado — no te la pierdas", "days": "Días", "hours": "Horas", "minutes": "Minutos", "seconds": "Segundos", "date": "14 de febrero de 2026", "claimOffer": "Reclamar oferta", "launchSpecial": "Especial de lanzamiento", "offerEnds": "La oferta termina el 28 de febrero de 2026", "downloadNow": "Descargar ahora"},
        "hero": {"title": "Detección automática de turnos<br>para jugadores de hockey", "description": "Sabe exactamente cuánto tiempo de hielo tienes — sin tocar tu reloj. Registra goles, penalizaciones y períodos. Solo inicia una sesión y juega.", "preOrder": "Pre-ordenar ahora", "platforms": "Disponible en Apple Watch + iPhone · Lanzamiento 14 de febrero de 2026", "shiftDetection": "Detección de turnos", "goalTracking": "Seguimiento de goles", "penaltyLogging": "Registro de penalizaciones", "gameAnalytics": "Análisis de juego"},
        "features": {
            "title": "Funciones", "subtitle": "Todo lo que necesitas para seguir tu juego",
            "shiftDetection": {"title": "Detección automática de turnos", "description": "Pisa el hielo y tu reloj lo sabe. Sin botones durante el juego — los sensores detectan patinaje vs. banco automáticamente."},
            "eventTracking": {"title": "Seguimiento de eventos del juego", "description": "Registra goles, asistencias y penalizaciones desde tu muñeca. Sigue los períodos y mantén un registro completo de cada juego."},
            "healthMetrics": {"title": "Métricas de salud en vivo", "description": "Monitorea ritmo cardíaco, calorías quemadas e intensidad de movimiento en tiempo real."},
            "analytics": {"title": "Análisis de sesión", "description": "Revisa tiempo total en hielo, cantidad de turnos, duración promedio de turno y récords personales."},
            "healthIntegration": {"title": "Integración con Apple Health", "description": "Las sesiones se sincronizan con Apple Health como entrenamientos de hockey."},
            "offline": {"title": "Funciona sin conexión", "description": "Tu reloj registra todo de forma independiente. No necesitas iPhone en el banco — los datos se sincronizan automáticamente después del juego."}
        },
        "howItWorks": {
            "title": "Cómo funciona", "subtitle": "Del calentamiento al análisis post-partido",
            "step1": {"number": "1", "title": "Antes del juego", "description": "Abre Ice Time Track en tu Apple Watch. Toca Juego, Práctica o Scrimmage."},
            "step2": {"number": "2", "title": "Durante el juego", "description": "Pisa el hielo y tu reloj lo detecta automáticamente. Registra goles y penalizaciones con un toque."},
            "step3": {"number": "3", "title": "Después del juego", "description": "Tu sesión se sincroniza con tu iPhone. Revisa tiempo en hielo, turnos, ritmo cardíaco y eventos del juego."}
        },
        "screenshots": {"title": "Míralo en acción", "subtitle": "Diseñado para jugadores de hockey"},
        "testimonials": {
            "title": "Lo que dicen los jugadores", "subtitle": "Confiado por jugadores de hockey en todas partes",
            "review1": {"quote": "\"Por fin una app que registra mi tiempo en el hielo sin tener que tocar nada. Un cambio total para el seguimiento de mis turnos.\"", "author": "— Hockey Dad"},
            "review2": {"quote": "\"Me encanta ver mi ritmo cardíaco y estadísticas de turnos después de cada juego. Me ayuda a entender mi condición física.\"", "author": "— Beer League Player"},
            "review3": {"quote": "\"La detección automática es sorprendentemente precisa. Mis hijos la usan en cada juego ahora.\"", "author": "— Youth Hockey Parent"}
        },
        "download": {"title": "¿Listo para registrar tu tiempo en el hielo?", "description": "Obtén Ice Time Track y comienza tu próxima sesión. Detección automática de turnos, registro de eventos de juego y métricas de salud — todo desde tu muñeca.", "preOrder": "Pre-ordenar ahora", "downloadNow": "Descargar ahora"},
        "footer": {"privacy": "Política de privacidad", "terms": "Términos de servicio", "support": "Soporte", "copyright": "© 2026 MasaWata. Todos los derechos reservados."}
    },
    "fi": {
        "appName": "Ice Time Track",
        "meta": {"title": "Ice Time Track - Automaattinen vaihtotunnistus Apple Watchille", "description": "Seuraa jääaikaasi automaattisesti Apple Watchilla. Tunnista vaihdot, kirjaa maalit ja jäähyt, seuraa sykettä ja liikettä."},
        "nav": {"features": "Ominaisuudet", "howItWorks": "Näin se toimii", "screenshots": "Kuvakaappaukset", "faq": "UKK", "cta": "Ennakkotilaa", "ctaDownload": "Lataa"},
        "countdown": {"title": "Julkaisuun", "promo": "1 vuosi hintaan $6,99", "promoSub": "Rajoitetun ajan tarjous — älä missaa", "days": "Päivää", "hours": "Tuntia", "minutes": "Minuuttia", "seconds": "Sekuntia", "date": "14. helmikuuta 2026", "claimOffer": "Lunasta tarjous", "launchSpecial": "Julkaisutarjous", "offerEnds": "Tarjous päättyy 28. helmikuuta 2026", "downloadNow": "Lataa nyt"},
        "hero": {"title": "Automaattinen vaihtotunnistus<br>jääkiekkoilijoille", "description": "Tiedä tarkalleen kuinka paljon jääaikaa saat — ilman kellon koskettamista. Seuraa maaleja, jäähyjä ja eriä. Aloita vain sessio ja pelaa.", "preOrder": "Ennakkotilaa nyt", "platforms": "Saatavilla Apple Watch + iPhone · Julkaisu 14. helmikuuta 2026", "shiftDetection": "Vaihtotunnistus", "goalTracking": "Maaliseuranta", "penaltyLogging": "Jäähykirjaus", "gameAnalytics": "Pelianalyysi"},
        "features": {
            "title": "Ominaisuudet", "subtitle": "Kaikki mitä tarvitset pelisi seuraamiseen",
            "shiftDetection": {"title": "Automaattinen vaihtotunnistus", "description": "Astu jäälle ja kellosi tietää sen. Ei painikkeita pelin aikana — anturit tunnistavat luistelun vs. vaihtopenkin automaattisesti."},
            "eventTracking": {"title": "Pelitapahtumien seuranta", "description": "Kirjaa maalit, syötöt ja jäähyt suoraan ranteestasi. Seuraa eriä ja pidä täydellinen kirja jokaisesta pelistä."},
            "healthMetrics": {"title": "Reaaliaikaiset terveysmittarit", "description": "Seuraa sykettä, palaneita kaloreita ja liikeintensiteettiä reaaliajassa."},
            "analytics": {"title": "Sessioanalyysi", "description": "Tarkastele kokonaisjääaikaa, vaihtojen määrää, keskimääräistä vaihdon pituutta ja henkilökohtaisia ennätyksiä."},
            "healthIntegration": {"title": "Apple Health -integraatio", "description": "Sessiot synkronoituvat Apple Healthiin jääkiekkoharjoituksina."},
            "offline": {"title": "Toimii offline", "description": "Kellosi tallentaa kaiken itsenäisesti. iPhonea ei tarvita vaihtopenkillä — data synkronoituu automaattisesti pelin jälkeen."}
        },
        "howItWorks": {
            "title": "Näin se toimii", "subtitle": "Lämmittelystä pelin jälkeiseen analyysiin",
            "step1": {"number": "1", "title": "Ennen peliä", "description": "Avaa Ice Time Track Apple Watchissasi. Napauta Peli, Harjoitus tai Harjoitusottelu."},
            "step2": {"number": "2", "title": "Pelin aikana", "description": "Astu jäälle ja kellosi tunnistaa sen automaattisesti. Kirjaa maalit ja jäähyt napautuksella."},
            "step3": {"number": "3", "title": "Pelin jälkeen", "description": "Sessiosi synkronoituu iPhoneesi. Tarkastele jääaikaa, vaihtoja, sykettä ja pelitapahtumia."}
        },
        "screenshots": {"title": "Katso se toiminnassa", "subtitle": "Suunniteltu jääkiekkoilijoille"},
        "testimonials": {
            "title": "Mitä pelaajat sanovat", "subtitle": "Jääkiekkoilijoiden luottama kaikkialla",
            "review1": {"quote": "\"Vihdoin sovellus joka seuraa jääaikaani ilman että tarvitsee napauttaa mitään. Mullistava vaihtojen seurantaan.\"", "author": "— Hockey Dad"},
            "review2": {"quote": "\"Rakastan syke- ja vaihtotilastojen näkemistä jokaisen pelin jälkeen. Auttaa ymmärtämään kuntoani.\"", "author": "— Beer League Player"},
            "review3": {"quote": "\"Automaattinen tunnistus on yllättävän tarkka. Lapseni käyttävät sitä jokaisessa pelissä nyt.\"", "author": "— Youth Hockey Parent"}
        },
        "download": {"title": "Valmiina seuraamaan jääaikaasi?", "description": "Hanki Ice Time Track ja aloita seuraava sessiosi. Automaattinen vaihtotunnistus, pelitapahtumien kirjaus ja terveysmittarit — kaikki ranteestasi.", "preOrder": "Ennakkotilaa nyt", "downloadNow": "Lataa nyt"},
        "footer": {"privacy": "Tietosuojakäytäntö", "terms": "Käyttöehdot", "support": "Tuki", "copyright": "© 2026 MasaWata. Kaikki oikeudet pidätetään."}
    },
    "fr": {
        "appName": "Ice Time Track",
        "meta": {"title": "Ice Time Track - Détection automatique des présences pour Apple Watch", "description": "Suivez votre temps de glace automatiquement avec Apple Watch. Détectez les présences, enregistrez les buts et pénalités, surveillez le rythme cardiaque et le mouvement."},
        "nav": {"features": "Fonctionnalités", "howItWorks": "Comment ça marche", "screenshots": "Captures", "faq": "FAQ", "cta": "Précommander", "ctaDownload": "Télécharger"},
        "countdown": {"title": "Lancement dans", "promo": "1 an pour 6,99 $", "promoSub": "Offre limitée dans le temps — ne la manquez pas", "days": "Jours", "hours": "Heures", "minutes": "Minutes", "seconds": "Secondes", "date": "14 février 2026", "claimOffer": "Réclamer l'offre", "launchSpecial": "Offre de lancement", "offerEnds": "L'offre se termine le 28 février 2026", "downloadNow": "Télécharger"},
        "hero": {"title": "Détection automatique des présences<br>pour les joueurs de hockey", "description": "Sachez exactement combien de temps de glace vous avez — sans toucher votre montre. Suivez les buts, les pénalités et les périodes. Démarrez simplement une session et jouez.", "preOrder": "Précommander", "platforms": "Disponible sur Apple Watch + iPhone · Lancement le 14 février 2026", "shiftDetection": "Détection des présences", "goalTracking": "Suivi des buts", "penaltyLogging": "Journal des pénalités", "gameAnalytics": "Analyse de match"},
        "features": {
            "title": "Fonctionnalités", "subtitle": "Tout ce dont vous avez besoin pour suivre votre match",
            "shiftDetection": {"title": "Détection automatique des présences", "description": "Montez sur la glace et votre montre le sait. Pas de boutons pendant le jeu — les capteurs détectent automatiquement le patinage vs. le banc."},
            "eventTracking": {"title": "Suivi des événements de match", "description": "Enregistrez buts, passes et pénalités directement depuis votre poignet. Suivez les périodes et gardez un historique complet."},
            "healthMetrics": {"title": "Métriques santé en direct", "description": "Surveillez le rythme cardiaque, les calories brûlées et l'intensité du mouvement en temps réel."},
            "analytics": {"title": "Analyse de session", "description": "Consultez le temps de glace total, le nombre de présences, la durée moyenne et les records personnels."},
            "healthIntegration": {"title": "Intégration Apple Santé", "description": "Les sessions se synchronisent avec Apple Santé en tant qu'entraînements de hockey."},
            "offline": {"title": "Fonctionne hors ligne", "description": "Votre montre enregistre tout de manière indépendante. Pas besoin d'iPhone sur le banc — les données se synchronisent automatiquement après le match."}
        },
        "howItWorks": {
            "title": "Comment ça marche", "subtitle": "De l'échauffement à l'analyse d'après-match",
            "step1": {"number": "1", "title": "Avant le match", "description": "Ouvrez Ice Time Track sur votre Apple Watch. Touchez Match, Entraînement ou Scrimmage."},
            "step2": {"number": "2", "title": "Pendant le match", "description": "Montez sur la glace et votre montre le détecte automatiquement. Enregistrez buts et pénalités d'un toucher."},
            "step3": {"number": "3", "title": "Après le match", "description": "Votre session se synchronise avec votre iPhone. Consultez le temps de glace, les présences, le rythme cardiaque et les événements."}
        },
        "screenshots": {"title": "Voyez-le en action", "subtitle": "Conçu pour les joueurs de hockey"},
        "testimonials": {
            "title": "Ce que disent les joueurs", "subtitle": "Approuvé par les joueurs de hockey partout",
            "review1": {"quote": "\"Enfin une app qui suit mon temps de glace sans que j'aie à toucher quoi que ce soit. Révolutionnaire pour le suivi de mes présences.\"", "author": "— Hockey Dad"},
            "review2": {"quote": "\"J'adore voir mon rythme cardiaque et mes stats de présences après chaque match. Ça m'aide à comprendre ma condition physique.\"", "author": "— Beer League Player"},
            "review3": {"quote": "\"La détection automatique est étonnamment précise. Mes enfants l'utilisent à chaque match maintenant.\"", "author": "— Youth Hockey Parent"}
        },
        "download": {"title": "Prêt à suivre votre temps de glace ?", "description": "Téléchargez Ice Time Track et commencez votre prochaine session. Détection automatique des présences, journal des événements et métriques santé — tout depuis votre poignet.", "preOrder": "Précommander", "downloadNow": "Télécharger"},
        "footer": {"privacy": "Politique de confidentialité", "terms": "Conditions d'utilisation", "support": "Support", "copyright": "© 2026 MasaWata. Tous droits réservés."}
    },
    "hu": {
        "appName": "Ice Time Track",
        "meta": {"title": "Ice Time Track - Automatikus váltásérzékelés Apple Watch-hoz", "description": "Kövesse jégidejét automatikusan az Apple Watch-csal. Érzékelje a váltásokat, naplózza a gólokat és büntetéseket, figyelje a pulzust és a mozgást."},
        "nav": {"features": "Funkciók", "howItWorks": "Hogyan működik", "screenshots": "Képernyőképek", "faq": "GYIK", "cta": "Előrendelés", "ctaDownload": "Letöltés"},
        "countdown": {"title": "Indulás", "promo": "1 év $6,99-ért", "promoSub": "Korlátozott idejű ajánlat — ne hagyja ki", "days": "Nap", "hours": "Óra", "minutes": "Perc", "seconds": "Másodperc", "date": "2026. február 14.", "claimOffer": "Ajánlat igénylése", "launchSpecial": "Indulási akció", "offerEnds": "Az ajánlat 2026. február 28-án lejár", "downloadNow": "Letöltés most"},
        "hero": {"title": "Automatikus váltásérzékelés<br>jégkorongosoknak", "description": "Tudja meg pontosan, mennyi jégidőt kap — anélkül, hogy megérintené az óráját. Kövesse a gólokat, büntetéseket és harmadokat. Csak indítson egy munkamenetet és játsszon.", "preOrder": "Előrendelés most", "platforms": "Elérhető Apple Watch + iPhone · Indulás 2026. február 14.", "shiftDetection": "Váltásérzékelés", "goalTracking": "Gólkövetés", "penaltyLogging": "Büntetésnaplózás", "gameAnalytics": "Mérkőzéselemzés"},
        "features": {
            "title": "Funkciók", "subtitle": "Minden, amire szüksége van a mérkőzés követéséhez",
            "shiftDetection": {"title": "Automatikus váltásérzékelés", "description": "Lépjen a jégre és az órája tudni fogja. Nincs szükség gombokra játék közben — az érzékelők automatikusan felismerik a korcsolyázást."},
            "eventTracking": {"title": "Mérkőzésesemények követése", "description": "Naplózzon gólokat, gólpasszokat és büntetéseket közvetlenül a csuklójáról."},
            "healthMetrics": {"title": "Élő egészségügyi mutatók", "description": "Figyelje a pulzust, az elégetett kalóriákat és a mozgás intenzitását valós időben."},
            "analytics": {"title": "Munkamenet-elemzés", "description": "Tekintse át a teljes jégidőt, a váltások számát, az átlagos váltáshosszt és a személyes rekordokat."},
            "healthIntegration": {"title": "Apple Health integráció", "description": "A munkamenetek jégkorong-edzésként szinkronizálódnak az Apple Health-be."},
            "offline": {"title": "Offline is működik", "description": "Az órája mindent önállóan rögzít. Nincs szükség iPhone-ra a kispadon — az adatok automatikusan szinkronizálódnak a mérkőzés után."}
        },
        "howItWorks": {
            "title": "Hogyan működik", "subtitle": "A bemelegítéstől a mérkőzés utáni elemzésig",
            "step1": {"number": "1", "title": "A mérkőzés előtt", "description": "Nyissa meg az Ice Time Track-et az Apple Watch-on. Koppintson a Mérkőzés, Edzés vagy Scrimmage gombra."},
            "step2": {"number": "2", "title": "A mérkőzés alatt", "description": "Lépjen a jégre és az órája automatikusan érzékeli. Naplózza a gólokat és büntetéseket egy koppintással."},
            "step3": {"number": "3", "title": "A mérkőzés után", "description": "Munkamenete szinkronizálódik az iPhone-jával. Tekintse át a jégidőt, váltásokat, pulzust és mérkőzéseseményeket."}
        },
        "screenshots": {"title": "Nézze meg működés közben", "subtitle": "Jégkorongosoknak tervezve"},
        "testimonials": {
            "title": "Mit mondanak a játékosok", "subtitle": "Jégkorongosok bizalmát élvezi mindenhol",
            "review1": {"quote": "\"Végre egy app, ami követi a jégidőmet anélkül, hogy bármit is meg kellene érintenem. Forradalmi a váltások követéséhez.\"", "author": "— Hockey Dad"},
            "review2": {"quote": "\"Imádom a pulzusom és váltásstatisztikáim megtekintését minden mérkőzés után.\"", "author": "— Beer League Player"},
            "review3": {"quote": "\"Az automatikus érzékelés meglepően pontos. A gyerekeim minden mérkőzésen használják.\"", "author": "— Youth Hockey Parent"}
        },
        "download": {"title": "Készen áll a jégidő követésére?", "description": "Töltse le az Ice Time Track-et és kezdje el következő munkamenetét. Automatikus váltásérzékelés, mérkőzésesemény-naplózás és egészségügyi mutatók — mindezt a csuklójáról.", "preOrder": "Előrendelés most", "downloadNow": "Letöltés most"},
        "footer": {"privacy": "Adatvédelmi irányelvek", "terms": "Szolgáltatási feltételek", "support": "Támogatás", "copyright": "© 2026 MasaWata. Minden jog fenntartva."}
    },
    "it": {
        "appName": "Ice Time Track",
        "meta": {"title": "Ice Time Track - Rilevamento automatico dei turni per Apple Watch", "description": "Monitora il tuo tempo sul ghiaccio automaticamente con Apple Watch. Rileva i turni, registra gol e penalità, monitora frequenza cardiaca e movimento."},
        "nav": {"features": "Funzionalità", "howItWorks": "Come funziona", "screenshots": "Screenshot", "faq": "FAQ", "cta": "Preordina", "ctaDownload": "Scarica"},
        "countdown": {"title": "Lancio tra", "promo": "1 anno a $6,99", "promoSub": "Offerta a tempo limitato — non perderla", "days": "Giorni", "hours": "Ore", "minutes": "Minuti", "seconds": "Secondi", "date": "14 febbraio 2026", "claimOffer": "Riscatta offerta", "launchSpecial": "Offerta di lancio", "offerEnds": "L'offerta scade il 28 febbraio 2026", "downloadNow": "Scarica ora"},
        "hero": {"title": "Rilevamento automatico dei turni<br>per giocatori di hockey", "description": "Sai esattamente quanto tempo passi sul ghiaccio — senza toccare l'orologio. Monitora gol, penalità e periodi. Avvia una sessione e gioca.", "preOrder": "Preordina ora", "platforms": "Disponibile su Apple Watch + iPhone · Lancio 14 febbraio 2026", "shiftDetection": "Rilevamento turni", "goalTracking": "Tracciamento gol", "penaltyLogging": "Registro penalità", "gameAnalytics": "Analisi partita"},
        "features": {
            "title": "Funzionalità", "subtitle": "Tutto ciò che ti serve per monitorare la tua partita",
            "shiftDetection": {"title": "Rilevamento automatico dei turni", "description": "Sali sul ghiaccio e il tuo orologio lo sa. Nessun pulsante durante il gioco — i sensori rilevano automaticamente il pattinaggio vs. la panchina."},
            "eventTracking": {"title": "Tracciamento eventi di gioco", "description": "Registra gol, assist e penalità direttamente dal polso. Monitora i periodi e mantieni un registro completo."},
            "healthMetrics": {"title": "Metriche salute in tempo reale", "description": "Monitora frequenza cardiaca, calorie bruciate e intensità del movimento in tempo reale."},
            "analytics": {"title": "Analisi sessione", "description": "Rivedi tempo totale sul ghiaccio, numero di turni, durata media dei turni e record personali."},
            "healthIntegration": {"title": "Integrazione Apple Salute", "description": "Le sessioni si sincronizzano con Apple Salute come allenamenti di hockey."},
            "offline": {"title": "Funziona offline", "description": "Il tuo orologio registra tutto in modo indipendente. Nessun iPhone necessario in panchina — i dati si sincronizzano automaticamente dopo la partita."}
        },
        "howItWorks": {
            "title": "Come funziona", "subtitle": "Dal riscaldamento all'analisi post-partita",
            "step1": {"number": "1", "title": "Prima della partita", "description": "Apri Ice Time Track sul tuo Apple Watch. Tocca Partita, Allenamento o Scrimmage."},
            "step2": {"number": "2", "title": "Durante la partita", "description": "Sali sul ghiaccio e il tuo orologio lo rileva automaticamente. Registra gol e penalità con un tocco."},
            "step3": {"number": "3", "title": "Dopo la partita", "description": "La tua sessione si sincronizza con l'iPhone. Rivedi tempo sul ghiaccio, turni, frequenza cardiaca ed eventi."}
        },
        "screenshots": {"title": "Guardalo in azione", "subtitle": "Progettato per giocatori di hockey"},
        "testimonials": {
            "title": "Cosa dicono i giocatori", "subtitle": "Scelto dai giocatori di hockey ovunque",
            "review1": {"quote": "\"Finalmente un'app che traccia il mio tempo sul ghiaccio senza dover toccare nulla. Rivoluzionario per il monitoraggio dei turni.\"", "author": "— Hockey Dad"},
            "review2": {"quote": "\"Adoro vedere la mia frequenza cardiaca e le statistiche dei turni dopo ogni partita.\"", "author": "— Beer League Player"},
            "review3": {"quote": "\"Il rilevamento automatico è sorprendentemente preciso. I miei figli lo usano ad ogni partita.\"", "author": "— Youth Hockey Parent"}
        },
        "download": {"title": "Pronto a monitorare il tuo tempo sul ghiaccio?", "description": "Scarica Ice Time Track e inizia la tua prossima sessione. Rilevamento automatico dei turni, registro eventi e metriche salute — tutto dal polso.", "preOrder": "Preordina ora", "downloadNow": "Scarica ora"},
        "footer": {"privacy": "Informativa sulla privacy", "terms": "Termini di servizio", "support": "Supporto", "copyright": "© 2026 MasaWata. Tutti i diritti riservati."}
    },
    "ja": {
        "appName": "Ice Time Track",
        "meta": {"title": "Ice Time Track - Apple Watch用自動シフト検出ホッケーアプリ", "description": "Apple Watchでアイスタイムを自動追跡。シフト検出、ゴール・ペナルティ記録、心拍数・動きのモニタリング。セッションを開始してプレーするだけ。"},
        "nav": {"features": "機能", "howItWorks": "使い方", "screenshots": "スクリーンショット", "faq": "FAQ", "cta": "予約注文", "ctaDownload": "ダウンロード"},
        "countdown": {"title": "リリースまで", "promo": "1年間 $6.99", "promoSub": "期間限定オファー — お見逃しなく", "days": "日", "hours": "時間", "minutes": "分", "seconds": "秒", "date": "2026年2月14日", "claimOffer": "オファーを受け取る", "launchSpecial": "リリース記念特別オファー", "offerEnds": "オファーは2026年2月28日に終了", "downloadNow": "ダウンロード"},
        "hero": {"title": "ホッケープレーヤーのための<br>自動シフト検出", "description": "ウォッチをタップせずに、正確なアイスタイムを把握。ゴール、ペナルティ、ピリオドを追跡。セッションを開始してプレーするだけ。", "preOrder": "今すぐ予約注文", "platforms": "Apple Watch + iPhoneで利用可能 · 2026年2月14日リリース", "shiftDetection": "シフト検出", "goalTracking": "ゴール追跡", "penaltyLogging": "ペナルティ記録", "gameAnalytics": "試合分析"},
        "features": {
            "title": "機能", "subtitle": "試合を追跡するために必要なすべて",
            "shiftDetection": {"title": "自動シフト検出", "description": "氷上に立つとウォッチが検知。プレー中にボタンを押す必要なし — センサーがスケートとベンチを自動判別。"},
            "eventTracking": {"title": "試合イベント追跡", "description": "手首からゴール、アシスト、ペナルティを記録。ピリオドを追跡し、すべての試合の完全な記録を保持。"},
            "healthMetrics": {"title": "リアルタイム健康指標", "description": "心拍数、消費カロリー、運動強度をリアルタイムでモニタリング。"},
            "analytics": {"title": "セッション分析", "description": "合計アイスタイム、シフト数、平均シフト時間、個人記録を確認。"},
            "healthIntegration": {"title": "Apple Health連携", "description": "セッションはホッケーワークアウトとしてApple Healthに同期。"},
            "offline": {"title": "オフラインで動作", "description": "ウォッチが独立してすべてを記録。ベンチでiPhoneは不要 — データは試合後に自動同期。"}
        },
        "howItWorks": {
            "title": "使い方", "subtitle": "ウォームアップから試合後の分析まで",
            "step1": {"number": "1", "title": "試合前", "description": "Apple WatchでIce Time Trackを開く。ゲーム、練習、スクリメージをタップして開始。"},
            "step2": {"number": "2", "title": "試合中", "description": "氷上に立つとウォッチが自動検出。タップでゴールとペナルティを記録。プレーに集中。"},
            "step3": {"number": "3", "title": "試合後", "description": "セッションがiPhoneに同期。アイスタイム、シフト、心拍数、試合イベントを確認。"}
        },
        "screenshots": {"title": "実際の画面", "subtitle": "ホッケープレーヤーのために設計"},
        "testimonials": {
            "title": "プレーヤーの声", "subtitle": "世界中のホッケープレーヤーが信頼",
            "review1": {"quote": "「何もタップせずにアイスタイムを追跡してくれるアプリ。シフト追跡の革命です。」", "author": "— Hockey Dad"},
            "review2": {"quote": "「試合後に心拍数とシフト統計を見るのが好き。自分のコンディションを理解するのに役立ちます。」", "author": "— Beer League Player"},
            "review3": {"quote": "「自動検出は驚くほど正確。子供たちは毎試合使っています。」", "author": "— Youth Hockey Parent"}
        },
        "download": {"title": "アイスタイムの追跡を始めましょう", "description": "Ice Time Trackをダウンロードして次のセッションを開始。自動シフト検出、試合イベント記録、健康指標 — すべて手首から。", "preOrder": "今すぐ予約注文", "downloadNow": "ダウンロード"},
        "footer": {"privacy": "プライバシーポリシー", "terms": "利用規約", "support": "サポート", "copyright": "© 2026 MasaWata. All rights reserved."}
    },
    "ko": {
        "appName": "Ice Time Track",
        "meta": {"title": "Ice Time Track - Apple Watch용 자동 하키 교대 감지", "description": "Apple Watch로 아이스 타임을 자동으로 추적하세요. 교대 감지, 골과 페널티 기록, 심박수와 움직임 모니터링."},
        "nav": {"features": "기능", "howItWorks": "사용 방법", "screenshots": "스크린샷", "faq": "FAQ", "cta": "사전 주문", "ctaDownload": "다운로드"},
        "countdown": {"title": "출시까지", "promo": "1년 $6.99", "promoSub": "기간 한정 제안 — 놓치지 마세요", "days": "일", "hours": "시간", "minutes": "분", "seconds": "초", "date": "2026년 2월 14일", "claimOffer": "제안 받기", "launchSpecial": "출시 특별 제안", "offerEnds": "제안은 2026년 2월 28일에 종료", "downloadNow": "지금 다운로드"},
        "hero": {"title": "하키 선수를 위한<br>자동 교대 감지", "description": "워치를 터치하지 않고 정확한 아이스 타임을 파악하세요. 골, 페널티, 피리어드를 추적합니다. 세션을 시작하고 플레이하세요.", "preOrder": "지금 사전 주문", "platforms": "Apple Watch + iPhone에서 사용 가능 · 2026년 2월 14일 출시", "shiftDetection": "교대 감지", "goalTracking": "골 추적", "penaltyLogging": "페널티 기록", "gameAnalytics": "경기 분석"},
        "features": {
            "title": "기능", "subtitle": "경기를 추적하는 데 필요한 모든 것",
            "shiftDetection": {"title": "자동 교대 감지", "description": "빙판에 서면 워치가 감지합니다. 경기 중 버튼을 누를 필요 없이 — 센서가 스케이팅과 벤치를 자동으로 구분합니다."},
            "eventTracking": {"title": "경기 이벤트 추적", "description": "손목에서 바로 골, 어시스트, 페널티를 기록하세요. 피리어드를 추적하고 모든 경기의 완전한 기록을 유지하세요."},
            "healthMetrics": {"title": "실시간 건강 지표", "description": "심박수, 소모 칼로리, 움직임 강도를 실시간으로 모니터링하세요."},
            "analytics": {"title": "세션 분석", "description": "총 아이스 타임, 교대 횟수, 평균 교대 시간, 개인 기록을 확인하세요."},
            "healthIntegration": {"title": "Apple Health 연동", "description": "세션이 하키 운동으로 Apple Health에 동기화됩니다."},
            "offline": {"title": "오프라인 작동", "description": "워치가 독립적으로 모든 것을 기록합니다. 벤치에서 iPhone이 필요 없습니다 — 경기 후 자동 동기화됩니다."}
        },
        "howItWorks": {
            "title": "사용 방법", "subtitle": "워밍업부터 경기 후 분석까지",
            "step1": {"number": "1", "title": "경기 전", "description": "Apple Watch에서 Ice Time Track을 엽니다. 경기, 연습 또는 스크리미지를 탭하여 시작합니다."},
            "step2": {"number": "2", "title": "경기 중", "description": "빙판에 서면 워치가 자동으로 감지합니다. 탭으로 골과 페널티를 기록합니다."},
            "step3": {"number": "3", "title": "경기 후", "description": "세션이 iPhone에 동기화됩니다. 아이스 타임, 교대, 심박수, 경기 이벤트를 확인합니다."}
        },
        "screenshots": {"title": "실제 화면 보기", "subtitle": "하키 선수를 위해 설계"},
        "testimonials": {
            "title": "선수들의 평가", "subtitle": "전 세계 하키 선수들이 신뢰",
            "review1": {"quote": "\"아무것도 터치하지 않고 아이스 타임을 추적하는 앱. 교대 추적의 혁명입니다.\"", "author": "— Hockey Dad"},
            "review2": {"quote": "\"매 경기 후 심박수와 교대 통계를 보는 것을 좋아합니다. 컨디션을 이해하는 데 도움이 됩니다.\"", "author": "— Beer League Player"},
            "review3": {"quote": "\"자동 감지가 놀라울 정도로 정확합니다. 아이들이 매 경기 사용합니다.\"", "author": "— Youth Hockey Parent"}
        },
        "download": {"title": "아이스 타임을 추적할 준비가 되셨나요?", "description": "Ice Time Track을 다운로드하고 다음 세션을 시작하세요. 자동 교대 감지, 경기 이벤트 기록, 건강 지표 — 모두 손목에서.", "preOrder": "지금 사전 주문", "downloadNow": "지금 다운로드"},
        "footer": {"privacy": "개인정보 보호정책", "terms": "이용약관", "support": "지원", "copyright": "© 2026 MasaWata. All rights reserved."}
    },
    "nb": {
        "appName": "Ice Time Track",
        "meta": {"title": "Ice Time Track - Automatisk skiftdeteksjon for Apple Watch", "description": "Spor istiden din automatisk med Apple Watch. Oppdag skift, logg mål og utvisninger, overvåk puls og bevegelse."},
        "nav": {"features": "Funksjoner", "howItWorks": "Slik fungerer det", "screenshots": "Skjermbilder", "faq": "FAQ", "cta": "Forhåndsbestill", "ctaDownload": "Last ned"},
        "countdown": {"title": "Lansering om", "promo": "1 år for $6,99", "promoSub": "Tidsbegrenset tilbud — ikke gå glipp av det", "days": "Dager", "hours": "Timer", "minutes": "Minutter", "seconds": "Sekunder", "date": "14. februar 2026", "claimOffer": "Krev tilbud", "launchSpecial": "Lanseringstilbud", "offerEnds": "Tilbudet avsluttes 28. februar 2026", "downloadNow": "Last ned nå"},
        "hero": {"title": "Automatisk skiftdeteksjon<br>for hockeyspillere", "description": "Vit nøyaktig hvor mye istid du får — uten å berøre klokken din. Spor mål, utvisninger og perioder. Bare start en økt og spill.", "preOrder": "Forhåndsbestill nå", "platforms": "Tilgjengelig på Apple Watch + iPhone · Lansering 14. februar 2026", "shiftDetection": "Skiftdeteksjon", "goalTracking": "Målsporing", "penaltyLogging": "Utvisningslogg", "gameAnalytics": "Kampanalyse"},
        "features": {
            "title": "Funksjoner", "subtitle": "Alt du trenger for å spore kampen din",
            "shiftDetection": {"title": "Automatisk skiftdeteksjon", "description": "Gå på isen og klokken din vet det. Ingen knapper å trykke under spill — sensorer oppdager skøyting vs. benk automatisk."},
            "eventTracking": {"title": "Kamphendelsesporing", "description": "Logg mål, assists og utvisninger rett fra håndleddet. Spor perioder og hold en komplett oversikt."},
            "healthMetrics": {"title": "Helsedata i sanntid", "description": "Overvåk puls, forbrente kalorier og bevegelsesintensitet i sanntid."},
            "analytics": {"title": "Øktanalyse", "description": "Se total istid, antall skift, gjennomsnittlig skiftlengde og personlige rekorder."},
            "healthIntegration": {"title": "Apple Helse-integrasjon", "description": "Økter synkroniseres til Apple Helse som hockeytreninger."},
            "offline": {"title": "Fungerer offline", "description": "Klokken din registrerer alt uavhengig. Ingen iPhone nødvendig på benken — data synkroniseres automatisk etter kampen."}
        },
        "howItWorks": {
            "title": "Slik fungerer det", "subtitle": "Fra oppvarming til analyse etter kampen",
            "step1": {"number": "1", "title": "Før kampen", "description": "Åpne Ice Time Track på Apple Watch. Trykk på Kamp, Trening eller Treningskamp."},
            "step2": {"number": "2", "title": "Under kampen", "description": "Gå på isen og klokken din oppdager det automatisk. Logg mål og utvisninger med et trykk."},
            "step3": {"number": "3", "title": "Etter kampen", "description": "Økten din synkroniseres til iPhone. Se istid, skift, puls og kamphendelser."}
        },
        "screenshots": {"title": "Se det i aksjon", "subtitle": "Designet for hockeyspillere"},
        "testimonials": {
            "title": "Hva spillere sier", "subtitle": "Betrodd av hockeyspillere overalt",
            "review1": {"quote": "\"Endelig en app som sporer istiden min uten at jeg trenger å trykke på noe. Game changer for skiftsporing.\"", "author": "— Hockey Dad"},
            "review2": {"quote": "\"Elsker å se pulsen og skiftstatistikken min etter hver kamp. Hjelper meg å forstå formen min.\"", "author": "— Beer League Player"},
            "review3": {"quote": "\"Den automatiske deteksjonen er overraskende nøyaktig. Barna mine bruker den hver kamp nå.\"", "author": "— Youth Hockey Parent"}
        },
        "download": {"title": "Klar til å spore istiden din?", "description": "Last ned Ice Time Track og start neste økt. Automatisk skiftdeteksjon, kamphendelseslogg og helsedata — alt fra håndleddet.", "preOrder": "Forhåndsbestill nå", "downloadNow": "Last ned nå"},
        "footer": {"privacy": "Personvernerklæring", "terms": "Vilkår for bruk", "support": "Støtte", "copyright": "© 2026 MasaWata. Alle rettigheter forbeholdt."}
    },
    "ru": {
        "appName": "Ice Time Track",
        "meta": {"title": "Ice Time Track - Автоматическое определение смен для Apple Watch", "description": "Отслеживайте время на льду автоматически с Apple Watch. Определение смен, запись голов и удалений, мониторинг пульса и движения."},
        "nav": {"features": "Функции", "howItWorks": "Как это работает", "screenshots": "Скриншоты", "faq": "FAQ", "cta": "Предзаказ", "ctaDownload": "Скачать"},
        "countdown": {"title": "До запуска", "promo": "1 год за $6.99", "promoSub": "Ограниченное предложение — не упустите", "days": "Дней", "hours": "Часов", "minutes": "Минут", "seconds": "Секунд", "date": "14 февраля 2026", "claimOffer": "Получить предложение", "launchSpecial": "Специальное предложение", "offerEnds": "Предложение заканчивается 28 февраля 2026", "downloadNow": "Скачать сейчас"},
        "hero": {"title": "Автоматическое определение смен<br>для хоккеистов", "description": "Точно знайте, сколько времени на льду вы получаете — без нажатий на часы. Отслеживайте голы, удаления и периоды. Просто начните сессию и играйте.", "preOrder": "Предзаказ сейчас", "platforms": "Доступно для Apple Watch + iPhone · Запуск 14 февраля 2026", "shiftDetection": "Определение смен", "goalTracking": "Отслеживание голов", "penaltyLogging": "Запись удалений", "gameAnalytics": "Аналитика матча"},
        "features": {
            "title": "Функции", "subtitle": "Всё необходимое для отслеживания игры",
            "shiftDetection": {"title": "Автоматическое определение смен", "description": "Выходите на лёд, и часы это знают. Никаких кнопок во время игры — сенсоры автоматически определяют катание vs. скамейку."},
            "eventTracking": {"title": "Отслеживание игровых событий", "description": "Записывайте голы, передачи и удаления прямо с запястья. Отслеживайте периоды и ведите полную запись каждой игры."},
            "healthMetrics": {"title": "Показатели здоровья в реальном времени", "description": "Мониторинг пульса, сожжённых калорий и интенсивности движения в реальном времени."},
            "analytics": {"title": "Анализ сессии", "description": "Просматривайте общее время на льду, количество смен, среднюю продолжительность смены и личные рекорды."},
            "healthIntegration": {"title": "Интеграция с Apple Здоровье", "description": "Сессии синхронизируются с Apple Здоровье как хоккейные тренировки."},
            "offline": {"title": "Работает офлайн", "description": "Часы записывают всё самостоятельно. iPhone на скамейке не нужен — данные синхронизируются автоматически после игры."}
        },
        "howItWorks": {
            "title": "Как это работает", "subtitle": "От разминки до анализа после игры",
            "step1": {"number": "1", "title": "Перед игрой", "description": "Откройте Ice Time Track на Apple Watch. Нажмите Игра, Тренировка или Товарищеская игра."},
            "step2": {"number": "2", "title": "Во время игры", "description": "Выходите на лёд, и часы автоматически определят это. Записывайте голы и удаления нажатием."},
            "step3": {"number": "3", "title": "После игры", "description": "Сессия синхронизируется с iPhone. Просмотрите время на льду, смены, пульс и игровые события."}
        },
        "screenshots": {"title": "Смотрите в действии", "subtitle": "Разработано для хоккеистов"},
        "testimonials": {
            "title": "Что говорят игроки", "subtitle": "Доверяют хоккеисты повсюду",
            "review1": {"quote": "\"Наконец приложение, которое отслеживает моё время на льду без нажатий. Революция в отслеживании смен.\"", "author": "— Hockey Dad"},
            "review2": {"quote": "\"Люблю смотреть пульс и статистику смен после каждой игры. Помогает понять мою физическую форму.\"", "author": "— Beer League Player"},
            "review3": {"quote": "\"Автоматическое определение удивительно точное. Мои дети используют его каждую игру.\"", "author": "— Youth Hockey Parent"}
        },
        "download": {"title": "Готовы отслеживать время на льду?", "description": "Скачайте Ice Time Track и начните следующую сессию. Автоматическое определение смен, запись игровых событий и показатели здоровья — всё с запястья.", "preOrder": "Предзаказ сейчас", "downloadNow": "Скачать сейчас"},
        "footer": {"privacy": "Политика конфиденциальности", "terms": "Условия использования", "support": "Поддержка", "copyright": "© 2026 MasaWata. Все права защищены."}
    },
    "sk": {
        "appName": "Ice Time Track",
        "meta": {"title": "Ice Time Track - Automatická detekcia striedaní pre Apple Watch", "description": "Sledujte svoj čas na ľade automaticky s Apple Watch. Detekcia striedaní, záznam gólov a trestov, monitorovanie tepu a pohybu."},
        "nav": {"features": "Funkcie", "howItWorks": "Ako to funguje", "screenshots": "Snímky", "faq": "FAQ", "cta": "Predobjednať", "ctaDownload": "Stiahnuť"},
        "countdown": {"title": "Spustenie za", "promo": "1 rok za $6,99", "promoSub": "Časovo obmedzená ponuka — nenechajte si ujsť", "days": "Dní", "hours": "Hodín", "minutes": "Minút", "seconds": "Sekúnd", "date": "14. februára 2026", "claimOffer": "Uplatniť ponuku", "launchSpecial": "Špeciálna ponuka", "offerEnds": "Ponuka končí 28. februára 2026", "downloadNow": "Stiahnuť teraz"},
        "hero": {"title": "Automatická detekcia striedaní<br>pre hokejistov", "description": "Zistite presne, koľko času na ľade máte — bez dotyku hodiniek. Sledujte góly, tresty a tretiny. Stačí spustiť a hrať.", "preOrder": "Predobjednať teraz", "platforms": "K dispozícii pre Apple Watch + iPhone · Spustenie 14. februára 2026", "shiftDetection": "Detekcia striedaní", "goalTracking": "Sledovanie gólov", "penaltyLogging": "Záznam trestov", "gameAnalytics": "Herná analytika"},
        "features": {
            "title": "Funkcie", "subtitle": "Všetko potrebné na sledovanie hry",
            "shiftDetection": {"title": "Automatická detekcia striedaní", "description": "Vstúpte na ľad a vaše hodinky to vedia. Žiadne tlačidlá počas hry — senzory automaticky rozpoznajú korčuľovanie vs. striedačku."},
            "eventTracking": {"title": "Sledovanie herných udalostí", "description": "Zaznamenávajte góly, asistencie a tresty priamo zo zápästia."},
            "healthMetrics": {"title": "Zdravotné metriky v reálnom čase", "description": "Monitorujte tep, spálené kalórie a intenzitu pohybu v reálnom čase."},
            "analytics": {"title": "Analytika relácií", "description": "Prezrite si celkový čas na ľade, počet striedaní, priemernú dĺžku striedania a osobné rekordy."},
            "healthIntegration": {"title": "Integrácia Apple Health", "description": "Relácie sa synchronizujú do Apple Health ako hokejové tréningy."},
            "offline": {"title": "Funguje offline", "description": "Vaše hodinky zaznamenávajú všetko nezávisle. Na striedačke nepotrebujete iPhone — dáta sa synchronizujú automaticky po zápase."}
        },
        "howItWorks": {
            "title": "Ako to funguje", "subtitle": "Od rozcvičky po analýzu po zápase",
            "step1": {"number": "1", "title": "Pred zápasom", "description": "Otvorte Ice Time Track na Apple Watch. Klepnite na Zápas, Tréning alebo Prípravný zápas."},
            "step2": {"number": "2", "title": "Počas zápasu", "description": "Vstúpte na ľad a vaše hodinky to automaticky detekujú. Zaznamenávajte góly a tresty klepnutím."},
            "step3": {"number": "3", "title": "Po zápase", "description": "Vaša relácia sa synchronizuje s iPhonom. Prezrite si čas na ľade, striedania, tep a herné udalosti."}
        },
        "screenshots": {"title": "Pozrite sa", "subtitle": "Navrhnuté pre hokejistov"},
        "testimonials": {
            "title": "Čo hovoria hráči", "subtitle": "Dôverujú nám hokejisti po celom svete",
            "review1": {"quote": "\"Konečne aplikácia, ktorá sleduje môj čas na ľade bez nutnosti čokoľvek ťukať.\"", "author": "— Hockey Dad"},
            "review2": {"quote": "\"Milujem sledovanie tepu a štatistík striedaní po každom zápase.\"", "author": "— Beer League Player"},
            "review3": {"quote": "\"Automatická detekcia je prekvapivo presná. Moje deti ju používajú každý zápas.\"", "author": "— Youth Hockey Parent"}
        },
        "download": {"title": "Pripravení sledovať čas na ľade?", "description": "Stiahnite si Ice Time Track a začnite ďalšiu reláciu. Automatická detekcia striedaní, záznam herných udalostí a zdravotné metriky — všetko z vášho zápästia.", "preOrder": "Predobjednať teraz", "downloadNow": "Stiahnuť teraz"},
        "footer": {"privacy": "Zásady ochrany osobných údajov", "terms": "Podmienky služby", "support": "Podpora", "copyright": "© 2026 MasaWata. Všetky práva vyhradené."}
    },
    "sv": {
        "appName": "Ice Time Track",
        "meta": {"title": "Ice Time Track - Automatisk skiftdetektering för Apple Watch", "description": "Spåra din istid automatiskt med Apple Watch. Upptäck skift, logga mål och utvisningar, övervaka puls och rörelse."},
        "nav": {"features": "Funktioner", "howItWorks": "Så fungerar det", "screenshots": "Skärmbilder", "faq": "FAQ", "cta": "Förbeställ", "ctaDownload": "Ladda ner"},
        "countdown": {"title": "Lansering om", "promo": "1 år för $6,99", "promoSub": "Tidsbegränsat erbjudande — missa inte", "days": "Dagar", "hours": "Timmar", "minutes": "Minuter", "seconds": "Sekunder", "date": "14 februari 2026", "claimOffer": "Lös in erbjudande", "launchSpecial": "Lanseringserbjudande", "offerEnds": "Erbjudandet slutar 28 februari 2026", "downloadNow": "Ladda ner nu"},
        "hero": {"title": "Automatisk skiftdetektering<br>för hockeyspelare", "description": "Vet exakt hur mycket istid du får — utan att trycka på din klocka. Spåra mål, utvisningar och perioder. Starta bara en session och spela.", "preOrder": "Förbeställ nu", "platforms": "Tillgänglig på Apple Watch + iPhone · Lansering 14 februari 2026", "shiftDetection": "Skiftdetektering", "goalTracking": "Målspårning", "penaltyLogging": "Utvisningslogg", "gameAnalytics": "Matchanalys"},
        "features": {
            "title": "Funktioner", "subtitle": "Allt du behöver för att spåra din match",
            "shiftDetection": {"title": "Automatisk skiftdetektering", "description": "Kliv ut på isen och din klocka vet det. Inga knappar under spel — sensorer upptäcker skridskoåkning vs. bänk automatiskt."},
            "eventTracking": {"title": "Matchhändelsespårning", "description": "Logga mål, assist och utvisningar direkt från handleden. Spåra perioder och håll en komplett historik."},
            "healthMetrics": {"title": "Hälsodata i realtid", "description": "Övervaka puls, förbrända kalorier och rörelseintensitet i realtid."},
            "analytics": {"title": "Sessionsanalys", "description": "Granska total istid, antal skift, genomsnittlig skiftlängd och personliga rekord."},
            "healthIntegration": {"title": "Apple Hälsa-integration", "description": "Sessioner synkroniseras till Apple Hälsa som hockeyträningar."},
            "offline": {"title": "Fungerar offline", "description": "Din klocka registrerar allt oberoende. Ingen iPhone behövs på bänken — data synkroniseras automatiskt efter matchen."}
        },
        "howItWorks": {
            "title": "Så fungerar det", "subtitle": "Från uppvärmning till analys efter matchen",
            "step1": {"number": "1", "title": "Före matchen", "description": "Öppna Ice Time Track på din Apple Watch. Tryck på Match, Träning eller Träningsmatch."},
            "step2": {"number": "2", "title": "Under matchen", "description": "Kliv ut på isen och din klocka upptäcker det automatiskt. Logga mål och utvisningar med ett tryck."},
            "step3": {"number": "3", "title": "Efter matchen", "description": "Din session synkroniseras med din iPhone. Granska istid, skift, puls och matchhändelser."}
        },
        "screenshots": {"title": "Se det i aktion", "subtitle": "Designat för hockeyspelare"},
        "testimonials": {
            "title": "Vad spelare säger", "subtitle": "Betrodd av hockeyspelare överallt",
            "review1": {"quote": "\"Äntligen en app som spårar min istid utan att jag behöver trycka på något. Game changer för skiftspårning.\"", "author": "— Hockey Dad"},
            "review2": {"quote": "\"Älskar att se min puls och skiftstatistik efter varje match. Hjälper mig förstå min kondition.\"", "author": "— Beer League Player"},
            "review3": {"quote": "\"Den automatiska detekteringen är förvånansvärt exakt. Mina barn använder den varje match nu.\"", "author": "— Youth Hockey Parent"}
        },
        "download": {"title": "Redo att spåra din istid?", "description": "Ladda ner Ice Time Track och starta din nästa session. Automatisk skiftdetektering, matchhändelsesloggning och hälsodata — allt från handleden.", "preOrder": "Förbeställ nu", "downloadNow": "Ladda ner nu"},
        "footer": {"privacy": "Integritetspolicy", "terms": "Användarvillkor", "support": "Support", "copyright": "© 2026 MasaWata. Alla rättigheter förbehållna."}
    },
    "zh-Hans": {
        "appName": "Ice Time Track",
        "meta": {"title": "Ice Time Track - Apple Watch自动冰球换班检测", "description": "使用Apple Watch自动追踪冰上时间。检测换班，记录进球和犯规，监测心率和运动。"},
        "nav": {"features": "功能", "howItWorks": "使用方法", "screenshots": "截图", "faq": "常见问题", "cta": "预购", "ctaDownload": "下载"},
        "countdown": {"title": "即将上线", "promo": "1年仅需$6.99", "promoSub": "限时优惠 — 不要错过", "days": "天", "hours": "时", "minutes": "分", "seconds": "秒", "date": "2026年2月14日", "claimOffer": "领取优惠", "launchSpecial": "上线特惠", "offerEnds": "优惠于2026年2月28日结束", "downloadNow": "立即下载"},
        "hero": {"title": "冰球运动员的<br>自动换班检测", "description": "无需触碰手表即可准确了解您的冰上时间。追踪进球、犯规和比赛时段。只需开始一个场次即可开始。", "preOrder": "立即预购", "platforms": "适用于Apple Watch + iPhone · 2026年2月14日上线", "shiftDetection": "换班检测", "goalTracking": "进球追踪", "penaltyLogging": "犯规记录", "gameAnalytics": "比赛分析"},
        "features": {
            "title": "功能", "subtitle": "追踪比赛所需的一切",
            "shiftDetection": {"title": "自动换班检测", "description": "踏上冰面，您的手表就会感知。比赛中无需按钮 — 传感器自动检测滑冰与休息。"},
            "eventTracking": {"title": "比赛事件追踪", "description": "直接从手腕记录进球、助攻和犯规。追踪比赛时段并保持完整的比赛记录。"},
            "healthMetrics": {"title": "实时健康数据", "description": "实时监测心率、消耗的卡路里和运动强度。"},
            "analytics": {"title": "场次分析", "description": "查看总冰上时间、换班次数、平均换班时长和个人记录。"},
            "healthIntegration": {"title": "Apple健康整合", "description": "场次作为冰球训练同步到Apple健康。"},
            "offline": {"title": "离线运行", "description": "您的手表独立记录一切。替补席上无需iPhone — 数据在比赛后自动同步。"}
        },
        "howItWorks": {
            "title": "使用方法", "subtitle": "从热身到赛后分析",
            "step1": {"number": "1", "title": "比赛前", "description": "在Apple Watch上打开Ice Time Track。点击比赛、训练或对抗赛开始。"},
            "step2": {"number": "2", "title": "比赛中", "description": "踏上冰面，手表自动检测。一键记录进球和犯规。专注比赛。"},
            "step3": {"number": "3", "title": "比赛后", "description": "场次同步到iPhone。查看冰上时间、换班、心率和比赛事件。"}
        },
        "screenshots": {"title": "查看实际效果", "subtitle": "专为冰球运动员设计"},
        "testimonials": {
            "title": "运动员怎么说", "subtitle": "全球冰球运动员的信赖之选",
            "review1": {"quote": "\"终于有一款不需要点击任何东西就能追踪冰上时间的应用。追踪换班的革命性工具。\"", "author": "— Hockey Dad"},
            "review2": {"quote": "\"喜欢在每场比赛后看到心率和换班统计。帮助我了解自己的体能状况。\"", "author": "— Beer League Player"},
            "review3": {"quote": "\"自动检测的准确性令人惊讶。我的孩子们每场比赛都在使用。\"", "author": "— Youth Hockey Parent"}
        },
        "download": {"title": "准备好追踪您的冰上时间了吗？", "description": "下载Ice Time Track并开始您的下一个场次。自动换班检测、比赛事件记录和健康数据 — 一切尽在手腕。", "preOrder": "立即预购", "downloadNow": "立即下载"},
        "footer": {"privacy": "隐私政策", "terms": "服务条款", "support": "支持", "copyright": "© 2026 MasaWata. 保留所有权利。"}
    },
    "zh-Hant": {
        "appName": "Ice Time Track",
        "meta": {"title": "Ice Time Track - Apple Watch自動冰球換班偵測", "description": "使用Apple Watch自動追蹤冰上時間。偵測換班，記錄進球和犯規，監測心率和運動。"},
        "nav": {"features": "功能", "howItWorks": "使用方法", "screenshots": "截圖", "faq": "常見問題", "cta": "預購", "ctaDownload": "下載"},
        "countdown": {"title": "即將上線", "promo": "1年僅需$6.99", "promoSub": "限時優惠 — 不要錯過", "days": "天", "hours": "時", "minutes": "分", "seconds": "秒", "date": "2026年2月14日", "claimOffer": "領取優惠", "launchSpecial": "上線特惠", "offerEnds": "優惠於2026年2月28日結束", "downloadNow": "立即下載"},
        "hero": {"title": "冰球運動員的<br>自動換班偵測", "description": "無需觸碰手錶即可準確了解您的冰上時間。追蹤進球、犯規和比賽時段。只需開始一個場次即可開始。", "preOrder": "立即預購", "platforms": "適用於Apple Watch + iPhone · 2026年2月14日上線", "shiftDetection": "換班偵測", "goalTracking": "進球追蹤", "penaltyLogging": "犯規記錄", "gameAnalytics": "比賽分析"},
        "features": {
            "title": "功能", "subtitle": "追蹤比賽所需的一切",
            "shiftDetection": {"title": "自動換班偵測", "description": "踏上冰面，您的手錶就會感知。比賽中無需按鈕 — 感測器自動偵測滑冰與休息。"},
            "eventTracking": {"title": "比賽事件追蹤", "description": "直接從手腕記錄進球、助攻和犯規。追蹤比賽時段並保持完整的比賽記錄。"},
            "healthMetrics": {"title": "即時健康數據", "description": "即時監測心率、消耗的卡路里和運動強度。"},
            "analytics": {"title": "場次分析", "description": "查看總冰上時間、換班次數、平均換班時長和個人記錄。"},
            "healthIntegration": {"title": "Apple健康整合", "description": "場次作為冰球訓練同步到Apple健康。"},
            "offline": {"title": "離線運行", "description": "您的手錶獨立記錄一切。替補席上無需iPhone — 資料在比賽後自動同步。"}
        },
        "howItWorks": {
            "title": "使用方法", "subtitle": "從熱身到賽後分析",
            "step1": {"number": "1", "title": "比賽前", "description": "在Apple Watch上打開Ice Time Track。點選比賽、練習或對抗賽開始。"},
            "step2": {"number": "2", "title": "比賽中", "description": "踏上冰面，手錶自動偵測。一鍵記錄進球和犯規。專注比賽。"},
            "step3": {"number": "3", "title": "比賽後", "description": "場次同步到iPhone。查看冰上時間、換班、心率和比賽事件。"}
        },
        "screenshots": {"title": "查看實際效果", "subtitle": "專為冰球運動員設計"},
        "testimonials": {
            "title": "運動員怎麼說", "subtitle": "全球冰球運動員的信賴之選",
            "review1": {"quote": "\"終於有一款不需要點選任何東西就能追蹤冰上時間的應用。追蹤換班的革命性工具。\"", "author": "— Hockey Dad"},
            "review2": {"quote": "\"喜歡在每場比賽後看到心率和換班統計。幫助我了解自己的體能狀況。\"", "author": "— Beer League Player"},
            "review3": {"quote": "\"自動偵測的準確性令人驚訝。我的孩子們每場比賽都在使用。\"", "author": "— Youth Hockey Parent"}
        },
        "download": {"title": "準備好追蹤您的冰上時間了嗎？", "description": "下載Ice Time Track並開始您的下一個場次。自動換班偵測、比賽事件記錄和健康數據 — 一切盡在手腕。", "preOrder": "立即預購", "downloadNow": "立即下載"},
        "footer": {"privacy": "隱私權政策", "terms": "服務條款", "support": "支援", "copyright": "© 2026 MasaWata. 保留所有權利。"}
    }
}


def main():
    # Load xcstrings
    xcstrings_path = os.path.abspath(XCSTRINGS_PATH)
    if not os.path.exists(xcstrings_path):
        print(f"Error: xcstrings file not found at {xcstrings_path}", file=sys.stderr)
        sys.exit(1)

    with open(xcstrings_path, 'r', encoding='utf-8') as f:
        xcstrings_data = json.load(f)

    os.makedirs(LOCALES_DIR, exist_ok=True)

    xcstrings_langs = ['cs', 'da', 'de', 'es', 'fi', 'fr', 'hu', 'it', 'ja', 'ko', 'nb', 'ru', 'sk', 'sv']

    for lang_code, ui_data in UI_TRANSLATIONS.items():
        # Get FAQ translations
        if lang_code in xcstrings_langs:
            faq_items = get_faq_translations(xcstrings_data, lang_code)
        else:
            # zh-Hans and zh-Hant - use UI_TRANSLATIONS FAQ if present, else use English
            faq_items = EN_TEMPLATE['faq']['items']

        # Merge: UI translations + FAQ translations
        locale_data = dict(ui_data)
        locale_data['faq'] = {
            'title': ui_data.get('faq', EN_TEMPLATE['faq']).get('title', EN_TEMPLATE['faq']['title']) if 'faq' not in ui_data else ui_data['faq']['title'] if isinstance(ui_data.get('faq'), dict) else EN_TEMPLATE['faq']['title'],
            'subtitle': ui_data.get('faq', EN_TEMPLATE['faq']).get('subtitle', EN_TEMPLATE['faq']['subtitle']) if 'faq' not in ui_data else ui_data['faq']['subtitle'] if isinstance(ui_data.get('faq'), dict) else EN_TEMPLATE['faq']['subtitle'],
            'items': faq_items
        }

        # Add faq title/subtitle from UI if not already there
        faq_titles = get_faq_section_translations(lang_code)
        if faq_titles:
            locale_data['faq']['title'] = faq_titles['title']
            locale_data['faq']['subtitle'] = faq_titles['subtitle']

        # Write locale file
        filepath = os.path.join(LOCALES_DIR, f'{lang_code}.json')
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(locale_data, f, ensure_ascii=False, indent=4)

        print(f"  Created: locales/{lang_code}.json")

    print(f"\nGenerated {len(UI_TRANSLATIONS)} locale files.")


def get_faq_section_translations(lang_code):
    """Return FAQ section title/subtitle translations."""
    faq_titles = {
        "cs": {"title": "Často kladené dotazy", "subtitle": "Vše, co potřebujete vědět o Ice Time Track"},
        "da": {"title": "Ofte stillede spørgsmål", "subtitle": "Alt hvad du behøver at vide om Ice Time Track"},
        "de": {"title": "Häufig gestellte Fragen", "subtitle": "Alles was du über Ice Time Track wissen musst"},
        "es": {"title": "Preguntas frecuentes", "subtitle": "Todo lo que necesitas saber sobre Ice Time Track"},
        "fi": {"title": "Usein kysytyt kysymykset", "subtitle": "Kaikki mitä sinun tarvitsee tietää Ice Time Trackista"},
        "fr": {"title": "Questions fréquemment posées", "subtitle": "Tout ce que vous devez savoir sur Ice Time Track"},
        "hu": {"title": "Gyakran ismételt kérdések", "subtitle": "Minden, amit az Ice Time Trackről tudni kell"},
        "it": {"title": "Domande frequenti", "subtitle": "Tutto ciò che devi sapere su Ice Time Track"},
        "ja": {"title": "よくある質問", "subtitle": "Ice Time Trackについて知っておくべきこと"},
        "ko": {"title": "자주 묻는 질문", "subtitle": "Ice Time Track에 대해 알아야 할 모든 것"},
        "nb": {"title": "Ofte stilte spørsmål", "subtitle": "Alt du trenger å vite om Ice Time Track"},
        "ru": {"title": "Часто задаваемые вопросы", "subtitle": "Всё, что нужно знать об Ice Time Track"},
        "sk": {"title": "Často kladené otázky", "subtitle": "Všetko, čo potrebujete vedieť o Ice Time Track"},
        "sv": {"title": "Vanliga frågor", "subtitle": "Allt du behöver veta om Ice Time Track"},
        "zh-Hans": {"title": "常见问题", "subtitle": "关于Ice Time Track您需要了解的一切"},
        "zh-Hant": {"title": "常見問題", "subtitle": "關於Ice Time Track您需要了解的一切"},
    }
    return faq_titles.get(lang_code)


if __name__ == '__main__':
    main()
