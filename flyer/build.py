"""Builds the sponsoring flyer for every club from template.html.

Usage: python3 build.py [slug ...]   (no slug = all clubs)
Needs Node.js with Playwright (render.js).
"""
import os
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))

# crest_shape: "round" fills the circle, "shield" sits centred on a white disc
CLUBS = [
    {
        "slug": "VfB-Schleiden-Handball",
        "club": "VfB Schleiden",
        "sport": "Handball",
        "crest": "vfb-schleiden-logo.png",
        "crest_shape": "round",
        "crest_scale": "1.015",
    },
    {
        "slug": "VfJ-Laurensberg-Fussball",
        "club": "VfJ Laurensberg",
        "sport": "Fußball",
        "crest": "vfj-laurensberg-logo.png",
        "crest_shape": "round",
        "crest_scale": "1",
    },
    {
        "slug": "ASV-Schwarz-Rot-Aachen-Handball",
        "club": "ASV Schwarz-Rot Aachen",
        "sport": "Handball",
        "crest": "asv-schwarz-rot-aachen-logo.png",
        "crest_shape": "shield",
        "crest_scale": "1",
    },
]


def build(club):
    with open(os.path.join(HERE, "template.html"), encoding="utf-8") as f:
        html = f.read()
    values = {
        "ASSETS": "../assets/",
        "CLUB": club["club"],
        "SPORT": club["sport"],
        "CREST": club["crest"],
        "CREST_SHAPE": club["crest_shape"],
        "CREST_SCALE": club["crest_scale"],
    }
    for key, value in values.items():
        html = html.replace("{{%s}}" % key, value)
    assert "{{" not in html, "unfilled placeholder in template"

    out_dir = os.path.join(HERE, club["slug"])
    os.makedirs(out_dir, exist_ok=True)
    html_path = os.path.join(out_dir, "flyer.html")
    with open(html_path, "w", encoding="utf-8") as f:
        f.write(html)

    prefix = os.path.join(out_dir, "Flyer_Sportsponsoring_" + club["slug"])
    subprocess.run(["node", os.path.join(HERE, "render.js"), html_path, prefix], check=True)
    print("built", club["slug"])


if __name__ == "__main__":
    wanted = set(sys.argv[1:])
    for club in CLUBS:
        if not wanted or club["slug"] in wanted:
            build(club)
