import { copyFileSync, mkdirSync } from 'node:fs';
import { join } from 'node:path';

// Output directory defined by make.fun container harness or default /output
const targetDir = process.env.MAKEFUN_OUTPUT_DIR ?? '/output';
mkdirSync(targetDir, { recursive: true });
copyFileSync(new URL('./entry.png', import.meta.url), join(targetDir, 'entry.png'));
console.log('Successfully delivered 1024x1024 entry.png broadsheet to', targetDir);
