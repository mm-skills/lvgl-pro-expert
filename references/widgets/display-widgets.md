# Display Widgets Reference

Display widgets present read-only data, visual status, charts, and graphics to the user. Always assign a unique `name` attribute to every widget instance.

---

## Quick Reference Summary

| Widget | Key Sub-Elements | Primary Styleable Parts | Primary Binding |
|---|---|---|---|
| `<lv_label>` | — | `main` | `bind_text`, `bind_text-fmt` |
| `<lv_image>` | — | `main` | `src` |
| `<lv_bar>` | — | `main`, `indicator` | `bind_value` |
| `<lv_scale>` | `<lv_scale-section>` | `main`, `indicator`, `items` | `bind_min_value`, `bind_max_value` |
| `<lv_chart>` | `<lv_chart-series>`, `<lv_chart-axis>`, `<lv_chart-cursor>` | `main`, `indicator`, `items`, `ticks` | Live series values |
| `<lv_spinner>` | — | `main`, `indicator` | — |
| `<lv_led>` | — | `main` | `color`, `brightness` |
| `<lv_line>` | — | `main` | `points` |
| `<lv_spangroup>` | `<lv_spangroup-span>` | `main` | Span styles |
| `<lv_calendar>` | `<lv_calendar-header_arrow>` | `main`, `items` | Date selection |

---

## 1. `<lv_label>`

Renders static, formatted, or translated text strings.

### Key Attributes
| Attribute | Type | Default | Description |
|---|---|---|---|
| `text` | String | `""` | Initial label text |
| `long_mode` | Enum | `wrap` | `wrap`, `dot`, `scroll`, `scroll_circular`, `clip` |
| `bind_text` | String | — | Subject string/integer to observe |
| `bind_text-fmt` | String | — | `printf`-style format string (e.g. `"%d °C"`) |
| `translation_tag` | String | — | Translation tag from `translations.xml` |

### Example
```xml
<!-- ✅ Correct: Formatted dynamic temperature readout with wrap mode -->
<lv_label name="temp_display"
          width="120"
          long_mode="wrap"
          text="-- °C"
          bind_text="subject_temp"
          bind_text-fmt="%d °C"
          style_text_font="montserrat_bold_24"
          style_text_color="0x0f172a" />

<!-- ❌ Incorrect: Putting printf format directly inside bind_text -->
<lv_label bind_text="subject_temp: %d °C" />
```

---

## 2. `<lv_image>`

Displays bitmap or vector image assets declared in `globals.xml`.

### Key Attributes
| Attribute | Type | Default | Description |
|---|---|---|---|
| `src` | String | — | Asset identifier defined in `<images>` in `globals.xml` |
| `rotation` | Integer | `0` | Angle in 0.1° units (e.g. `900` = 90° clockwise) |
| `scale` | Integer | `256` | Scaling factor where `256` = 100% |
| `pivot_x`, `pivot_y` | Integer | Center | Transform pivot point coordinates in px |

### Example
```xml
<!-- ✅ Correct: 90-degree rotated icon asset -->
<lv_image name="fan_icon"
          src="icon_fan"
          rotation="900"
          scale="256"
          align="center" />
```

---

## 3. `<lv_bar>`

Progress bar or level indicator.

### Key Attributes
| Attribute | Type | Default | Description |
|---|---|---|---|
| `value` | Integer | `0` | Current progress value |
| `min_value` / `max_value` | Integer | `0` / `100` | Value range boundaries |
| `start_value` | Integer | `0` | Starting value when `mode="range"` |
| `mode` | Enum | `normal` | `normal`, `symmetrical`, or `range` |
| `bind_value` | String | — | Subject integer binding |

### Example
```xml
<!-- ✅ Correct: Progress bar with rounded indicator styling -->
<lv_bar name="battery_bar"
        width="180" height="12"
        min_value="0" max_value="100"
        value="75"
        bind_value="subject_battery"
        style_bg_color-indicator="0x22c55e"
        style_radius="6" />
```

---

## 4. `<lv_scale>`

Linear or circular graduated scale with ticks and labeled increments.

### Key Attributes
| Attribute | Type | Default | Description |
|---|---|---|---|
| `mode` | Enum | `horizontal_bottom` | `horizontal_top`, `horizontal_bottom`, `vertical_left`, `vertical_right`, `round_inner`, `round_outer` |
| `total_tick_count` | Integer | `11` | Total tick marks |
| `major_tick_every` | Integer | `2` | Number of minor ticks between major ticks |
| `min_value` / `max_value` | Integer | `0` / `100` | Numeric scale range |
| `label_show` | Boolean | `true` | Display numeric labels next to major ticks |

### Sub-Element: `<lv_scale-section>`
Defines a colored range band on the scale.
- Attributes: `style_main`, `style_items`, `style_indicator`, `bind_min_value`, `bind_max_value`

