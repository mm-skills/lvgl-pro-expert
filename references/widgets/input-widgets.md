# Input Widgets Reference

Input widgets receive touch, pointer, and keypad interaction. Always provide a unique `name` attribute on every widget instance so C code generators and event systems can bind handlers properly.

---

## Quick Reference Summary

| Widget | Primary Styleable Parts | Primary Event / Binding |
|---|---|---|
| `<lv_slider>` | `main`, `indicator`, `knob` | `bind_value`, `value_changed` |
| `<lv_arc>` | `main`, `indicator`, `knob` | `bind_value`, `value_changed` |
| `<lv_dropdown>` | `main`, `indicator`, `list` (`main`, `selected`, `scrollbar`) | `bind_value`, `value_changed` |
| `<lv_roller>` | `main`, `selected` | `bind_value`, `value_changed` |
| `<lv_spinbox>` | `main`, `cursor` | `bind_value`, `value_changed` |
| `<lv_switch>` | `main`, `indicator`, `knob` | `bind_checked`, `value_changed` |
| `<lv_checkbox>` | `main`, `indicator` | `bind_checked`, `clicked` |
| `<lv_keyboard>` | `main`, `items` | `textarea` target |
| `<lv_buttonmatrix>` | `main`, `items` | `clicked`, `value_changed` |

---

## 1. `<lv_slider>`

Interactive bar for selecting a numeric value along a line.

### Key Attributes
| Attribute | Type | Default | Description |
|---|---|---|---|
| `value` | Integer | `0` | Initial slider value |
| `min_value` / `max_value` | Integer | `0` / `100` | Minimum and maximum values |
| `left_value` | Integer | `0` | Left value when `mode="range"` |
| `mode` | Enum | `normal` | `normal`, `symmetrical`, or `range` |
| `bind_value` | String | — | Subject name to observe/mutate |

### Example
```xml
<!-- ✅ Correct: Slider with range mode and part styling -->
<lv_slider name="temp_slider"
           width="220" height="16"
           min_value="10" max_value="40"
           value="22"
           bind_value="subject_temp"
           style_bg_color-indicator="0x3b82f6"
           style_bg_color-knob="0x1d4ed8" />

<!-- ❌ Incorrect: Missing name attribute and using invalid part syntax -->
<lv_slider min="10" max="40" style_bg_color="0x3b82f6" part="indicator" />
```

---

## 2. `<lv_arc>`

Circular gauge or rotary slider. Set `clickable="true"` to let users drag the knob.

### Key Attributes
| Attribute | Type | Default | Description |
|---|---|---|---|
| `value` | Integer | `0` | Current value |
| `min_value` / `max_value` | Integer | `0` / `100` | Minimum and maximum values |
| `bg_start_angle` | Integer | `135` | Background track start angle in degrees (0–360) |
| `bg_end_angle` | Integer | `45` | Background track end angle in degrees (0–360) |
| `rotation` | Integer | `0` | Zero-degree angle offset |
| `mode` | Enum | `normal` | `normal`, `reverse`, or `symmetrical` |
| `clickable` | Boolean | `false` | Enable touch dragging of knob |

### Example
```xml
<!-- ✅ Correct: Interactive circular thermostat arc -->
<lv_arc name="thermo_arc"
        width="180" height="180"
        align="center"
        min_value="16" max_value="32"
        value="21"
        bg_start_angle="135" bg_end_angle="45"
        clickable="true"
        bind_value="subject_setpoint"
        style_arc_width-main="8"
        style_arc_width-indicator="12"
        style_arc_color-indicator="0xef4444" />
```

---

## 3. `<lv_dropdown>`

Collapsible selection menu. Options must be delimited by XML newline entities (`&#10;`).

### Key Attributes
| Attribute | Type | Default | Description |
|---|---|---|---|
| `options` | String | — | Option list separated by `&#10;` |
| `selected` | Integer | `0` | Zero-based index of selected option |
| `dir` | Enum | `bottom` | Expansion direction: `bottom`, `top`, `left`, `right` |
| `text` | String | — | Static header label (overrides showing selected text) |
| `bind_value` | String | — | Subject integer binding index |

### Example
```xml
<!-- ✅ Correct: Options delimited by XML entity &#10; -->
<lv_dropdown name="mode_select"
             width="160"
             options="Off&#10;Heating&#10;Cooling&#10;Auto"
             selected="1"
             bind_value="subject_mode" />

<!-- ❌ Incorrect: Literal \n or raw newlines break option parsing -->
<lv_dropdown name="mode_select" options="Off\nHeating\nCooling\nAuto" />
```

---

## 4. `<lv_roller>`

Scrollable rotating drum picker. Ideal for compact wheel-style selections (time, dates).

