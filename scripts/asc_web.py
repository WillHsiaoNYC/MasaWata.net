"""Shared helpers for ASC-backed localized MasaWata product pages."""

from __future__ import annotations

import html
import json
from datetime import date
from pathlib import Path


LOCALE_INFO = {
    "ar-SA": ("ar-SA", "العربية", True),
    "ca": ("ca", "Català", False),
    "cs": ("cs", "Čeština", False),
    "da": ("da", "Dansk", False),
    "de-DE": ("de-DE", "Deutsch", False),
    "el": ("el", "Ελληνικά", False),
    "en-US": ("en-US", "English", False),
    "es-ES": ("es-ES", "Español (España)", False),
    "es-MX": ("es-MX", "Español (México)", False),
    "fi": ("fi", "Suomi", False),
    "fr-FR": ("fr-FR", "Français", False),
    "he": ("he", "עברית", True),
    "hi": ("hi", "हिन्दी", False),
    "hr": ("hr", "Hrvatski", False),
    "hu": ("hu", "Magyar", False),
    "id": ("id", "Bahasa Indonesia", False),
    "it": ("it", "Italiano", False),
    "ja": ("ja", "日本語", False),
    "ko": ("ko", "한국어", False),
    "nl-NL": ("nl-NL", "Nederlands", False),
    "no": ("no", "Norsk", False),
    "pl": ("pl", "Polski", False),
    "pt-BR": ("pt-BR", "Português (Brasil)", False),
    "pt-PT": ("pt-PT", "Português (Portugal)", False),
    "ro": ("ro", "Română", False),
    "ru": ("ru", "Русский", False),
    "sk": ("sk", "Slovenčina", False),
    "sl-SI": ("sl-SI", "Slovenščina", False),
    "sv": ("sv", "Svenska", False),
    "th": ("th", "ไทย", False),
    "tr": ("tr", "Türkçe", False),
    "uk": ("uk", "Українська", False),
    "vi": ("vi", "Tiếng Việt", False),
    "zh-Hans": ("zh-Hans", "简体中文", False),
    "zh-Hant": ("zh-Hant", "繁體中文", False),
}


