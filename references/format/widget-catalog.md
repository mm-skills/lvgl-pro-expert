# LVGL Pro XML: Widget Catalog

Covers all 29 LVGL Pro widgets with core props in-skill and MCP pointers for exhaustive detail.

> [!NOTE]
> **How to use this catalog:**
> 1. Find your widget's **Core props** here — covers >90% of daily usage, instant lookup
> 2. If you need a prop not listed, use the **MCP query** shown at the end of each entry
> 3. If MCP is unavailable: read `tmp/lvgl_pro/lvgl_widgets_xml/v9.5.0/<widget>.xml` directly
>
> Widget tags map directly to LVGL C types. All widgets inherit universal props from `lv_obj`.

---

## Universal Properties (all widgets inherit these)

These come from `lv_obj` — do **not** repeat per-widget. For full `lv_obj` prop list (170 props)
use MCP query: `"lv_obj all properties layout flex scroll alignment"`.

| Prop | Type | Notes |
|------|------|-------|
| `name` | string | **Required** — becomes the C variable name |
| `x`, `y` | int / % | Offset from alignment point |
| `width`, `height` | int / % / `"content"` | Prefer `"content"` or `"100%"` over hardcoded px |
| `align` | enum | `center` · `top_left` · `top_mid` · `top_right` · `bottom_left` · `bottom_mid` · `bottom_right` · `left_mid` · `right_mid` |
| `flex_flow` | enum | `row` · `column` · `row_wrap` · `column_wrap` · `row_reverse` · `column_reverse` |
| `style_flex_main_place` | enum | `start` · `end` · `center` · `space_evenly` · `space_around` · `space_between` |
| `style_flex_cross_place` | enum | `start` · `end` · `center` |
| `style_pad_row`, `style_pad_column` | int | Gap between flex children |
| `hidden` | bool | Visibility toggle |
| `clickable` | bool | Whether widget receives touch/click events |

---

## 1. Containers & Text

### `<lv_obj>` — Base Container
The foundation of all layouts. Use as a generic panel or flex container.

**Core props:** All universal props apply. No additional widget-specific props.
**Parts:** `main`, `scrollbar`
**Example:**
```xml
<lv_obj name="panel" width="100%" height="content" flex_flow="column"
        style_pad_row="16" style_bg_color="0x1a1a2e" />
```

---

### `<lv_label>` — Text Label

**Core props:**

| Prop | Type | Description |
|------|------|-------------|
| `text` | string | Static text content |
| `long_mode` | enum | How overflow is handled (see enums below) |
| `bind_text` | subject | Bind text to a reactive subject |
| `bind_text-fmt` | string | Printf format string for bound value, e.g. `"%d°C"` |

**`long_mode` enum:** `wrap` · `scroll` · `scroll_circular` · `clip` · `dots`

**Parts:** `main`, `selected`
**Example:**
```xml
<lv_label name="lbl_temp" bind_text="subject_temp" bind_text-fmt="%d°C" />
<lv_label name="lbl_title" text="Settings" long_mode="clip" />
```
> 2 additional props exist (`recolor`, `translation_tag`).
> **MCP:** `"lv_label all properties long_mode recolor translation"`

---

### `<lv_image>` — Image Display

**Core props:**

| Prop | Type | Description |
|------|------|-------------|
| `src` | image | Image name from `globals.xml` `<images>` block |
| `rotation` | int | Degrees (e.g. `900` = 90°) |
| `scale_x`, `scale_y` | int | Scale factor — 100 = original size |
| `pivot_x`, `pivot_y` | int / % | Rotation/scale pivot point |
| `inner_align` | enum | How image fills its bounds |
| `bind_src` | subject:pointer | Bind image source to a pointer subject |

**`inner_align` enum (14 values — common: `default` · `center` · `stretch` · `contain` · `cover`):**
> Full list: `default`, `top_left`, `top_mid`, `top_right`, `bottom_left`, `bottom_mid`,
> `bottom_right`, `left_mid`, `right_mid`, `center`, `stretch`, `tile`, `contain`, `cover`
> **MCP:** `"lv_image inner_align enum values tile stretch contain cover"`

