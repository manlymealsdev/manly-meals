#!/usr/bin/env python3
"""Add 4 recipes to fill the remaining empty subcategories."""
import os, json, textwrap
from PIL import Image, ImageDraw, ImageFont

RECIPE_DIR = "src/content/recipes"
IMG_DIR = "public/images/recipes"

BASE=(22,26,27); CARD=(46,46,46); ACCENT=(190,102,0); INK=(231,220,207); MUTED=(154,149,140)
FONT_BOLD="/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
FONT_REG="/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
CAT_TINT={"Beef":(150,60,40),"Chicken":(180,130,60),"Pork":(170,90,90),"Fish":(60,110,130),
          "Budget Meals":(90,120,70),"Meal Prep":(110,90,140),"Low Carb":(70,130,110)}

def q(s): return json.dumps(s, ensure_ascii=False)

def make_image(slug,title,category):
    W,H=1280,720; img=Image.new("RGB",(W,H),BASE); d=ImageDraw.Draw(img)
    tint=CAT_TINT.get(category,ACCENT)
    for i in range(0,H,2):
        a=max(0,0.18-i/H*0.18)
        d.line([(0,i),(W,i)],fill=(int(BASE[0]+(tint[0]-BASE[0])*a),int(BASE[1]+(tint[1]-BASE[1])*a),int(BASE[2]+(tint[2]-BASE[2])*a)),width=2)
    d.ellipse([W-360,-200,W+200,360],fill=(int(BASE[0]+(ACCENT[0]-BASE[0])*0.10),int(BASE[1]+(ACCENT[1]-BASE[1])*0.10),int(BASE[2]+(ACCENT[2]-BASE[2])*0.10)))
    d.rectangle([90,250,130,470],fill=ACCENT)
    d.text((160,250),category.upper(),font=ImageFont.truetype(FONT_BOLD,34),fill=ACCENT)
    f_title=ImageFont.truetype(FONT_BOLD,78); y=300
    for ln in textwrap.wrap(title.upper(),width=18)[:3]:
        d.text((158,y),ln,font=f_title,fill=INK); y+=86
    d.text((160,H-80),"MANLY MEALS",font=ImageFont.truetype(FONT_BOLD,30),fill=INK)
    d.text((160,H-44),"placeholder image — swap with a real photo",font=ImageFont.truetype(FONT_REG,24),fill=MUTED)
    for x in (W-150,W-120,W-90): d.line([(x,470),(x,560)],fill=ACCENT,width=8)
    img.save(os.path.join(IMG_DIR,f"{slug}.jpg"),"JPEG",quality=88)

def fm(r):
    L=["---",f"title: {q(r['title'])}",f"description: {q(r['description'])}",
       f"category: {q(r['category'])}",f"subcategory: {q(r['subcategory'])}"]
    if r.get("sections"): L.append("sections:"); L+=[f"  - {q(s)}" for s in r["sections"]]
    else: L.append("sections: []")
    if r.get("budgetFilters"): L.append("budgetFilters:"); L+=[f"  - {q(s)}" for s in r["budgetFilters"]]
    else: L.append("budgetFilters: []")
    L.append(f"image: {q('/images/recipes/'+r['slug']+'.jpg')}")
    L.append(f"imageAlt: {q(r['title'])}")
    L+=[f"prepTime: {r['prep']}",f"cookTime: {r['cook']}",f"servings: {r['servings']}"]
    c=r["macros"]; L.append(f"macros: {{ calories: {c[0]}, protein: {c[1]}, carbs: {c[2]}, fat: {c[3]} }}")
    L.append("ingredients:")
    for qty,unit,item in r["ingredients"]:
        L.append(f"  - {{ qty: {'null' if qty is None else qty}, unit: {q(unit)}, item: {q(item)} }}")
    L.append("instructions:"); L+=[f"  - {q(s)}" for s in r["instructions"]]
    L.append(f"isBudget: {'true' if r.get('isBudget') else 'false'}")
    if r.get("costPerServing") is not None: L.append(f"costPerServing: {r['costPerServing']}")
    L.append("costBreakdown: []")
    if r.get("gear"): L.append("gear:"); L+=[f"  - {{ name: {q(n)}, note: {q(note)} }}" for n,note in r["gear"]]
    else: L.append("gear: []")
    L+=[f"pubDate: {r['pubDate']}",f"featured: {'true' if r.get('featured') else 'false'}","---","",
        r.get("body","").strip(),""]
    return "\n".join(L)

