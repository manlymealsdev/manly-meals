#!/usr/bin/env python3
"""Generate recipe markdown + branded SVG placeholder images for Manly Meals."""
import os, json, textwrap

RECIPE_DIR = "src/content/recipes"
IMG_DIR = "public/images/recipes"
os.makedirs(RECIPE_DIR, exist_ok=True)
os.makedirs(IMG_DIR, exist_ok=True)

# Palette (matches Tailwind config)
BASE = "#161A1B"; CARD = "#2E2E2E"; ACCENT = "#BE6600"; INK = "#E7DCCF"; HEADER = "#1C2526"

def yaml_str(s):
    return json.dumps(s, ensure_ascii=False)  # safe quoting incl. unicode

def ingredients_yaml(items):
    lines = []
    for it in items:
        qty = "null" if it[0] is None else it[0]
        lines.append(f"  - {{ qty: {qty}, unit: {yaml_str(it[1])}, item: {yaml_str(it[2])} }}")
    return "\n".join(lines)

def list_yaml(items):
    return "\n".join(f"  - {yaml_str(x)}" for x in items)

def cost_yaml(items):
    return "\n".join(f"  - {{ item: {yaml_str(i)}, cost: {c} }}" for i, c in items)

def gear_yaml(items):
    return "\n".join(f"  - {{ name: {yaml_str(n)}, note: {yaml_str(note)} }}" for n, note in items)

def macros_yaml(m):
    return (f"  calories: {m[0]}\n  protein: {m[1]}\n  carbs: {m[2]}\n  fat: {m[3]}")

def write_recipe(r):
    slug = r["slug"]
    fm = []
    fm.append("---")
    fm.append(f"title: {yaml_str(r['title'])}")
    fm.append(f"description: {yaml_str(r['description'])}")
    fm.append(f"category: {yaml_str(r['category'])}")
    fm.append(f"subcategory: {yaml_str(r['subcategory'])}")
    fm.append("sections:" + ("" if not r.get("sections") else "\n" + list_yaml(r["sections"])) + ("  []" if not r.get("sections") else ""))
    fm.append("budgetFilters:" + ("  []" if not r.get("budgetFilters") else "\n" + list_yaml(r["budgetFilters"])))
    fm.append(f"image: {yaml_str('/images/recipes/' + slug + '.svg')}")
    fm.append(f"imageAlt: {yaml_str(r['title'])}")
    fm.append(f"prepTime: {r['prepTime']}")
    fm.append(f"cookTime: {r['cookTime']}")
    fm.append(f"servings: {r['servings']}")
    fm.append("macros:\n" + macros_yaml(r["macros"]))
    fm.append("ingredients:\n" + ingredients_yaml(r["ingredients"]))
    fm.append("instructions:\n" + list_yaml(r["instructions"]))
    fm.append(f"isBudget: {'true' if r.get('isBudget') else 'false'}")
    if r.get("costPerServing") is not None:
        fm.append(f"costPerServing: {r['costPerServing']}")
    fm.append("costBreakdown:" + ("  []" if not r.get("costBreakdown") else "\n" + cost_yaml(r["costBreakdown"])))
    fm.append("gear:" + ("  []" if not r.get("gear") else "\n" + gear_yaml(r["gear"])))
    fm.append(f"pubDate: {r['pubDate']}")
    fm.append(f"featured: {'true' if r.get('featured') else 'false'}")
    fm.append("---")
    fm.append("")
    with open(f"{RECIPE_DIR}/{slug}.md", "w") as f:
        f.write("\n".join(fm))

# Category accent tints for placeholder variety
TINTS = {
    "Beef": "#7A2E1E", "Chicken": "#8A6A1E", "Pork": "#7A3550",
    "Fish": "#1E4A6A", "Budget Meals": "#3E5A2E", "Meal Prep": "#3A3A55", "Low Carb": "#2E5A4A",
}

def write_svg(r):
    slug = r["slug"]; title = r["title"]; cat = r["category"]
    tint = TINTS.get(cat, ACCENT)
    # Word-wrap the title for the SVG
    words = title.upper().split()
    lines, cur = [], ""
    for w in words:
        if len(cur + " " + w) > 16:
            lines.append(cur.strip()); cur = w
        else:
            cur += " " + w
    if cur.strip(): lines.append(cur.strip())
    lines = lines[:3]
    tspans = ""
    start_y = 360 - (len(lines)-1)*34
    for i, ln in enumerate(lines):
        tspans += f'<tspan x="60" y="{start_y + i*68}">{ln}</tspan>'
    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1280 720" width="1280" height="720" role="img" aria-label="{title}">
  <defs>
    <linearGradient id="g" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0" stop-color="{HEADER}"/>
      <stop offset="0.55" stop-color="{tint}"/>
      <stop offset="1" stop-color="{BASE}"/>
    </linearGradient>
    <radialGradient id="r" cx="78%" cy="22%" r="60%">
      <stop offset="0" stop-color="{ACCENT}" stop-opacity="0.45"/>
      <stop offset="1" stop-color="{ACCENT}" stop-opacity="0"/>
    </radialGradient>
    <pattern id="dots" width="34" height="34" patternUnits="userSpaceOnUse">
      <circle cx="2" cy="2" r="1.4" fill="{INK}" opacity="0.06"/>
    </pattern>
  </defs>
  <rect width="1280" height="720" fill="url(#g)"/>
  <rect width="1280" height="720" fill="url(#dots)"/>
  <rect width="1280" height="720" fill="url(#r)"/>
  <g transform="translate(1060,120)" opacity="0.9">
    <circle r="78" fill="{ACCENT}"/>
    <g stroke="{BASE}" stroke-width="7" stroke-linecap="round" stroke-linejoin="round" fill="none" transform="translate(-22,-40)">
      <path d="M0 0 v22 a8 8 0 0 0 8 8 v40 M0 0 v18 M14 0 v18"/>
      <path d="M44 0 c-6 0 -10 8 -10 18 s4 14 8 14 v38" />
    </g>
  </g>
  <text x="60" y="120" font-family="Anton, Impact, sans-serif" font-size="30" letter-spacing="3" fill="{ACCENT}">MANLY MEALS · {cat.upper()}</text>
  <text font-family="Anton, Impact, sans-serif" font-size="76" fill="{INK}" letter-spacing="1">{tspans}</text>
  <rect x="60" y="600" width="120" height="10" rx="5" fill="{ACCENT}"/>
  <text x="60" y="660" font-family="Barlow, sans-serif" font-size="26" fill="{INK}" opacity="0.7">Simple. Cheap. Delicious.</text>
</svg>'''
    with open(f"{IMG_DIR}/{slug}.svg", "w") as f:
        f.write(svg)

# ---------------------------------------------------------------------------
print("generator ready")