### Example
```xml
<!-- ✅ Correct: Horizontal bottom scale with styled threshold section -->
<lv_scale name="tachometer_scale"
          width="260" height="60"
          mode="horizontal_bottom"
          total_tick_count="11"
          major_tick_every="2"
          min_value="0" max_value="8000"
          label_show="true">
    <lv_scale-section style_main="style_redline"
                      bind_min_value="subject_redline_min"
                      bind_max_value="subject_redline_max" />
</lv_scale>
```

---

## 5. `<lv_chart>`

Visual chart for plotting lines, bars, or scatter points.

### Key Attributes
| Attribute | Type | Default | Description |
|---|---|---|---|
| `type` | Enum | `line` | `line`, `bar`, or `scatter` |
| `point_count` | Integer | `10` | Number of data points per series |

### Sub-Elements
1. `<lv_chart-series color="..." axis="primary_y|secondary_y" values="..." />`: Data line or bar set.
2. `<lv_chart-axis axis="primary_y|secondary_y" min_value="..." max_value="..." />`: Y-axis range limits.
3. `<lv_chart-cursor color="..." dir="hor|ver|all" pos_x="..." pos_y="..." />`: Target guide crosshair.

### Example
```xml
<!-- ✅ Correct: Two series chart with dual axis definitions -->
<lv_chart name="env_chart" width="90%" height="180" type="line" point_count="8">
    <lv_chart-series color="0xef4444" axis="primary_y" values="20 24 28 32 30 26 22 21" />
    <lv_chart-series color="0x3b82f6" axis="secondary_y" values="45 50 60 75 70 65 55 50" />
    <lv_chart-axis axis="primary_y" min_value="0" max_value="50" />
    <lv_chart-axis axis="secondary_y" min_value="0" max_value="100" />
</lv_chart>
```

---

## 6. `<lv_spinner>`

Indeterminate loading animation.

### Key Attributes & Styling
Uses standard positioning and style attributes (`arc_color`, `arc_width` on `main` and `indicator` parts).

### Example
```xml
<!-- ✅ Correct: Loading spinner with customized track width and color -->
<lv_spinner name="sync_spinner"
            width="48" height="48"
            align="center"
            style_arc_color-indicator="0x3b82f6"
            style_arc_width-indicator="4"
            style_arc_color-main="0xe2e8f0"
            style_arc_width-main="4" />
```

---

## 7. `<lv_led>`

Status indicator mimicking a physical LED diode.

### Key Attributes
| Attribute | Type | Default | Description |
|---|---|---|---|
| `color` | Color | `0xff0000` | Diode emissive glow color |
| `brightness` | Integer | `255` | LED brightness level (0 = off, 255 = max bright) |

### Example
```xml
<!-- ✅ Correct: Green system power status LED -->
<lv_led name="power_led"
        width="20" height="20"
        color="0x22c55e"
        brightness="255" />
```

---

## 8. `<lv_line>`

Renders 2D multi-segment vector lines connecting ordered points.

### Key Attributes
| Attribute | Type | Default | Description |
|---|---|---|---|
| `points` | String | — | Space-separated `x,y` coordinates (e.g. `"0,0 50,30 100,0"`) |
| `y_invert` | Boolean | `false` | Invert Y coordinates so Y grows upwards |

### Example
```xml
<!-- ✅ Correct: Connected vector polyline -->
<lv_line name="divider_line"
         points="0,0 120,40 240,0"
         style_line_width="3"
         style_line_color="0x64748b"
         style_line_rounded="true" />
```

---

## 9. `<lv_spangroup>`

Multi-style rich-text container allowing individual substrings to have distinct styles.

### Sub-Element: `<lv_spangroup-span>`
- Attributes: `text`, `style` (references a named `<style>` class).

### Example
```xml
<!-- ✅ Correct: Inline rich text with individual span styling -->
<lv_spangroup name="rich_notice" width="280" height="content" overflow="ellipsis">
    <lv_spangroup-span text="Status: " style="style_bold" />
    <lv_spangroup-span text="CRITICAL" style="style_alert_red" />
    <lv_spangroup-span text=" - Over temperature detected." style="style_regular" />
</lv_spangroup>
```

---

## 10. `<lv_calendar>`

Full month calendar grid.

### Key Attributes
| Attribute | Type | Description |
|---|---|---|
| `today_year`, `today_month`, `today_day` | Integer | Date coordinates highlighted as "today" |
| `shown_year`, `shown_month` | Integer | Currently displayed month/year view |

### Sub-Elements
- `<lv_calendar-header_arrow />`: Adds previous/next navigation arrows on top of the month grid.

### Example
```xml
<!-- ✅ Correct: Monthly calendar with navigation header -->
<lv_calendar name="schedule_cal"
             width="280" height="220"
             align="center"
             today_year="2026" today_month="8" today_day="23"
             shown_year="2026" shown_month="8">
    <lv_calendar-header_arrow />
</lv_calendar>
```
