// THE WORLD TODAY — Friday 20 November 2026 (Node 22, standard library only).
//
// The entry image is drawn by gen_image.py and committed as entry.png beside
// this file. This program just hands it to the grader: it creates the output
// directory when it is missing and copies the image there, byte for byte.
//
// Run it locally with:
//   mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts

import { copyFileSync, mkdirSync } from 'node:fs';
import { dirname, join } from 'node:path';
import { fileURLToPath } from 'node:url';

const here = dirname(fileURLToPath(import.meta.url));
const outDir = process.env.MAKEFUN_OUTPUT_DIR ?? '/output';
const target = join(outDir, 'entry.png');

mkdirSync(outDir, { recursive: true });
copyFileSync(join(here, 'entry.png'), target);
