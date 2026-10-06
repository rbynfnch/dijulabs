import { defineConfig } from 'astro/config';
import { SITE } from './src/data/site.ts';

export default defineConfig({
  site: SITE.url,
  output: 'static',
  trailingSlash: 'never',
  build: { format: 'file' },
});
