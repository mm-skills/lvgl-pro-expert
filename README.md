# LVGL Pro Expert

AI skill for generating [LVGL Pro Editor](https://lvgl.io/docs/pro) XML project files programmatically.

## What This Skill Does

Teaches AI agents to generate complete, valid LVGL Pro XML projects — the same
files you'd create in the LVGL Pro Editor — from natural language descriptions.
The generated projects open in the editor, render in the live preview, and
export valid LVGL C code for embedded displays.

## Features

- **14-item anti-pitfall checklist** — catches the mistakes that cause silent failures
- **Progressive reference system** — widget catalog, style system, data binding, animations
- **Validation script** — checks generated XML against known widget types and attribute schemas
- **Scaffold generator** — creates project structure with embedded AGENTS.md for AI continuity
- **Audit script** — verifies skill references against upstream widget schemas
- **3 example projects** — hello world, thermostat with data binding, settings with theming

## Project Structure

```
SKILL.md                    ← Core instructions for AI agents
docs/
  xml_format_specification.md ← Complete XML format reference (~1,800 lines)
references/
  format/                   ← File structure, widgets, styles, binding, animations, assets
  widgets/                  ← Input, display, container, and custom widget guides
  components/               ← Component system, slots, inheritance
  targets/                  ← Ecosystem configs (Zephyr, Linux, VSCode, UI-only)
  upstream/                 ← Official LVGL Pro docs, AGENTS.md, CLI/MCP, blog conventions
  ux/                       ← Embedded display design guidelines
scripts/
  generate_project.py       ← Scaffold a new project (incl. AGENTS.md)
  validate_project.py       ← Validate XML structure and references
  audit_skill.py            ← Audit skill refs against upstream widget schemas
examples/
  hello_world/              ← Minimal 3-file project
  thermostat/               ← Data binding showcase
  settings_screen/          ← Theme switching and navigation
```

## Usage

### As an AI Skill

Copy or clone this directory to `.agents/skills/lvgl-pro-expert/` in your project:

```bash
git clone https://github.com/mm-skills/lvgl-pro-expert.git .agents/skills/lvgl-pro-expert
```

## Compatibility

- **LVGL Pro Editor** v9.5+
- **LVGL** v9.5.0
- Python 3.8+ (for scripts)

## Sources & Credits

1. `lvgl/lvgl_pro` GitHub repo — https://github.com/lvgl/lvgl_pro (AGENTS.md, tutorials, widget schemas, official docs)
2. *LVGL Pro Project Structure and Naming Guide* by Felix Biego — https://lvgl.io/blog/lvgl-pro-project-structure-guide
3. *Building a Custom Widget with Scroll Effects in LVGL Pro* by Felix Biego — https://lvgl.io/blog/tutorial-lvgl-pro-custom-widgets
4. Official LVGL Pro docs — https://lvgl.io/docs/pro

## License

MIT — see [LICENSE](LICENSE).
