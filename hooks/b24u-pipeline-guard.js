// B24U pipeline guard — PreToolUse hook.
// Cases:
//   A) Write/Edit on clients/<X>/<prefix>-v<N>.<ext>:
//      - blocks when missing pipeline artefacts (baseline/facts/diagnostics)
//        for prompt/special-instructions files.
//      - blocks Write/Edit of v<N≥1> when previous version v<N-1> is absent on disk
//        (no version skipping; the previous version must exist as the backup).
//      - blocks Edit of an existing v0 file (v0 is the immutable baseline snapshot).
//   B) mcp__playwright__browser_evaluate / browser_click with destructive keywords:
//      blocks unless clients/<active>/snapshots/<today>-before-*.md exists.
//   C) Bash rm/Remove-Item on anything inside clients/<X>/ except snapshots/:
//      blocks unless today's pre-snapshot exists.
//
// Universal rule: to delete or replace anything (prompts, feeds, instructions,
// services, any client artefact), a backup must exist first.

const fs = require('fs');
const path = require('path');

let raw = '';
process.stdin.setEncoding('utf8');
process.stdin.on('data', (c) => { raw += c; });
process.stdin.on('end', () => {
  let input;
  try { input = JSON.parse(raw); } catch { return; }

  const reason = computeBlockReason(input);
  if (reason) {
    process.stdout.write(JSON.stringify({
      hookSpecificOutput: {
        hookEventName: 'PreToolUse',
        permissionDecision: 'deny',
        permissionDecisionReason: reason,
      },
    }));
  }
});

function findClientDirFromPath(filePath) {
  const norm = String(filePath || '').replace(/\\/g, '/');
  const parts = norm.split('/');
  const idx = parts.lastIndexOf('clients');
  if (idx < 0 || parts.length <= idx + 1) return null;
  // clients/_archived/<name>/... — real client dir is one level deeper
  const next = parts[idx + 1];
  if (next && next.startsWith('_') && parts.length > idx + 2) {
    return parts.slice(0, idx + 3).join('/');
  }
  return parts.slice(0, idx + 2).join('/');
}

function activeClient(cwdPath) {
  const root = path.join(cwdPath, 'clients');
  if (!fs.existsSync(root)) return null;
  let entries;
  try { entries = fs.readdirSync(root, { withFileTypes: true }); } catch { return null; }
  const dirs = entries
    .filter((d) => d.isDirectory() && !d.name.startsWith('_'))
    .map((d) => {
      const p = path.join(root, d.name);
      let mtime = 0;
      try {
        const files = fs.readdirSync(p);
        for (const f of files) {
          try {
            const st = fs.statSync(path.join(p, f));
            if (st.mtimeMs > mtime) mtime = st.mtimeMs;
          } catch {}
        }
        if (mtime === 0) mtime = fs.statSync(p).mtimeMs;
      } catch {}
      return { name: d.name, dir: p, mtime };
    })
    .sort((a, b) => b.mtime - a.mtime);
  return dirs[0] || null;
}

function hasTodaySnapshot(clientDir) {
  const today = new Date().toISOString().slice(0, 10);
  const snapDir = path.join(clientDir, 'snapshots');
  if (!fs.existsSync(snapDir)) return false;
  try {
    return fs.readdirSync(snapDir).some(
      (f) => f.includes(today) && /before/i.test(f)
    );
  } catch { return false; }
}

