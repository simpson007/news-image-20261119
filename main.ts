import { copyFile, mkdir } from "node:fs/promises";
import { dirname, join, resolve } from "node:path";
import { fileURLToPath } from "node:url";

// The finished front page this repository holds, next to this file.
const source = resolve(dirname(fileURLToPath(import.meta.url)), "entry.png");

// The harness hands the entry its output directory through the
// environment; locally it defaults to /output, as the rules describe.
const outDir = process.env.MAKEFUN_OUTPUT_DIR ?? "/output";

// Put the picture where the judge will look for it, then say where
// it landed so a local run is easy to confirm by eye.
async function placeEntry(): Promise<string> {
  const target = join(outDir, "entry.png");
  await mkdir(outDir, { recursive: true });
  await copyFile(source, target);
  return target;
}

const placed = await placeEntry();
console.log(`entry.png -> ${placed}`);