UI = {
    "ar-SA": ("حول التطبيق", "لقطات الشاشة", "تنزيل من App Store", "سياسة الخصوصية", "شروط الخدمة", "الدعم", "اللغة"),
    "ca": ("Sobre l’app", "Captures de pantalla", "Descarrega a l’App Store", "Política de privadesa", "Condicions del servei", "Assistència", "Idioma"),
    "cs": ("O aplikaci", "Snímky obrazovky", "Stáhnout v App Storu", "Zásady ochrany soukromí", "Podmínky služby", "Podpora", "Jazyk"),
    "da": ("Om appen", "Skærmbilleder", "Hent i App Store", "Privatlivspolitik", "Servicevilkår", "Support", "Sprog"),
    "de-DE": ("Über die App", "Screenshots", "Im App Store laden", "Datenschutzrichtlinie", "Nutzungsbedingungen", "Support", "Sprache"),
    "el": ("Σχετικά με την εφαρμογή", "Στιγμιότυπα οθόνης", "Λήψη από το App Store", "Πολιτική απορρήτου", "Όροι χρήσης", "Υποστήριξη", "Γλώσσα"),
    "en-US": ("About the app", "Screenshots", "Download on the App Store", "Privacy Policy", "Terms of Service", "Support", "Language"),
    "es-ES": ("Acerca de la app", "Capturas de pantalla", "Descargar en App Store", "Política de privacidad", "Términos del servicio", "Soporte", "Idioma"),
    "es-MX": ("Acerca de la app", "Capturas de pantalla", "Descargar en App Store", "Política de privacidad", "Términos del servicio", "Soporte", "Idioma"),
    "fi": ("Tietoja apista", "Näyttökuvat", "Lataa App Storesta", "Tietosuojakäytäntö", "Käyttöehdot", "Tuki", "Kieli"),
    "fr-FR": ("À propos de l’app", "Captures d’écran", "Télécharger dans l’App Store", "Politique de confidentialité", "Conditions d’utilisation", "Assistance", "Langue"),
    "he": ("על האפליקציה", "צילומי מסך", "הורדה מה-App Store", "מדיניות פרטיות", "תנאי שירות", "תמיכה", "שפה"),
    "hi": ("ऐप के बारे में", "स्क्रीनशॉट", "App Store से डाउनलोड करें", "गोपनीयता नीति", "सेवा की शर्तें", "सहायता", "भाषा"),
    "hr": ("O aplikaciji", "Snimke zaslona", "Preuzmi na App Storeu", "Pravila privatnosti", "Uvjeti pružanja usluge", "Podrška", "Jezik"),
    "hu": ("Az alkalmazásról", "Képernyőképek", "Letöltés az App Store-ból", "Adatvédelmi irányelvek", "Szolgáltatási feltételek", "Támogatás", "Nyelv"),
    "id": ("Tentang aplikasi", "Tangkapan layar", "Unduh di App Store", "Kebijakan Privasi", "Ketentuan Layanan", "Dukungan", "Bahasa"),
    "it": ("Informazioni sull’app", "Screenshot", "Scarica dall’App Store", "Informativa sulla privacy", "Termini di servizio", "Assistenza", "Lingua"),
    "ja": ("アプリについて", "スクリーンショット", "App Storeからダウンロード", "プライバシーポリシー", "利用規約", "サポート", "言語"),
    "ko": ("앱 정보", "스크린샷", "App Store에서 다운로드", "개인정보 처리방침", "서비스 약관", "지원", "언어"),
    "nl-NL": ("Over de app", "Schermafbeeldingen", "Download in de App Store", "Privacybeleid", "Servicevoorwaarden", "Ondersteuning", "Taal"),
    "no": ("Om appen", "Skjermbilder", "Last ned i App Store", "Personvernerklæring", "Tjenestevilkår", "Kundestøtte", "Språk"),
    "pl": ("O aplikacji", "Zrzuty ekranu", "Pobierz w App Store", "Polityka prywatności", "Warunki korzystania z usługi", "Wsparcie", "Język"),
    "pt-BR": ("Sobre o app", "Capturas de tela", "Baixar na App Store", "Política de Privacidade", "Termos de Serviço", "Suporte", "Idioma"),
    "pt-PT": ("Sobre a app", "Capturas de ecrã", "Descarregar na App Store", "Política de Privacidade", "Termos de Serviço", "Suporte", "Idioma"),
    "ro": ("Despre aplicație", "Capturi de ecran", "Descarcă din App Store", "Politica de confidențialitate", "Termeni și condiții", "Asistență", "Limbă"),
    "ru": ("О приложении", "Снимки экрана", "Загрузить из App Store", "Политика конфиденциальности", "Условия использования", "Поддержка", "Язык"),
    "sk": ("O aplikácii", "Snímky obrazovky", "Stiahnuť v App Store", "Zásady ochrany osobných údajov", "Podmienky používania", "Podpora", "Jazyk"),
    "sl-SI": ("O aplikaciji", "Posnetki zaslona", "Prenesi iz trgovine App Store", "Pravilnik o zasebnosti", "Pogoji uporabe", "Podpora", "Jezik"),
    "sv": ("Om appen", "Skärmavbilder", "Hämta i App Store", "Integritetspolicy", "Användarvillkor", "Support", "Språk"),
    "th": ("เกี่ยวกับแอป", "ภาพหน้าจอ", "ดาวน์โหลดจาก App Store", "นโยบายความเป็นส่วนตัว", "ข้อกำหนดการให้บริการ", "ความช่วยเหลือ", "ภาษา"),
    "tr": ("Uygulama hakkında", "Ekran görüntüleri", "App Store’dan indir", "Gizlilik Politikası", "Hizmet Koşulları", "Destek", "Dil"),
    "uk": ("Про застосунок", "Знімки екрана", "Завантажити з App Store", "Політика конфіденційності", "Умови надання послуг", "Підтримка", "Мова"),
    "vi": ("Giới thiệu ứng dụng", "Ảnh chụp màn hình", "Tải xuống từ App Store", "Chính sách quyền riêng tư", "Điều khoản dịch vụ", "Hỗ trợ", "Ngôn ngữ"),
    "zh-Hans": ("关于本应用", "屏幕截图", "从 App Store 下载", "隐私政策", "服务条款", "支持", "语言"),
    "zh-Hant": ("關於此 App", "螢幕快照", "從 App Store 下載", "隱私權政策", "服務條款", "支援", "語言"),
}


def load_metadata(site_dir: Path) -> dict:
    return json.loads((site_dir / "asc-metadata.json").read_text(encoding="utf-8"))


def locale_url(base_url: str, locale: str) -> str:
    return f"{base_url}/" if locale == "en-US" else f"{base_url}/{locale}/"


def screenshot_files(site_dir: Path, locale: str) -> list[Path]:
    return sorted((site_dir / "images" / "asc" / locale).glob("*.webp"))


