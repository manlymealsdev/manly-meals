#!/usr/bin/env python3
"""Make salt/pepper precise ('to taste') and add helpful timing/visual cues to
vague instruction lines across existing recipes. Keeps the short, plain tone."""
import glob, re, yaml, json

def q(s):
    return json.dumps(s, ensure_ascii=False)

# Salt/pepper ingredient items -> 'to taste'
SP_MAP = {
    'Salt & pepper': 'Salt & pepper, to taste',
    'Salt': 'Salt, to taste',
    'Coarse salt': 'Coarse salt, to taste',
    'Black pepper': 'Black pepper, to taste',
    'Garlic powder, salt, pepper': 'Garlic powder, salt, and pepper, to taste',
    'Salt, pepper, garlic powder': 'Salt, pepper, and garlic powder, to taste',
    'Salt, pepper, and garlic powder': 'Salt, pepper, and garlic powder, to taste',
}

RICE = ("Cook the rice: simmer covered in twice its volume of water for 15-18 minutes "
        "until the water is absorbed, then fluff with a fork.")

EXACT = {
    "Cook the rice.": RICE,
    "Boil the egg noodles and drain.": "Boil the egg noodles until tender, about 8 minutes, then drain.",
    "Boil and drain the macaroni.": "Boil the macaroni until tender, about 8 minutes, then drain.",
    "Cook until the cheese melts.": "Cook until the cheese melts, about 2 minutes.",
    "Heat the rice and divide between two bowls.": "Heat the rice through and divide between two warm bowls.",
    "Warm the tortillas.": "Warm the tortillas in a dry pan or microwave until pliable.",
    "Warm the buns.": "Warm the buns in the pan or a toaster.",
    "Toast the sesame buns.": "Toast the sesame buns cut-side down until golden.",
    "Toast the buns.": "Toast the buns cut-side down until golden.",
    "Season the chicken and broccoli.": "Season the chicken and broccoli with the garlic powder, salt, and pepper to taste.",
    "Cook the rice and divide between two bowls.": RICE + " Divide between two bowls.",
}

def enhance(s):
    if s in EXACT:
        return EXACT[s]
    # Ground-meat browning, no time given
    if re.match(r"^Brown the (ground beef|ground pork|beef)\b", s) and not re.search(r"\d", s):
        core = s.rstrip(".")
        drain = ""
        m = re.search(r",? and drain( the fat)?$", core)
        if m:
            core = core[:m.start()]
            drain = ", then drain"
        return f"{core}, breaking it up with a spoon, 5-6 minutes until no pink remains{drain}."
    # Other 'Brown ...' lines with no time
    if re.match(r"^Brown ", s) and not re.search(r"\d", s):
        return s.rstrip(".") + ", about 6 minutes."
    # Searing with 'per side' but no doneness cue
    if "Sear" in s and "per side" in s and "until" not in s and "brown" not in s.lower() and "crust" not in s.lower():
        return s.rstrip(".") + ", until a deep crust forms."
    # 'to taste' inside instructions
    s = s.replace("with salt and pepper.", "with salt and pepper to taste.")
    return s

def replace_block(fm, key, new_lines):
    lines = fm.split("\n"); out = []; i = 0
    while i < len(lines):
        ln = lines[i]
        if ln.startswith(key + ":"):
            if ln.strip() == key + ": []":
                i += 1
            else:
                i += 1
                while i < len(lines) and lines[i].startswith("  - "):
                    i += 1
            out.append(key + ":")
            out.extend(new_lines)
            continue
        out.append(ln); i += 1
    return "\n".join(out)

n = 0
for f in sorted(glob.glob("src/content/recipes/*.md")):
    raw = open(f).read()
    parts = raw.split("---", 2)
    fm = parts[1]
    d = yaml.safe_load(fm)
    # salt/pepper on ingredient items
    new_ings = []
    for ing in d["ingredients"]:
        item = ing["item"]
        if item in SP_MAP:
            item = SP_MAP[item]
        new_ings.append((ing.get("qty"), ing.get("unit", ""), item))
    ing_lines = [f"  - {{ qty: {'null' if qy is None else qy}, unit: {q(un)}, item: {q(it)} }}"
                 for qy, un, it in new_ings]
    fm = replace_block(fm, "ingredients", ing_lines)
    # instructions cues
    new_instr = [enhance(s) for s in d["instructions"]]
    instr_lines = [f"  - {q(s)}" for s in new_instr]
    fm = replace_block(fm, "instructions", instr_lines)
    open(f, "w").write("---" + fm + "---" + parts[2])
    n += 1

print(f"Edited {n} recipes (salt/pepper + instruction cues).")
