node -e "const fs=require('fs');console.log('cwd :',process.cwd());console.log('real:',fs.realpathSync.native(process.cwd()));console.log('tests:',fs.readdirSync('tests'))"