def _description_html(text: str) -> str:
    lines = text.replace("\r\n", "\n").splitlines()
    blocks: list[str] = []
    paragraph: list[str] = []
    bullets: list[str] = []

    def flush_paragraph() -> None:
        if paragraph:
            blocks.append(f"<p>{html.escape(' '.join(paragraph))}</p>")
            paragraph.clear()

    def flush_bullets() -> None:
        if bullets:
            blocks.append("<ul>" + "".join(f"<li>{html.escape(x)}</li>" for x in bullets) + "</ul>")
            bullets.clear()

    for raw in lines:
        line = raw.strip()
        if not line:
            flush_paragraph()
            flush_bullets()
            continue
        if line.startswith(("•", "·", "- ")):
            flush_paragraph()
            bullets.append(line.lstrip("•·- ").strip())
            continue
        cased = [ch for ch in line if ch.isalpha() and ch.lower() != ch.upper()]
        sentence_punctuation = (".", "!", "?", "。", "！", "？")
        uppercase_heading = (
            bool(cased)
            and all(ch == ch.upper() for ch in cased)
            and not any(mark in line for mark in sentence_punctuation)
        )
        uncased_heading = (
            not cased
            and any(ch.isalpha() for ch in line)
            and len(line) <= 40
            and not any(mark in line for mark in sentence_punctuation)
            and not line.endswith((":", "："))
        )
        if len(line) <= 80 and (uppercase_heading or uncased_heading):
            flush_paragraph()
            flush_bullets()
            blocks.append(f"<h3>{html.escape(line)}</h3>")
            continue
        flush_bullets()
        paragraph.append(line)
    flush_paragraph()
    flush_bullets()
    return "\n".join(blocks)


def render_asc_page(
    *,
    site_dir: Path,
    locale: str,
    metadata: dict,
    base_url: str,
    app_store_id: str,
    icon_path: str,
    privacy_url: str,
    support_url: str,
    accent: str,
    accent_dark: str,
    background: str = "#ffffff",
    surface: str = "#f4f7fb",
    ink: str = "#132033",
    muted: str = "#59687c",
    line: str = "#dce4ef",
    color_scheme: str = "light",
) -> str:
    item = metadata["locales"][locale]
    html_lang, native_name, rtl = LOCALE_INFO[locale]
    about, shots_label, download, privacy, terms, support, language = UI[locale]
    canonical = locale_url(base_url, locale)
    app_url = f"https://apps.apple.com/app/id{app_store_id}"
    title = item.get("name") or metadata["appName"]
    subtitle = item.get("subtitle") or title
    promo = item.get("promotionalText") or item.get("description", "").split("\n\n", 1)[0]
    description = item.get("description") or promo
    shots = screenshot_files(site_dir, locale)
    shot_urls = [f"{base_url}/images/asc/{locale}/{p.name}" for p in shots]
    app_prefix = "" if locale == "en-US" else "../"
    global_prefix = "../" if locale == "en-US" else "../../"
    relative_shots = [f"{app_prefix}images/asc/{locale}/{p.name}" for p in shots]
    alternates = "\n".join(
        f'  <link rel="alternate" hreflang="{LOCALE_INFO[code][0]}" href="{locale_url(base_url, code)}">'
        for code in metadata["locales"]
    )
    language_links = "\n".join(
        f'<a href="{(("./" if code == "en-US" else f"{code}/") if locale == "en-US" else ("../" if code == "en-US" else f"../{code}/"))}" lang="{LOCALE_INFO[code][0]}">{html.escape(LOCALE_INFO[code][1])}</a>'
        for code in metadata["locales"]
    )
    gallery = "\n".join(
        f'<figure><img src="{src}" alt="{html.escape(title)} — {shots_label} {i}" loading="lazy"></figure>'
        for i, src in enumerate(relative_shots, 1)
    )
    schema = json.dumps(
        {
            "@context": "https://schema.org",
            "@type": "SoftwareApplication",
            "name": title,
            "description": promo,
            "applicationCategory": "UtilitiesApplication",
            "operatingSystem": "iOS, iPadOS, watchOS",
            "url": canonical,
            "downloadUrl": app_url,
            "image": shot_urls,
        },
        ensure_ascii=False,
    ).replace("</", "<\\/")
    direction = "rtl" if rtl else "ltr"
    return f'''<!doctype html>
<html lang="{html_lang}" dir="{direction}">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{html.escape(title)} — {html.escape(subtitle)}</title>
  <meta name="description" content="{html.escape(promo, quote=True)}">
  <meta name="apple-itunes-app" content="app-id={app_store_id}">
  <link rel="canonical" href="{canonical}">
{alternates}
  <link rel="alternate" hreflang="x-default" href="{base_url}/">
  <link rel="stylesheet" href="{global_prefix}includes/asc-localized.css">
  <style>:root{{color-scheme:{color_scheme};--accent:{accent};--accent-dark:{accent_dark};--bg:{background};--surface:{surface};--ink:{ink};--muted:{muted};--line:{line}}}</style>
  <script type="application/ld+json">{schema}</script>
</head>
<body>
  <header class="asc-header">
    <a class="asc-brand" href="{('./' if locale == 'en-US' else '../')}"><img src="{app_prefix}{icon_path}" alt="" width="44" height="44"><span>{html.escape(title)}</span></a>
    <details class="asc-languages">
      <summary>{html.escape(language)}: {html.escape(native_name)}</summary>
      <nav>{language_links}</nav>
    </details>
  </header>
  <main>
    <section class="asc-hero">
      <div class="asc-hero-copy">
        <p class="asc-eyebrow">{html.escape(title)}</p>
        <h1>{html.escape(subtitle)}</h1>
        <p>{html.escape(promo)}</p>
        <a class="asc-button" href="{app_url}" rel="noopener">{html.escape(download)}</a>
      </div>
      {f'<img class="asc-hero-shot" src="{relative_shots[0]}" alt="{html.escape(title)}">' if relative_shots else ''}
    </section>
    <section class="asc-content" id="about">
      <h2>{html.escape(about)}</h2>
      <div class="asc-prose">{_description_html(description)}</div>
    </section>
    <section class="asc-screens" id="screenshots">
      <h2>{html.escape(shots_label)}</h2>
      <div class="asc-gallery">{gallery}</div>
    </section>
    <section class="asc-download">
      <h2>{html.escape(title)}</h2>
      <p>{html.escape(promo)}</p>
      <a class="asc-button" href="{app_url}" rel="noopener">{html.escape(download)}</a>
    </section>
  </main>
  <footer>
    <a href="{privacy_url}">{html.escape(privacy)}</a>
    <a href="https://www.apple.com/legal/internet-services/itunes/dev/stdeula/">{html.escape(terms)}</a>
    <a href="{support_url}">{html.escape(support)}</a>
  </footer>
</body>
</html>
'''


