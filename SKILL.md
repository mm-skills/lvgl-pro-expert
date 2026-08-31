---
name: lvgl-pro-expert
description: >
  Generate LVGL Pro Editor XML project files programmatically for LVGL-based
  embedded UI development. Trigger on: "LVGL Pro", "LVGL Pro Editor", "LVGL XML",
  "LVGL UI project", "lv_obj XML", "generate LVGL UI", "embedded display XML",
  "LVGL component", "LVGL screen layout", "XML UI editor", "LVGL widget",
  "data binding LVGL", "LVGL animation", "LVGL Pro project", "LVGL v9 UI",
  "embedded touchscreen UI", "HMI display project".
  Use when the user wants to create, scaffold, or modify LVGL Pro Editor XML
  projects without the visual editor, or when they want an AI-generated UI
  layout for embedded displays using LVGL v9. Also trigger when the user asks
  about LVGL Pro XML syntax, component architecture, data binding with subjects,
  or animation timelines — even if they don't explicitly say "use a skill".
---

# LVGL Pro Expert

Generate complete LVGL Pro Editor XML projects that open correctly in the
LVGL Pro Editor, render in the live preview, and export valid LVGL C code
for embedded displays (ESP32, STM32, Renesas, NXP, etc.).

## Quick Start

A minimal LVGL Pro project needs three files:

```
my_project/
├── project.xml        ← Display targets and LVGL version
├── globals.xml        ← Shared styles, constants, subjects, assets
└── screens/
    └── screen_home.xml ← At least one screen
```

**project.xml:**
```xml
<project lvgl_version="9.5.0">
    <targets>
        <target name="default">
            <display width="480" height="320" />
        </target>
    </targets>
</project>
```

**globals.xml:**
```xml
<globals>
    <api></api>
    <consts></consts>
    <subjects></subjects>
    <images></images>
    <fonts></fonts>
    <styles></styles>
</globals>
```

**screens/screen_home.xml:**
```xml
<screen>
    <view flex_flow="column"
          style_flex_main_place="center"
          style_flex_cross_place="center">
        <lv_label name="title" text="Hello, LVGL Pro!" />
    </view>
</screen>
```

Use `scripts/generate_project.py` for scaffolding, or write the XML directly
using the reference files below.

---

## ❌ Anti-Pitfall Checklist

Read BEFORE generating any project files. These are the mistakes that cause
silent failures or editor load errors.

### 1. Options use `&#10;`, NOT `\n`

Dropdown and roller options must use the XML entity `&#10;` for line separators.
Real newlines or `\n` sequences break option parsing.

```xml
✅ <lv_dropdown name="mode" options="Heat&#10;Cool&#10;Auto" />
❌ <lv_dropdown name="mode" options="Heat\nCool\nAuto" />
```

### 2. Widget sub-elements use hyphenated names

Complex widgets define their internal structure with hyphenated child tags,
not attributes. Each widget type has its own sub-element vocabulary.

```xml
✅ <lv_tabview name="tabs">
       <lv_tabview-tab text="Home">...</lv_tabview-tab>
   </lv_tabview>

❌ <lv_tabview name="tabs" tabs="Home,Settings" />
```

→ See `references/format/widget-catalog.md` for the full sub-element list.

### 3. Style selectors use hyphens, not separate attributes

To style a specific widget part in a specific state, append
`-<part>` and/or `-<state>` to the style property name:

```xml
✅ style_bg_color-indicator-checked="0x4CAF50"
❌ style_bg_color="0x4CAF50" selector="indicator" state="checked"
```

Common parts: `main`, `indicator`, `knob`, `items`, `selected`, `cursor`.
Common states: `default`, `pressed`, `checked`, `focused`, `disabled`.

### 4. Constants use `#` prefix, component props use `$`

These are two different reference systems — don't mix them up.