### Key Attributes
| Attribute | Type | Default | Description |
|---|---|---|---|
| `options` | String | — | Options separated by `&#10;` |
| `selected` | Integer | `0` | Zero-based index |
| `options-mode` | Enum | `normal` | `normal` (stops at ends) or `infinite` (wraps) |
| `visible_row_count`| Integer | `3` | Number of rows visible simultaneously |

### Example
```xml
<!-- ✅ Correct: Infinite scrolling day selector -->
<lv_roller name="day_roller"
           width="120"
           options="Mon&#10;Tue&#10;Wed&#10;Thu&#10;Fri&#10;Sat&#10;Sun"
           options-mode="infinite"
           visible_row_count="3"
           bind_value="subject_day"
           style_text_color-selected="0x2563eb" />
```

---

## 5. `<lv_spinbox>`

Numeric input with step increment/decrement buttons and configurable decimal position.

### Key Attributes
| Attribute | Type | Default | Description |
|---|---|---|---|
| `value` | Integer | `0` | Current integer value |
| `range_min` / `range_max` | Integer | `0` / `99999` | Value limits |
| `digit_count` | Integer | `5` | Total number of digits displayed |
| `dec_point_pos` | Integer | `0` | Decimal point position from right (0 = integer) |
| `step` | Integer | `1` | Increment step per button press |

### Example
```xml
<!-- ✅ Correct: Currency spinbox showing 000.00 -->
<lv_spinbox name="price_input"
            width="140" height="40"
            range_min="0" range_max="99999"
            digit_count="5" dec_point_pos="2"
            step="10"
            value="1999" />
```

---

## 6. `<lv_switch>`

Two-state toggle switch for binary preferences.

### Key Attributes
| Attribute | Type | Default | Description |
|---|---|---|---|
| `checked` | Boolean | `false` | Initial toggle state |
| `bind_checked` | String | — | Subject boolean/integer binding |

### Example
```xml
<!-- ✅ Correct: Styled toggle switch with subject binding -->
<lv_switch name="wifi_toggle"
           width="50" height="26"
           checked="true"
           bind_checked="subject_wifi_en"
           style_bg_color-indicator-checked="0x22c55e"
           style_bg_color-knob="0xffffff" />
```

---

## 7. `<lv_checkbox>`

Checkable box accompanied by a text label.

### Key Attributes
| Attribute | Type | Default | Description |
|---|---|---|---|
| `text` | String | `""` | Accompanying label text |
| `checked` | Boolean | `false` | Initial check state |
| `bind_checked` | String | — | Subject binding |

### Example
```xml
<!-- ✅ Correct: Checkbox with custom checked colors -->
<lv_checkbox name="agree_check"
             text="Enable notifications"
             checked="false"
             bind_checked="subject_notif"
             style_bg_color-indicator-checked="0x6366f1" />
```

---

## 8. `<lv_keyboard>`

On-screen virtual keyboard that sends characters directly into a targeted `<lv_textarea>`.

### Key Attributes
| Attribute | Type | Default | Description |
|---|---|---|---|
| `mode` | Enum | `text_lower` | `text_lower`, `text_upper`, `special`, `number` |
| `textarea` | String | `""` | Name of the `<lv_textarea>` widget to target |

### Example
```xml
<!-- ✅ Correct: Textarea paired with an on-screen keyboard -->
<lv_textarea name="user_input" width="90%" height="40" placeholder_text="Enter PIN..." one_line="true" />

<lv_keyboard name="pin_keyboard"
             width="100%" height="160"
             align="bottom_mid"
             mode="number"
             textarea="user_input" />
```

---

## 9. `<lv_buttonmatrix>`

High-performance grid of buttons rendered as a single lightweight widget.

### Key Attributes
| Attribute | Type | Description |
|---|---|---|
| `map` | String | Space-separated list of single-quoted button labels. Use `'&#10;'` for row breaks. |
| `ctrl_map` | String | Space-separated button control flags matching each button in `map`. |

### Control Flags (`ctrl_map`)
- `none`: Normal button behavior
- `checkable`: Can be toggled on/off
- `checked`: Starts in checked state (combine with `checkable|checked`)
- `disabled`: Unclickable and visually dimmed
- `hidden`: Hidden while reserving grid slot

### Example
```xml
<!-- ✅ Correct: 3x3 numeric keypad with row breaks and flag control -->
<lv_buttonmatrix name="num_pad"
                 width="240" height="200"
                 align="center"
                 map="'1' '2' '3' '&#10;' '4' '5' '6' '&#10;' '7' '8' '9' '&#10;' '*' '0' '#'"
                 ctrl_map="none none none none none none none none none none none none"
                 style_bg_color-items="0x334155" />

<!-- ❌ Incorrect: Raw unquoted labels and \n row breaks -->
<lv_buttonmatrix name="num_pad" map="1 2 3 \n 4 5 6" />
```
