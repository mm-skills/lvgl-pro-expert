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

## 5. Generator Code Validation Pitfalls

When running `lvglpro generate`, the schema validator is exceptionally strict and catches issues the local validator script might miss:

1. **Slots MUST use `<lv_obj>`:** In component views, you define the insertion point for a `<slot>` by placing a widget with the same `name`. If you follow documentation blindly and write `<container name="content" />`, the generator will fail with `Unknown element: container` (unless you explicitly defined a `container` component). **Always use `<lv_obj name="slot_name" width="100%" height="100%">`** with a transparent style for slot placeholders.
2. **Prop Subject Types:** When defining a `<prop>` that takes a subject, use `type="subject"`. Do not use `type="subject_int"` or `type="subject_string"` in the XML api—these will cause an `Invalid enum value` error. The generator handles the typing automatically.
3. **Gestures are Generic:** You cannot bind directional gestures like `trigger="gesture_left"` or `trigger="gesture_up"` directly in the XML `<event_cb>`. The only valid LVGL v9 gesture trigger is `trigger="gesture"`. Route it to a single C callback (e.g. `on_gesture(lv_event_t* e)`) and determine the direction natively using `lv_indev_get_gesture_dir(lv_indev_active())` which returns `LV_DIR_LEFT`, `LV_DIR_RIGHT`, `LV_DIR_TOP`, or `LV_DIR_BOTTOM`.
4. **C++ Macro Gotchas:** Speaking of gestures, LVGL v9 uses `LV_DIR_TOP` and `LV_DIR_BOTTOM`. Do **not** use `LV_DIR_UP` or `LV_DIR_DOWN` in your C++ code.

5. **Size Constants:** Do not use C macros like `LV_SIZE_CONTENT` or `lv_size_content` in XML. Use `width="content"` or `height="content"`.
6. **Boolean Properties:** For boolean style properties (like `style_arc_rounded`), do not use `"1"` or `"0"`. The validator expects `"true"` or `"false"`.
7. **Arc Range:** The `<lv_arc>` widget uses `min_value` and `max_value`, not `min` and `max`.
8. **Value Binding Syntax:** `bind_value` is an *attribute* on the widget (e.g., `<lv_arc bind_value="subject_name" />`), it is **not** a child element. Only complex bindings (`<bind_flag_if_eq>`) and events (`<subject_set_int_event>`) are child tags.
