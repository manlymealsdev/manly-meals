#!/usr/bin/env python3
"""Rescale listed recipes to ~2 servings, preserve all other fields, add meal-prep note."""
import glob, json, yaml, os

REC_DIR = "src/content/recipes"
NOTE = "**Note:** Double or quadruple this recipe for meal prep."

def q(s):
    return json.dumps(s, ensure_ascii=False)

def emit(d, ingredients, instructions, gear, body):
    L = ["---",
         f"title: {q(d['title'])}",
         f"description: {q(d['description'])}",
         f"category: {q(d['category'])}",
         f"subcategory: {q(d['subcategory'])}"]
    if d.get("sections"):
        L.append("sections:"); L += [f"  - {q(s)}" for s in d["sections"]]
    else:
        L.append("sections: []")
    if d.get("budgetFilters"):
        L.append("budgetFilters:"); L += [f"  - {q(s)}" for s in d["budgetFilters"]]
    else:
        L.append("budgetFilters: []")
    L.append(f"image: {q(d['image'])}")
    L.append(f"imageAlt: {q(d['imageAlt'])}")
    L.append(f"prepTime: {d['prepTime']}")
    L.append(f"cookTime: {d['cookTime']}")
    L.append(f"servings: {d['servings']}")
    m = d["macros"]
    L.append(f"macros: {{ calories: {m['calories']}, protein: {m['protein']}, carbs: {m['carbs']}, fat: {m['fat']} }}")
    L.append("ingredients:")
    for qty, unit, item in ingredients:
        qv = "null" if qty is None else qty
        L.append(f"  - {{ qty: {qv}, unit: {q(unit)}, item: {q(item)} }}")
    L.append("instructions:")
    L += [f"  - {q(s)}" for s in instructions]
    L.append(f"isBudget: {'true' if d.get('isBudget') else 'false'}")
    if d.get("costPerServing") is not None:
        L.append(f"costPerServing: {d['costPerServing']}")
    if d.get("costBreakdown"):
        L.append("costBreakdown:")
        L += [f"  - {{ item: {q(c['item'])}, cost: {c['cost']} }}" for c in d["costBreakdown"]]
    else:
        L.append("costBreakdown: []")
    if d.get("gear"):
        L.append("gear:")
        L += [f"  - {{ name: {q(g['name'])}, note: {q(g.get('note',''))} }}" for g in gear]
    else:
        L.append("gear: []")
    L.append(f"pubDate: {d['pubDate']}")
    L.append(f"featured: {'true' if d.get('featured') else 'false'}")
    L.append("---")
    L.append("")
    L.append(body.strip())
    L.append("")
    return "\n".join(L)

