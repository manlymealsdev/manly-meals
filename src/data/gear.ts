// -----------------------------------------------------------------------------
// Kitchen gear list. Replace the `url` placeholders with your real Amazon
// affiliate links (e.g. https://www.amazon.com/dp/XXXX?tag=YOURTAG-20).
// -----------------------------------------------------------------------------

export interface GearTier {
  label: 'Budget Option' | 'Solid / Mid-Tier' | 'Premium Option';
  name: string;
  price: string;
  url: string;
}

export interface GearItem {
  name: string;
  why: string;
  /** Affiliate link placeholder — swap in your tagged URL. */
  url: string;
  /** Rough price for planning, optional. */
  price?: string;
  /** Group it appears under on the Gear page. */
  group: string;
  /** Include in the Total Kitchen Starter Bundle? */
  bundle?: boolean;
  /** Optional 3-tier buying options for the most important items. */
  tiers?: GearTier[];
}

// -----------------------------------------------------------------------------
// CENTRAL affiliate tag. Change this in ONE place and every Amazon link on the
// site updates. `withAffiliateTag` guarantees the tag is present on any Amazon
// URL at render time — even if a future link is added without it.
// -----------------------------------------------------------------------------
export const AMAZON_TAG = 'manlymeals-20';

export function withAffiliateTag(url: string): string {
  if (!url || !/amazon\./i.test(url)) return url; // only touch Amazon links
  try {
    const u = new URL(url);
    u.searchParams.set('tag', AMAZON_TAG); // adds or overwrites ?tag=
    return u.toString();
  } catch {
    // Fallback if the URL can't be parsed
    if (/[?&]tag=/i.test(url)) return url.replace(/(tag=)[^&]*/i, `$1${AMAZON_TAG}`);
    return url + (url.includes('?') ? '&' : '?') + `tag=${AMAZON_TAG}`;
  }
}

/** Build a tagged Amazon search URL from a plain query string. */
export function amazonSearch(query: string): string {
  const k = encodeURIComponent(query.trim()).replace(/%20/g, '+');
  return `https://www.amazon.com/s?k=${k}&tag=${AMAZON_TAG}`;
}