```xml
<!-- Constants (defined in <consts>, referenced with #) -->
<consts><color name="accent" value="0x6366f1" /></consts>
<lv_label style_text_color="#accent" />

<!-- Component props (defined in <api>, referenced with $) -->
<api><prop name="title" type="string" default="Hello" /></api>
<lv_label text="$title" />
```

### 5. `bind_text-fmt` uses printf-style format strings

The format string is a **separate attribute** with a hyphenated name, not a
child element or part of `bind_text`:

```xml
✅ <lv_label bind_text="subject_temp" bind_text-fmt="%d°C" />
❌ <lv_label bind_text="subject_temp" format="%d°C" />
```

### 6. Screen navigation has two distinct patterns

Use `<screen_create_event>` for screens that are created fresh each time
(dynamic). Use `<screen_load_event>` for screens that persist in memory
(permanent, faster transitions).

```xml
<!-- Dynamic: creates a new screen instance each time -->
<screen_create_event screen="settings_screen" trigger="clicked" />

<!-- Permanent: screen stays in memory, just switches to it -->
<screen_load_event screen="home_screen" trigger="clicked" />
```

Mark permanent screens with `permanent="true"` in their `<screen>` tag.

### 7. Subject types must match their event types

An `<int>` subject must be mutated with `<subject_set_int_event>`, a
`<string>` subject with `<subject_set_string_event>`. Mismatched types
compile but produce undefined runtime behaviour.

```xml
<subjects>
    <int name="subject_count" default="0" />
    <string name="subject_label" default="Hello" />
</subjects>

✅ <subject_set_int_event subject="subject_count" value="5" trigger="clicked" />
✅ <subject_set_string_event subject="subject_label" value="World" trigger="clicked" />
❌ <subject_set_string_event subject="subject_count" value="5" trigger="clicked" />
```

### 8. `<component>` vs `<widget>` — know the difference

Components are **pure XML** reusable blocks — no C code required. Widgets
need a **C implementation** with a custom XML parser. Always prefer
components unless you need custom rendering or low-level algorithms.

### 9. Every widget needs a `name` attribute

The `name` becomes the C variable name in exported code. Missing names
cause compilation errors. Names must be unique within their screen scope.

```xml
✅ <lv_slider name="volume_slider" min_value="0" max_value="100" />
❌ <lv_slider min_value="0" max_value="100" />
```

### 10. `memory` and `if_target` go on the container tag

These attributes belong on `<images>`, `<fonts>`, or `<memory>` blocks,
not on individual `<data>` or `<bin>` children:

```xml
✅ <images memory="ospi" if_target="large">
       <data name="logo" src_path="images/logo.png" />
   </images>

❌ <images>
       <data name="logo" src_path="images/logo.png" memory="ospi" />
   </images>
```

### 11. Styles are initialized once

Styles evaluate once, before props are bound. Therefore, an `$api_prop` **cannot** go into a `<style>`. It must go directly onto the widget:

```xml
❌ <!-- NO: style evaluates once, before props are bound -->
<style name="style_bg" bg_color="$color"/>

✅ <!-- YES -->
<view style_bg_color="$color"/>
```

### 12. Project Naming Conflicts

Never name your project `lvgl`. This will cause a namespace conflict with the LVGL library itself. Choose a unique name specific to your product.

### 13. Editing Generated C Files

Never edit generated C files manually. Any manual changes made to the generated C files will be overwritten and lost the next time you hit "Export Code" in the editor. Modify the source XML instead.

### 14. Inline Styles and Sizing

Never write inline styles in your XML (e.g., `<lv_obj style_bg_color="0x000000" />`). Always define named `<style>` blocks in a `<styles>` section. 
Additionally, prefer using `width="content"`, `height="content"`, or `100%` over hardcoded pixel values to make components flexible and reusable.

### 15. Custom Widget Naming

Always use the `wd_` prefix for custom widget XML files (e.g. `wd_list`, `wd_menu`) to clearly distinguish them from standard components or built-in widgets.

---

## Core Workflow

### Step 1: Understand Requirements

