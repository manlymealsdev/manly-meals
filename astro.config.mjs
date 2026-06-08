// @ts-check
import { defineConfig } from 'astro/config';
import tailwind from '@astrojs/tailwind';
import sitemap from '@astrojs/sitemap';

// IMPORTANT: change `site` to your real domain before deploying.
export default defineConfig({
  site: 'https://manly-meals.com',
  integrations: [tailwind(), sitemap()],
  build: {
    inlineStylesheets: 'auto',
  },
});
