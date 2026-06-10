const fs = require('fs');
const path = require('path');

// Scan for sorry that might be easy to fill
const dirs = ['SylvaFormalization', '.'];
const easyPatterns = [
  { name: 'True goal', regex: /:=\s*True\s*:=\s*by\s*\n\s*sorry/ },
  { name: 'Trivial goal after simp', regex: /simp\s*\n\s*sorry/ },
  { name: 'rfl', regex: /rfl\s*--/ },
  { name: 'obvious', regex: /trivial|linarith|omega|norm_num| positivity/ }
];

for (const dir of dirs) {
  const files = fs.readdirSync(dir).filter(f => f.endsWith('.lean') && !f.includes('_amputated') && !f.includes('_filled') && !f.includes('_fixed') && !f.includes('_final') && !f.includes('.bak.'));
  for (const file of files) {
    const content = fs.readFileSync(path.join(dir, file), 'utf-8');
    const lines = content.split('\n');
    for (let i = 0; i < lines.length; i++) {
      const code = lines[i].split('--')[0];
      if (/\bsorry\b/.test(code)) {
        // Check context
        const context = lines.slice(Math.max(0, i-3), i+1).join('\n');
        console.log('--- ' + dir + '/' + file + ' line ' + (i+1) + ' ---');
        console.log(context);
        console.log('');
      }
    }
  }
}
