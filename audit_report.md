# LVGL Pro Expert — Skill Compliance Audit

**Upstream:** `lvgl_pro` v9.5.0 (shallow clone in `tmp/lvgl_pro`)
**Skill:** `references/format/widget-catalog.md`
**Widgets audited:** 29

## Summary

| Level | Count | Meaning |
|-------|-------|---------|
| ✅ PASS | 80 | In upstream and documented in skill |
| ❌ FAIL | 0 | In skill but NOT in upstream (hallucination) |
| ⚠️ WARN-CORE | 74 | Core prop in upstream, missing from skill |
| ℹ️ INFO | 186 | Extended prop — expected, MCP pointer covers |

## ⚠️ Core Warnings — Real Gaps to Fix

### `lv_animimg`
- Core prop `src` (image_src[count]) in upstream but MISSING from skill catalog
- Core prop `duration` (int) in upstream but MISSING from skill catalog

### `lv_arc`
- Core prop `rotation` (int) in upstream but MISSING from skill catalog
- Core prop `value` (int) in upstream but MISSING from skill catalog
- Core prop `mode` (enum:lv_arc_mode) in upstream but MISSING from skill catalog

### `lv_bar`
- Core prop `mode` (enum:lv_bar_mode) in upstream but MISSING from skill catalog
- Core prop `orientation` (enum:lv_bar_orientation) in upstream but MISSING from skill catalog

### `lv_buttonmatrix`
- Core prop `map` (string[NULL]) in upstream but MISSING from skill catalog

### `lv_calendar`
- Sub-element `<lv_calendar-header_arrow>` not documented in skill catalog
- Sub-element `<lv_calendar-header_dropdown>` not documented in skill catalog

### `lv_chart`
- Core prop `type` (enum:lv_chart_type) in upstream but MISSING from skill catalog
- Sub-element `<lv_chart-series>` not documented in skill catalog
- Sub-element `<lv_chart-cursor>` not documented in skill catalog

### `lv_checkbox`
- Core prop `text` (string) in upstream but MISSING from skill catalog

### `lv_dropdown`
- Core prop `text` (string) in upstream but MISSING from skill catalog
- Core prop `options` (string) in upstream but MISSING from skill catalog
- Core prop `selected` (int) in upstream but MISSING from skill catalog
- Sub-element `<lv_dropdown-list>` not documented in skill catalog

### `lv_gif`
- Core prop `src` (image) in upstream but MISSING from skill catalog

### `lv_image`
- Core prop `src` (image) in upstream but MISSING from skill catalog
- Core prop `rotation` (int) in upstream but MISSING from skill catalog

### `lv_keyboard`
- Core prop `mode` (enum:lv_keyboard_mode) in upstream but MISSING from skill catalog

### `lv_label`
- Core prop `text` (string) in upstream but MISSING from skill catalog

### `lv_led`
- Core prop `color` (color) in upstream but MISSING from skill catalog
- Core prop `brightness` (opa) in upstream but MISSING from skill catalog

### `lv_line`
- Core prop `points` (precise_points[count]) in upstream but MISSING from skill catalog

### `lv_obj`
- Sub-element `<lv_obj-style>` not documented in skill catalog
- Sub-element `<lv_obj-remove_style>` not documented in skill catalog
- Sub-element `<lv_obj-remove_style_all>` not documented in skill catalog
- Sub-element `<lv_obj-bind_style>` not documented in skill catalog
- Sub-element `<lv_obj-bind_style_prop>` not documented in skill catalog
- Sub-element `<lv_obj-event_cb>` not documented in skill catalog
- Sub-element `<lv_obj-screen_load_event>` not documented in skill catalog
- Sub-element `<lv_obj-screen_create_event>` not documented in skill catalog
- Sub-element `<lv_obj-play_timeline_event>` not documented in skill catalog
- Sub-element `<lv_obj-subject_toggle_event>` not documented in skill catalog
- Sub-element `<lv_obj-subject_set_int_event>` not documented in skill catalog
- Sub-element `<lv_obj-subject_set_float_event>` not documented in skill catalog
- Sub-element `<lv_obj-subject_set_string_event>` not documented in skill catalog
- Sub-element `<lv_obj-subject_increment_event>` not documented in skill catalog
- Sub-element `<lv_obj-bind_flag_if_eq>` not documented in skill catalog
- Sub-element `<lv_obj-bind_flag_if_not_eq>` not documented in skill catalog
- Sub-element `<lv_obj-bind_flag_if_gt>` not documented in skill catalog
- Sub-element `<lv_obj-bind_flag_if_ge>` not documented in skill catalog
- Sub-element `<lv_obj-bind_flag_if_lt>` not documented in skill catalog
- Sub-element `<lv_obj-bind_flag_if_le>` not documented in skill catalog
- Sub-element `<lv_obj-bind_state_if_eq>` not documented in skill catalog
- Sub-element `<lv_obj-bind_state_if_not_eq>` not documented in skill catalog
- Sub-element `<lv_obj-bind_state_if_gt>` not documented in skill catalog
- Sub-element `<lv_obj-bind_state_if_ge>` not documented in skill catalog
- Sub-element `<lv_obj-bind_state_if_lt>` not documented in skill catalog
- Sub-element `<lv_obj-bind_state_if_le>` not documented in skill catalog