**Parts:** `main`
**Example:**
```xml
<lv_image name="img_logo" src="logo_img" scale_x="100" scale_y="100" align="center" />
```

---

## 2. Interactive Controls

### `<lv_button>` — Standard Button
No widget-specific API props. Size/style via universal props.

**Parts:** `main`
**Example:**
```xml
<lv_button name="btn_ok" width="120" height="40">
    <lv_label name="lbl_ok" text="OK" align="center" />
    <screen_load_event screen="home_screen" />
</lv_button>
```

---

### `<lv_switch>` — Toggle Switch

**Core props:**

| Prop | Type | Description |
|------|------|-------------|
| `checked` | bool | Initial on/off state |
| `bind_value` | subject | Bind checked state to an int subject (0/1) |

**Parts:** `main`, `indicator`, `knob`
**Example:** `<lv_switch name="sw_wifi" bind_value="subject_wifi_on" />`

---

### `<lv_checkbox>` — Checkbox

**Core props:**

| Prop | Type | Description |
|------|------|-------------|
| `text` | string | Label shown beside the checkbox |
| `bind_value` | subject | Bind checked state to an int subject (0/1) |

**Parts:** `main`, `indicator`
**Example:** `<lv_checkbox name="cb_agree" text="Accept Terms" />`

---

### `<lv_slider>` — Slider

**Core props:**

| Prop | Type | Description |
|------|------|-------------|
| `value` | int | Current value |
| `min_value` | int | Minimum (default 0). If min > max, fills right-to-left |
| `max_value` | int | Maximum (default 100) |
| `start_value` | int | Range-mode lower knob value |
| `mode` | enum | `normal` · `range` · `symmetrical` |
| `orientation` | enum | `auto` · `horizontal` · `vertical` |
| `bind_value` | subject | Bind current value to a subject |

**`value-anim`** / **`start_value-anim`**: bool — animate value changes (default `false`)

**Parts:** `main` (track), `indicator` (fill), `knob` (handle — two knobs in `range` mode)
**Example:**
```xml
<lv_slider name="sld_vol" value="50" min_value="0" max_value="100"
           bind_value="subject_volume" width="80%" />
```
> **MCP:** `"lv_slider all properties range mode symmetrical orientation"`

---

### `<lv_arc>` — Circular Arc / Gauge

**Core props:**

