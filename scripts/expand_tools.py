#!/usr/bin/env python3
"""Expand every recipe's gear/tools list to 4-6 relevant tools, based on its
actual ingredients and instructions. Keeps the existing cooking vessel(s)."""
import glob, re, yaml, json

def q(s):
    return json.dumps(s, ensure_ascii=False)

# Candidate hand-tools (no cooking vessels — those stay from the recipe's own gear)
def build_tools(d):
    ings = " ".join(i.get("item", "").lower() for i in d["ingredients"])
    units = " ".join(str(i.get("unit", "")).lower() for i in d["ingredients"])
    instr = " ".join(s.lower() for s in d["instructions"])
    title = d["title"].lower()
    cat = d["category"]
    text = ings + " " + instr + " " + title

    existing = [(g["name"], g.get("note", "")) for g in d.get("gear", [])]
    have = {n.lower() for n, _ in existing}
    out = list(existing)

    def add(name, note):
        if name.lower() in {n.lower() for n, _ in out}:
            return
        out.append((name, note))

    needs_knife = any(w in text for w in ["onion","garlic","pepper","cabbage","lemon","lime",
        "broccoli","zucchini","potato","scallion","sliced","minced","diced","chopped","quartered",
        "chop","slice","mince"])
    is_fish = cat == "Fish" or any(w in text for w in ["salmon","shrimp","tuna","white fish","fish"])
    is_patty = any(w in text for w in ["smash","burger","patties","patty","meatball","salisbury"])
    browns_ground = ("ground beef" in ings or "ground pork" in ings) and "brown" in instr
    needs_bowl = browns_ground or is_patty or any(w in instr for w in
        ["mix","whisk","beat","coat","form","marinate","scramble","toss"]) or "egg" in ings or "breadcrumb" in ings
    needs_temp = any(w in text for w in ["chicken breast","chicken thigh","pork chop","ribeye",
        "steak","salmon","white fish","roast","pork shoulder","drumstick","chops","fillet","thighs"])
    needs_flip = any(w in instr for w in ["sear","flip","grill","fry","saute"]) or is_patty or is_fish
    pasta = any(w in ings for w in ["pasta","noodle","macaroni","spaghetti"])
    canned = "can" in units or "cans" in units or "jar" in units or "jars" in units or "can" in ings
    measured = any(u in units for u in ["cup","cups","tbsp","tsp"])

    if needs_knife:
        add("Chef's Knife", "For all the chopping and slicing.")
        add("Cutting Board", "Keep raw meat and veg separate.")
    if needs_bowl:
        add("Mixing Bowl", "Mixing, coating, and prep.")
    if needs_temp:
        add("Instant-Read Meat Thermometer", "Take the guesswork out of doneness.")
    if is_fish:
        add("Fish Spatula", "Thin edge slides under delicate fillets.")
    elif is_patty:
        add("Sturdy Spatula", "For flipping and pressing.")
    elif needs_flip:
        add("Tongs", "Flip and turn without piercing.")
    if browns_ground:
        add("Wooden Spoon", "Break up the meat as it browns.")
    if pasta:
        add("Colander", "Drain it fast.")
    if canned:
        add("Can Opener", "For the cans.")
    if measured:
        add("Measuring Cups & Spoons", "Get the ratios right.")

    # Ensure at least 4 with sensible padding
    for name, note in [("Chef's Knife","For all the chopping and slicing."),
                       ("Cutting Board","A sturdy board for prep."),
                       ("Mixing Bowl","Mixing and prep."),
                       ("Measuring Cups & Spoons","Get the ratios right."),
                       ("Tongs","Flip and serve.")]:
        if len(out) >= 4:
            break
        add(name, note)

    return out[:6]  # cap at 6

def replace_gear_block(fm, tools):
    lines = fm.split("\n")
    out = []
    i = 0
    while i < len(lines):
        ln = lines[i]
        if ln.startswith("gear:"):
            # skip existing block
            if ln.strip() == "gear: []":
                i += 1
            else:
                i += 1
                while i < len(lines) and lines[i].startswith("  - "):
                    i += 1
            # write new block
            out.append("gear:")
            for name, note in tools:
                out.append(f"  - {{ name: {q(name)}, note: {q(note)} }}")
            continue
        out.append(ln)
        i += 1
    return "\n".join(out)

n = 0
counts = {}
for f in sorted(glob.glob("src/content/recipes/*.md")):
    raw = open(f).read()
    parts = raw.split("---", 2)
    d = yaml.safe_load(parts[1])
    tools = build_tools(d)
    counts[f] = len(tools)
    newfm = replace_gear_block(parts[1], tools)
    open(f, "w").write("---" + newfm + "---" + parts[2])
    n += 1

print(f"Updated tools on {n} recipes.")
bad = {k: v for k, v in counts.items() if not (4 <= v <= 6)}
print("Recipes outside 4-6 tools:", bad if bad else "none")