export const GEAR: GearItem[] = [
  // --- Knives & Cutting ---
  {
    name: "8-inch Chef's Knife",
    why: 'The one knife that does 90% of the work.',
    url: 'https://www.amazon.com/Mercer-Culinary-Chefs-Knife-Ultimate/dp/B005P0OJ4S?tag=manlymeals-20',
    price: '~$15',
    group: 'Knives & Cutting',
    bundle: true,
    tiers: [
      { label: 'Budget Option', name: 'Mercer Culinary 8"', price: '~$15', url: 'https://www.amazon.com/Mercer-Culinary-Chefs-Knife-Ultimate/dp/B005P0OJ4S?tag=manlymeals-20' },
      { label: 'Solid / Mid-Tier', name: 'Victorinox Fibrox 8"', price: '~$51', url: 'https://www.amazon.com/Victorinox-Fibrox-Chefs-Knife-8-Inch/dp/B000638D32?tag=manlymeals-20' },
      { label: 'Premium Option', name: 'Wüsthof Classic 8"', price: '~$170', url: 'https://www.amazon.com/Wusthof-1040100120-Classic-8-Inch-Chefs/dp/B085V653KM?tag=manlymeals-20' },
    ],
  },
  {
    name: 'Plastic Cutting Board (set of 2)',
    why: 'One for raw meat, one for everything else. Dishwasher safe.',
    url: 'https://www.amazon.com/OXO-Grips-Utility-Cutting-Board/dp/B082WMNWFP?tag=manlymeals-20',
    price: '~$15',
    group: 'Knives & Cutting',
    bundle: true,
    tiers: [
      { label: 'Budget Option', name: 'OXO Good Grips Utility', price: '~$15', url: 'https://www.amazon.com/OXO-Grips-Utility-Cutting-Board/dp/B082WMNWFP?tag=manlymeals-20' },
      { label: 'Solid / Mid-Tier', name: 'Epicurean Composite', price: '~$25', url: 'https://www.amazon.com/Epicurean-Cutting-Non-Slip-14-5-Inch-11-25-Inch/dp/B08WBNQ3Q3?tag=manlymeals-20' },
      { label: 'Premium Option', name: 'John Boos Maple Block', price: '~$90', url: 'https://www.amazon.com/John-Boos-R03-Reversible-Cutting/dp/B0000CFV4K?tag=manlymeals-20' },
    ],
  },
  {
    name: 'Paring Knife',
    why: 'Small blade for the close work: garlic, peeling, trimming, deveining.',
    url: 'https://www.amazon.com/Cuisinart-C77TR-3PR-Triple-Collection-Paring/dp/B06XYN4YFC?tag=manlymeals-20',
    price: '~$10',
    group: 'Knives & Cutting',
  },

  // --- Cookware ---
  {
    name: '12-inch Cast Iron Skillet',
    why: 'Sears steak, fries eggs, lasts forever. The MVP of the kitchen.',
    url: 'https://www.amazon.com/Lodge-Seasoned-Cast-Iron-Skillet/dp/B00006JSUB?tag=manlymeals-20',
    price: '~$30',
    group: 'Cookware',
    bundle: true,
    tiers: [
      { label: 'Budget Option', name: 'Lodge 12" Cast Iron', price: '~$30', url: 'https://www.amazon.com/Lodge-Seasoned-Cast-Iron-Skillet/dp/B00006JSUB?tag=manlymeals-20' },
      { label: 'Solid / Mid-Tier', name: 'Lodge Chef Collection 12"', price: '~$45', url: 'https://www.amazon.com/Lodge-Chef-Collection-Chef-Style-Skillet/dp/B07Z6TV9Y7?tag=manlymeals-20' },
      { label: 'Premium Option', name: 'Stargazer 12"', price: '~$145', url: 'https://www.amazon.com/Stargazer-12-Inch-Cast-Iron/dp/B0CB75WJZP?tag=manlymeals-20' },
    ],
  },
  {
    name: 'Stainless Steel Frying Pan',
    why: 'For eggs and anything delicate where cast iron is overkill.',
    url: 'https://www.amazon.com/Tramontina-Stainless-Induction-Ready-Dishwasher-Safe-NSF-Certified/dp/B096MWCS6L?tag=manlymeals-20',
    price: '~$40',
    group: 'Cookware',
    bundle: true,
    tiers: [
      { label: 'Budget Option', name: 'Tramontina 12" Tri-Ply', price: '~$40', url: 'https://www.amazon.com/Tramontina-Stainless-Induction-Ready-Dishwasher-Safe-NSF-Certified/dp/B096MWCS6L?tag=manlymeals-20' },
      { label: 'Solid / Mid-Tier', name: 'Cuisinart MultiClad Pro 12"', price: '~$70', url: 'https://www.amazon.com/Cuisinart-722-30G-Classic-12-Inch-Skillet/dp/B0078P9D8U?tag=manlymeals-20' },
      { label: 'Premium Option', name: 'All-Clad D3 12"', price: '~$160', url: 'https://www.amazon.com/All-Clad-Dishwasher-Stainless-Cookware-Silver/dp/B00FUF5K8W?tag=manlymeals-20' },
    ],
  },
  {
    name: '6-Quart Slow Cooker',
    why: 'Dump ingredients in the morning, eat dinner with zero effort.',
    url: 'https://www.amazon.com/s?k=crock+pot+6+quart+manual+slow+cooker&tag=manlymeals-20',
    price: '~$40',
    group: 'Cookware',
    bundle: true,
    tiers: [
      { label: 'Budget Option', name: 'Crock-Pot 6qt Manual', price: '~$35', url: 'https://www.amazon.com/s?k=crock+pot+6+quart+manual+slow+cooker&tag=manlymeals-20' },
      { label: 'Solid / Mid-Tier', name: 'Hamilton Beach Programmable', price: '~$50', url: 'https://www.amazon.com/s?k=hamilton+beach+programmable+slow+cooker+6+quart&tag=manlymeals-20' },
      { label: 'Premium Option', name: 'Instant Pot Multi-Cooker', price: '~$100', url: 'https://www.amazon.com/s?k=instant+pot+duo+multi+cooker&tag=manlymeals-20' },
    ],
  },
  {
    name: 'Heavy Sheet Pan (2-pack)',
    why: 'Sheet-pan dinners and meal prep. Cheap and endlessly useful.',
    url: 'https://www.amazon.com/s?k=nordic+ware+half+sheet+pan+2+pack&tag=manlymeals-20',
    price: '~$25',
    group: 'Cookware',
    bundle: true,
    tiers: [
      { label: 'Budget Option', name: 'Nordic Ware Half Sheet (2)', price: '~$25', url: 'https://www.amazon.com/s?k=nordic+ware+half+sheet+pan+2+pack&tag=manlymeals-20' },
      { label: 'Solid / Mid-Tier', name: 'USA Pan Aluminized Steel', price: '~$40', url: 'https://www.amazon.com/s?k=usa+pan+aluminized+steel+half+sheet+pan&tag=manlymeals-20' },
      { label: 'Premium Option', name: 'Williams Sonoma Goldtouch', price: '~$60', url: 'https://www.amazon.com/s?k=williams+sonoma+goldtouch+half+sheet+pan&tag=manlymeals-20' },
    ],
  },
  {
    name: 'Medium Saucepan with Lid',
    why: 'Rice, pasta, soups, sauces. You need exactly one good one.',
    url: 'https://www.amazon.com/s?k=stainless+steel+saucepan+with+lid+3+quart&tag=manlymeals-20',
    price: '~$25',
    group: 'Cookware',
  },

  // --- Tools & Gadgets ---
  {
    name: 'Instant-Read Meat Thermometer',
    why: 'The single best tool for not ruining meat. Stop guessing.',
    url: 'https://www.amazon.com/s?k=thermopro+instant+read+meat+thermometer&tag=manlymeals-20',
    price: '~$15',
    group: 'Tools & Gadgets',
    bundle: true,
    tiers: [
      { label: 'Budget Option', name: 'ThermoPro TP-19', price: '~$15', url: 'https://www.amazon.com/s?k=thermopro+tp19+instant+read+thermometer&tag=manlymeals-20' },
      { label: 'Solid / Mid-Tier', name: 'ThermoPop 2', price: '~$35', url: 'https://www.amazon.com/s?k=thermoworks+thermopop+2+thermometer&tag=manlymeals-20' },
      { label: 'Premium Option', name: 'Thermapen ONE', price: '~$105', url: 'https://www.amazon.com/s?k=thermapen+one+instant+read+thermometer&tag=manlymeals-20' },
    ],
  },
  {
    name: 'Stainless Steel Tongs',
    why: 'Locking, spring-loaded, dishwasher safe. Grab, flip, and plate anything.',
    url: 'https://www.amazon.com/s?k=stainless+steel+locking+tongs+kitchen&tag=manlymeals-20',
    price: '~$12',
    group: 'Tools & Gadgets',
    bundle: true,
  },
  {
    name: 'Fish Spatula',
    why: 'Thin and flexible. Best flipper for fish, burgers, and eggs.',
    url: 'https://www.amazon.com/s?k=fish+spatula+stainless+steel&tag=manlymeals-20',
    price: '~$12',
    group: 'Tools & Gadgets',
  },
  {
    name: 'Sturdy Skillet Spatula',
    why: 'Stiff, wide metal blade for smashing burgers and scraping the fond.',
    url: 'https://www.amazon.com/s?k=smash+burger+spatula+metal&tag=manlymeals-20',
    price: '~$12',
    group: 'Tools & Gadgets',
  },
  {
    name: 'Collapsible Colander',
    why: 'Drains pasta and rinses veg, then folds flat to save drawer space.',
    url: 'https://www.amazon.com/s?k=collapsible+silicone+colander+strainer&tag=manlymeals-20',
    price: '~$15',
    group: 'Tools & Gadgets',
  },
  {
    name: 'Oven Mitts / Pit Mat',
    why: 'Heavy heat-proof grips for cast iron handles and hot grates. No floral prints.',
    url: 'https://www.amazon.com/s?k=heat+resistant+oven+mitts&tag=manlymeals-20',
    price: '~$18',
    group: 'Tools & Gadgets',
  },
  {
    name: 'Cast Iron Cleaner',
    why: 'Chainmail scrubber or stiff brush to clean cast iron without killing the seasoning.',
    url: 'https://www.amazon.com/s?k=cast+iron+chainmail+scrubber&tag=manlymeals-20',
    price: '~$10',
    group: 'Tools & Gadgets',
  },
  {
    name: 'Mixing Bowl Set',
    why: 'Marinating, mixing, and prep. Nesting set saves space.',
    url: 'https://www.amazon.com/s?k=stainless+steel+mixing+bowls+set&tag=manlymeals-20',
    price: '~$20',
    group: 'Tools & Gadgets',
    bundle: true,
  },
  {
    name: 'Measuring Cups & Spoons',
    why: 'Until you can eyeball it, measure it. Cheap insurance.',
    url: 'https://www.amazon.com/s?k=stainless+steel+measuring+cups+and+spoons+set&tag=manlymeals-20',
    price: '~$10',
    group: 'Tools & Gadgets',
    bundle: true,
  },

  // --- Storage & Prep ---
  {
    name: 'Glass Meal Prep Containers (10-pack)',
    why: 'Microwave and dishwasher safe. The backbone of meal prep.',
    url: 'https://www.amazon.com/s?k=glass+meal+prep+containers+10+pack&tag=manlymeals-20',
    price: '~$35',
    group: 'Storage & Prep',
    bundle: true,
    tiers: [
      { label: 'Budget Option', name: 'Prep Naturals Glass (10)', price: '~$35', url: 'https://www.amazon.com/s?k=prep+naturals+glass+meal+prep+containers+10+pack&tag=manlymeals-20' },
      { label: 'Solid / Mid-Tier', name: 'Pyrex Simply Store Set', price: '~$50', url: 'https://www.amazon.com/s?k=pyrex+simply+store+glass+container+set&tag=manlymeals-20' },
      { label: 'Premium Option', name: 'Glasslock 18-Piece Set', price: '~$70', url: 'https://www.amazon.com/s?k=glasslock+18+piece+glass+container+set&tag=manlymeals-20' },
    ],
  },
  {
    name: 'Freezer Storage Bags',
    why: 'Portion and freeze. Label them so you actually use them.',
    url: 'https://www.amazon.com/s?k=freezer+storage+bags+gallon&tag=manlymeals-20',
    price: '~$12',
    group: 'Storage & Prep',
  },
  {
    name: 'Parchment Paper',
    why: 'Line sheet pans for no-stick roasting and zero scrubbing afterward.',
    url: 'https://www.amazon.com/s?k=parchment+paper+baking+sheets&tag=manlymeals-20',
    price: '~$8',
    group: 'Storage & Prep',
  },
];

/** Items included in the Total Kitchen Starter Bundle. */
export const BUNDLE = GEAR.filter((g) => g.bundle);

/** Unique group names, in first-seen order. */
export const GEAR_GROUPS = [...new Set(GEAR.map((g) => g.group))];

export const AFFILIATE_DISCLOSURE =
  'As an Amazon Associate, I earn from qualifying purchases.';
