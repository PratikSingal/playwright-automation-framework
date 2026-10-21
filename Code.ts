node -e "const fs=require('fs');console.log('cwd :',process.cwd());console.log('real:',fs.realpathSync.native(process.cwd()));console.log('tests:',fs.readdirSync('tests'))"

import { defineConfig } from '@playwright/test';

export default defineConfig({
  testDir: './tests',
});
npx playwright test --config=debug.config.ts --list
npx playwright --version
npm ls @playwright/test playwright

node -e "require('fs').readdirSync('tests',{withFileTypes:true}).forEach(d=>console.log(d.name,'file:',d.isFile(),'dir:',d.isDirectory(),'link:',d.isSymbolicLink()))"
