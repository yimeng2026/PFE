// Amputate Lean files - replace proof bodies with sorry
// Usage: node amputate_lean.js

const fs = require('fs');
const path = require('path');

const BASE_DIR = 'C:\\Users\\一梦\\.kimi_openclaw\\workspace\\sylva_formalization';

// Directories to exclude
const EXCLUDE_DIRS = [
  'lake',
  'backup',
  'backup_20260423',
  'root_lean_backup',
  '.git',
  'build',
  'lean_packages'
];

// Files to exclude (already amputated, filled, fixed, etc.)
const EXCLUDE_PATTERNS = [
  /_amputated\.lean$/,
  /_filled\.lean$/,
  /_fixed\.lean$/,
  /_final\.lean$/,
  /_completed\.lean$/,
  /_simplified\.lean$/,
  /_restored\.lean$/,
  /_new_lemmas\.lean$/,
  /_new_header\.lean$/,
  /_bak\.lean$/,
  /_v[0-9]+\.lean$/,
  /_deep_amputated\.lean$/,
  /_continue\.lean$/,
  /_stage1\.lean$/,
  /_interface\.lean$/,
  /_backup\.lean$/,
  /lakefile\.lean$/
];

function shouldExclude(filePath) {
  const normalized = filePath.replace(/\\/g, '/');
  for (const dir of EXCLUDE_DIRS) {
    if (normalized.includes('/' + dir + '/')) return true;
    if (normalized.endsWith('/' + dir)) return true;
  }
  for (const pattern of EXCLUDE_PATTERNS) {
    if (pattern.test(filePath)) return true;
  }
  return false;
}

function findLeanFiles(dir, files = []) {
  const entries = fs.readdirSync(dir, { withFileTypes: true });
  for (const entry of entries) {
    const fullPath = path.join(dir, entry.name);
    if (entry.isDirectory()) {
      if (!shouldExclude(fullPath)) {
        findLeanFiles(fullPath, files);
      }
    } else if (entry.name.endsWith('.lean')) {
      if (!shouldExclude(fullPath)) {
        files.push(fullPath);
      }
    }
  }
  return files;
}

// Keywords that start declarations at the top level
const DECLARATION_KEYWORDS = [
  'theorem ', 'lemma ', 'def ', 'structure ', 'inductive ', 'class ', 'instance ',
  'abbrev ', 'macro ', 'syntax ', 'declare_syntax_cat ', 'infix ', 'infixl ',
  'infixr ', 'prefix ', 'postfix ', 'notation ', 'section ', 'namespace ', 'end ',
  'open ', 'export ', 'variable ', 'variables ', 'universe ', 'universes ',
  'set_option ', 'attribute ', '@[', '#check ', '#eval ', '#reduce ', 'axiom ',
  'opaque ', 'partial ', 'private ', 'protected ', 'mutual ', 'noncomputable ',
  'abbreviation ', 'local ', 'scoped ', 'macro_rules ', 'deriving ', 'where ',
  'example ', 'elab ', 'elab_rules ', 'defun ', 'theorem! ', 'lemma! ',
  'have ', 'suffices ', 'show ', 'let ', 'letI ', 'letI ', 'letR ', 'match ',
  'if ', 'try ', 'all_goals ', 'any_goals ', 'focus ', 'calc ', 'cases ',
  'rcases ', 'obtain ', 'intro ', 'intros ', 'rintro ', 'rename_i ', 'revert ',
  'clear ', 'subst ', 'subst_vars ', 'induction ', 'generalize ', 'specialize ',
  'apply ', 'exact ', 'refine ', 'refine' , 'use ', 'existsi ', 'constructor ',
  'split ', 'left ', 'right ', 'rfl ', 'simp ', 'simpa ', 'dsimp ', ' dsimpa ',
  'unfold ', 'delta ', 'change ', 'convert ', 'congr ', 'congr! ', 'ring ',
  'ring_nf ', 'linarith ', 'nlinarith ', 'omega ', 'norm_num ', 'norm_cast ',
  'push_neg ', 'by_contra ', 'by_cases ', 'contradiction ', 'exfalso ', 'tauto ',
  'aesop ', 'finish ', 'solve_by_elim ', 'decide ', 'native_decide ', 'trivial ',
  'rfl', 'omega', 'aesop', 'tauto', 'nlinarith', 'linarith', 'ring', 'norm_num',
  'simp', 'dsimp', 'unfold', 'delta', 'change', 'convert', 'congr', 'congr!',
  'refine', 'refine', 'apply', 'exact', 'use', 'constructor', 'split', 'left',
  'right', 'intro', 'intros', 'rintro', 'rename_i', 'revert', 'clear', 'subst',
  'subst_vars', 'induction', 'generalize', 'specialize', 'rcases', 'obtain',
  'cases', 'all_goals', 'any_goals', 'focus', 'calc', 'have', 'suffices',
  'show', 'let', 'letI', 'letR', 'match', 'if', 'try', 'native_decide',
  'solve_by_elim', 'decide', 'trivial', 'contradiction', 'exfalso',
  'push_neg', 'by_contra', 'by_cases'
];

