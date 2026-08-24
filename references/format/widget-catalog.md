# LVGL Pro XML: Widget Catalog

Covers the core LVGL widgets, their standard attributes, styling parts, and available states.

> [!NOTE]
> Widget tags map directly to LVGL C types. E.g., `<lv_button>` becomes `lv_button_create()`. All widgets inherit universal positioning, size, and layout properties from `<lv_obj>`.

## Universal Properties (Inherited by all widgets)

| Attribute | Type | Description |
|-----------|------|-------------|
| `x`, `y` | Int/Pct | Position offset from alignment point |
| `width`, `height` | Int/Pct/`"content"` | Widget size |
| `align` | Enum | `center`, `top_left`, `bottom_right`, `left_mid`, etc. |
| `hidden` | Boolean | Visibility |
| `clickable` | Boolean | Whether it receives input |
| `scrollable` | Boolean | Whether children can be scrolled |

---

## 1. Containers & Basic Elements

### `<lv_obj>` — Base Container
The fundamental layout container.
- **Parts:** `main`, `scrollbar`
- **Example:** `<lv_obj width="100%" height="content" layout="flex" flex_flow="row" />`

### `<lv_label>` — Text
- **Attributes:** `text` (String), `long_mode` (`"wrap"`, `"dot"`, `"scroll"`, `"clip"`)
- **Parts:** `main`
- **Example:** `<lv_label text="Hello World" style_text_color="0xFF0000" />`

### `<lv_image>` — Image
- **Attributes:** `src` (String, name from globals), `rotation` (Int, 0.1° units), `scale` (Int, 256=100%)
- **Parts:** `main`
- **Example:** `<lv_image src="img_logo" rotation="900" />`

---

## 2. Interactive Controls

### `<lv_button>` — Standard Button
- **Attributes:** `checkable`, `checked`
- **Parts:** `main`
- **Example:**
```xml
<lv_button width="100" height="40">
    <lv_label text="Click Me" align="center" />
</lv_button>
```

### `<lv_switch>` — Toggle Switch
- **Attributes:** `checked` (Boolean)
- **Parts:** `main`, `indicator`, `knob`
- **Example:** `<lv_switch checked="true" />`

### `<lv_checkbox>` — Checkbox
- **Attributes:** `text` (Label text), `checked` (Boolean)
- **Parts:** `main`, `indicator`
- **Example:** `<lv_checkbox text="Accept Terms" checked="false" />`

### `<lv_slider>` — Slider
- **Attributes:** `value`, `min_value`, `max_value`, `mode` (`"normal"`, `"range"`)
- **Parts:** `main`, `indicator`, `knob`
- **Example:** `<lv_slider value="50" min_value="0" max_value="100" width="80%" />`

### `<lv_arc>` — Circular Gauge/Arc
- **Attributes:** `value`, `min_value`, `max_value`, `bg_start_angle`, `bg_end_angle`, `rotation`
- **Parts:** `main`, `indicator`, `knob`
- **Example:** `<lv_arc value="75" min_value="0" max_value="100" bg_start_angle="135" bg_end_angle="45" />`

---

## 3. Lists & Selection

### `<lv_dropdown>` — Dropdown Menu
- **Attributes:** `options` (String, newline separated by `&#10;`), `selected` (Index), `dir` (`"bottom"`, `"top"`, `"left"`, `"right"`)
- **Parts:** `main`, `indicator`, list: `main`, `selected`, `scrollbar`
- **Example:** `<lv_dropdown options="Apple&#10;Banana&#10;Orange" selected="1" />`

### `<lv_roller>` — Roller/Tumbler
- **Attributes:** `options` (String, `&#10;` sep), `selected` (Index), `options_mode` (`"normal"`, `"infinite"`), `visible_row_count`
- **Parts:** `main`, `selected`
- **Example:** `<lv_roller options="Jan&#10;Feb&#10;Mar" visible_row_count="3" />`

---

## 4. Complex Data Displays

### `<lv_bar>` — Progress Bar
- **Attributes:** `value`, `min_value`, `max_value`
- **Parts:** `main`, `indicator`
- **Example:** `<lv_bar value="45" width="200" height="20" />`

### `<lv_chart>` — Chart
- **Attributes:** `type` (`"line"`, `"bar"`, `"scatter"`), `point_count`, `min_value`, `max_value`
- **Parts:** `main`, `indicator`, `items`, `scrollbar`, `ticks`
- **Example:** `<lv_chart type="line" point_count="10" />`

### `<lv_tabview>` — Tab View
- **Attributes:** `tab_bar_position` (`"top"`, `"bottom"`, `"left"`, `"right"`, `"none"`), `tab_bar_size`
- **Parts:** `main`, buttons: `main`, `items`
- **Children:** `<lv_tabview-tab>`
- **Example:**
```xml
<lv_tabview tab_bar_position="top">
    <lv_tabview-tab text="Tab 1">
        <lv_label text="Content 1" />
    </lv_tabview-tab>
    <lv_tabview-tab text="Tab 2">
        <lv_label text="Content 2" />
    </lv_tabview-tab>
</lv_tabview>
```

### `<lv_table>` — Table
- **Attributes:** `row_count`, `column_count`
- **Children:** `<lv_table-cell>`
- **Example:**
```xml
<lv_table row_count="2" column_count="2">
    <lv_table-cell row="0" column="0" value="Header 1" />
    <lv_table-cell row="1" column="0" value="Data 1" />
</lv_table>
```

---

## Widget Part Map Summary

| Widget | Standard Parts |
|--------|----------------|
| `lv_obj` | `main`, `scrollbar` |
| `lv_button`, `lv_label`, `lv_image` | `main` |
| `lv_slider`, `lv_arc`, `lv_switch` | `main`, `indicator`, `knob` |
| `lv_bar`, `lv_checkbox` | `main`, `indicator` |
| `lv_textarea` | `main`, `cursor`, `selected` |
