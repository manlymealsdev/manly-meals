#!/usr/bin/env python3
"""Create 8 new tight-budget recipes (category Budget Meals)."""
import os, json
REC_DIR = "src/content/recipes"
NOTE = "**Note:** Double or quadruple this recipe for meal prep."
EN = "\u2013"

def q(s):
    return json.dumps(s, ensure_ascii=False)

def emit(r):
    L = ["---",
         f"title: {q(r['title'])}",
         f"description: {q(r['description'])}",
         f"category: {q('Budget Meals')}",
         f"subcategory: {q(r['filter'])}",
         "sections: []",
         "budgetFilters:",
         f"  - {q(r['filter'])}",
         f"image: {q('/images/recipes/' + r['slug'] + '.jpg')}",
         f"imageAlt: {q('Overhead photo of ' + r['title'] + ' plated and ready to eat')}",
         f"prepTime: {r['prep']}",
         f"cookTime: {r['cook']}",
         f"servings: {r['servings']}",
         f"macros: {{ calories: {r['m'][0]}, protein: {r['m'][1]}, carbs: {r['m'][2]}, fat: {r['m'][3]} }}",
         "ingredients:"]
    for qty, unit, item in r["ingredients"]:
        qv = "null" if qty is None else qty
        L.append(f"  - {{ qty: {qv}, unit: {q(unit)}, item: {q(item)} }}")
    L.append("instructions:")
    L += [f"  - {q(s)}" for s in r["instructions"]]
    L.append("isBudget: true")
    if r.get("gear"):
        L.append("gear:")
        L += [f"  - {{ name: {q(n)}, note: {q(note)} }}" for n, note in r["gear"]]
    else:
        L.append("gear: []")
    L.append(f"pubDate: {r['pubDate']}")
    L.append(f"featured: {'true' if r.get('featured') else 'false'}")
    L += ["---", "", NOTE, ""]
    return "\n".join(L)