Before generating, establish:
- **Display**: Resolution (width × height), shape (rectangular or round with `radius`)
- **Ecosystem**: Zephyr (7 named boards), Linux, VSCode, or UI-only?
  → Read `references/targets/ecosystems-overview.md` for details.
- **Screens**: How many, navigation flow between them
- **Widgets**: What UI elements on each screen
- **Data binding**: Any dynamic values that change at runtime (use subjects)
- **Theming**: Light/dark mode switching? (use `<bind_style>`)

### Step 2: Generate Project Scaffold

Option A — Run the scaffold script:
```bash
python3 scripts/generate_project.py \
  --name "MyProject" \
  --width 480 --height 320 \
  --screens "home settings about" \
  --output /path/to/output/
```

Option B — Write the XML directly using the Quick Start template above.

### Step 3: Define Global Resources

In `globals.xml`, declare everything shared across screens:
→ Read `references/format/project-structure.md`

- **Constants** (`<consts>`): Named values reused across the UI
- **Subjects** (`<subjects>`): Reactive data bindings
- **Styles** (`<styles>`): Reusable style definitions
- **Images** (`<images>`): Image assets
- **Fonts** (`<fonts>`): Custom fonts

### Step 4: Build Screens

Create one XML file per screen in `screens/`.
→ Read `references/format/widget-catalog.md` for widget attributes.
→ Read `references/widgets/` for widget-group guidance.

Each screen has a `<screen>` root with a `<view>` child that holds the
widget tree. Use flex layout for responsive positioning:

```xml
<screen>
    <view flex_flow="column" style_pad_row="16">
        <!-- widgets here -->
    </view>
</screen>
```

### Step 5: Add Data Binding

Connect UI widgets to application data using subjects.
→ Read `references/format/data-binding.md`

### Step 6: Add Animations and Navigation

Wire screen transitions and timeline animations.
→ Read `references/format/animations.md`

### Step 7: Extract Reusable Components

Factor repeated UI patterns into `<component>` files in `components/`.
→ Read `references/components/component-system.md`

### Step 8: Validate

Option A — Use the validation script:
```bash
python3 scripts/validate_project.py /path/to/project/
```

Option B — If the LVGL Pro CLI is installed:
```bash
lvglpro validate /path/to/project/
```

---

## Reference Lookup Table

| When you need to... | Read this reference |
|---|---|
| Understand file structure (project.xml, globals.xml) | `references/format/project-structure.md` |
| Find a widget's attributes, parts, or sub-elements | `references/format/widget-catalog.md` |
| Style a widget or use part+state selectors | `references/format/styles-and-parts.md` |
| Bind data with subjects or fire events | `references/format/data-binding.md` |
| Create animations, timelines, or screen transitions | `references/format/animations.md` |
| Work with images, fonts, or memory allocation | `references/format/assets.md` |
| Work with sliders, arcs, dropdowns, rollers, etc. | `references/widgets/input-widgets.md` |
| Work with labels, images, bars, charts, scales, etc. | `references/widgets/display-widgets.md` |
| Work with containers, tabviews, tables | `references/widgets/container-widgets.md` |
| Create a custom C-backed widget | `references/widgets/custom-widgets.md` |
| Build reusable components with props and slots | `references/components/component-system.md` |
| Choose an ecosystem (Zephyr, Linux, VSCode, UI-only) | `references/targets/ecosystems-overview.md` |
| Configure a Zephyr board target | `references/targets/zephyr-boards.md` |
| Design touch-friendly layouts for embedded displays | `references/ux/design-guidelines.md` |
| Debug validation errors or editor issues | `references/troubleshooting.md` |
| Read the complete XML format specification | `docs/xml_format_specification.md` |
| Official AGENTS.md / Ground rules | `references/upstream/official-agents-guide.md` |
| Official examples (components, globals) | `references/upstream/official-examples.md` |
| CLI tools and MCP server | `references/upstream/cli-and-ai-tools.md` |
| Translations / i18n | `references/upstream/translations.md` |
| Project structure, naming, and custom widget conventions | `references/upstream/blog-conventions.md` |

