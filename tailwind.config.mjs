/** @type {import('tailwindcss').Config} */
export default {
  content: ['./src/**/*.{astro,html,js,jsx,md,mdx,ts,tsx,vue}'],
  theme: {
    extend: {
      colors: {
        // Core brand palette
        header: '#1C2526', // sticky top bar / header
        card: '#2E2E2E', // cards & panels
        accent: '#BE6600', // burnt-copper accent
        'accent-bright': '#E07B0B', // hover state for accent
        ink: '#E7DCCF', // primary text (warm cream)
        // Support shades
        coal: '#161A1B', // page background (slightly darker than header)
        'coal-2': '#1F2526', // alternating section background
        line: '#3A3F40', // hairline borders
        muted: '#9A958C', // secondary / muted text
      },
      fontWeight: {
        // Allow numeric utility classes (font-600 / font-700) alongside defaults
        600: '600',
        700: '700',
      },
      fontFamily: {
        // Heavy condensed display for big headlines
        display: ['Anton', 'Impact', 'sans-serif'],
        // Condensed heading font
        heading: ['"Barlow Condensed"', 'sans-serif'],
        // Clean technical body font
        body: ['Barlow', 'system-ui', 'sans-serif'],
      },
      maxWidth: {
        content: '1200px',
        prose: '720px',
      },
      boxShadow: {
        card: '0 8px 24px rgba(0,0,0,0.45)',
        'card-hover': '0 16px 40px rgba(0,0,0,0.6)',
      },
      borderRadius: {
        xl2: '1.25rem',
      },
      keyframes: {
        'fade-up': {
          '0%': { opacity: '0', transform: 'translateY(16px)' },
          '100%': { opacity: '1', transform: 'translateY(0)' },
        },
      },
      animation: {
        'fade-up': 'fade-up 0.6s ease-out both',
      },
    },
  },
  plugins: [],
};