RECIPES=[
  dict(slug="grilled-chicken-meal-prep", title="Grill & Portion Chicken Boxes",
       description="Batch-grilled chicken portioned out for the whole week.",
       category="Meal Prep", subcategory="Grill & Portion", isBudget=True,
       prep=10, cook=20, servings=6, macros=(360,46,4,16),
       ingredients=[(3,"lbs","chicken breasts"),(2,"tbsp","olive oil"),
                    (1,"tbsp","garlic powder"),(1,"tbsp","paprika"),(None,"","Salt & pepper")],
       instructions=["Oil and season the chicken on both sides.",
                     "Grill over medium-high heat 6-7 minutes per side until cooked through.",
                     "Rest 5 minutes, then slice.",
                     "Divide into 6 containers with a starch and a veg.",
                     "Refrigerate up to 4 days."],
       gear=[("Grill or Grill Pan","Get it hot before the chicken hits."),
             ("Meal Prep Containers","Glass holds up best.")],
       pubDate="2026-04-29"),
  dict(slug="freezer-beef-burritos", title="Make-Ahead Freezer Beef Burritos",
       description="Wrap a big batch now, microwave dinner all month.",
       category="Meal Prep", subcategory="Freezer Meals", isBudget=True,
       sections=["Budget Meals"], budgetFilters=["Big Batch"],
       prep=20, cook=15, servings=10, macros=(440,26,42,20),
       ingredients=[(2,"lbs","ground beef"),(1,"packet","taco seasoning"),
                    (2,"cans","refried beans"),(10,"","large flour tortillas"),
                    (2,"cups","shredded cheese")],
       instructions=["Brown the beef, drain, and stir in the taco seasoning.",
                     "Warm the refried beans until spreadable.",
                     "Fill each tortilla with beans, beef, and cheese, then roll tight.",
                     "Wrap each burrito in foil and freeze.",
                     "Reheat from frozen: microwave 2-3 minutes or oven 25 minutes at 375F."],
       gear=[("Large Skillet",""),("Foil & Freezer Bags","Label with the date.")],
       pubDate="2026-04-28"),
  dict(slug="grilled-ribeye", title="Grilled Ribeye Steak",
       description="A simple, perfectly charred ribeye with nothing to hide behind.",
       category="Low Carb", subcategory="Steaks & Grills", isBudget=False,
       prep=5, cook=10, servings=2, macros=(640,46,0,50),
       ingredients=[(2,"","ribeye steaks"),(1,"tbsp","olive oil"),
                    (None,"","Coarse salt"),(None,"","Black pepper")],
       instructions=["Pull the steaks out 30 minutes early and pat dry.",
                     "Rub with oil and season hard with salt and pepper.",
                     "Grill over high heat 4-5 minutes per side for medium-rare.",
                     "Rest 5 minutes before slicing."],
       gear=[("Grill or Cast Iron","High heat is everything."),
             ("Meat Thermometer","130F for medium-rare.")],
       pubDate="2026-04-27"),
  dict(slug="garlic-butter-shrimp-low-carb", title="Garlic Butter Shrimp & Zucchini",
       description="Fast, lean garlic butter shrimp over sauteed zucchini.",
       category="Low Carb", subcategory="Fish & Shrimp", isBudget=False,
       prep=10, cook=10, servings=4, macros=(300,30,8,16),
       ingredients=[(1.5,"lbs","shrimp, peeled"),(3,"","zucchini, sliced"),
                    (4,"tbsp","butter"),(4,"","garlic cloves, minced"),(None,"","Salt & pepper")],
       instructions=["Melt 2 tbsp butter and saute the zucchini 4-5 minutes, then set aside.",
                     "Melt the rest of the butter and cook the garlic 30 seconds.",
                     "Add the shrimp and cook 2-3 minutes per side.",
                     "Return the zucchini, season, toss, and serve."],
       gear=[("Large Skillet","")],
       pubDate="2026-04-26"),
]

for r in RECIPES:
    with open(os.path.join(RECIPE_DIR, r["slug"]+".md"),"w") as f: f.write(fm(r))
    make_image(r["slug"], r["title"], r["category"])
print(f"Added {len(RECIPES)} recipes + images.")