---

## AI Integration

LVGL Pro has first-class AI agent support. Follow these principles:

1. **Ground attribute usage in the schema files.** Never invent XML attributes.
   The official widget schemas at `lvgl_widgets_xml/<version>/lv_*.xml` are the
   source of truth. If an attribute isn't in the schema, it doesn't exist.

2. **Use the MCP server for live documentation lookups.** LVGL provides an
   official Model Context Protocol server at `https://lvgl.mcp.kapa.ai/`
   (configured in each project's `.claude/.mcp.json`). Query it for version-specific
   API details. It is read-only.

3. **Prefer `<component>` over `<widget>`.** Components are pure XML and
   require no C code. Only create a `<widget>` when you need custom rendering
   or low-level algorithms that XML composition can't express.

4. **Check `globals.xml` before adding ad-hoc values.** Reuse existing
   palettes, typography scales, and spacing tokens. Only add new constants or
   styles when the existing design system doesn't cover the need.

5. **Iterate with the CLI workflow.** Write XML → run `lvglpro validate` → run `lvglpro screenshot` → visually verify the result. Guessing is not the same as knowing. Always run `scripts/validate_project.py` or `lvglpro validate` on generated output before presenting it to the user.

---

## Output Verification Checklist

Before delivering generated project files, verify:

- [ ] `project.xml` exists with `<targets>` and `<display>`
- [ ] `globals.xml` exists with required sections (`<api>`, `<consts>`, `<subjects>`, etc.)
- [ ] At least one screen XML file exists in `screens/`
- [ ] Every widget has a `name` attribute
- [ ] Widget names are unique within each screen
- [ ] All subject references (`bind_text`, `bind_value`) match declarations in `globals.xml`
- [ ] Constant references (`#name`) match declarations in `<consts>`
- [ ] Screen navigation targets reference existing screen files
- [ ] Dropdown/roller options use `&#10;` for separators
- [ ] Style selectors use hyphenated syntax (`style_prop-part-state`)
- [ ] No unknown widget types (check against the 30+ supported types)
- [ ] Round displays use `radius` attribute on `<display>`

---

## Supported Widget Types

30+ widget types available (LVGL v9.5):

`lv_obj` · `lv_label` · `lv_button` · `lv_image` · `lv_slider` ·
`lv_arc` · `lv_bar` · `lv_switch` · `lv_checkbox` · `lv_dropdown` ·
`lv_roller` · `lv_textarea` · `lv_keyboard` · `lv_spinner` ·
`lv_spinbox` · `lv_scale` · `lv_table` · `lv_tabview` · `lv_chart` ·
`lv_calendar` · `lv_led` · `lv_line` · `lv_canvas` · `lv_spangroup` ·
`lv_buttonmatrix` · `lv_imagebutton` · `lv_animimg` · `lv_gif` ·
`lv_qrcode`

→ See `references/format/widget-catalog.md` for full attribute tables.

---

## Supported Event Actions

| Category | Event Tags |
|----------|-----------|
| Subject mutation | `<subject_set_int_event>`, `<subject_set_string_event>`, `<subject_toggle_event>`, `<subject_increment_event>` |
| Screen navigation | `<screen_create_event>`, `<screen_load_event>` |
| Animation | `<play_timeline_event>` |
| C callback | `<event_cb>` |
| Conditional binding | `<bind_flag_if_eq>`, `<bind_flag_if_gt>`, `<bind_state_if_gt>`, `<bind_style>` |

→ See `references/format/data-binding.md` for event structures and trigger values.

---

## Example Projects

Three example projects are included in `examples/`:

- **hello_world/** — Minimal 3-file project with a label
- **thermostat/** — Data binding with arc, subjects, increment events, formatted text
- **settings_screen/** — Theme switching with `<bind_style>`, screen navigation