R = [
  dict(slug="sloppy-joes", title="Sloppy Joes with Sesame Buns", filter="Ground & Cheap",
       description="Saucy ground beef piled on toasted sesame buns. Cheap, messy, and filling.",
       prep=5, cook=15, servings=2, m=(620,30,45,34),
       ingredients=[(0.75,"lb","ground beef"),(0.5,"cup","ketchup"),(1,"tbsp","brown sugar"),
                    (1,"tbsp","mustard"),(2,"","sesame buns"),(None,"","Salt & pepper")],
       instructions=["Brown the ground beef in a skillet and drain the fat.",
                     "Stir in the ketchup, brown sugar, and mustard.",
                     "Simmer 5 minutes until thick.",
                     "Toast the sesame buns.",
                     "Pile the beef on the buns and serve."],
       gear=[("Skillet","")], pubDate="2026-06-01", featured=True),
  dict(slug="cheesy-rice-beans", title="Cheesy Rice and Beans", filter="Pantry Staples",
       description="Pantry-cheap, calorie-dense, and ready in fifteen minutes.",
       prep=5, cook=15, servings=2, m=(560,22,78,16),
       ingredients=[(1,"cup","rice"),(1,"can","black beans, drained"),
                    (1,"cup","shredded cheddar cheese"),(0.5,"tsp","cumin"),(None,"","Salt & pepper")],
       instructions=["Cook the rice.",
                     "Stir in the black beans and cumin, and heat through.",
                     "Melt in the shredded cheddar.",
                     "Season with salt and pepper and serve."],
       gear=[("Pot","")], pubDate="2026-05-31"),
  dict(slug="beef-bolognese", title="Simple Beef Bolognese", filter="Ground & Cheap",
       description="Beef, pasta, and a jar of sauce. The cheapest hearty pasta there is.",
       prep=5, cook=20, servings=2, m=(700,34,80,26),
       ingredients=[(0.5,"lb","ground beef"),(8,"oz","pasta"),(1,"jar (15oz)","pizza sauce"),
                    (0.25,"cup","milk"),(None,"","Salt")],
       instructions=["Boil the pasta until tender, then drain.",
                     "Brown the ground beef in a skillet and drain.",
                     "Add the pizza sauce and milk, then simmer 10 minutes.",
                     "Salt to taste and toss with the pasta."],
       gear=[("Pot",""),("Skillet","")], pubDate="2026-05-30"),
  dict(slug="breakfast-burritos", title="Breakfast Burritos", filter="Pantry Staples",
       description="Eggs, hash browns, and hot sauce wrapped up cheap for any meal of the day.",
       prep=5, cook=15, servings=2, m=(560,24,48,30),
       ingredients=[(2,"","large flour tortillas"),(4,"","eggs"),(1,"cup","frozen hash browns"),
                    (None,"","Salsa or hot sauce"),(None,"","Salt & pepper")],
       instructions=["Crisp the hash browns in a skillet.",
                     "Scramble the eggs and season.",
                     "Warm the tortillas.",
                     "Fill each with hash browns, eggs, and hot sauce.",
                     "Roll tight and serve."],
       gear=[("Skillet","")], pubDate="2026-05-29"),
  dict(slug="tuna-casserole", title="Easy Tuna Casserole", filter="Big Batch",
       description="Canned tuna, pasta, and cheese baked into a cheap, filling casserole.",
       prep=10, cook=25, servings=2, m=(520,30,42,22),
       ingredients=[(4,"oz","egg noodles"),(1,"can","tuna, drained"),
                    (0.5,"can","cream of mushroom soup"),(0.5,"cup","shredded cheddar cheese"),
                    (0.25,"cup","milk")],
       instructions=["Boil the egg noodles and drain.",
                     "Mix the tuna, soup, and milk.",
                     "Combine with the noodles in a baking dish.",
                     "Top with cheddar.",
                     "Bake at 375F for 20 minutes until bubbly."],
       gear=[("Baking Dish","")], pubDate="2026-05-28"),
  dict(slug="fried-egg-rice", title="Fried Eggs, Rice, Soy Sauce & Hot Sauce", filter="Pantry Staples",
       description="Three fried eggs over rice with soy and hot sauce. Pennies a plate.",
       prep=2, cook=8, servings=2, m=(480,20,56,18),
       ingredients=[(1.5,"cups","cooked rice"),(3,"","eggs"),(2,"tbsp","soy sauce"),
                    (None,"","Hot sauce"),(1,"tbsp","oil")],
       instructions=["Heat the rice and divide between two bowls.",
                     "Fry the eggs in the oil to your liking.",
                     "Set the eggs on the rice.",
                     "Hit with soy sauce and hot sauce and serve."],
       gear=[("Skillet","")], pubDate="2026-05-27"),
  dict(slug="hot-dogs-kraut", title="Classic Hot Dogs with Kraut", filter=f"$5{EN}$10 Meals",
       description="Dogs, buns, and a pile of sauerkraut. About as cheap as dinner gets.",
       prep=2, cook=8, servings=2, m=(520,18,40,32),
       ingredients=[(4,"","hot dogs"),(4,"","hot dog buns"),(1,"cup","sauerkraut"),(None,"","Mustard")],
       instructions=["Heat the hot dogs in a pan or boiling water for 5-7 minutes.",
                     "Warm the buns.",
                     "Load each with a dog, sauerkraut, and mustard.",
                     "Serve hot."],
       gear=[("Skillet or Pot","")], pubDate="2026-05-26"),
  dict(slug="hot-dog-mac", title="Hot Dog Mac and Cheese", filter="Big Batch",
       description="Boxed mac stretched with sliced hot dogs. Cheap, hot, and filling.",
       prep=5, cook=15, servings=2, m=(640,22,72,30),
       ingredients=[(1,"box","macaroni and cheese"),(3,"","hot dogs, sliced"),
                    (2,"tbsp","butter"),(0.25,"cup","milk")],
       instructions=["Boil and drain the macaroni.",
                     "Stir in the butter, milk, and cheese packet.",
                     "Fold in the sliced hot dogs.",
                     "Heat through and serve."],
       gear=[("Pot","")], pubDate="2026-05-25"),
]

for r in R:
    open(os.path.join(REC_DIR, r["slug"] + ".md"), "w").write(emit(r))
print(f"Created {len(R)} new budget recipes.")
