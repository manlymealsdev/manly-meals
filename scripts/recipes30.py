#!/usr/bin/env python3
"""Generate 30 schema-valid recipe .md files + branded JPG placeholder images."""
import os, json, textwrap
from PIL import Image, ImageDraw, ImageFont

RECIPE_DIR = "src/content/recipes"
IMG_DIR = "public/images/recipes"
os.makedirs(RECIPE_DIR, exist_ok=True)
os.makedirs(IMG_DIR, exist_ok=True)

BASE = (22, 26, 27)
CARD = (46, 46, 46)
ACCENT = (190, 102, 0)
INK = (231, 220, 207)
MUTED = (154, 149, 140)
HEADER = (28, 37, 38)

FONT_BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
FONT_REG = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"

CAT_TINT = {
    "Beef": (150, 60, 40), "Chicken": (180, 130, 60), "Pork": (170, 90, 90),
    "Fish": (60, 110, 130), "Budget Meals": (90, 120, 70),
    "Meal Prep": (110, 90, 140), "Low Carb": (70, 130, 110),
}

def q(s):  # safe YAML string
    return json.dumps(s, ensure_ascii=False)

def make_image(slug, title, category):
    W, H = 1280, 720
    img = Image.new("RGB", (W, H), BASE)
    d = ImageDraw.Draw(img)
    tint = CAT_TINT.get(category, ACCENT)
    # diagonal tint wash top-left
    for i in range(0, H, 2):
        a = max(0, 0.18 - i / H * 0.18)
        d.line([(0, i), (W, i)], fill=(
            int(BASE[0] + (tint[0] - BASE[0]) * a),
            int(BASE[1] + (tint[1] - BASE[1]) * a),
            int(BASE[2] + (tint[2] - BASE[2]) * a)), width=2)
    # corner glow
    d.ellipse([W - 360, -200, W + 200, 360], fill=(
        int(BASE[0] + (ACCENT[0] - BASE[0]) * 0.10),
        int(BASE[1] + (ACCENT[1] - BASE[1]) * 0.10),
        int(BASE[2] + (ACCENT[2] - BASE[2]) * 0.10)))
    # accent bar
    d.rectangle([90, 250, 130, 470], fill=ACCENT)
    # category eyebrow
    f_eye = ImageFont.truetype(FONT_BOLD, 34)
    d.text((160, 250), category.upper(), font=f_eye, fill=ACCENT)
    # title wrapped
    f_title = ImageFont.truetype(FONT_BOLD, 78)
    lines = textwrap.wrap(title.upper(), width=18)[:3]
    y = 300
    for ln in lines:
        d.text((158, y), ln, font=f_title, fill=INK)
        y += 86
    # wordmark + placeholder note
    f_small = ImageFont.truetype(FONT_BOLD, 30)
    d.text((160, H - 80), "MANLY MEALS", font=f_small, fill=INK)
    f_note = ImageFont.truetype(FONT_REG, 24)
    d.text((160, H - 44), "placeholder image — swap with a real photo", font=f_note, fill=MUTED)
    # fork/knife motif
    d.line([(W - 150, 470), (W - 150, 560)], fill=ACCENT, width=8)
    d.line([(W - 120, 470), (W - 120, 560)], fill=ACCENT, width=8)
    d.line([(W - 90, 470), (W - 90, 560)], fill=ACCENT, width=8)
    img.save(os.path.join(IMG_DIR, f"{slug}.jpg"), "JPEG", quality=88)