function computeBlockReason(input) {
  const tool = input.tool_name || '';
  const ti = input.tool_input || {};
  const cwd = input.cwd || process.cwd();

  // CASE A: Write/Edit inside clients/<X>/
  if (tool === 'Write' || tool === 'Edit') {
    const fp = String(ti.file_path || '').replace(/\\/g, '/');
    if (!/\/clients\/[^/]+\//i.test(fp)) return null;

    const clientDir = findClientDirFromPath(fp);
    const fileName = fp.split('/').pop();

    // A1: prompt / special-instructions need pipeline pre-artefacts (baseline + facts/diag)
    if (/^(system-prompt|special-instructions)-v/i.test(fileName) && clientDir && fs.existsSync(clientDir)) {
      let files = [];
      try { files = fs.readdirSync(clientDir); } catch {}
      const hasBaseline = files.some((f) => /^baseline-/i.test(f));
      const hasFactsOrDiag = files.some((f) => /^(facts|diagnostics)-/i.test(f));
      if (!hasBaseline) {
        return `Шаг 2 пайплайна B24U не выполнен: в "${clientDir}" нет baseline-*.md. ` +
          `Снять baseline кабинета "как есть" (templates/cabinet-snapshot-template.md) ` +
          `до правки промпта. См. .claude/skills/b24u-platform/SKILL.md → Шаг 2.`;
      }
      if (!hasFactsOrDiag) {
        return `Шаги 3-6 пайплайна B24U не выполнены: в "${clientDir}" нет facts-*.md ` +
          `или diagnostics-*.md. Сначала собери факты сайта (Шаг 3) и диагностику фида/поиска ` +
          `(Шаг 4) до правки промпта (Шаг 7). См. SKILL.md.`;
      }
    }

    // A2: versioned file rules — applies to any *-v<N>.<ext> in clients/<X>/
    //     (system-prompt-v2.xml, special-instructions-v3.txt, feed-config-v1.md, services-v1.md, etc.)
    const verMatch = fileName.match(/^(.+)-v(\d+)(\.[^.]+)$/i);
    if (verMatch && clientDir && fs.existsSync(clientDir)) {
      const [, prefix, nStr, ext] = verMatch;
      const n = parseInt(nStr, 10);

      // A2.a: v0 is immutable once created (it is the baseline backup for revert).
      if (n === 0 && fs.existsSync(fp)) {
        return `Файл v0 неизменяем: "${fileName}" уже существует и является baseline ` +
          `для отката. Создавай новую версию (v1, v2, ...) рядом, не перезаписывай v0. ` +
          `Это правило защищает резервную копию исходного состояния.`;
      }

      // A2.b: writing v<N> (N>=1) requires v<N-1> already on disk as backup.
      if (n >= 1) {
        const prev = path.join(clientDir, `${prefix}-v${n - 1}${ext}`);
        if (!fs.existsSync(prev)) {
          return `Нельзя писать "${fileName}" без предыдущей версии "${prefix}-v${n - 1}${ext}" ` +
            `на диске — резервная копия предыдущей версии обязательна. ` +
            `Сначала сохрани текущее состояние как ${prefix}-v${n - 1}${ext}, потом создавай v${n}.`;
        }
      }
    }
  }

  // CASE B: Playwright destructive in B24U
  if (
    tool === 'mcp__playwright__browser_evaluate' ||
    tool === 'mcp__playwright__browser_click'
  ) {
    const blob = JSON.stringify(ti);
    const destructiveRe = /Удалить|Очистить|очистка|удаление|снести|стереть|обнул|пересоздать|переустановить|Reset|Delete|Clear|Remove|Truncate|Wipe|Purge|Drop|Overwrite|Replace|deleteFeed|removeFeed/i;
    const isDestructive = destructiveRe.test(blob);
    if (isDestructive) {
      const ac = activeClient(cwd);
      // Gate only when working inside a project with an active client (otherwise unrelated).
      if (!ac && !/partner\.b24u\.ru|b24u/i.test(blob)) return null;
      if (!ac) {
        return `Деструктив в кабинете B24U (${tool}) без активного клиента в "${path.join(cwd, 'clients')}". ` +
          `Сначала создай clients/<name>/ и baseline (SKILL.md, Шаг 2).`;
      }
      if (!hasTodaySnapshot(ac.dir)) {
        const today = new Date().toISOString().slice(0, 10);
        const snapDir = path.join(ac.dir, 'snapshots');
        return `Деструктив в кабинете B24U (клиент: ${ac.name}) без сегодняшнего pre-snapshot. ` +
          `Снять snapshot ВСЕЙ затрагиваемой конфигурации (URL фида, ручные записи БЗ, ` +
          `документы, настройки сканера, текущая версия промпта) в "${snapDir}/${today}-before-<action>.md" ` +
          `до клика. Универсальное правило: чтобы что-то удалить/заменить — резервная копия обязательна. ` +
          `Урок Kstore 2026-05-13: "Удалить все данные сканирования" удалила и фид-конфиг ` +
          `вместе с эмбеддингами — восстановление невозможно.`;
      }
    }
  }

  // CASE C: Bash rm / Remove-Item on anything inside clients/<X>/ (except snapshots/)
  if (tool === 'Bash') {
    const cmd = String(ti.command || '');
    // Catch destructive shell ops on clients/ paths
    const isShellDestructive = /\b(rm|Remove-Item|rd|rmdir|del)\b/i.test(cmd);
    if (isShellDestructive) {
      // Look for clients/<X>/... in the command
      const clientPathMatch = cmd.match(/clients[/\\][^/\\\s"']+/i);
      if (clientPathMatch) {
        const clientRel = clientPathMatch[0].replace(/\\/g, '/');
        // Skip if target is snapshots/ — those are backups themselves
        if (/clients\/[^/]+\/snapshots/i.test(clientRel)) return null;
        // Skip if it's the _archived folder (already archived)
        if (/clients\/_archived/i.test(clientRel)) return null;

        const ac = activeClient(cwd);
        if (ac && !hasTodaySnapshot(ac.dir)) {
          const today = new Date().toISOString().slice(0, 10);
          return `Bash удаление в "${clientRel}" без сегодняшнего snapshot. ` +
            `Сначала сделай snapshot затрагиваемых файлов в "${ac.dir}/snapshots/${today}-before-<action>.md". ` +
            `Правило: чтобы удалить что угодно из конфигурации клиента — резервная копия обязательна.`;
        }
      }
    }
  }

  return null;
}