def render_redirect(target: str) -> str:
    safe = html.escape(target, quote=True)
    return f'''<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="robots" content="noindex">
<meta http-equiv="refresh" content="0; url={safe}"><link rel="canonical" href="{safe}">
<title>Redirecting…</title></head><body><p><a href="{safe}">Continue</a></p></body></html>
'''


def build_site(
    *,
    site_dir: Path,
    base_url: str,
    app_store_id: str,
    icon_path: str,
    privacy_url: str,
    support_url: str,
    accent: str,
    accent_dark: str,
    aliases: dict[str, str] | None = None,
    background: str = "#ffffff",
    surface: str = "#f4f7fb",
    ink: str = "#132033",
    muted: str = "#59687c",
    line: str = "#dce4ef",
    color_scheme: str = "light",
) -> int:
    metadata = load_metadata(site_dir)
    locales = metadata.get("locales", {})
    if "en-US" not in locales:
        raise RuntimeError(f"{site_dir.name}: live ASC snapshot has no en-US locale")
    for locale in locales:
        target = site_dir / "index.html" if locale == "en-US" else site_dir / locale / "index.html"
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(
            render_asc_page(
                site_dir=site_dir,
                locale=locale,
                metadata=metadata,
                base_url=base_url,
                app_store_id=app_store_id,
                icon_path=icon_path,
                privacy_url=privacy_url,
                support_url=support_url,
                accent=accent,
                accent_dark=accent_dark,
                background=background,
                surface=surface,
                ink=ink,
                muted=muted,
                line=line,
                color_scheme=color_scheme,
            ),
            encoding="utf-8",
        )
        print(f"  Created: {target.relative_to(site_dir)} ({locale})")

    for legacy, locale in (aliases or {}).items():
        if locale not in locales:
            raise RuntimeError(f"{site_dir.name}: redirect target {locale} is not in ASC")
        target = site_dir / legacy / "index.html"
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(render_redirect(locale_url(base_url, locale)), encoding="utf-8")
        print(f"  Redirect: {legacy}/ → {locale}/")

    today = date.today().isoformat()
    lines = [
        '<?xml version="1.0" encoding="UTF-8"?>',
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9"',
        '        xmlns:xhtml="http://www.w3.org/1999/xhtml">',
    ]
    for locale in locales:
        url = locale_url(base_url, locale)
        lines.extend(
            [
                "  <url>",
                f"    <loc>{url}</loc>",
                f"    <lastmod>{today}</lastmod>",
                f"    <priority>{'1.0' if locale == 'en-US' else '0.9'}</priority>",
            ]
        )
        for alternate in locales:
            lines.append(
                f'    <xhtml:link rel="alternate" hreflang="{alternate}" href="{locale_url(base_url, alternate)}"/>'
            )
        lines.append(
            f'    <xhtml:link rel="alternate" hreflang="x-default" href="{base_url}/"/>'
        )
        lines.append("  </url>")
    lines.append("</urlset>")
    (site_dir / "sitemap.xml").write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"\nBuilt {len(locales)} ASC-aligned pages + sitemap.xml")
    return len(locales)
