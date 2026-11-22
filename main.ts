import { copyFileSync, mkdirSync } from 'node:fs';
import { join } from 'node:path';

const targetDir = process.env.MAKEFUN_OUTPUT_DIR ?? '/output';
mkdirSync(targetDir, { recursive: true });
copyFileSync(new URL('./entry.png', import.meta.url), join(targetDir, 'entry.png'));