// Simple keywords that indicate the start of a new declaration or section
const TOP_LEVEL_STARTERS = [
  'theorem ', 'lemma ', 'def ', 'structure ', 'inductive ', 'class ', 'instance ',
  'abbrev ', 'macro ', 'syntax ', 'notation ', 'section ', 'namespace ', 'end ',
  'open ', 'export ', 'variable ', 'universe ', 'set_option ', 'attribute ',
  '@[', '#check ', '#eval ', '#reduce ', 'axiom ', 'opaque ', 'noncomputable ',
  'abbreviation ', 'local ', 'scoped ', 'example ', 'elab ', 'import ', '-- ',
  '/- ', 'deriving ', 'where ', 'macro_rules ', 'infix ', 'infixl ', 'infixr ',
  'prefix ', 'postfix ', 'declare_syntax_cat ', 'private ', 'protected ', 'mutual '
];

function isTopLevelStarter(line) {
  const trimmed = line.trimStart();
  if (trimmed === '') return false;
  for (const starter of TOP_LEVEL_STARTERS) {
    if (trimmed.startsWith(starter)) return true;
  }
  return false;
}

function getIndent(line) {
  const match = line.match(/^(\s*)/);
  return match ? match[1].length : 0;
}

function isProofDeclaration(line) {
  const trimmed = line.trim();
  // Match theorem/lemma declarations
  const isDecl = /^(theorem|lemma)\s+/.test(trimmed);
  if (!isDecl) return false;
  // Check if it has a proof body indicator
  return trimmed.includes(':=');
}

function isTrivialProofBody(line) {
  const trimmed = line.trim();
  // Single-line trivial proofs we should keep
  const trivialPatterns = [
    /^:=\s*by\s*trivial\s*$/,
    /^:=\s*by\s*rfl\s*$/,
    /^:=\s*by\s*simp\s*$/,
    /^:=\s*by\s*norm_num\s*$/,
    /^:=\s*by\s*linarith\s*$/,
    /^:=\s*by\s*nlinarith\s*$/,
    /^:=\s*by\s*ring\s*$/,
    /^:=\s*by\s*omega\s*$/,
    /^:=\s*by\s*decide\s*$/,
    /^:=\s*by\s*exact\s+\w+\s*$/,
    /^:=\s*by\s*apply\s+\w+\s*$/,
    /^:=\s*by\s*exact\s+\w+\.\w+\s*$/,
    /^:=\s*by\s*refine\s*$/,
    /^:=\s*by\s*refine'\s*$/,
    /^:=\s*by\s*aesop\s*$/,
    /^:=\s*by\s*exfalso\s*$/,
    /^:=\s*by\s*contradiction\s*$/,
    /^:=\s*\w+\s*$/,
    /^:=\s*true\s*$/,
    /^:=\s*false\s*$/,
    /^:=\s*0\s*$/,
    /^:=\s*1\s*$/,
    /^:=\s*\{\s*\}\s*$/,
    /^:=\s*\[\s*\]\s*$/,
    /^:=\s*fun\s+.*=>\s*.+\s*$/,
    /^:=\s*fun\s+.*\mapsto\s*.+\s*$/,
    /^:=\s*λ\s+.*=>\s*.+\s*$/,
    /^:=\s*λ\s+.*\mapsto\s*.+\s*$/,
    /^:=\s*id\s*$/,
    /^:=\s*rfl\s*$/,
    /^:=\s*by\s*simpa\s*$/,
    /^:=\s*by\s*simp_all\s*$/,
    /^:=\s*by\s*assumption\s*$/,
    /^:=\s*by\s*infer_instance\s*$/,
    /^:=\s*by\s*finish\s*$/,
    /^:=\s*by\s*clarify\s*$/,
    /^:=\s*by\s*obviously\s*$/,
    /^:=\s*by\s*solve_by_elim\s*$/,
    /^:=\s*by\s*native_decide\s*$/,
    /^:=\s*by\s*compare\s*$/,
    /^:=\s*by\s*cc\s*$/,
    /^:=\s*by\s*ac_rfl\s*$/,
    /^:=\s*by\s*positivity\s*$/,
    /^:=\s*by\s*field_simp\s*$/,
    /^:=\s*by\s*group\s*$/,
    /^:=\s*by\s*abel\s*$/,
    /^:=\s*by\s*polyrith\s*$/,
    /^:=\s*by\s*linear_combination\s*$/,
    /^:=\s*by\s*rewrite_search\s*$/,
    /^:=\s*by\s*hint\s*$/,
    /^:=\s*by\s*try\s*\{\s*trivial\s*\}\s*$/,
    /^:=\s*by\s*try\s*\{\s*rfl\s*\}\s*$/,
    /^:=\s*by\s*try\s*\{\s*simp\s*\}\s*$/,
    /^:=\s*by\s*try\s*\{\s*norm_num\s*\}\s*$/,
    /^:=\s*by\s*try\s*\{\s*linarith\s*\}\s*$/,
    /^:=\s*by\s*try\s*\{\s*nlinarith\s*\}\s*$/,
    /^:=\s*by\s*try\s*\{\s*ring\s*\}\s*$/,
    /^:=\s*by\s*try\s*\{\s*omega\s*\}\s*$/,
    /^:=\s*by\s*try\s*\{\s*decide\s*\}\s*$/,
  ];
  for (const pattern of trivialPatterns) {
    if (pattern.test(trimmed)) return true;
  }
  return false;
}

