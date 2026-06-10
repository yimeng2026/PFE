const fs = require('fs');
const path = require('path');

function findSorryInFile(filePath) {
  const content = fs.readFileSync(filePath, 'utf-8');
  const lines = content.split('\n');
  let inBlockComment = false;
  const results = [];
  
  for (let i = 0; i < lines.length; i++) {
    let line = lines[i];
    
    // Handle block comments
    if (inBlockComment) {
      const endIdx = line.indexOf('-/');
      if (endIdx >= 0) {
        line = line.substring(endIdx + 2);
        inBlockComment = false;
      } else {
        continue;
      }
    }
    
    // Check for block comment start
    let idx = 0;
    while (true) {
      const startIdx = line.indexOf('/-', idx);
      if (startIdx >= 0) {
        const endIdx = line.indexOf('-/', startIdx);
        if (endIdx >= 0) {
          line = line.substring(0, startIdx) + line.substring(endIdx + 2);
          idx = startIdx;
        } else {
          line = line.substring(0, startIdx);
          inBlockComment = true;
          break;
        }
      } else {
        break;
      }
    }
    
    if (inBlockComment) continue;
    
    // Remove line comments
    const commentIdx = line.indexOf('--');
    if (commentIdx >= 0) {
      line = line.substring(0, commentIdx);
    }
    
    // Remove string literals
    line = line.replace(/"[^"]*"/g, '""');
    
    if (/\bsorry\b/.test(line)) {
      results.push({line: i+1, text: lines[i].trim()});
    }
  }
  
  return results;
}

const dir = 'SylvaFormalization';
const files = fs.readdirSync(dir).filter(f => f.endsWith('.lean') && !f.includes('_amputated') && !f.includes('_filled') && !f.includes('_fixed') && !f.includes('_final') && !f.includes('.bak.'));

for (const file of files.sort()) {
  const results = findSorryInFile(path.join(dir, file));
  if (results.length > 0) {
    console.log('File: ' + file);
    console.log('  Count: ' + results.length);
    for (const r of results) {
      console.log('  Line ' + r.line + ': ' + r.text);
    }
    console.log('');
  }
}
