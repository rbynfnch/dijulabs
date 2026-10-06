import { SITE } from '../data/site';
export const GET = () => new Response(`User-agent: *\nAllow: /\n\nSitemap: ${SITE.url}/sitemap.xml\n`);