function isMultiLineProofStart(line) {
  const trimmed = line.trim();
  // Theorem/lemma with := by at the end
  return /^(theorem|lemma)\s+.*:=\s*by\s*$/.test(trimmed);
}

function isTheoremOrLemmaWithProof(line) {
  const trimmed = line.trim();
  return /^(theorem|lemma)\s+.*:=\s+/.test(trimmed) && !isTrivialProofBody(line);
}

function amputateFile(content, fileName) {
  const lines = content.split('\n');
  const result = [];
  let inProof = false;
  let proofIndent = -1;
  let sorryCount = 0;
  let proofStartLine = -1;

  for (let i = 0; i < lines.length; i++) {
    const line = lines[i];
    const trimmed = line.trim();
    const indent = getIndent(line);

    if (inProof) {
      // Check if we've exited the proof
      // We exit when we see a line at the same or lower indentation
      // that's a top-level declaration starter
      if (trimmed !== '' && indent <= proofIndent) {
        // Check if this is a continuation or a new declaration
        if (isTopLevelStarter(line)) {
          // Exit the proof
          inProof = false;
          result.push(line);
          continue;
        }
      }

      // Skip all lines inside the proof body
      continue;
    }

    // Not in a proof - check if this line starts a theorem/lemma with a proof body
    const isDecl = /^(theorem|lemma)\s+/.test(trimmed);
    if (isDecl) {
      // Check if this declaration line has a trivial proof body
      if (isTrivialProofBody(line)) {
        // Keep trivial proofs
        result.push(line);
      } else if (isMultiLineProofStart(line)) {
        // Multi-line proof: theorem foo : Type := by
        result.push(line);
        inProof = true;
        proofIndent = indent;
        proofStartLine = i;
        // Add sorry at the next indentation level
        const sorryLine = ' '.repeat(proofIndent + 2) + 'sorry  -- AMPUTATED: proof body replaced';
        result.push(sorryLine);
        sorryCount++;
      } else if (isTheoremOrLemmaWithProof(line)) {
        // Single-line non-trivial proof: theorem foo : Type := expr
        // We need to replace the proof body
        const match = line.match(/^(\s*(?:theorem|lemma)\s+[^:]+)(\s*:=\s*.*)$/);
        if (match) {
          const prefix = match[1];
          result.push(prefix + ' := by');
          const sorryLine = ' '.repeat(indent + 2) + 'sorry  -- AMPUTATED: proof body replaced';
          result.push(sorryLine);
          sorryCount++;
        } else {
          result.push(line);
        }
      } else {
        // No proof body yet - might continue on next line
        result.push(line);
      }
    } else {
      result.push(line);
    }
  }

  return { content: result.join('\n'), sorryCount };
}

// Main processing
const leanFiles = findLeanFiles(BASE_DIR);
console.log(`Found ${leanFiles.length} .lean files to process`);

let totalSorryCount = 0;
let processedCount = 0;

for (const filePath of leanFiles) {
  const relativePath = path.relative(BASE_DIR, filePath);
  const dirName = path.dirname(filePath);
  const baseName = path.basename(filePath, '.lean');
  const amputatedPath = path.join(dirName, baseName + '_amputated.lean');

  // Skip if amputated version already exists
  if (fs.existsSync(amputatedPath)) {
    console.log(`  SKIP (exists): ${relativePath}`);
    continue;
  }

  const content = fs.readFileSync(filePath, 'utf-8');
  const { content: amputatedContent, sorryCount } = amputateFile(content, relativePath);

  // Only create amputated version if there are proof bodies to amputate
  if (sorryCount > 0) {
    const header = `-- AMPUTATED VERSION: 原始证明体被替换为 sorry，待 lake build 恢复后回填\n-- Source: ${relativePath}\n-- Sorry count: ${sorryCount}\n\n`;
    const finalContent = header + amputatedContent;

    fs.writeFileSync(amputatedPath, finalContent, 'utf-8');
    console.log(`  CREATED: ${relativePath} → ${baseName}_amputated.lean (${sorryCount} sorry)`);
    totalSorryCount += sorryCount;
    processedCount++;
  } else {
    console.log(`  SKIP (no proofs): ${relativePath}`);
  }
}

console.log(`\n========================================`);
console.log(`Summary:`);
console.log(`  Files processed: ${processedCount}`);
console.log(`  Total sorry count: ${totalSorryCount}`);
console.log(`========================================`);
