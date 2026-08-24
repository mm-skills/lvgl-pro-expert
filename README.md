# LVGL Pro Expert

AI skill for generating [LVGL Pro Editor](https://lvgl.io/docs/pro) XML project files programmatically.

## What This Skill Does

Teaches AI agents to generate complete, valid LVGL Pro XML projects — the same
files you'd create in the LVGL Pro Editor — from natural language descriptions.
The generated projects open in the editor, render in the live preview, and
export valid LVGL C code for embedded displays.

## Features

- **10-item anti-pitfall checklist** — catches the mistakes that cause silent failures
- **Progressive reference system** — widget catalog, style system, data binding, animations
- **Validation script** — checks generated XML against known widget types and attribute schemas
- **Scaffold generator** — creates minimal project structure from the command line
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
  ux/                       ← Embedded display design guidelines
scripts/
  generate_project.py       ← Scaffold a new project
  validate_project.py       ← Validate XML structure and references
examples/
  hello_world/              ← Minimal 3-file project
  thermostat/               ← Data binding showcase
  settings_screen/          ← Theme switching and navigation
```

## Usage

### As an AI Skill

Add to your project via [skill-manager](https://github.com/mm-skills/skill-manager):

```bash
.agents/skills/skill-manager/scripts/add.sh '{"name": "lvgl-pro-expert"}'
```

### Manual

Copy this directory to `.agents/skills/lvgl-pro-expert/` in your project.

## Compatibility

- **LVGL Pro Editor** v9.5+
- **LVGL** v9.5.0
- Python 3.8+ (for scripts)

## License

MIT — see [LICENSE](LICENSE).
