"""Prepare reproducible, self-contained HTML for the studio's raster exports.

Run with --render-dir outside the repository, then render the HTML at its declared
CSS dimensions and device scale 1 using ego-browser. No source logo is modified.
The renderer owns PNG exports; this script also refreshes the vector favicon.
"""

import argparse
import base64
from pathlib import Path
import xml.etree.ElementTree as ET


ROOT = Path(__file__).resolve().parents[1]
BRAND = ROOT / "assets/brand"


def document(title: str, width: int, height: int, css: str, content: str) -> str:
    return f'''<!doctype html>
<html lang="en"><head><meta charset="utf-8"><title>{title}</title>
<meta name="viewport" content="width={width}, initial-scale=1">
<style>
* {{ box-sizing: border-box; }}
html, body {{ margin: 0; width: {width}px; height: {height}px; overflow: hidden; }}
body {{ font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif; }}
{css}
</style></head><body>{content}</body></html>
'''


def build(render_dir: Path) -> None:
    render_dir.mkdir(parents=True, exist_ok=True)
    ET.register_namespace("", "http://www.w3.org/2000/svg")
    source = ET.parse(BRAND / "masawata-tech-mark.svg").getroot()
    paths = "\n".join(ET.tostring(path, encoding="unicode") for path in source
                      if path.tag.endswith("}path"))
    icon = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="150 100 1000 1000" role="img" aria-label="MasaWata Tech">
<rect x="150" y="100" width="1000" height="1000" rx="180" fill="#fffaf3"/>
{paths}
</svg>
'''
    (ROOT / "favicon.svg").write_text(icon, encoding="utf-8")
    # Touch icons fill the entire square; the platform supplies its own mask.
    square_icon = icon.replace(' rx="180"', '')
    for size, name, artwork in ((180, "touch-icon", square_icon), (32, "favicon-32", icon)):
        (render_dir / f"{name}.html").write_text(document(
            "MasaWata Tech icon", size, size, "svg { display: block; width: 100%; height: 100%; }", artwork,
        ), encoding="utf-8")
    encoded = base64.b64encode((BRAND / "masawata-tech-logo.png").read_bytes()).decode("ascii")
    social = document("MasaWata Tech studio share image", 1200, 630, '''
body { background: #0b3158; color: #fffaf3; padding: 52px 60px; }
.lockup { display: block; width: 1080px; height: 360px; border-radius: 24px; }
p { margin: 35px 0 18px; font-size: 36px; font-weight: 600; line-height: 1.25; letter-spacing: -.02em; }
.address { display: flex; align-items: center; gap: 16px; font-size: 24px; font-weight: 400; }
.address::before { content: ""; width: 44px; height: 5px; background: #08a097; border-radius: 3px; }
''', f'''<main class="canvas">
<img class="lockup" src="data:image/png;base64,{encoded}" width="1080" height="360" alt="MasaWata Tech">
<p>Focused apps for iPhone &amp; Apple Watch.</p>
<div class="address">masawata.net</div>
</main>''')
    (render_dir / "studio-social.html").write_text(social, encoding="utf-8")
    print(f"Prepared favicon.svg and three HTML render sources in {render_dir}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--render-dir", type=Path, required=True)
    build(parser.parse_args().render_dir.resolve())
