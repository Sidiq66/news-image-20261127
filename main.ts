// THE DAILY GLOBE — news-image-20261127 entry (Node 22, standard library only).
// The front page is the entry.png beside this file; the program copies it to
// /output/entry.png (or $MAKEFUN_OUTPUT_DIR when set, for local runs):
//   mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts

import { copyFileSync, readFileSync, statSync } from 'node:fs';
import { join } from 'node:path';
import { fileURLToPath } from 'node:url';

const SRC = fileURLToPath(new URL('./entry.png', import.meta.url));
const DEST = join(process.env.MAKEFUN_OUTPUT_DIR ?? '/output', 'entry.png');

// The gate takes a whole PNG of at most 1 MiB and 1024 by 1024 pixels;
// refuse to hand over anything that breaks those limits.
copyFileSync(SRC, DEST);

// Read width and height straight from the PNG header (IHDR chunk):
// bytes 16..19 are the width, 20..23 the height, both big-endian.
function pngSize(path: string): { width: number; height: number } {
  const buf = readFileSync(path);
  if (buf.length < 24 || buf.readUInt32BE(12) !== 0x49484452) {
    throw new Error('entry.png is not a PNG file');
  }
  return { width: buf.readUInt32BE(16), height: buf.readUInt32BE(20) };
}

const bytes = statSync(DEST).size;
if (bytes > 1048576) {
  throw new Error(`entry.png is ${bytes} bytes, over the 1 MiB limit`);
}
const { width, height } = pngSize(DEST);
if (width > 1024 || height > 1024) {
  throw new Error(`entry.png is ${width}x${height}, over the 1024x1024 limit`);
}
console.log(`wrote ${DEST} (${bytes} bytes, ${width}x${height})`);

// The picture itself: THE DAILY GLOBE for Friday 27 November 2026 —
// Trump says Putin wants a deal; New Zealand's official count leaves a
// hung parliament; the Thanksgiving storm's aftermath; SAP's 10,000 job
// cuts; and the Bears' last-seconds 39–35 win over the Lions. Drawn by
// build_image.py (PIL, no photographs, no downloaded assets); every fact
// was checked against at least two news sources (see NEWS_BRIEF_27NOV.md
// in the workspace, not shipped here).
