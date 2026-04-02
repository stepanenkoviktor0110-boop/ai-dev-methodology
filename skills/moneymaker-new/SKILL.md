---
name: moneymaker-new
argument-hint: "{project-name}"
description: |
  Creates a new Moneymaker project: validates config and name, scaffolds
  ~/.moneymaker/projects/{name}/ with context.md and materials/.

  Use when: "новый проект moneymaker", "создай проект moneymaker", "moneymaker new",
  "moneymaker создай проект", "moneymaker new project", "создать проект moneymaker",
  "заведи проект moneymaker", "init moneymaker project"
---

# moneymaker-new

Creates a new Moneymaker project directory with empty context scaffold.

## Phase 1: Validation

1. Check that `~/.moneymaker/config.yml` exists.

   ```bash
   test -f ~/.moneymaker/config.yml && echo "EXISTS" || echo "MISSING"
   ```

   If MISSING → tell the user: "Конфиг не найден. Сначала запустите `/moneymaker-setup`." Stop here — do not create any files.

2. Validate the project name against pattern `^[a-zA-Z0-9_-]+$`.

   If the name contains characters outside this set → show the first invalid character, explain the allowed pattern (Latin letters, digits, hyphens, underscores), and stop.

   Examples of invalid names: `my project` (space), `../evil` (slash and dot), `клиент` (Cyrillic). Explain that the name uses Latin kebab-case.

3. Check that `~/.moneymaker/projects/{name}/` does not already exist.

   ```bash
   test -d ~/.moneymaker/projects/{name} && echo "EXISTS" || echo "FREE"
   ```

   If EXISTS → show notice: "Проект {name} уже существует." List directory contents with `ls -la ~/.moneymaker/projects/{name}/`. Stop without overwriting.

**Checkpoint:** Config exists, project name is valid, directory is free. Proceed to scaffold.

## Phase 2: Scaffold

1. Create the project directory (including parent dirs if `~/.moneymaker/projects/` does not exist yet):

   ```bash
   mkdir -p ~/.moneymaker/projects/{name}
   ```

2. Create `context.md` inside the project directory with this exact content:

   ```markdown
   # Context: {name}

   ## Требования

   ## Договорённости

   ## Открытые вопросы
   ```

   Sections stay empty — no placeholder text, no examples, no hints inside them. The user fills them via `/moneymaker-add`.

3. Create the `materials/` folder inside the project directory:

   ```bash
   mkdir ~/.moneymaker/projects/{name}/materials
   ```

4. Show the user the created structure:

   ```bash
   find ~/.moneymaker/projects/{name} \( -type f -o -type d \) | sort
   ```

5. Print the next-step tip: "Next: `/moneymaker-add {project-name} {text}`"

**Checkpoint:** Directory created, context.md has 3 empty sections, materials/ exists, next-step hint shown.

## Self-Verification

Before finishing, verify:

- [ ] `~/.moneymaker/config.yml` checked before creating any files
- [ ] Project name validated against `^[a-zA-Z0-9_-]+$`
- [ ] `~/.moneymaker/projects/{name}/` created
- [ ] `context.md` created with heading and 3 empty sections (Требования, Договорённости, Открытые вопросы)
- [ ] `materials/` created inside the project directory
- [ ] Next-step hint "/moneymaker-add {project} {text}" shown to user
