node -e "const fs=require('fs');console.log('cwd :',process.cwd());console.log('real:',fs.realpathSync.native(process.cwd()));console.log('tests:',fs.readdirSync('tests'))"

import { defineConfig } from '@playwright/test';

export default defineConfig({
  testDir: './tests',
});
npx playwright test --config=debug.config.ts --list
npx playwright --version
npm ls @playwright/test playwright

node -e "require('fs').readdirSync('tests',{withFileTypes:true}).forEach(d=>console.log(d.name,'file:',d.isFile(),'dir:',d.isDirectory(),'link:',d.isSymbolicLink()))"


// Workaround: OneDrive files show up as symlinks to Node, so Playwright skips them.
import * as fs from 'fs';
import * as path from 'path';

const proto = fs.Dirent.prototype as any;
const origIsFile = proto.isFile;
const origIsDir = proto.isDirectory;
const origIsLink = proto.isSymbolicLink;

function target(d: any): fs.Stats | undefined {
  try {
    return fs.statSync(path.join(d.parentPath ?? d.path, d.name));
  } catch {
    return undefined;
  }
}

proto.isFile = function () {
  if (origIsFile.call(this)) return true;
  return origIsLink.call(this) && !!target(this)?.isFile();
};
proto.isDirectory = function () {
  if (origIsDir.call(this)) return true;
  return origIsLink.call(this) && !!target(this)?.isDirectory();
};
proto.isSymbolicLink = function () {
  return origIsLink.call(this) && !target(this);
};
