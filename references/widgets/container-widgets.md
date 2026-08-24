# Container Widgets Reference

Container widgets organize, group, and structure other widgets across the screen.

---

## 1. `<lv_obj>` — Base Object & Universal Container

`<lv_obj>` is both the base ancestor for all LVGL widgets and the primary layout container for cards, toolbars, and scrollable panels.

### Key Attributes & Container Flags
| Attribute | Type | Default | Description |
|---|---|---|---|
| `scrollable` | Boolean | `true` | Allow content to scroll when larger than bounds |
| `scrollbar_mode` | Enum | `auto` | `auto`, `on`, `off`, or `active` |
| `scroll_snap_x` / `scroll_snap_y` | Enum | `none` | Snap alignment: `start`, `center`, `end`, `none` |
| `scroll_one` | Boolean | `false` | Limit scroll swipe to one snap stop |
| `ignore_layout` / `floating` | Boolean | `false` | Detach widget from parent flex/grid positioning |
| `flex_in_new_track` | Boolean | `false` | Force flex item into a new row or column |

### Default Style Reset
By default, `<lv_obj>` has a white background, rounded corners, padding, and a border. To use `<lv_obj>` as a clean transparent layout wrapper, include `<remove_style_all />` or set style properties to `0`.

### Example
```xml
<!-- ✅ Correct: Clean flex row card container -->
<lv_obj name="sensor_card"
        width="100%" height="content"
        layout="flex"
        flex_flow="row"
        style_flex_main_place="space_between"
        style_flex_cross_place="center"
        style_pad_all="12"
        style_radius="8"
        style_bg_color="0x1e293b"
        style_border_width="0">
    <lv_label text="Temperature" style_text_color="0xffffff" />
    <lv_label bind_text="subject_temp" bind_text-fmt="%d°C" style_text_color="0x38bdf8" />
</lv_obj>

<!-- ✅ Correct: Snapping horizontal carousel container -->
<lv_obj name="page_carousel"
        width="100%" height="160"
        scrollable="true"
        scroll_snap_x="center"
        scroll_one="true"
        layout="flex"
        flex_flow="row"
        style_pad_gap="16" />
```

---

## 2. `<lv_tabview>` — Multi-Page Tab Container

Provides a tab bar with swipeable or selectable content pages.

### Key Attributes
| Attribute | Type | Default | Description |
|---|---|---|---|
| `tab_bar_position` | Enum | `top` | `top`, `bottom`, `left`, `right`, or `none` |
| `tab_bar_size` | Integer | `40` | Height (top/bottom) or width (left/right) of the tab bar in px |

### Sub-Elements
1. `<lv_tabview-tab text="...">`: Creates a content page container.
2. `<lv_tabview-tab_button index="...">`: Parents custom child widgets (such as status badges or icons) directly onto an existing tab button.

### Example
```xml
<!-- ✅ Correct: Bottom tab bar with customized tab buttons -->
<lv_tabview name="main_tabs"
            width="100%" height="100%"
            tab_bar_position="bottom"
            tab_bar_size="50">
    <!-- Tab 1 -->
    <lv_tabview-tab text="Sensors">
        <lv_label text="Sensor readings..." align="center" />
    </lv_tabview-tab>

    <!-- Tab 2 -->
    <lv_tabview-tab text="Settings">
        <lv_label text="Device settings..." align="center" />
    </lv_tabview-tab>

    <!-- Optional: Attach child toggle switch to Tab 2's tab button -->
    <lv_tabview-tab_button index="1">
        <lv_switch name="quick_toggle" width="36" height="18" align="right_mid" x="-6" ignore_layout="true" />
    </lv_tabview-tab_button>
</lv_tabview>
```

---

## 3. `<lv_table>` — Lightweight Grid Table

Displays tabular text data in rows and columns without allocating individual sub-widgets for every cell.

### Key Attributes
| Attribute | Type | Default | Description |
|---|---|---|---|
| `row_count` | Integer | `1` | Number of rows |
| `column_count` | Integer | `1` | Number of columns |

### Sub-Elements
1. `<lv_table-column column="0" width="120px" />`: Sets explicit column width in pixels.
2. `<lv_table-cell row="0" column="0" value="Text" ctrl="merge_right" />`: Populates cell text and control flags (`merge_right`, etc.).

### Example
```xml
<!-- ✅ Correct: Structured data table with custom column widths -->
<lv_table name="log_table"
          row_count="3" column_count="2"
          align="center"
          width="90%">
    <lv_table-column column="0" width="80px" />
    <lv_table-column column="1" width="180px" />

    <lv_table-cell row="0" column="0" value="Time" />
    <lv_table-cell row="0" column="1" value="Event Description" />

    <lv_table-cell row="1" column="0" value="10:00" />
    <lv_table-cell row="1" column="1" value="System Booted" />

    <lv_table-cell row="2" column="0" value="10:05" />
    <lv_table-cell row="2" column="1" value="WiFi Connected" />
</lv_table>
```

---

## 4. `<lv_canvas>` — Direct Pixel Buffer Drawing Surface

Provides a dedicated drawing surface for custom line art, direct pixel manipulation, or software rendering pipelines.

### Key Attributes
| Attribute | Type | Description |
|---|---|---|
| `width` | Integer | Canvas buffer width in pixels |
| `height` | Integer | Canvas buffer height in pixels |
| `color_format` | Enum | Pixel format (e.g. `argb8888`, `rgb565`, `a8`) |

### Example
```xml
<!-- ✅ Correct: Offscreen drawing canvas -->
<lv_canvas name="custom_gauge_canvas"
           width="200" height="200"
           color_format="rgb565"
           align="center" />
```
