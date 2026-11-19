// news-image-20261119 entry. Node 22, standard library only.
//
// entry.png is the finished front page for Thursday 19 November 2026,
// drawn ahead of time by render.py (Pillow, deterministic, no network).
// This program only copies it to the grader's output directory, so two
// runs write byte-identical files.
//
// Local run: mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts

import { copyFileSync, mkdirSync } from "node:fs";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";

const here = dirname(fileURLToPath(import.meta.url));
const target = process.env.MAKEFUN_OUTPUT_DIR ?? "/output";
mkdirSync(target, { recursive: true });
copyFileSync(join(here, "entry.png"), join(target, "entry.png"));
