#!/usr/bin/env python3
"""Add 4 strong Chicken Breasts recipes with cue-rich instructions."""
import os, json
REC_DIR = "src/content/recipes"
NOTE = "**Note:** Double or quadruple this recipe for meal prep."

def q(s): return json.dumps(s, ensure_ascii=False)

def emit(r):
    L = ["---",
         f"title: {q(r['title'])}",
         f"description: {q(r['description'])}",
         f"category: \"Chicken\"",
         f"subcategory: \"Chicken Breasts\""]
    if r.get("sections"):
        L.append("sections:"); L += [f"  - {q(s)}" for s in r["sections"]]
    else:
        L.append("sections: []")
    L.append("budgetFilters: []")
    L.append(f"image: {q('/images/recipes/' + r['slug'] + '.jpg')}")
    L.append(f"imageAlt: {q('Overhead photo of ' + r['title'] + ' plated and ready to eat')}")
    L += [f"prepTime: {r['prep']}", f"cookTime: {r['cook']}", f"servings: {r['servings']}"]
    m = r["m"]
    L.append(f"macros: {{ calories: {m[0]}, protein: {m[1]}, carbs: {m[2]}, fat: {m[3]} }}")
    L.append("ingredients:")
    for qty, unit, item in r["ingredients"]:
        L.append(f"  - {{ qty: {'null' if qty is None else qty}, unit: {q(unit)}, item: {q(item)} }}")
    L.append("instructions:")
    L += [f"  - {q(s)}" for s in r["instructions"]]
    L.append("isBudget: false")
    L.append("gear:")
    L += [f"  - {{ name: {q(n)}, note: {q(note)} }}" for n, note in r["gear"]]
    L += [f"pubDate: {r['pubDate']}", f"featured: {'true' if r.get('featured') else 'false'}", "---", "", NOTE, ""]
    return "\n".join(L)

R = [
  dict(slug="juicy-pan-seared-chicken", title="Juicy Pan-Seared Chicken Breast",
       description="The foundation: a golden, juicy chicken breast that isn't dry.",
       prep=5, cook=15, servings=2, m=(360,45,2,18), featured=True,
       ingredients=[(2,"","chicken breasts"),(1,"tbsp","olive oil"),(1,"tsp","garlic powder"),
                    (1,"tsp","paprika"),(None,"","Salt & pepper, to taste")],
       instructions=[
         "Pound the breasts to an even 3/4-inch thickness so they cook evenly.",
         "Pat dry and season both sides with the garlic powder, paprika, and salt and pepper to taste.",
         "Heat the oil in a skillet over medium-high until it shimmers.",
         "Sear undisturbed 6-7 minutes until deep golden, then flip.",
         "Cook another 5-6 minutes until the center reaches 165F on a thermometer.",
         "Rest 5 minutes before slicing so the juices stay in."],
       gear=[("Skillet","Stainless or cast iron for a good sear."),
             ("Instant-Read Meat Thermometer","165F is done."),
             ("Tongs","Flip without piercing."),
             ("Chef's Knife","Slice after resting."),
             ("Cutting Board","")],
       pubDate="2026-06-07"),
  dict(slug="creamy-garlic-chicken", title="Creamy Garlic Chicken Breast",
       description="Seared chicken in a quick garlic cream sauce. Restaurant move, one pan.",
       prep=5, cook=20, servings=2, m=(520,46,6,34),
       ingredients=[(2,"","chicken breasts"),(1,"tbsp","olive oil"),(4,"","garlic cloves, minced"),
                    (1,"cup","heavy cream"),(0.25,"cup","grated parmesan"),(None,"","Salt & pepper, to taste")],
       instructions=[
         "Pat the chicken dry and season with salt and pepper to taste.",
         "Sear in the oil over medium-high 6-7 minutes per side until golden and 165F inside, then remove.",
         "Lower the heat, add the garlic, and cook 30 seconds until fragrant.",
         "Pour in the cream and simmer 3-4 minutes until it thickens enough to coat a spoon.",
         "Stir in the parmesan until melted and smooth.",
         "Return the chicken, spoon the sauce over, and serve."],
       gear=[("Skillet","One pan does it all."),
             ("Instant-Read Meat Thermometer","Check the thick end."),
             ("Tongs",""),
             ("Chef's Knife","For the garlic."),
             ("Cutting Board","")],
       pubDate="2026-06-08"),
  dict(slug="garlic-butter-chicken-bites", title="Garlic Butter Chicken Bites",
       description="Bite-size chicken seared in garlic butter. Fast, and great over rice.",
       prep=10, cook=12, servings=2, m=(420,44,3,24),
       ingredients=[(2,"","chicken breasts, cut into 1-inch cubes"),(3,"tbsp","butter"),
                    (4,"","garlic cloves, minced"),(1,"tsp","paprika"),(None,"","Salt & pepper, to taste")],
       instructions=[
         "Pat the chicken cubes dry and season with the paprika and salt and pepper to taste.",
         "Melt 1 tablespoon of the butter in a skillet over medium-high until foaming.",
         "Add the chicken in a single layer and sear 2-3 minutes without moving until browned.",
         "Toss and cook 3-4 minutes more until no longer pink and 165F inside.",
         "Lower the heat, add the rest of the butter and the garlic, and cook 1 minute until fragrant.",
         "Spoon the garlic butter over and serve."],
       gear=[("Skillet","Wide enough for a single layer."),
             ("Instant-Read Meat Thermometer",""),
             ("Chef's Knife","Cube the chicken evenly."),
             ("Cutting Board",""),
             ("Wooden Spoon","Toss the bites.")],
       pubDate="2026-06-08"),
  dict(slug="honey-mustard-chicken", title="Honey Mustard Baked Chicken Breast",
       description="Sheet-pan chicken with a sticky honey mustard glaze. Almost no cleanup.",
       prep=5, cook=25, servings=2, m=(380,44,14,14),
       ingredients=[(2,"","chicken breasts"),(2,"tbsp","Dijon mustard"),(2,"tbsp","honey"),
                    (1,"tbsp","olive oil"),(None,"","Salt & pepper, to taste")],
       instructions=[
         "Preheat the oven to 400F and line a sheet pan.",
         "Whisk the mustard, honey, and oil into a glaze.",
         "Season the chicken with salt and pepper to taste, then coat in the glaze.",
         "Bake 22-25 minutes until the center reaches 165F and the glaze is sticky.",
         "Rest 5 minutes before slicing."],
       gear=[("Sheet Pan","Line it for zero cleanup."),
             ("Instant-Read Meat Thermometer","165F internal."),
             ("Mixing Bowl","Whisk the glaze."),
             ("Chef's Knife",""),
             ("Cutting Board","")],
       pubDate="2026-06-07"),
]

for r in R:
    open(os.path.join(REC_DIR, r["slug"] + ".md"), "w").write(emit(r))
print(f"Created {len(R)} new Chicken Breasts recipes.")
