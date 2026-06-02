# Manly Meals 🔪🥩

**Straightforward Recipes for Guys Who Don't Cook.** Simple. Cheap. Delicious.

A fast, mobile-first, SEO-friendly recipe site built with **Astro 5 + Tailwind CSS v3**. Static output (deploys anywhere), recipe content lives in plain Markdown files, and adding a new recipe is as easy as dropping in one `.md` file.

> **This build (`manly-meals-final`) includes:** subcategory cards show titles only (no descriptions); a more prominent "Kitchen Gear" nav link; updated About page copy; a compact "Total Kitchen Starter Bundle" with an estimated ~$280–$350 total; "Stainless Steel Frying Pan" (renamed from Non-Stick); and a large hero image at the top of every recipe page (branded placeholder images included).

---

## Tech stack

- **Astro 5** — static site generator, zero JS shipped by default
- **Tailwind CSS v3** (`@astrojs/tailwind`) — utility styling, `tailwind.config.mjs`
- **Content Collections** — typed Markdown recipes validated by a Zod schema
- **@astrojs/sitemap** — auto `sitemap-index.xml`
- **schema.org Recipe JSON-LD** — rich results in Google
- Google Fonts: Anton (display), Barlow Condensed (headings), Barlow (body)

---

## Run locally

You need **Node.js 18.17+ (or 20+)** and npm.

```bash
# 1. install dependencies
npm install

# 2. start the dev server (hot reload)
npm run dev
# → open http://localhost:4321

# 3. build the production site
npm run build
# → static output in ./dist

# 4. preview the production build locally
npm run preview
```

---

## Project structure

```
manly-meals/
├─ astro.config.mjs          # Astro config (site URL, integrations)
├─ tailwind.config.mjs       # color palette, fonts, shadows
├─ tsconfig.json
├─ public/
│  ├─ favicon.svg
│  ├─ robots.txt
│  └─ images/recipes/        # one image per recipe (SVG placeholders for now)
├─ scripts/                  # Python generators for placeholder recipes/images
│  ├─ generate.py
│  └─ recipes.py
└─ src/
   ├─ data/
   │  ├─ categories.ts        # ← single source of truth for nav + subcategories
   │  └─ gear.ts              # ← gear list + affiliate links + disclosure
   ├─ content/
   │  ├─ config.ts            # Zod schema for recipes
   │  └─ recipes/*.md         # ← one Markdown file per recipe
   ├─ components/             # Header, Footer, RecipeCard, ServingsScaler, GearBox, ...
   ├─ layouts/BaseLayout.astro
   ├─ styles/global.css
   └─ pages/
      ├─ index.astro          # homepage
      ├─ beef / chicken / pork / fish / meal-prep / low-carb .astro
      ├─ budget-meals.astro   # flat page with filter buttons
      ├─ gear.astro           # Manly Kitchen Gear + Starter Bundle
      ├─ about.astro
      ├─ 404.astro
      └─ recipes/[slug].astro # recipe template (hero → ingredients → steps → scaler → cost → gear)
```

---

## Add a new recipe (the easy part)

1. Create `src/content/recipes/your-recipe-slug.md`.
2. Drop a matching image at `public/images/recipes/your-recipe-slug.svg` (or `.jpg`/`.png` — just match the `image` field).
3. Rebuild. It automatically appears on the homepage "Latest Recipes" and in its category/subcategory.

Frontmatter template:

```markdown
---
title: "Garlic Butter Pork Chops"
description: "Juicy chops in a quick garlic butter pan sauce."
category: "Pork"                     # Beef | Chicken | Pork | Fish | Budget Meals | Meal Prep | Low Carb
subcategory: "Pork Chops"            # must match a subcategory in src/data/categories.ts
sections: ["Low Carb"]               # extra category pages this recipe also shows on (optional)
budgetFilters: []                    # e.g. ["Ground & Cheap", "Pantry Staples"] (optional)
image: "/images/recipes/garlic-butter-pork-chops.svg"
imageAlt: "Seared pork chops in garlic butter"
prepTime: 5                          # minutes
cookTime: 12                         # minutes
servings: 2
macros: { calories: 520, protein: 42, carbs: 3, fat: 38 }
ingredients:
  - { qty: 2, unit: "", item: "bone-in pork chops" }
  - { qty: 3, unit: "tbsp", item: "butter" }
  - { qty: 3, unit: "", item: "garlic cloves, smashed" }
instructions:
  - "Pat chops dry and season both sides with salt and pepper."
  - "Sear 3–4 min per side in a hot pan until golden."
  - "Add butter and garlic, baste 1 min, rest 5 min, serve."
isBudget: false                      # true → shows on Budget Meals + renders cost breakdown
costPerServing: null                 # e.g. 2.10 (only used when isBudget: true)
costBreakdown: []                    # e.g. [{ item: "Pork chops", cost: 3.20 }]
gear:
  - { name: "Cast Iron Skillet", note: "Best sear you'll get." }
pubDate: 2026-05-20
featured: false
---

Optional intro paragraph / tips in Markdown body.
```

> Tip: `qty` can be `null` for "to taste" items. The 1x / 2x / 4x servings scaler automatically multiplies every numeric `qty` and snaps to clean fractions (¼ ⅓ ½ ⅔ ¾).

---

## Edit categories, nav, and gear

- **Navigation + subcategory cards** → `src/data/categories.ts` (one array drives the whole site).
- **Kitchen gear, Starter Bundle, and affiliate links** → `src/data/gear.ts`. Replace the placeholder URLs (`https://www.amazon.com/dp/PLACEHOLDER?tag=manlymeals-20`) with your real Amazon Associates links. The disclosure text — *"As an Amazon Associate, I earn from qualifying purchases."* — is defined once here and reused.
- **Site URL** (for sitemap + canonical/OG tags) → `site:` in `astro.config.mjs`.
- **Colors / fonts** → `tailwind.config.mjs`.

---

## Swap the placeholder images

The recipe images are branded **SVG placeholders** (generated offline). To use real photos, replace the files in `public/images/recipes/` — keep the same filename (or update the `image:` field in the recipe's frontmatter). JPG/PNG/WebP all work.

You can regenerate the placeholders with `python3 scripts/recipes.py` if you change recipe data.

---

## Deploy

The site builds to a static `dist/` folder, so it hosts anywhere. Two common options:

### Vercel
1. Push the repo to GitHub/GitLab/Bitbucket.
2. In Vercel: **New Project → Import** your repo.
3. Vercel auto-detects Astro. Confirm:
   - **Build command:** `npm run build`
   - **Output directory:** `dist`
4. Deploy. (CLI alternative: `npm i -g vercel` then run `vercel`.)

### Netlify
1. Push the repo to your Git provider.
2. In Netlify: **Add new site → Import an existing project**.
3. Settings:
   - **Build command:** `npm run build`
   - **Publish directory:** `dist`
4. Deploy.

Optional `netlify.toml` you can commit to the project root:

```toml
[build]
  command = "npm run build"
  publish = "dist"
```

After your first deploy, update `site:` in `astro.config.mjs` to your real domain and redeploy so the sitemap and canonical URLs are correct.

---

## Notes

- **Zero profanity, zero fluff** — copy is intentionally short and direct.
- **Mobile-first**: 44–48px tap targets, horizontal-scroll nav on phones, large hero images, fast static pages.
- **SEO**: per-page meta + Open Graph/Twitter tags, schema.org Recipe JSON-LD on every recipe, sitemap, robots.txt.
