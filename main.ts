// news-image-20261119 entry. Node 22, standard library only.
//
// The front page for Thursday 19 November 2026 is already drawn:
// render.py (Pillow, deterministic, no network) produced entry.png.
// All this program does is place a copy in the grader's output
// directory, so repeated runs write byte-identical files.
//
// Local run: mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts

import { copyFileSync, mkdirSync } from "node:fs";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";

// The folder this file lives in — entry.png sits beside it.
const sourceDir = dirname(fileURLToPath(import.meta.url));

function deliver() {
  const outDir = process.env.MAKEFUN_OUTPUT_DIR ?? "/output";
  mkdirSync(outDir, { recursive: true });
  copyFileSync(join(sourceDir, "entry.png"), join(outDir, "entry.png"));
}

deliver();