# Per-recipe overrides: servings, ingredients, optional cookTime/costBreakdown
I = lambda *t: list(t)  # ingredient list helper
OV = {
  "chuck-roast": dict(servings=2, cookTime=150, ingredients=I(
        (1,"lb","chuck roast"),(0.5,"packet","onion soup mix"),
        (0.5,"can","cream of mushroom soup"),(0.33,"cup","beef broth"))),
  "crispy-chicken-breasts": dict(servings=2, ingredients=I(
        (2,"","chicken breasts"),(0.25,"cup","grated parmesan"),
        (0.5,"tsp","garlic powder"),(0.5,"tsp","paprika"),(None,"","Salt & pepper"))),
  "honey-garlic-thighs": dict(servings=2, ingredients=I(
        (4,"","bone-in chicken thighs"),(3,"tbsp","honey"),
        (2,"","garlic cloves, minced"),(1,"tbsp","soy sauce"),(None,"","Salt & pepper"))),
  "bbq-drumsticks": dict(servings=2, ingredients=I(
        (6,"","chicken drumsticks"),(0.5,"cup","BBQ sauce"),
        (0.5,"tsp","garlic powder"),(None,"","Salt & pepper"))),
  "salsa-chicken": dict(servings=2, ingredients=I(
        (2,"","chicken breasts"),(1,"cup","salsa"),
        (0.5,"tsp","cumin"),(None,"","Salt & pepper"))),
  "lemon-garlic-chicken": dict(servings=2, ingredients=I(
        (2,"","chicken breasts"),(2,"","garlic cloves, minced"),
        (0.5,"","lemon, juiced"),(1,"tbsp","olive oil"),(None,"","Salt & pepper"))),
  "crispy-chicken-thighs": dict(servings=2, ingredients=I(
        (4,"","bone-in chicken thighs"),(0.5,"tsp","garlic powder"),
        (0.5,"tsp","paprika"),(None,"","Salt & pepper"))),
  "garlic-butter-pork-chops": dict(servings=2, ingredients=I(
        (2,"","pork chops"),(2,"tbsp","butter"),
        (2,"","garlic cloves, minced"),(None,"","Salt & pepper"))),
  "lemon-pepper-salmon": dict(servings=2, ingredients=I(
        (2,"","salmon fillets"),(1,"tsp","lemon pepper seasoning"),
        (0.5,"tbsp","olive oil"))),
  "white-fish-lemon": dict(servings=2, ingredients=I(
        (2,"","white fish fillets"),(1.5,"tbsp","butter"),
        (0.5,"","lemon, juiced"),(None,"","Salt & pepper"))),
  "garlic-shrimp": dict(servings=2, ingredients=I(
        (0.75,"lb","shrimp, peeled"),(2,"","garlic cloves, minced"),
        (1.5,"tbsp","butter"),(0.5,"","lemon, juiced"))),
  "tuna-nachos": dict(servings=2, ingredients=I(
        (2,"cans","tuna, drained"),(1,"cup","shredded cheddar cheese"),
        (None,"","Tortilla chips"),(None,"","Salsa or hot sauce"))),
  "pork-cabbage-skillet": dict(servings=2, ingredients=I(
        (0.75,"lb","ground pork"),(0.5,"small head","cabbage, shredded"),
        (2,"","garlic cloves, minced"),(2,"tbsp","soy sauce"),(None,"","Salt & pepper"))),
  "bean-sausage-soup": dict(servings=2, ingredients=I(
        (0.5,"lb","smoked sausage"),(1,"can","beans"),
        (0.5,"","onion, diced"),(2,"cups","chicken broth")),
        costBreakdown=[{"item":"Smoked sausage","cost":1.0},{"item":"Beans","cost":0.5},
                       {"item":"Onion","cost":0.13},{"item":"Broth","cost":0.87}]),
  "chicken-beans": dict(servings=2, ingredients=I(
        (2,"","chicken thighs"),(1,"can","black beans"),
        (0.5,"can","diced tomatoes"),(0.5,"tsp","cumin")),
        costBreakdown=[{"item":"Chicken thighs","cost":1.5},{"item":"Black beans","cost":1.0},
                       {"item":"Tomatoes","cost":0.5}]),
  "budget-chili": dict(servings=2, ingredients=I(
        (0.5,"lb","ground beef"),(1,"can","beans"),
        (1,"can","diced tomatoes"),(1,"tbsp","chili seasoning")),
        costBreakdown=[{"item":"Ground beef","cost":1.33},{"item":"Beans","cost":0.67},
                       {"item":"Tomatoes","cost":0.33},{"item":"Seasoning","cost":0.47}]),
  "bbq-meatballs": dict(servings=2, cookTime=240, ingredients=I(
        (1,"lb","ground beef"),(0.5,"cup","BBQ sauce"),
        (1,"","egg"),(0.25,"cup","breadcrumbs"))),
  "chicken-broccoli": dict(servings=2, ingredients=I(
        (4,"","chicken thighs"),(2,"cups","broccoli florets"),
        (None,"","Garlic powder, salt, pepper"))),
  "low-carb-chili": dict(servings=2, cookTime=240, ingredients=I(
        (1,"lb","ground beef"),(1,"can","diced tomatoes"),
        (1,"tbsp","chili powder"),(0.5,"","onion, diced"))),
}

for slug, ov in OV.items():
    path = os.path.join(REC_DIR, slug + ".md")
    raw = open(path).read()
    d = yaml.safe_load(raw.split("---", 2)[1])
    d["servings"] = ov["servings"]
    if "cookTime" in ov:
        d["cookTime"] = ov["cookTime"]
    if "costBreakdown" in ov:
        d["costBreakdown"] = ov["costBreakdown"]
    out = emit(d, ov["ingredients"], d["instructions"], d.get("gear", []), NOTE)
    open(path, "w").write(out)

print(f"Rescaled {len(OV)} recipes. (pulled-pork & slow-cooker-carnitas left unchanged.)")
