// -----------------------------------------------------------------------------
// Single source of truth for navigation, categories, and subcategories.
// Edit here to change the site's structure everywhere at once.
// -----------------------------------------------------------------------------

export interface Subcategory {
  name: string;
  blurb: string;
}

export interface Category {
  /** Display name used in the nav and headings */
  name: string;
  /** URL path, e.g. "/beef" */
  slug: string;
  /** Short line shown under the category title */
  blurb: string;
  /** Card subcategories. Empty for flat pages (Budget Meals). */
  subcategories: Subcategory[];
  /** Filter buttons for flat pages instead of subcategory cards */
  filters?: string[];
}

export const CATEGORIES: Category[] = [
  {
    name: 'Beef',
    slug: '/beef',
    blurb: 'Burgers, steaks, chili. Big flavor, low effort.',
    subcategories: [
      { name: 'Ground Beef', blurb: 'Burgers, tacos, chili, skillet dinners.' },
      { name: 'Steaks & Grills', blurb: 'Ribeye, sirloin, and how to not ruin them.' },
      { name: 'Roasts', blurb: 'Set it, forget it, slice it Sunday.' },
      { name: 'Slow Cooker / One-Pot', blurb: 'Dump it in, walk away, eat later.' },
    ],
  },
  {
    name: 'Chicken',
    slug: '/chicken',
    blurb: 'The everyday workhorse. Cheap, fast, never boring.',
    subcategories: [
      { name: 'Chicken Breasts', blurb: 'Juicy, not dry. We promise.' },
      { name: 'Chicken Thighs', blurb: 'Cheaper and more forgiving than breasts.' },
      { name: 'Wings & Drumsticks', blurb: 'Game day, every day.' },
      { name: 'Slow Cooker / One-Pot', blurb: 'Minimal dishes, maximum dinner.' },
      { name: 'Grills & BBQ', blurb: 'Char marks and sticky sauce.' },
    ],
  },
  {
    name: 'Pork',
    slug: '/pork',
    blurb: 'Chops, shoulder, ground. Underrated and cheap.',
    subcategories: [
      { name: 'Ground Pork', blurb: 'Meatballs, stir-fries, easy weeknight wins.' },
      { name: 'Pork Chops', blurb: 'Thick-cut, seared, never shoe-leather.' },
      { name: 'Pork Shoulder & Roasts', blurb: 'Pulled pork and big-batch payoff.' },
      { name: 'Slow Cooker / One-Pot & Grills', blurb: 'Low effort, low and slow.' },
    ],
  },
  {
    name: 'Fish',
    slug: '/fish',
    blurb: 'Fast protein. Most of it is done in 10 minutes.',
    subcategories: [
      { name: 'Salmon', blurb: 'Crispy skin, no fuss.' },
      { name: 'White Fish', blurb: 'Cod, tilapia, and other cheap wins.' },
      { name: 'Shrimp', blurb: 'Frozen bag to dinner in minutes.' },
      { name: 'Canned & Easy', blurb: 'Tuna, sardines, pantry power.' },
    ],
  },
  {
    name: 'Budget Meals',
    slug: '/budget-meals',
    blurb: 'Feed yourself for the price of a coffee.',
    subcategories: [],
    filters: ['Ground & Cheap', 'Big Batch', 'Soups & Fillers', '$5–$10 Meals', 'Pantry Staples'],
  },
  {
    name: 'Meal Prep',
    slug: '/meal-prep',
    blurb: 'Cook once on Sunday. Eat all week.',
    subcategories: [
      { name: 'Slow Cooker Batches', blurb: 'One pot, five lunches.' },
      { name: 'Sheet Pan Meals', blurb: 'One tray, zero babysitting.' },
      { name: 'Skillet & One-Pan', blurb: 'Fast cook, fast cleanup.' },
      { name: 'Grill & Portion', blurb: 'Batch grill, box it up.' },
      { name: 'Freezer Meals', blurb: 'Future you will thank present you.' },
    ],
  },
  {
    name: 'Low Carb',
    slug: '/low-carb',
    blurb: 'High protein, no carb crash. Still tastes like food.',
    subcategories: [
      { name: 'Steaks & Grills', blurb: 'Pure protein, zero filler.' },
      { name: 'Ground Meats', blurb: 'Skillet meals without the bun.' },
      { name: 'Chicken Thighs & Skillets', blurb: 'Crispy, fatty, satisfying.' },
      { name: 'Slow Cooker', blurb: 'Low-carb, low-effort batches.' },
      { name: 'Fish & Shrimp', blurb: 'Lean, fast, keto-friendly.' },
    ],
  },
];

/** The 7 flat nav links, in exact order. */
export const NAV_LINKS = CATEGORIES.map((c) => ({ name: c.name, slug: c.slug }));

/** Look up a category by its slug (e.g. "/beef"). */
export function getCategory(slug: string): Category | undefined {
  return CATEGORIES.find((c) => c.slug === slug);
}
