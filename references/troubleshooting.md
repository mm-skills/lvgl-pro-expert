# Troubleshooting & Common Pitfalls

Quick diagnostic guide for errors encountered during LVGL Pro XML authoring, validation, and editor loading.

---

## Diagnostic Matrix

| Error Symptom / Log Message | Root Cause | Solution / Fix |
|---|---|---|
| **Unknown widget type `<widget_name>`** | Missing `lv_` prefix or typo | Ensure official widgets use `lv_` prefix (e.g. `<lv_button>`, `<lv_slider>`). Custom components use directory name without prefix. |
| **Missing `name` attribute** | Widget declared without `name="..."` | Add a unique `name` attribute to every widget instance (required for C code export). |
| **Options not splitting in dropdown/roller** | Literal `\n` or raw line break in `options` | Use the XML newline entity `&#10;` to separate options: `options="A&#10;B&#10;C"`. |
| **Style not applying to indicator/knob** | Incorrect part/state selector syntax | Use hyphenated attribute syntax `style_bg_color-indicator-checked="0x22c55e"` or `<style name="..." selector="indicator\|checked" />`. |
| **Subject binding not updating UI** | Mismatched subject type and event tag | Bind integer subjects with `<subject_set_int_event>`, string subjects with `<subject_set_string_event>`. |
| **Screen navigation fails to transition** | Target screen file missing or misspelled | Verify the target screen XML exists in `screens/<name>.xml`. Omit `.xml` extension in `screen="..."` attribute. |
| **Editor fails to open / blank canvas** | `project.xml` missing `<targets>` or `<display>` | Ensure `project.xml` defines `<targets><target name="default"><display width="..." height="..." /></target></targets>`. |
| **Constant value not resolving** | Using `$` instead of `#` for constant | Use `#token_name` to reference values in `<consts>`. The `$` prefix is strictly for component props (`$prop_name`). |
| **Memory attribute ignored** | `memory` placed on child tag | Place `memory="region_name"` on `<images>` or `<fonts>` container blocks, not on individual `<data>` or `<bin>` tags. |

---

## 1. Dropdown & Roller Option Parsing
```xml
<!-- ✅ Correct -->
<lv_dropdown name="mode" options="Heat&#10;Cool&#10;Auto" />

<!-- ❌ Incorrect: Literal \n is treated as literal text characters '\' and 'n' -->
<lv_dropdown name="mode" options="Heat\nCool\nAuto" />
```

---

## 2. Style Selector Targeting
```xml
<!-- ✅ Correct: Hyphenated inline part-state selector -->
<lv_switch name="sw" style_bg_color-indicator-checked="0x10b981" />

<!-- ❌ Incorrect: Separate invalid attributes on base widget -->
<lv_switch name="sw" style_bg_color="0x10b981" selector="indicator" state="checked" />
```

---

## 3. Subject Type and Event Matching
```xml
<!-- In globals.xml: <subjects><int name="counter" value="0" /></subjects> -->

<!-- ✅ Correct -->
<lv_button name="inc_btn">
    <subject_increment_event subject="counter" step="1" trigger="clicked" />
</lv_button>

<!-- ❌ Incorrect: Setting integer subject with string event -->
<lv_button name="inc_btn">
    <subject_set_string_event subject="counter" value="1" trigger="clicked" />
</lv_button>
```

---

## 4. Project Validation
Run the automated validator script before opening in the LVGL Pro Editor:
```bash
python3 scripts/validate_project.py /path/to/my_project/
```
