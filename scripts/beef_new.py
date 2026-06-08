#!/usr/bin/env python3
"""Add new Beef recipes: 4 Ground Beef + 1 Steaks & Grills (keeps that subcat populated)."""
import os, json
REC_DIR = "src/content/recipes"
NOTE = "**Note:** Double or quadruple this recipe for meal prep."

def q(s):
    return json.dumps(s, ensure_ascii=False)

def emit(r):
    L = ["---",
         f"title: {q(r['title'])}",
         f"description: {q(r['description'])}",
         f"category: \"Beef\"",
         f"subcategory: {q(r['subcategory'])}"]
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
    L.append(f"isBudget: {'true' if r.get('isBudget') else 'false'}")
    L.append("gear:")
    L += [f"  - {{ name: {q(n)}, note: {q(note)} }}" for n, note in r["gear"]]
    L += [f"pubDate: {r['pubDate']}", f"featured: {'true' if r.get('featured') else 'false'}", "---", "", NOTE, ""]
    return "\n".join(L)

R = [
  dict(slug="salisbury-steak", title="Salisbury Steak with Gravy", subcategory="Ground Beef",
       description="Beefy patties smothered in quick onion gravy. Diner comfort food, fast.",
       prep=10, cook=20, servings=2, m=(580,34,18,40),
       ingredients=[(0.75,"lb","ground beef"),(0.25,"cup","breadcrumbs"),(1,"","egg"),
                    (0.5,"","onion, sliced"),(1,"tbsp","flour"),(1,"cup","beef broth"),(None,"","Salt & pepper")],
       instructions=["Mix the beef, breadcrumbs, egg, salt, and pepper, then form 2 patties.",
                     "Sear the patties 3-4 minutes per side, then remove.",
                     "Cook the onion in the same pan until soft.",
                     "Stir in the flour, then the broth, and simmer into a gravy.",
                     "Return the patties and simmer 5 minutes. Serve."],
       gear=[("Skillet","")], pubDate="2026-06-02", featured=True),
  dict(slug="ground-beef-stir-fry", title="Ground Beef Stir-Fry", subcategory="Ground Beef",
       description="Beef, frozen veg, and soy over rice. Faster than takeout and half the price.",
       prep=5, cook=15, servings=2, m=(560,30,45,28),
       ingredients=[(0.75,"lb","ground beef"),(2,"cups","frozen stir-fry vegetables"),
                    (3,"","garlic cloves, minced"),(3,"tbsp","soy sauce"),(1.5,"cups","cooked rice")],
       instructions=["Brown the ground beef in a large skillet and drain.",
                     "Add the garlic and cook 30 seconds.",
                     "Add the frozen vegetables and cook 5 minutes.",
                     "Stir in the soy sauce.",
                     "Serve over rice."],
       gear=[("Large Skillet or Wok","")], pubDate="2026-06-03"),
  dict(slug="cheeseburger-pasta", title="One-Pan Cheeseburger Pasta", subcategory="Ground Beef",
       description="Cheeseburger flavor in one skillet of pasta. Hamburger Helper, done right.",
       prep=5, cook=20, servings=2, m=(680,36,62,32),
       ingredients=[(0.75,"lb","ground beef"),(6,"oz","pasta"),(1,"cup","beef broth"),
                    (0.5,"cup","milk"),(1,"cup","shredded cheddar cheese"),(None,"","Salt & pepper")],
       instructions=["Brown the ground beef in a deep skillet and drain.",
                     "Add the pasta, broth, and milk.",
                     "Simmer covered about 12 minutes until the pasta is tender.",
                     "Stir in the cheddar and season.",
                     "Serve hot."],
       gear=[("Deep Skillet","")], pubDate="2026-06-04"),
  dict(slug="beef-pepper-skillet", title="Beef & Pepper Skillet", subcategory="Ground Beef",
       description="Ground beef, peppers, and onion in one pan. Pile it on rice or in a tortilla.",
       prep=10, cook=15, servings=2, m=(480,30,16,32),
       ingredients=[(0.75,"lb","ground beef"),(2,"","bell peppers, sliced"),(0.5,"","onion, sliced"),
                    (2,"","garlic cloves, minced"),(1,"tsp","paprika"),(None,"","Salt & pepper")],
       instructions=["Brown the ground beef in a large skillet and drain.",
                     "Add the onion and peppers, cooking 6-8 minutes until soft.",
                     "Add the garlic and paprika, cooking 1 minute.",
                     "Season and serve."],
       gear=[("Large Skillet","")], pubDate="2026-06-05"),
  # Keeps Steaks & Grills populated after smashburgers moves out
  dict(slug="pan-seared-ribeye", title="Pan-Seared Ribeye", subcategory="Steaks & Grills",
       description="A great steak needs almost nothing: high heat, salt, and butter.",
       sections=["Low Carb"],
       prep=5, cook=10, servings=2, m=(640,46,0,50),
       ingredients=[(2,"","ribeye steaks"),(1,"tbsp","oil"),(2,"tbsp","butter"),
                    (2,"","garlic cloves, smashed"),(None,"","Coarse salt"),(None,"","Black pepper")],
       instructions=["Pat the steaks dry and season hard with salt and pepper.",
                     "Sear in oil over high heat 3-4 minutes per side.",
                     "Add the butter and garlic, basting for 1 minute.",
                     "Rest 5 minutes before slicing."],
       gear=[("Cast Iron Skillet","High heat is everything."),("Meat Thermometer","130F for medium-rare.")],
       pubDate="2026-06-06"),
]

for r in R:
    open(os.path.join(REC_DIR, r["slug"] + ".md"), "w").write(emit(r))
print(f"Created {len(R)} new beef recipes.")
