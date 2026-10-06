// ADD A NEW APP HERE. Drop screenshots in /public/apps/<slug>/ and add one entry below.
// Optional: public/og/<slug>.png (1200x630) for the share image, public/apps/<slug>/icon.png for the icon.

export type AppStatus = 'live' | 'beta' | 'in-development' | 'coming-soon';

export interface App {
  slug: string;
  name: string;
  tagline: string;
  description: string;
  status: AppStatus;
  version?: string;
  url?: string; // where the app lives (e.g. https://giftly.netlify.app)
  installable: boolean; // is it an installable PWA?
  platforms?: string; // small label on the detail page
  screenshots: { src: string; alt: string }[]; // 2-4 max
  features?: string[];
  why?: string; // optional "Why I built it" note on the detail page
  accent?: string; // icon background
}

const shots = (slug: string, name: string, n = 3) =>
  Array.from({ length: n }, (_, i) => ({
    src: `/apps/${slug}/screen-${i + 1}.webp`,
    alt: `${name} screenshot ${i + 1} (placeholder)`,
  }));

export const apps: App[] = [
  {
    slug: 'giftly',
    name: 'Giftly',
    tagline: 'Give better. Remember more.',
    description:
      'A year-round gift organizer for keeping track of people, ideas, budgets, and occasions.',
    status: 'beta',
    version: '0.9.0',
    url: 'https://giftly.netlify.app', // placeholder
    installable: true,
    platforms: 'iOS & Android · PWA',
    screenshots: shots('giftly', 'Giftly'),
    features: ['People & recipients', 'Gift ideas', 'Wishlists', 'Budgets & actuals', 'Purchase tracking', 'Occasions'],
    why: 'I wanted a better way to keep track of the people I love, the gifts they want, and the occasions that matter, without turning gifting into another chore.',
    accent: '#245274',
  },
  {
    slug: 'momntm',
    name: 'MOMNTM',
    tagline: 'Build momentum.',
    description:
      'A personal project and task system designed to help you focus on what matters next.',
    status: 'live',
    version: '1.4.0',
    url: 'https://momntm.netlify.app', // placeholder
    installable: true,
    platforms: 'iOS & Android · PWA',
    screenshots: shots('momntm', 'MOMNTM'),
    features: ['One clear next step', 'Projects & tasks', 'Daily focus', 'Works offline'],
    accent: '#111821',
  },
  {
    slug: 'ranch-manager',
    name: 'Ranch Manager',
    tagline: 'Everything in one place.',
    description: 'A simple, beautiful system for managing your ranch, livestock, and operations.',
    status: 'in-development',
    installable: false,
    platforms: 'Coming to iOS & Android',
    screenshots: shots('ranch-manager', 'Ranch Manager'),
    features: ['Livestock records', 'Pastures & rotation', 'Supplies', 'Tasks'],
    accent: '#4a5c3e',
  },
];

export const getApp = (slug: string) => apps.find((a) => a.slug === slug);
export const appNumber = (slug: string) =>
  String(apps.findIndex((a) => a.slug === slug) + 1).padStart(3, '0');