| Prop | Type | Description |
|------|------|-------------|
| `value` | int | Current value |
| `min_value` | int | Minimum value |
| `max_value` | int | Maximum value |
| `start_angle` | int | Arc indicator start angle (degrees, 0 = 3 o'clock) |
| `end_angle` | int | Arc indicator end angle |
| `bg_start_angle` | int | Background arc start angle |
| `bg_end_angle` | int | Background arc end angle |
| `rotation` | int | Rotate the whole arc widget |
| `mode` | enum | `normal` · `symmetrical` · `reverse` |
| `bind_value` | subject | Bind current value to a subject |

> 1 additional prop: `change_rate` (rate-limit touch input, int ms).
> **MCP:** `"lv_arc change_rate properties mode symmetrical"`

**Parts:** `main` (background arc), `indicator` (filled arc), `knob` (drag handle)
**Example:**
```xml
<lv_arc name="arc_temp" value="22" min_value="15" max_value="35"
        bg_start_angle="135" bg_end_angle="45"
        mode="symmetrical" bind_value="subject_temp" />
```

---

### `<lv_spinbox>` — Numeric Spinbox

**Core props:**

| Prop | Type | Description |
|------|------|-------------|
| `value` | int | Current integer value |
| `digit_count` | int | Total number of digits to display |
| `decimal_point_position` | int | Digits after decimal point |
| `range_max` | int | Maximum allowed value |
| `range_min` | int | Minimum allowed value |
| `step` | int | Increment/decrement step |
| `rollover` | bool | Wrap around at min/max |
| `bind_value` | subject | Bind value to a subject |

**Parts:** `main`, `cursor`, `selected`
**Example:**
```xml
<lv_spinbox name="spb_setpoint" value="200" digit_count="4"
            decimal_point_position="1" range_min="0" range_max="999" step="1" />
```
> **MCP:** `"lv_spinbox digit_count decimal_point rollover step range"`

---

### `<lv_textarea>` — Text Input

**Core props:**

| Prop | Type | Description |
|------|------|-------------|
| `text` | string | Initial text content |
| `placeholder_text` | string | Hint shown when empty |
| `one_line` | bool | Single-line mode (default false) |
| `password_mode` | bool | Mask typed characters |
| `password_show_time` | int | ms to briefly show each typed char (default 1500) |
| `text_selection` | bool | Enable text selection (default true) |
| `cursor_pos` | int | Initial cursor position |

**Parts:** `main`, `scrollbar`, `selected`, `cursor`, `textarea_placeholder`
**Example:**
```xml
<lv_textarea name="ta_email" placeholder_text="Enter email" one_line="true" />
```
> **MCP:** `"lv_textarea password one_line cursor_pos placeholder"`

---

### `<lv_keyboard>` — On-screen Keyboard

**Core props:**

| Prop | Type | Description |
|------|------|-------------|
| `mode` | enum | Initial keyboard layout |
| `popovers` | bool | Show enlarged key preview on press |
| `textarea` | lv_obj | Attach keyboard to a specific textarea widget |

**`mode` enum (common: `text_lower` · `text_upper` · `number`):**
> Full: `text_upper`, `text_lower`, `text_arabic`, `special`, `number`, `user_1`–`user_4`
> **MCP:** `"lv_keyboard mode enum user layout popovers"`

**Parts:** `main`, `items` — combine `items` with states: `items|pressed`, `items|checked`
**Example:**
```xml
<lv_keyboard name="kb" mode="text_lower" popovers="true" textarea="ta_input" />
```

---

### `<lv_imagebutton>` — Image-backed Button

**Core props:**

| Prop | Type | Description |
|------|------|-------------|
| `state` | enum | Initial state of the button |

**Sub-elements** (`src_left`, `src_mid`, `src_right` — set per state):
```xml
<lv_imagebutton name="ibtn_play">
    <lv_imagebutton-src_mid state="released" src="img_play" />
    <lv_imagebutton-src_mid state="pressed" src="img_play_pressed" />
    <lv_imagebutton-src_mid state="checked_released" src="img_pause" />
</lv_imagebutton>
```
**`state` enum:** `released` · `pressed` · `disabled` · `checked_released` · `checked_pressed` · `checked_disabled`

**Parts:** `main`
> **MCP:** `"lv_imagebutton state src_left src_mid src_right image button"`

---

## 3. Selection Widgets

### `<lv_dropdown>` — Dropdown Menu

**Core props:**

| Prop | Type | Description |
|------|------|-------------|
| `options` | string | Options separated by `&#10;` (XML newline) |
| `selected` | int | Initially selected index (0-based) |
| `dir` | enum | Which direction the list opens |
| `symbol` | image | Icon shown beside the button text |
| `text` | string | Fixed label instead of selected option |
| `bind_value` | subject | Bind selected index to a subject |

**`dir` enum:** `bottom` (default) · `top` · `left` · `right`

**Sub-element:** `<lv_dropdown-list>` — styles the open list popup
**Parts (button):** `main`, `indicator`
**Parts (list):** `main`, `scrollbar`, `selected`

**Example:**
```xml
<lv_dropdown name="dd_mode" options="Heat&#10;Cool&#10;Auto"
             selected="0" bind_value="subject_mode" />
```
> **MCP:** `"lv_dropdown symbol text fixed label dir enum"`

---

### `<lv_roller>` — Roller / Tumbler

**Core props:**

| Prop | Type | Description |
|------|------|-------------|
| `options` | string | Options separated by `&#10;` |
| `options-mode` | enum | `normal` (stops at ends) · `infinite` (wraps) |
| `selected` | int | Initially selected index |
| `selected-animated` | bool | Animate selection change |
| `visible_row_count` | int | How many rows are visible at once |
| `bind_value` | subject | Bind selected index to a subject |

**Parts:** `main`, `selected`
**Example:**
```xml
<lv_roller name="rol_day"
           options="Mon&#10;Tue&#10;Wed&#10;Thu&#10;Fri&#10;Sat&#10;Sun"
           options-mode="infinite" visible_row_count="3" selected="0" />
```
> **MCP:** `"lv_roller options mode infinite visible_row_count"`

---

### `<lv_buttonmatrix>` — Button Matrix

**Core props:**

| Prop | Type | Description |
|------|------|-------------|
| `map` | string[] | Button labels; `"\n"` starts a new row, `""` ends the map |
| `ctrl_map` | enum[] | Control flags per button |
| `one_checked` | bool | Force exactly one button checked at all times |
| `selected_button` | int | Select a button by index |

**`ctrl_map` common flags:** `hidden` · `disabled` · `checkable` · `checked` · `no_repeat` · `click_trig` · `popover` · `recolor` · `width_1`…`width_15` (relative column width)
> 28 total enum values. **MCP:** `"lv_buttonmatrix ctrl_map width enum checkable hidden"`

**Parts:** `main` (background), `items` (buttons)
**Example:**
```xml
<lv_buttonmatrix name="btnm" map="'Btn1' 'Btn2' '\n' 'Wide' ''"
                 ctrl_map="width_2 width_2 width_4" />
```

---

## 4. Data Display

### `<lv_bar>` — Progress Bar

**Core props:**

| Prop | Type | Description |
|------|------|-------------|
| `value` | int | Current fill value |
| `min_value` | int | Minimum |
| `max_value` | int | Maximum |
| `start_value` | int | Range-mode start (lower fill) |
| `mode` | enum | `normal` · `symmetrical` · `range` |
| `orientation` | enum | `auto` · `horizontal` · `vertical` |
| `bind_value` | subject | Bind fill value to a subject |

**`value-anim`** / **`start_value-anim`**: bool — animate transitions (default `false`)

**Parts:** `main` (track), `indicator` (fill)
**Example:**
```xml
<lv_bar name="bar_progress" value="65" min_value="0" max_value="100"
        mode="normal" width="200" height="20" />
```
> **MCP:** `"lv_bar mode symmetrical range orientation bind_value"`

---

### `<lv_chart>` — Chart

**Core props:**

| Prop | Type | Description |
|------|------|-------------|
| `type` | enum | Chart rendering style |
| `point_count` | int | Data points per series |
| `update_mode` | enum | How new data is added |
| `hor_div_line_count` | int | Horizontal grid lines |
| `ver_div_line_count` | int | Vertical grid lines |

**`type` enum:** `none` · `line` · `bar` · `stacked` · `scatter`
**`update_mode` enum:** `shift` (scrolls left) · `circular` (ring buffer)

**Sub-elements:**
```xml
<lv_chart name="chart" type="line" point_count="20" update_mode="shift">
    <lv_chart-series color="0x4CAF50" axis="primary_y" values="10,20,15,30" />
    <lv_chart-series color="0x2196F3" axis="secondary_y" values="5,8,12,6" />
    <lv_chart-axis axis="primary_y" min_value="0" max_value="100" />
    <lv_chart-cursor color="0xFF5722" dir="right" />
</lv_chart>
```
**`lv_chart-axis` `axis` enum:** `primary_x` · `primary_y` · `secondary_x` · `secondary_y`

**Parts:** `main`, `items`, `indicator`, `cursor`, `scrollbar`
> **MCP:** `"lv_chart series cursor axis configuration properties"`

---

### `<lv_scale>` — Scale / Gauge Ruler

**Core props:**

| Prop | Type | Description |
|------|------|-------------|
| `mode` | enum | Layout mode of the scale |
| `range_min_value` | int | Minimum value |
| `range_max_value` | int | Maximum value |
| `total_tick_count` | int | Total number of ticks |
| `major_tick_every` | int | Every Nth tick is a major tick |
| `label_show` | bool | Show text labels at major ticks |
| `angle_range` | int | Arc span in degrees (round scales) |
| `rotation` | int | Rotate the scale (degrees) |

**`mode` enum:** `horizontal_top` · `horizontal_bottom` · `vertical_left` · `vertical_right` · `round`

**Sub-elements:** `<lv_scale-section>` — style a value range within the scale:
```xml
<lv_scale name="gauge" mode="round" range_min_value="0" range_max_value="100"
          total_tick_count="21" major_tick_every="5" angle_range="270" rotation="135">
    <lv_scale-section min_value="0" max_value="60"
                      indicator_style="style_green_tick" />
    <lv_scale-section min_value="60" max_value="100"
                      indicator_style="style_red_tick" />
</lv_scale>
```
**Parts:** `main`, `indicator` (major ticks + labels), `items` (minor ticks)
> 3 additional props. **MCP:** `"lv_scale all properties sections major minor tick label"`

---

### `<lv_led>` — LED Indicator

**Core props:**

| Prop | Type | Description |
|------|------|-------------|
| `color` | color | LED color, e.g. `"0xff0000"` |
| `brightness` | opa | Brightness as % or 0–255 |

**Parts:** `main`
**Example:** `<lv_led name="led_status" color="0x00ff00" brightness="80%" />`

---

### `<lv_line>` — Polyline

**Core props:**

| Prop | Type | Description |
|------|------|-------------|
| `points` | precise_points[] | Point list, e.g. `"(10 20) (60 40) (20 60)"` |
| `y_invert` | bool | If true, y=0 is at the bottom of the widget |

**Parts:** `main` — use `line_width`, `line_color`, `line_rounded`, `line_dash_width`/`line_dash_gap`
**Example:** `<lv_line name="ln_graph" points="(0 50) (50 10) (100 40)" />`

---

### `<lv_spinner>` — Loading Spinner

**Core props:**

| Prop | Type | Description |
|------|------|-------------|
| `anim_duration` | int | Full rotation time in ms (e.g. `1500`) |
| `arc_sweep` | int | Spinning arc length in degrees (180–360) |

**Parts:** `main` (background arc), `indicator` (spinning arc)
**Example:** `<lv_spinner name="sp_loading" anim_duration="1000" arc_sweep="90" />`

---

### `<lv_animimg>` — Animated Image

**Core props:**

| Prop | Type | Description |
|------|------|-------------|
| `src` | image_src[count] | Array of image sources for animation frames |
| `duration` | int | Total animation cycle duration in ms |
| `repeat_count` | int | Number of loops (0 = infinite) |

**Parts:** `main`
**Example:** `<lv_animimg name="aimg_spin" src="frame1 frame2 frame3" duration="600" repeat_count="0" />`
> **MCP:** `"lv_animimg src frames duration repeat_count animation"`

---

### `<lv_gif>` — GIF Player

**Core props:**

| Prop | Type | Description |
|------|------|-------------|
| `src` | image | GIF file source |
| `loop_count` | int | Number of loops |

**Parts:** `main`
**Example:** `<lv_gif name="gif_logo" src="logo_gif" />`
> **MCP:** `"lv_gif src loop_count properties"`

---

### `<lv_qrcode>` — QR Code

**Core props:**

| Prop | Type | Description |
|------|------|-------------|
| `data` | string | UTF-8 string to encode |
| `size` | int | QR code pixel size |
| `dark_color` | color | Foreground module color (default black) |
| `light_color` | color | Background color (default white) |
| `quiet_zone` | bool | Add margin border around the code |

**Parts:** `main` — background/border only; module colors use `dark_color`/`light_color`
**Example:**
```xml
<lv_qrcode name="qr_wifi" data="WIFI:S:MySSID;T:WPA;P:password;;" size="150" />
```

---

### `<lv_canvas>` — Canvas (Custom Drawing)
No widget-specific API props. Drawing is done via event callbacks.

**Parts:** `main`
> **MCP:** `"lv_canvas drawing custom buffer lv_canvas_set_buffer"`

---

## 5. Complex Containers

### `<lv_tabview>` — Tab View

**Core props:**

| Prop | Type | Description |
|------|------|-------------|
| `tab_bar_position` | enum | `top` (default) · `bottom` · `left` · `right` |
| `active` | int | Active tab index (0-based) |
| `active-anim` | bool | Animate tab switching (default `false`) |

**Sub-elements:**
- `<lv_tabview-tab text="Label">` — adds a tab with content
- `<lv_tabview-tab_bar>` — style the tab button bar
- `<lv_tabview-tab_button index="N">` — parent widgets onto a specific tab button

**Parts:** `main`
**Example:**
```xml
<lv_tabview name="tabs" tab_bar_position="top" active="0">
    <lv_tabview-tab text="Home">
        <lv_label name="lbl_home" text="Home content" />
    </lv_tabview-tab>
    <lv_tabview-tab text="Settings">
        <lv_label name="lbl_settings" text="Settings content" />
    </lv_tabview-tab>
</lv_tabview>
```
> **MCP:** `"lv_tabview tab_bar_position active anim tab_button index"`

---

### `<lv_table>` — Table

**Core props:**

| Prop | Type | Description |
|------|------|-------------|
| `col_count` | int | Number of columns |
| `row_count` | int | Number of rows |

**Sub-element:** `<lv_table-cell row="R" col="C" value="text" />`

**Parts:** `main`, `items` (cells) — use `items|checked` for selected cell style
**Example:**
```xml
<lv_table name="tbl_data" col_count="3" row_count="4">
    <lv_table-cell row="0" col="0" value="Name" />
    <lv_table-cell row="0" col="1" value="Value" />
</lv_table>
```
> Additional: `col_width` per column. **MCP:** `"lv_table col_width cell row column value"`

---

### `<lv_spangroup>` — Mixed-Style Text

**Core props:**

| Prop | Type | Description |
|------|------|-------------|
| `overflow` | enum | `clip` · `ellipsis` |
| `max_lines` | int | Maximum visible lines |
| `indent` | int | First-line indent in px |

**Sub-element:** `<lv_spangroup-span text="..." style="style_name" />`
Spans support `bind_text`/`bind_text-fmt` too.

**Parts:** `main`
**Example:**
```xml
<lv_spangroup name="sg_desc" width="300" height="content">
    <lv_spangroup-span text="Status: " style="style_normal" />
    <lv_spangroup-span bind_text="subject_status" style="style_bold" />
</lv_spangroup>
```

---

### `<lv_calendar>` — Calendar Picker

**Core props:**

| Prop | Type | Description |
|------|------|-------------|
| `today_year` | int | Current year (e.g. `2025`) |
| `today_month` | int | Current month (1–12) |
| `today_day` | int | Current day (1–31) |
| `shown_year` | int | Year to display in the view |
| `shown_month` | int | Month to display in the view |
| `chinese_mode` | bool | Use Chinese lunar calendar formatting |

**Parts:** `main`, `items` (day cells), `indicator` (today highlight)
**Example:**
```xml
<lv_calendar name="cal" today_year="2025" today_month="8" today_day="31"
             shown_year="2025" shown_month="8" />
```
> **MCP:** `"lv_calendar today shown_year month day highlighted chinese_mode"`

---

## Widget Part Map Summary

| Widget | Parts |
|--------|-------|
| `lv_obj`, `lv_button`, `lv_label`, `lv_image`, `lv_canvas` | `main` |
| `lv_slider`, `lv_arc`, `lv_switch` | `main`, `indicator`, `knob` |
| `lv_bar`, `lv_checkbox`, `lv_scale` | `main`, `indicator` |
| `lv_slider`, `lv_arc` (also) | + `items` (minor ticks on scale) |
| `lv_textarea` | `main`, `scrollbar`, `selected`, `cursor`, `textarea_placeholder` |
| `lv_chart` | `main`, `items`, `indicator`, `cursor`, `scrollbar` |
| `lv_dropdown` button / list | `main`, `indicator` / `main`, `scrollbar`, `selected` |
| `lv_roller` | `main`, `selected` |
| `lv_buttonmatrix`, `lv_keyboard` | `main`, `items` |
| `lv_spinner` | `main` (bg arc), `indicator` (spinning arc) |
| `lv_spinbox` | `main`, `cursor`, `selected` |
