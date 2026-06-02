import { defineCollection, z } from 'astro:content';

const recipes = defineCollection({
  type: 'content',
  schema: z.object({
    title: z.string(),
    description: z.string(),
    // Primary category MUST match a category name in src/data/categories.ts
    category: z.enum(['Beef', 'Chicken', 'Pork', 'Fish', 'Budget Meals', 'Meal Prep', 'Low Carb']),
    subcategory: z.string(),
    // A recipe can ALSO appear on these section pages (cross-listing)
    sections: z.array(z.enum(['Budget Meals', 'Meal Prep', 'Low Carb'])).default([]),
    // Budget page filter tags (only used when the recipe shows on Budget Meals)
    budgetFilters: z.array(z.string()).default([]),
    image: z.string(),
    imageAlt: z.string().default(''),
    prepTime: z.number(), // minutes
    cookTime: z.number(), // minutes
    servings: z.number(),
    macros: z.object({
      calories: z.number(),
      protein: z.number(), // grams
      carbs: z.number(), // grams
      fat: z.number(), // grams
    }),
    ingredients: z.array(
      z.object({
        qty: z.number().nullable().default(null), // null = "to taste" / no number
        unit: z.string().default(''),
        item: z.string(),
      })
    ),
    instructions: z.array(z.string()),
    isBudget: z.boolean().default(false),
    gear: z
      .array(z.object({ name: z.string(), note: z.string().default('') }))
      .default([]),
    pubDate: z.coerce.date(),
    featured: z.boolean().default(false),
  }),
});

export const collections = { recipes };