def fm(r):
    L = []
    L.append("---")
    L.append(f"title: {q(r['title'])}")
    L.append(f"description: {q(r['description'])}")
    L.append(f"category: {q(r['category'])}")
    L.append(f"subcategory: {q(r['subcategory'])}")
    if r.get("sections"):
        L.append("sections:")
        L += [f"  - {q(s)}" for s in r["sections"]]
    else:
        L.append("sections: []")
    if r.get("budgetFilters"):
        L.append("budgetFilters:")
        L += [f"  - {q(s)}" for s in r["budgetFilters"]]
    else:
        L.append("budgetFilters: []")
    L.append(f"image: {q('/images/recipes/' + r['slug'] + '.jpg')}")
    L.append(f"imageAlt: {q(r['title'])}")
    L.append(f"prepTime: {r['prep']}")
    L.append(f"cookTime: {r['cook']}")
    L.append(f"servings: {r['servings']}")
    c = r["macros"]
    L.append(f"macros: {{ calories: {c[0]}, protein: {c[1]}, carbs: {c[2]}, fat: {c[3]} }}")
    L.append("ingredients:")
    for qty, unit, item in r["ingredients"]:
        qv = "null" if qty is None else qty
        L.append(f"  - {{ qty: {qv}, unit: {q(unit)}, item: {q(item)} }}")
    L.append("instructions:")
    L += [f"  - {q(s)}" for s in r["instructions"]]
    L.append(f"isBudget: {'true' if r.get('isBudget') else 'false'}")
    if r.get("costPerServing") is not None:
        L.append(f"costPerServing: {r['costPerServing']}")
    if r.get("costBreakdown"):
        L.append("costBreakdown:")
        L += [f"  - {{ item: {q(i)}, cost: {cst} }}" for i, cst in r["costBreakdown"]]
    else:
        L.append("costBreakdown: []")
    if r.get("gear"):
        L.append("gear:")
        L += [f"  - {{ name: {q(n)}, note: {q(note)} }}" for n, note in r["gear"]]
    else:
        L.append("gear: []")
    L.append(f"pubDate: {r['pubDate']}")
    L.append(f"featured: {'true' if r.get('featured') else 'false'}")
    L.append("---")
    L.append("")
    L.append(r.get("body", "").strip())
    L.append("")
    return "\n".join(L)