### `lv_qrcode`
- Core prop `data` (string) in upstream but MISSING from skill catalog

### `lv_roller`
- Core prop `options` (string) in upstream but MISSING from skill catalog
- Core prop `selected` (int) in upstream but MISSING from skill catalog

### `lv_scale`
- Core prop `mode` (enum:lv_scale_mode) in upstream but MISSING from skill catalog
- Core prop `rotation` (deg) in upstream but MISSING from skill catalog
- Sub-element `<lv_scale-section>` not documented in skill catalog

### `lv_slider`
- Core prop `mode` (enum:lv_slider_mode) in upstream but MISSING from skill catalog
- Core prop `orientation` (enum:lv_slider_orientation) in upstream but MISSING from skill catalog

### `lv_spangroup`
- Core prop `overflow` (enum:lv_span_overflow) in upstream but MISSING from skill catalog
- Core prop `indent` (int) in upstream but MISSING from skill catalog
- Sub-element `<lv_spangroup-span>` not documented in skill catalog

### `lv_spinbox`
- Core prop `value` (int) in upstream but MISSING from skill catalog
- Core prop `min_value` (int) in upstream but MISSING from skill catalog
- Core prop `max_value` (int) in upstream but MISSING from skill catalog
- Core prop `step` (int) in upstream but MISSING from skill catalog

### `lv_switch`
- Core prop `orientation` (enum:lv_switch_orientation) in upstream but MISSING from skill catalog

### `lv_table`
- Sub-element `<lv_table-column>` not documented in skill catalog
- Sub-element `<lv_table-cell>` not documented in skill catalog

### `lv_tabview`
- Sub-element `<lv_tabview-tab_bar>` not documented in skill catalog
- Sub-element `<lv_tabview-tab>` not documented in skill catalog
- Sub-element `<lv_tabview-tab_button>` not documented in skill catalog

### `lv_textarea`
- Core prop `text` (string) in upstream but MISSING from skill catalog

## Per-Widget Status

- ⚠️ `lv_animimg` — core gaps: 2, extended (MCP): 0
- ⚠️ `lv_arc` — core gaps: 3, extended (MCP): 0
- ⚠️ `lv_bar` — core gaps: 2, extended (MCP): 2
- ✅ `lv_button` — core gaps: 0, extended (MCP): 0
- ⚠️ `lv_buttonmatrix` — core gaps: 1, extended (MCP): 0
- ⚠️ `lv_calendar` — core gaps: 2, extended (MCP): 0
- ✅ `lv_canvas` — core gaps: 0, extended (MCP): 0
- ⚠️ `lv_chart` — core gaps: 3, extended (MCP): 0
- ⚠️ `lv_checkbox` — core gaps: 1, extended (MCP): 0
- ⚠️ `lv_dropdown` — core gaps: 4, extended (MCP): 2
- ⚠️ `lv_gif` — core gaps: 1, extended (MCP): 0
- ⚠️ `lv_image` — core gaps: 2, extended (MCP): 0
- ✅ `lv_imagebutton` — core gaps: 0, extended (MCP): 1
- ⚠️ `lv_keyboard` — core gaps: 1, extended (MCP): 2
- ⚠️ `lv_label` — core gaps: 1, extended (MCP): 3
- ⚠️ `lv_led` — core gaps: 2, extended (MCP): 0
- ⚠️ `lv_line` — core gaps: 1, extended (MCP): 0
- ⚠️ `lv_obj` — core gaps: 26, extended (MCP): 169
- ⚠️ `lv_qrcode` — core gaps: 1, extended (MCP): 1
- ⚠️ `lv_roller` — core gaps: 2, extended (MCP): 0
- ⚠️ `lv_scale` — core gaps: 3, extended (MCP): 3
- ⚠️ `lv_slider` — core gaps: 2, extended (MCP): 0
- ⚠️ `lv_spangroup` — core gaps: 3, extended (MCP): 0
- ⚠️ `lv_spinbox` — core gaps: 4, extended (MCP): 2
- ✅ `lv_spinner` — core gaps: 0, extended (MCP): 0
- ⚠️ `lv_switch` — core gaps: 1, extended (MCP): 0
- ⚠️ `lv_table` — core gaps: 2, extended (MCP): 1
- ⚠️ `lv_tabview` — core gaps: 3, extended (MCP): 0
- ⚠️ `lv_textarea` — core gaps: 1, extended (MCP): 0