# en dash for budget filter
EN = "\u2013"
RECIPES = [
  # ---------- BEEF ----------
  dict(slug="taco-skillet", title="One-Pan Ground Beef Taco Skillet",
       description="Quick and filling taco skillet with beans and corn.",
       category="Beef", subcategory="Ground Beef", isBudget=True,
       budgetFilters=["Ground & Cheap"], costPerServing=1.50,
       costBreakdown=[("Ground beef",4.00),("Black beans",1.00),("Corn",1.00)],
       prep=5, cook=15, servings=4, macros=(520,38,18,32),
       ingredients=[(1,"lb","ground beef (80/20)"),(1,"packet","taco seasoning"),
                    (1,"can (15oz)","black beans, drained"),(1,"cup","frozen corn"),
                    (1,"cup","shredded cheddar cheese")],
       instructions=["Brown the ground beef in a large skillet, then drain excess fat.",
                     "Add taco seasoning, black beans, and corn. Stir well.",
                     "Cook for 5 minutes until everything is hot.",
                     "Top with cheese, cover until melted, and serve."],
       gear=[("Large Skillet","Cast iron or stainless holds heat best.")],
       pubDate="2026-05-29", featured=True),
  dict(slug="smashburgers", title="Classic Smashburgers",
       description="Thin, crispy-edged burgers with a deep sear.",
       category="Beef", subcategory="Steaks & Grills", isBudget=False,
       prep=5, cook=10, servings=4, macros=(620,38,33,38),
       ingredients=[(1,"lb","ground beef (80/20)"),(4,"","burger buns"),
                    (4,"","slices American cheese"),(None,"","Salt & pepper")],
       instructions=["Divide the beef into 4 loose balls.",
                     "Heat a cast iron skillet very hot and add a little oil.",
                     "Smash each ball flat, season, and cook 2-3 minutes per side.",
                     "Add cheese, let it melt, and serve on buns."],
       gear=[("Cast Iron Skillet","Screaming hot equals crust."),("Sturdy Spatula","For a real smash.")],
       pubDate="2026-05-28", featured=True),
  dict(slug="chuck-roast", title="Lazy Oven Chuck Roast",
       description="Set-it-and-forget-it tender chuck roast.",
       category="Beef", subcategory="Roasts", isBudget=True,
       prep=10, cook=210, servings=6, macros=(480,52,8,28),
       ingredients=[(3,"to 4 lb","chuck roast"),(1,"packet","onion soup mix"),
                    (1,"can","cream of mushroom soup"),(1,"cup","beef broth")],
       instructions=["Season the roast with salt and pepper.",
                     "Mix the soups and broth, then pour over the roast.",
                     "Cover and bake at 325F for 3.5 hours until fork-tender."],
       gear=[("Dutch Oven","Holds heat low and slow.")],
       pubDate="2026-05-27"),
  dict(slug="mississippi-roast", title="Slow Cooker Mississippi Pot Roast",
       description="Set-and-forget tender pot roast with pepperoncini.",
       category="Beef", subcategory="Slow Cooker / One-Pot", isBudget=True,
       prep=5, cook=480, servings=8, macros=(450,48,4,28),
       ingredients=[(3,"to 4 lb","chuck roast"),(1,"packet","ranch dressing mix"),
                    (1,"packet","au jus gravy mix"),(1,"","stick butter"),
                    (6,"","pepperoncini peppers")],
       instructions=["Place the roast in the slow cooker.",
                     "Sprinkle both seasoning packets over the roast.",
                     "Add the butter and pepperoncini peppers.",
                     "Cook on low for 8 hours, then shred and serve."],
       gear=[("Slow Cooker","A 6-quart is the sweet spot.")],
       pubDate="2026-05-26"),
  # ---------- CHICKEN ----------
  dict(slug="crispy-chicken-breasts", title="Crispy Baked Chicken Breasts",
       description="Simple crispy parmesan-crusted chicken breasts.",
       category="Chicken", subcategory="Chicken Breasts", isBudget=False,
       prep=10, cook=25, servings=4, macros=(380,42,2,22),
       ingredients=[(4,"","chicken breasts"),(0.5,"cup","grated parmesan"),
                    (1,"tsp","garlic powder"),(1,"tsp","paprika"),(None,"","Salt & pepper")],
       instructions=["Preheat the oven to 425F.",
                     "Mix the parmesan and spices together.",
                     "Coat the chicken generously in the mixture.",
                     "Bake 22-25 minutes until crispy and cooked through."],
       gear=[("Baking Sheet","Line with foil for easy cleanup.")],
       pubDate="2026-05-25"),
  dict(slug="honey-garlic-thighs", title="Honey Garlic Chicken Thighs",
       description="Sweet and savory sticky chicken thighs.",
       category="Chicken", subcategory="Chicken Thighs", isBudget=False,
       prep=5, cook=25, servings=4, macros=(420,35,12,26),
       ingredients=[(8,"","bone-in chicken thighs"),(0.33,"cup","honey"),
                    (4,"","garlic cloves, minced"),(2,"tbsp","soy sauce"),(None,"","Salt & pepper")],
       instructions=["Season the thighs with salt and pepper.",
                     "Mix the honey, garlic, and soy sauce.",
                     "Pour the sauce over the chicken.",
                     "Bake at 425F for 25 minutes, basting halfway through."],
       gear=[("Baking Dish","Glass or ceramic works great.")],
       pubDate="2026-05-24"),
  dict(slug="bbq-drumsticks", title="Sticky BBQ Drumsticks",
       description="Sweet and sticky oven-baked drumsticks.",
       category="Chicken", subcategory="Wings & Drumsticks", isBudget=True,
       prep=5, cook=45, servings=4, macros=(410,38,18,22),
       ingredients=[(12,"","chicken drumsticks"),(1,"cup","BBQ sauce"),
                    (1,"tsp","garlic powder"),(None,"","Salt & pepper")],
       instructions=["Season the drumsticks with salt, pepper, and garlic powder.",
                     "Bake at 400F for 35 minutes.",
                     "Brush with BBQ sauce and bake 10 more minutes."],
       gear=[("Baking Sheet","Foil-lined saves scrubbing.")],
       pubDate="2026-05-23"),
  dict(slug="salsa-chicken", title="Slow Cooker Salsa Chicken",
       description="Super simple dump-and-go salsa chicken.",
       category="Chicken", subcategory="Slow Cooker / One-Pot", isBudget=True,
       prep=5, cook=360, servings=6, macros=(320,45,6,12),
       ingredients=[(6,"","chicken breasts"),(2,"jars","salsa"),
                    (1,"tsp","cumin"),(None,"","Salt & pepper")],
       instructions=["Place the chicken in the slow cooker.",
                     "Cover with salsa and cumin.",
                     "Cook on low for 6 hours, then shred and serve."],
       gear=[("Slow Cooker","Set it and walk away.")],
       pubDate="2026-05-22"),
  dict(slug="lemon-garlic-chicken", title="Lemon Garlic Chicken Breasts",
       description="Bright and simple lemon garlic chicken.",
       category="Chicken", subcategory="Chicken Breasts", isBudget=False,
       prep=5, cook=20, servings=4, macros=(360,44,3,18),
       ingredients=[(4,"","chicken breasts"),(3,"","garlic cloves, minced"),
                    (1,"","lemon, juiced"),(2,"tbsp","olive oil"),(None,"","Salt & pepper")],
       instructions=["Season the chicken with salt and pepper.",
                     "Mix the garlic, lemon juice, and olive oil.",
                     "Marinate the chicken for 5 minutes if you have time.",
                     "Pan-sear 6-7 minutes per side until cooked through."],
       gear=[("Skillet","Stainless or cast iron.")],
       pubDate="2026-05-21"),
  dict(slug="crispy-chicken-thighs", title="Crispy Oven Chicken Thighs",
       description="Crispy-skin chicken thighs with minimal effort.",
       category="Chicken", subcategory="Chicken Thighs", isBudget=True,
       sections=["Low Carb"],
       prep=5, cook=35, servings=4, macros=(420,38,2,30),
       ingredients=[(8,"","bone-in chicken thighs"),(1,"tsp","garlic powder"),
                    (1,"tsp","paprika"),(None,"","Salt & pepper")],
       instructions=["Preheat the oven to 425F.",
                     "Season the thighs generously on both sides.",
                     "Place skin-side up on a baking sheet.",
                     "Bake 35 minutes until the skin is crispy."],
       gear=[("Baking Sheet","")],
       pubDate="2026-05-20", featured=True),
  dict(slug="grilled-bbq-chicken", title="Grilled BBQ Chicken Breasts",
       description="Charred, juicy BBQ chicken straight off the grill.",
       category="Chicken", subcategory="Grills & BBQ", isBudget=False,
       prep=5, cook=15, servings=4, macros=(360,40,14,14),
       ingredients=[(4,"","chicken breasts"),(1,"cup","BBQ sauce"),
                    (1,"tbsp","olive oil"),(None,"","Salt & pepper")],
       instructions=["Oil and season the chicken on both sides.",
                     "Grill over medium-high heat for 6 minutes.",
                     "Flip and grill 5 more minutes.",
                     "Brush BBQ sauce on both sides for the last 2-3 minutes.",
                     "Rest 5 minutes before serving."],
       gear=[("Grill or Grill Pan","Get it hot before the chicken hits.")],
       pubDate="2026-05-19"),
  # ---------- PORK ----------
  dict(slug="pork-cabbage-skillet", title="Ground Pork & Cabbage Stir Skillet",
       description="Fast and cheap cabbage and pork stir-fry.",
       category="Pork", subcategory="Ground Pork", isBudget=True,
       prep=10, cook=15, servings=4, macros=(380,28,12,26),
       ingredients=[(1,"lb","ground pork"),(1,"small head","cabbage, shredded"),
                    (3,"","garlic cloves, minced"),(3,"tbsp","soy sauce"),(None,"","Salt & pepper")],
       instructions=["Brown the ground pork in a large skillet.",
                     "Add the garlic and cook 1 minute.",
                     "Add the shredded cabbage and soy sauce.",
                     "Stir-fry 8-10 minutes until the cabbage is tender."],
       gear=[("Large Skillet or Wok","Plenty of room to toss.")],
       pubDate="2026-05-18"),
  dict(slug="garlic-butter-pork-chops", title="Garlic Butter Pork Chops",
       description="Juicy pork chops with rich garlic butter.",
       category="Pork", subcategory="Pork Chops", isBudget=False,
       sections=["Low Carb"],
       prep=5, cook=15, servings=4, macros=(460,42,3,32),
       ingredients=[(4,"","pork chops"),(4,"tbsp","butter"),
                    (4,"","garlic cloves, minced"),(None,"","Salt & pepper")],
       instructions=["Season the chops with salt and pepper.",
                     "Sear 4 minutes per side in a hot pan.",
                     "Add the butter and garlic, basting for 2 minutes.",
                     "Rest 5 minutes before serving."],
       gear=[("Cast Iron Skillet","Best sear you can get.")],
       pubDate="2026-05-17"),
  dict(slug="pulled-pork", title="Slow Cooker Pulled Pork",
       description="Classic tender pulled pork.",
       category="Pork", subcategory="Pork Shoulder & Roasts", isBudget=True,
       sections=["Meal Prep"],
       prep=10, cook=480, servings=8, macros=(380,45,8,18),
       ingredients=[(4,"lb","pork shoulder"),(1,"cup","BBQ sauce"),
                    (1,"","onion, sliced"),(None,"","Salt & pepper")],
       instructions=["Season the pork with salt and pepper.",
                     "Place the onion in the bottom of the slow cooker.",
                     "Add the pork and BBQ sauce.",
                     "Cook on low for 8 hours, then shred and serve."],
       gear=[("Slow Cooker","")],
       pubDate="2026-05-16", featured=True),
  dict(slug="slow-cooker-carnitas", title="Slow Cooker Pork Carnitas",
       description="Crispy-edged pulled pork with lime and cumin.",
       category="Pork", subcategory="Slow Cooker / One-Pot & Grills", isBudget=True,
       sections=["Meal Prep"],
       prep=10, cook=480, servings=8, macros=(360,40,4,20),
       ingredients=[(4,"lb","pork shoulder"),(2,"tsp","cumin"),
                    (1,"","onion, quartered"),(2,"","limes, juiced"),(None,"","Salt & pepper")],
       instructions=["Season the pork with cumin, salt, and pepper.",
                     "Add the onion and lime juice to the slow cooker.",
                     "Cook on low for 8 hours.",
                     "Shred, then crisp under the broiler for 5 minutes.",
                     "Serve hot."],
       gear=[("Slow Cooker","")],
       pubDate="2026-05-15"),
  # ---------- FISH ----------
  dict(slug="lemon-pepper-salmon", title="Lemon Pepper Salmon",
       description="Simple and flavorful pan-seared salmon.",
       category="Fish", subcategory="Salmon", isBudget=False,
       sections=["Low Carb"],
       prep=5, cook=15, servings=4, macros=(320,38,2,18),
       ingredients=[(4,"","salmon fillets"),(2,"tsp","lemon pepper seasoning"),
                    (1,"tbsp","olive oil")],
       instructions=["Pat the salmon dry and season with lemon pepper.",
                     "Heat the oil in a skillet.",
                     "Cook skin-side down for 5-6 minutes.",
                     "Flip and cook 4-5 more minutes."],
       gear=[("Stainless or Cast Iron Skillet","Skin gets crispy on high heat.")],
       pubDate="2026-05-14"),
  dict(slug="white-fish-lemon", title="Pan-Seared White Fish with Lemon Butter",
       description="Quick and bright pan-seared white fish.",
       category="Fish", subcategory="White Fish", isBudget=True,
       prep=5, cook=10, servings=4, macros=(280,32,2,16),
       ingredients=[(4,"","white fish fillets"),(3,"tbsp","butter"),
                    (1,"","lemon, juiced"),(None,"","Salt & pepper")],
       instructions=["Season the fish with salt and pepper.",
                     "Sear in butter 3-4 minutes per side.",
                     "Finish with a squeeze of lemon juice."],
       gear=[("Skillet","")],
       pubDate="2026-05-13"),
  dict(slug="garlic-shrimp", title="Garlic Shrimp Scampi Skillet",
       description="Fast garlic butter shrimp.",
       category="Fish", subcategory="Shrimp", isBudget=False,
       sections=["Low Carb"],
       prep=5, cook=10, servings=4, macros=(280,32,4,14),
       ingredients=[(1.5,"lbs","shrimp, peeled"),(4,"","garlic cloves, minced"),
                    (3,"tbsp","butter"),(1,"","lemon, juiced")],
       instructions=["Melt the butter in a skillet.",
                     "Add the garlic and cook 30 seconds.",
                     "Add the shrimp and cook 2-3 minutes per side.",
                     "Finish with lemon juice."],
       gear=[("Skillet","")],
       pubDate="2026-05-12"),
  dict(slug="tuna-nachos", title="Canned Tuna Skillet Nachos",
       description="Quick and cheap tuna nachos.",
       category="Fish", subcategory="Canned & Easy", isBudget=True,
       prep=5, cook=10, servings=2, macros=(450,38,18,24),
       ingredients=[(2,"cans","tuna, drained"),(1,"cup","shredded cheddar cheese"),
                    (None,"","Tortilla chips"),(None,"","Salsa or hot sauce")],
       instructions=["Layer chips, tuna, and cheese in an oven-safe skillet.",
                     "Cook until the cheese melts.",
                     "Top with salsa or hot sauce and serve."],
       gear=[("Oven-Safe Skillet","")],
       pubDate="2026-05-11"),
  # ---------- BUDGET MEALS ----------
  dict(slug="beef-rice-bowl", title="$6 Beef & Rice Bowl",
       description="Cheap and filling beef and rice bowl.",
       category="Budget Meals", subcategory="Ground & Cheap", isBudget=True,
       budgetFilters=["Ground & Cheap"], costPerServing=1.50,
       costBreakdown=[("Ground beef",4.00),("Rice",1.00),("Frozen veg",1.00)],
       prep=5, cook=20, servings=4, macros=(520,28,48,22),
       ingredients=[(1,"lb","ground beef"),(2,"cups","rice"),
                    (1,"bag","frozen mixed vegetables"),(None,"","Soy sauce")],
       instructions=["Cook the rice.",
                     "Brown the beef in a skillet.",
                     "Add the vegetables and a splash of soy sauce.",
                     "Serve over rice."],
       gear=[("Skillet","")],
       pubDate="2026-05-10"),
  dict(slug="bean-sausage-soup", title="Giant Pot Bean & Sausage Soup",
       description="Hearty and cheap filling soup.",
       category="Budget Meals", subcategory="Soups & Fillers", isBudget=True,
       budgetFilters=["Soups & Fillers"], costPerServing=1.25,
       costBreakdown=[("Smoked sausage",4.00),("Beans",2.00),("Onion",0.50),("Broth",3.50)],
       prep=10, cook=30, servings=8, macros=(380,22,35,16),
       ingredients=[(1,"lb","smoked sausage"),(2,"cans","beans"),
                    (1,"","onion, diced"),(4,"cups","chicken broth")],
       instructions=["Brown the sausage and onion.",
                     "Add the beans and broth.",
                     "Simmer for 25 minutes and serve."],
       gear=[("Large Pot","")],
       pubDate="2026-05-09"),
  dict(slug="chicken-beans", title="One-Pot Chicken & Beans",
       description="Easy one-pot chicken and beans.",
       category="Budget Meals", subcategory="Big Batch", isBudget=True,
       budgetFilters=["Big Batch"], costPerServing=1.50,
       costBreakdown=[("Chicken thighs",5.00),("Black beans",2.00),("Tomatoes",1.00)],
       prep=10, cook=25, servings=6, macros=(410,35,32,14),
       ingredients=[(6,"","chicken thighs"),(2,"cans","black beans"),
                    (1,"can","diced tomatoes"),(1,"tsp","cumin")],
       instructions=["Brown the chicken in a large pot.",
                     "Add the beans, tomatoes, and cumin.",
                     "Simmer for 20 minutes and serve."],
       gear=[("Large Pot","")],
       pubDate="2026-05-08"),
  dict(slug="budget-chili", title=f"$5{EN}$10 a Day Chili",
       description="Cheap and hearty classic chili.",
       category="Budget Meals", subcategory=f"$5{EN}$10 Meals", isBudget=True,
       budgetFilters=[f"$5{EN}$10 Meals"], costPerServing=1.40,
       costBreakdown=[("Ground beef",4.00),("Beans",2.00),("Tomatoes",1.00),("Seasoning",1.40)],
       prep=10, cook=45, servings=6, macros=(420,32,38,18),
       ingredients=[(1,"lb","ground beef"),(2,"cans","beans"),
                    (1,"can","diced tomatoes"),(2,"tbsp","chili seasoning")],
       instructions=["Brown the ground beef.",
                     "Add the beans, tomatoes, and chili seasoning.",
                     "Simmer 30-40 minutes and serve."],
       gear=[("Large Pot or Dutch Oven","")],
       pubDate="2026-05-07"),
  dict(slug="pantry-egg-fried-rice", title="Pantry Egg Fried Rice",
       description="Cheap, fast fried rice from whatever's in the pantry.",
       category="Budget Meals", subcategory="Pantry Staples", isBudget=True,
       budgetFilters=["Pantry Staples"], costPerServing=1.00,
       costBreakdown=[("Rice",0.75),("Eggs",1.25),("Frozen veg",1.00),("Soy sauce",1.00)],
       prep=5, cook=10, servings=4, macros=(380,12,52,12),
       ingredients=[(3,"cups","cooked rice"),(3,"","eggs"),
                    (1,"cup","frozen peas and carrots"),(3,"tbsp","soy sauce"),(2,"tbsp","oil")],
       instructions=["Heat the oil in a large skillet.",
                     "Scramble the eggs and set aside.",
                     "Add the rice and frozen veg, frying 3-4 minutes.",
                     "Stir in the soy sauce and eggs.",
                     "Serve hot."],
       gear=[("Large Skillet or Wok","")],
       pubDate="2026-05-06"),
  # ---------- MEAL PREP ----------
  dict(slug="bbq-meatballs", title="Big Batch Slow Cooker BBQ Meatballs",
       description="Easy make-ahead meatballs.",
       category="Meal Prep", subcategory="Slow Cooker Batches", isBudget=True,
       prep=10, cook=360, servings=10, macros=(380,32,12,22),
       ingredients=[(2,"lbs","ground beef"),(1,"bottle","BBQ sauce"),
                    (1,"","egg"),(0.5,"cup","breadcrumbs")],
       instructions=["Mix the beef, egg, and breadcrumbs, then form meatballs.",
                     "Place the meatballs in the slow cooker.",
                     "Cover with BBQ sauce.",
                     "Cook on low for 6 hours."],
       gear=[("Slow Cooker","")],
       pubDate="2026-05-05"),
  dict(slug="sausage-sheet-pan", title="Sheet Pan Sausage, Potato & Pepper",
       description="Easy one-pan sausage dinner.",
       category="Meal Prep", subcategory="Sheet Pan Meals", isBudget=True,
       prep=10, cook=35, servings=5, macros=(460,24,28,28),
       ingredients=[(2,"lbs","sausage links"),(6,"","potatoes, cubed"),
                    (2,"","bell peppers, sliced"),(None,"","Salt, pepper, garlic powder")],
       instructions=["Preheat the oven to 425F.",
                     "Toss everything on a sheet pan with seasoning.",
                     "Bake 35 minutes, stirring halfway through."],
       gear=[("Sheet Pan","")],
       pubDate="2026-05-04"),
  dict(slug="skillet-chicken-rice", title="Skillet Chicken & Rice Meal Prep",
       description="One-pan chicken and rice that boxes up for the week.",
       category="Meal Prep", subcategory="Skillet & One-Pan", isBudget=True,
       prep=10, cook=30, servings=5, macros=(480,35,45,16),
       ingredients=[(6,"","chicken thighs"),(2,"cups","rice"),
                    (4,"cups","chicken broth"),(1,"tsp","garlic powder"),(None,"","Salt & pepper")],
       instructions=["Season and sear the chicken in a deep skillet, then remove.",
                     "Add the rice and broth to the same pan.",
                     "Nestle the chicken back in.",
                     "Cover and simmer 20 minutes.",
                     "Rest, then portion into containers."],
       gear=[("Deep Skillet with Lid","")],
       pubDate="2026-05-03"),
  # ---------- LOW CARB ----------
  dict(slug="bacon-cheeseburger-skillet", title="Bacon Cheeseburger Skillet (No Bun)",
       description="Low carb cheeseburger skillet.",
       category="Low Carb", subcategory="Ground Meats", isBudget=False,
       prep=5, cook=15, servings=4, macros=(580,42,4,44),
       ingredients=[(1.5,"lbs","ground beef"),(8,"","slices bacon, chopped"),
                    (1,"cup","shredded cheddar")],
       instructions=["Cook the bacon until crispy, then remove.",
                     "Brown the beef in the bacon fat.",
                     "Top with cheese and the cooked bacon and serve."],
       gear=[("Cast Iron Skillet","")],
       pubDate="2026-05-02"),
  dict(slug="chicken-broccoli", title="Crispy Chicken Thighs & Broccoli",
       description="Simple low carb chicken dinner.",
       category="Low Carb", subcategory="Chicken Thighs & Skillets", isBudget=False,
       prep=5, cook=30, servings=4, macros=(440,38,6,30),
       ingredients=[(8,"","chicken thighs"),(4,"cups","broccoli florets"),
                    (None,"","Garlic powder, salt, pepper")],
       instructions=["Season the chicken and broccoli.",
                     "Roast at 425F for 30 minutes and serve."],
       gear=[("Sheet Pan","")],
       pubDate="2026-05-01"),
  dict(slug="low-carb-chili", title="Slow Cooker Low Carb Chili",
       description="Hearty low carb chili.",
       category="Low Carb", subcategory="Slow Cooker", isBudget=True,
       prep=10, cook=360, servings=6, macros=(420,38,12,24),
       ingredients=[(2,"lbs","ground beef"),(2,"cans","diced tomatoes"),
                    (2,"tbsp","chili powder"),(1,"","onion, diced")],
       instructions=["Brown the beef and onion.",
                     "Add everything to the slow cooker.",
                     "Cook on low for 6 hours and serve."],
       gear=[("Slow Cooker","")],
       pubDate="2026-04-30"),
]

assert len(RECIPES) == 30, f"expected 30, got {len(RECIPES)}"
slugs = [r["slug"] for r in RECIPES]
assert len(set(slugs)) == 30, "duplicate slugs!"

for r in RECIPES:
    with open(os.path.join(RECIPE_DIR, r["slug"] + ".md"), "w") as f:
        f.write(fm(r))
    make_image(r["slug"], r["title"], r["category"])

print(f"Wrote {len(RECIPES)} recipes + images.")
