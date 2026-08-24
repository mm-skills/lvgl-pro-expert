# LVGL Pro XML Format Specification
**Version:** v9.5.0

This document serves as the official format specification for the LVGL Pro XML architecture. It details the project structure, global registry, styling system, layout mechanisms, data binding, and widget definitions used to build modern, declarative UIs in LVGL Pro.

## Table of Contents

- [1. File Inventory & Project Architecture](#1-file-inventory--project-architecture)
- [2. `project.xml` — Project Configuration](#2-projectxml--project-configuration)
- [3. `globals.xml` — Global Registry](#3-globalsxml--global-registry)
- [4. Screen Definitions (`screens/*.xml`)](#4-screen-definitions-screensxml)
- [5. Widget Catalog](#5-widget-catalog)
- [6. The Styling System](#6-the-styling-system)
- [7. Layout System](#7-layout-system)
- [8. Data Binding System](#8-data-binding-system)
- [9. Components (`components/<name>/<name>.xml`)](#9-components-componentsnamenamexml)
- [10. Widgets (`widgets/<name>/<name>.xml`)](#10-widgets-widgetsnamenamexml)
- [11. Event Callbacks](#11-event-callbacks)
- [12. Color Format](#12-color-format)
- [13. Value Formats](#13-value-formats)
- [14. Constants Reference System (`#const_name`)](#14-constants-reference-system-const_name)
- [15. Inline Part+State Style Selectors (Hyphenated Syntax)](#15-inline-partstate-style-selectors-hyphenated-syntax)
- [16. Conditional Style Binding (`<bind_style>`)](#16-conditional-style-binding-bind_style)
- [17. Screen Navigation & Transitions](#17-screen-navigation--transitions)
- [18. Animation System (`<animations>` / `<timeline>`)](#18-animation-system-animations--timeline)
- [19. Translation / Internationalization System](#19-translation--internationalization-system)
- [20. Component Inheritance](#20-component-inheritance)
- [21. Additional Widget Flags & Attributes](#21-additional-widget-flags--attributes)
- [22. Subject Event Types (Declarative Subject Mutation)](#22-subject-event-types-declarative-subject-mutation)
- [23. Animation Property Definitions](#23-animation-property-definitions)
- [24. Widget Sub-Elements (Hyphenated Child Tags)](#24-widget-sub-elements-hyphenated-child-tags)
- [25. Component Slot System](#25-component-slot-system)
- [26. Expression Syntax (`{...}`)](#26-expression-syntax-)
- [27. Automated Testing Framework (`<test>`)](#27-automated-testing-framework-test)
- [28. Conditional Asset Groups (`if_target`)](#28-conditional-asset-groups-if_target)

---

## 1. File Inventory & Project Architecture

LVGL Pro uses a **modular multi-file XML architecture**. A project is a **directory** containing:

| File/Directory | Format | Purpose | Required? |
|----------------|--------|---------|-----------|
| `project.xml` | XML | Project configuration: display targets, LVGL version, theme | ✅ |
| `globals.xml` | XML | Global registry: subjects, images, fonts, styles, constants, API definitions | ✅ |
| `translations.xml` | XML | Multi-language translation strings | Optional |
| `screens/<name>.xml` | XML | Screen definitions: widget tree, local styles, layout | ✅ (≥1) |
| `components/<name>/<name>.xml` | XML | Reusable UI components (pure XML, no custom C) | Optional |
| `widgets/<name>/<name>.xml` | XML | Custom widgets (XML + custom C code, with `_gen.c`/`_gen.h`) | Optional |
| `images/` | Directory | Image assets (PNG, JPG, SVG) referenced by `globals.xml` | Optional |
| `fonts/` | Directory | Font files (TTF, OTF, BIN) referenced by `globals.xml` | Optional |

### 1.1 Directory Structure Example

```text
my_project/
├── project.xml
├── globals.xml
├── screens/
│   ├── main.xml
│   ├── settings.xml
│   └── splash.xml
├── components/
│   ├── button/
│   │   └── button.xml
│   ├── toggle_switch/
│   │   └── toggle_switch.xml
│   └── top_bar/
│       └── top_bar.xml
├── widgets/
│   └── wd_battery/
│       └── wd_battery.xml
├── images/
│   ├── logo.png
│   └── icon_wifi.png
└── fonts/
    ├── Inter_28_Bold.ttf
    └── Montserrat-SemiBold.ttf
```

> [!IMPORTANT]
> Components and widgets each live in their own **named subdirectory** — the subdirectory name
> matches the component/widget name and becomes the XML tag used to instantiate it.

---

## 2. `project.xml` — Project Configuration

Defines the hardware display targets, LVGL version, and theme.

### Simple Example (Basic Template)
```xml
<project lvgl_version="9.5.0" theme="simple">
    <targets>
        <target name="target1">
            <display width="480" height="320" />
        </target>
    </targets>
</project>
```

### Full Example (with memory declarations)
```xml
<project name="tutorials" lvgl_version="9.5.0" theme="default">
    <targets>
        <target name="target1">
            <display width="480" height="320" />
            <memory name="int_ram" size="1MB" />
            <memory name="int_flash" size="2MB" bandwidth="100MB/s" />
        </target>
    </targets>
</project>
```

### Round Display Example
```xml
<project lvgl_version="9.5.0">
    <targets>
        <target name="target1">
            <display width="466" height="466" radius="233" />
        </target>
    </targets>
</project>
```

### `<project>` Attributes

| Attribute | Type | Description | Required? |
|-----------|------|-------------|-----------|
| `name` | String | Project name identifier | Optional |
| `lvgl_version` | String | Target LVGL version (e.g., `"9.5.0"`) | ✅ |
| `theme` | String | Default theme: `"simple"`, `"default"` | Optional |

### `<display>` Attributes

| Attribute | Type | Description | Required? |
|-----------|------|-------------|-----------|
| `width` | Integer (px) | Display width in pixels | ✅ |
| `height` | Integer (px) | Display height in pixels | ✅ |
| `radius` | Integer (px) | Corner radius for round displays (set to `width/2` for circular) | Optional |
| `color_depth` | Integer | Bit depth (e.g., `16`, `24`, `32`) | Optional |
| `dpi` | Integer | Display DPI for scaling calculations | Optional |
| `color_format` | String | Default pixel format (e.g., `"RGB565"`, `"ARGB8888"`) | Optional |

### `<memory>` Attributes (Hardware Target Memory Declaration)

| Attribute | Type | Description | Required? |
|-----------|------|-------------|-----------|
| `name` | String | Memory region name (e.g., `"int_ram"`, `"int_flash"`) | ✅ |
| `size` | String | Memory size (e.g., `"1MB"`, `"2MB"`, `"512KB"`) | ✅ |
| `bandwidth` | String | Memory bandwidth (e.g., `"100MB/s"`) | Optional |

> [!NOTE]
> Use `radius` to define circular/round displays. For a fully circular display, set `radius` to
> half the width. Omit or set to `0` for standard rectangular displays.
>
> The `memory` attribute on `<images>` and `<fonts>` blocks in `globals.xml` (e.g.,
> `<images memory="int_flash">`) references these declared memory regions.

---

## 3. `globals.xml` — Global Registry

The central registry for all shared assets, state variables, styles, and constants. Every font, image, and subject used anywhere in the project **must** be declared here.

### 3.1 Top-Level Structure

```xml
<globals>
    <api>
        <!-- Custom enum definitions -->
    </api>

    <consts>
        <!-- Global constants: <px>, <int>, <color>, <bool> -->
    </consts>

    <styles>
        <!-- Global reusable style definitions -->
    </styles>

    <subjects>
        <!-- Reactive state variables (data binding targets) -->
    </subjects>

    <images>
        <!-- Image asset declarations -->
    </images>

    <fonts>
        <!-- Font asset declarations -->
    </fonts>
</globals>
```

### 3.2 Subjects (Reactive State Variables)

Subjects are the reactive data binding system using a declarative observer pattern.

```xml
<subjects>
    <string name="subject_time" value="10:20" />
    <string name="subject_date" value="Sat 27" />
    <string name="subject_name" value="Project" />
    <int name="subject_stars" value="345" />
    <int name="subject_prs" value="35" />
    <int name="subject_issues" value="27" />
    <int name="subject_wifi" value="1" />
    <int name="battery_value" value="50" />
    <int name="charging" value="0" />
    <int name="battery_theme" value="0" help="subject to set battery theme. values: 0 (light), (1) dark" />
</subjects>
```

| Subject Type | Tag | Value Format | Description |
|--------------|-----|--------------|-------------|
| Integer | `<int>` | Numeric | Integer state (counters, booleans as 0/1, percentages) |
| String | `<string>` | Text | Text state (labels, formatted values) |
| Float | `<float>` | Decimal | Floating-point state |
| Boolean | `<bool>` | `"true"`/`"false"` | Boolean state (in `<consts>` block) |

| Attribute | Required? | Description |
|-----------|-----------|-------------|
| `name` | ✅ | Unique identifier, used in `bind_*` attributes throughout the project |
| `value` | ✅ | Initial/default value |
| `min_value` | Optional | Minimum allowed value (for integer subjects) |
| `max_value` | Optional | Maximum allowed value (for integer subjects) |
| `help` | Optional | Documentation string describing the subject's purpose |

### 3.3 Images

The `<images>` block supports three tag types: `<data>` (embed in C array), `<file>` (load from filesystem at runtime), and `<convert>` (build-time SVG→PNG conversion).

```xml
<images memory="int_flash">
    <!-- Embedded image data (converted to C array at build time) -->
    <data name="flower_data" src_path="images/orange-flower.png" color_format="argb8888" />

    <!-- Filesystem image (loaded at runtime from the device's filesystem) -->
    <file name="flower_file" src_path="images/orange-flower.png" />

    <!-- SVG→PNG conversion pipeline: convert at build time, then embed -->
    <convert
        src="images/icons/svg/wifi.svg"
        dest="images/icons/wifi.png"
        width="#icon_size"
        color_format="argb8888"
    />
    <data name="icon_wifi" src_path="images/icons/wifi.png" color_format="argb8888" />
</images>
```

#### `<data>` — Embedded Image (C Array)

| Attribute | Required? | Description |
|-----------|-----------|-------------|
| `name` | ✅ | Unique identifier, used in `src="..."` attributes on `<lv_image>` widgets |
| `src_path` | ✅ | Relative path to the image file from the project root |
| `color_format` | ✅ | Pixel format for encoding (see Color Formats table below) |

#### `<file>` — Runtime Filesystem Image

| Attribute | Required? | Description |
|-----------|-----------|-------------|
| `name` | ✅ | Unique identifier |
| `src_path` | ✅ | Relative path to the image file |

> [!NOTE]
> `<file>` images are loaded from the device filesystem at runtime. They require a filesystem
> driver to be configured. Use `<data>` for MCUs without a filesystem.

#### `<convert>` — Build-Time Image Conversion

| Attribute | Required? | Description |
|-----------|-----------|-------------|
| `src` | ✅ | Source image path (e.g., SVG) |
| `dest` | ✅ | Destination image path (e.g., PNG) |
| `width` | Optional | Target width (can use `#const_name` references) |
| `color_format` | Optional | Target color format |

> [!TIP]
> The `<convert>` + `<data>` pattern is the standard way to use SVG icons:
> 1. Convert SVG → PNG at build time with `<convert>`
> 2. Embed the resulting PNG with `<data>`

#### `<images>` Block Attribute

| Attribute | Description |
|-----------|-------------|
| `memory` | Target memory region name (declared in `project.xml` `<memory>`) e.g., `"int_flash"` |

#### Image Color Formats

| Format | Description | Memory | Use Case |
|--------|-------------|--------|----------|
| `rgb565` | 16-bit RGB (5-6-5), no alpha | 2 bytes/px | Backgrounds, photos (no transparency) |
| `rgb565a8` | 16-bit RGB + separate 8-bit alpha | 3 bytes/px | Icons, UI elements with transparency |
| `rgb888` | 24-bit true color RGB | 3 bytes/px | High-quality images, no transparency |
| `argb8888` | 32-bit RGBA with full alpha | 4 bytes/px | Highest quality with transparency |
| `xrgb8888` | 32-bit RGB, alpha channel ignored | 4 bytes/px | 32-bit alignment without transparency |
| `a8` | 8-bit alpha-only mask | 1 byte/px | Monochrome icons (tinted via `recolor`) |
| `a4` | 4-bit alpha mask | 0.5 bytes/px | Low-res monochrome icons |
| `a2` | 2-bit alpha mask | 0.25 bytes/px | Simple masks |
| `a1` | 1-bit alpha mask | 0.125 bytes/px | Binary masks |
| `l8` | 8-bit grayscale/luminance | 1 byte/px | Grayscale images |
| `i8` | 8-bit indexed color with palette | 1 byte/px | Palette-based images |
| `i4` | 4-bit indexed color | 0.5 bytes/px | Low-color palette images |
| `i2` | 2-bit indexed color | 0.25 bytes/px | Minimal palette images |
| `i1` | 1-bit indexed color | 0.125 bytes/px | Binary color images |
| `native` | Matches display driver depth | Variable | Auto-match to target hardware |

### 3.4 Fonts

Three font backends are supported. The `<fonts>` block can target a memory region:

```xml
<fonts memory="int_flash">
    <!-- Binary bitmap: as_file="false" = embed as C array (fastest) -->
    <bin
        name="montserrat_14_c_array"
        as_file="false"
        bpp="2"
        src_path="fonts/Montserrat_Medium.ttf"
        size="14"
        range="0x20-0x7f"
        symbols="°äü"
    />

    <!-- Binary bitmap: as_file="true" = create .bin file loadable at runtime -->
    <bin
        name="montserrat_16_bin_file"
        as_file="true"
        bpp="2"
        src_path="fonts/Montserrat_Medium.ttf"
        size="16"
        range="0x20-0x7f"
        symbols="°"
    />

    <!-- Tiny TTF: as_file="false" = convert TTF raw data to C array, render at runtime -->
    <tiny_ttf name="montserrat_18_tiny_ttf_data" as_file="false" size="18" src_path="fonts/Montserrat_Medium.ttf" />

    <!-- Tiny TTF: as_file="true" = load TTF from filesystem at runtime -->
    <tiny_ttf name="montserrat_20_tiny_ttf_file" as_file="true" size="20" src_path="fonts/Montserrat_Medium.ttf" />

    <!-- FreeType: full vector rendering engine -->
    <freetype
        name="font_noto_large"
        src_path="fonts/NotoSans.ttf"
        size="36"
    />
</fonts>
```

#### Font Type Comparison

| Type | Tag | Rendering | MCU Footprint | Use Case |
|------|-----|-----------|---------------|----------|
| Binary bitmap | `<bin>` | Pre-compiled at build time | Lowest CPU/RAM | Production on resource-constrained MCUs |
| Tiny TTF | `<tiny_ttf>` | STB TrueType rasterizer | Medium | Runtime scaling without FreeType overhead |
| FreeType | `<freetype>` | Full FreeType 2 engine | Highest (needs PSRAM) | Complex scripts, kerning, high-quality rendering |

#### `<bin>` Font Attributes

| Attribute | Required? | Description |
|-----------|-----------|-------------|
| `name` | ✅ | Unique identifier, used in `text_font="..."` or `style_text_font="..."` |
| `src_path` | ✅ | Relative path to the source TTF/OTF file |
| `size` | ✅ | Font size in pixels |
| `bpp` | ✅ | Bits per pixel for anti-aliasing (`1`, `2`, `4`, `8`) |
| `range` | ✅ | Unicode range to include (e.g., `"0x20-0x7F"` for ASCII) |
| `as_file` | Optional | `"true"` = load from filesystem at runtime; `"false"` = embed in binary |
| `symbols` | Optional | Additional individual characters to include beyond the range |

### 3.5 Global Styles

Styles defined in `globals.xml` are available across all screens and components:

```xml
<styles>
    <style name="card_bg" bg_color="0x2A2A2A" radius="8" pad_all="12" />
    <style name="text_white" text_color="0xFFFFFF" />
</styles>
```

### 3.6 Constants

```xml
<consts>
    <int name="space_sm" value="8" />
    <int name="space_md" value="16" />
    <int name="space_lg" value="24" />
    <color name="primary" value="0x24EAA2" />
    <bool name="low_power" value="false" />
</consts>
```

---

## 4. Screen Definitions (`screens/*.xml`)

Each screen is a separate XML file defining the widget tree for one view.

### 4.1 Screen Structure

```xml
<screen>
    <styles>
        <!-- Local styles scoped to this screen -->
        <style name="style_main" bg_color="0x0F0F0F" />
    </styles>

    <!-- The root widget of the screen -->
    <view extends="lv_obj" scrollable="false">
        <style name="style_main" />

        <!-- Child widgets go here -->
        <lv_label text="Hello World" align="center" />
    </view>
</screen>
```

### 4.2 The `<view>` Root Element

Every screen must have exactly one `<view>` element as its root widget container.

| Attribute | Description |
|-----------|-------------|
| `extends` | Base LVGL widget type (default: `lv_obj`). Can be omitted. |
| `scrollable` | `"true"` / `"false"` — enables/disables scrolling on the root |
| `scroll_snap_x` | Snap mode: `"center"`, `"start"`, `"end"`, `"none"` |
| `scroll_one` | `"true"` — scroll only one snap point at a time |

### 4.3 Local Styles Block

The `<styles>` block inside a `<screen>` defines styles scoped to that screen only. These take precedence over global styles of the same name.

---

## 5. Widget Catalog

All widgets use XML tags that map 1:1 to LVGL C widget types. Properties map directly to the
corresponding `lv_<widget>_set_<property>()` C API functions.

### 5.1 Universal Object Properties

Every widget supports these attributes (corresponding to `lv_obj_*` functions):

#### Positioning & Size

| Attribute | Type | Description |
|-----------|------|-------------|
| `x` | Integer/Percentage | Horizontal position offset |
| `y` | Integer/Percentage | Vertical position offset |
| `width` | Integer/Percentage/`"content"` | Widget width |
| `height` | Integer/Percentage/`"content"` | Widget height |
| `min_width`, `max_width` | Integer | Min/max width constraints |
| `min_height`, `max_height` | Integer | Min/max height constraints |
| `align` | Enum | Alignment within parent (see Alignment Values) |

#### Alignment Values

| Value | Description |
|-------|-------------|
| `center` | Center of parent |
| `top_left` | Top-left corner |
| `top_mid` | Top center |
| `top_right` | Top-right corner |
| `bottom_left` | Bottom-left corner |
| `bottom_mid` | Bottom center |
| `bottom_right` | Bottom-right corner |
| `left_mid` | Left center |
| `right_mid` | Right center |

#### Flags & Behavior

| Attribute | Type | Description |
|-----------|------|-------------|
| `name` | String | Widget identifier (for code references and event targeting) |
| `clickable` | Boolean | Whether the widget responds to clicks |
| `scrollable` | Boolean | Whether the widget is scrollable |
| `hidden` | Boolean | Whether the widget is hidden |
| `checkable` | Boolean | Whether the widget is checkable |
| `checked` | Boolean | Whether the widget is in checked state |
| `disabled` | Boolean | Whether the widget is disabled |

### 5.2 Complete Widget Tag Reference

#### `<lv_obj>` — Base Object / Container

The fundamental container widget. Used for panels, groups, and layout containers.

| Attribute | Type | Description |
|-----------|------|-------------|
| `scrollable` | Boolean | Enable scrolling |
| `scrollbar_mode` | Enum | `"auto"`, `"on"`, `"off"`, `"active"` |

**Style parts:** `main`, `scrollbar`

---

#### `<lv_label>` — Text Label

| Attribute | Type | Description |
|-----------|------|-------------|
| `text` | String | Text content |
| `long_mode` | Enum | `"wrap"`, `"dot"`, `"scroll"`, `"scroll_circular"`, `"clip"` |

**Style parts:** `main`

---

#### `<lv_button>` — Button

| Attribute | Type | Description |
|-----------|------|-------------|
| `checkable` | Boolean | Toggleable button |
| `checked` | Boolean | Initial checked state |

**Style parts:** `main`

---

#### `<lv_image>` — Image

| Attribute | Type | Description |
|-----------|------|-------------|
| `src` | String | Image name (registered in `globals.xml`) |
| `pivot_x`, `pivot_y` | Integer | Rotation pivot point |
| `rotation` | Integer | Rotation in 0.1° units (e.g., `900` = 90°) |
| `scale` | Integer | Scale factor (256 = 100%) |
| `scale_x`, `scale_y` | Integer | Axis-specific scale |

**Style parts:** `main`

---

#### `<lv_arc>` — Arc / Circular Gauge

| Attribute | Type | Description |
|-----------|------|-------------|
| `value` | Integer | Current value |
| `min_value` / `max_value` | Integer | Value range (alternative: `min`, `max`) |
| `bg_start_angle` | Integer | Background arc start angle |
| `bg_end_angle` | Integer | Background arc end angle |
| `rotation` | Integer | Rotation offset |
| `mode` | Enum | `"normal"`, `"reverse"`, `"symmetrical"` |
| `clickable` | Boolean | Whether the user can drag the knob |

**Style parts:** `main`, `indicator`, `knob`

---

#### `<lv_slider>` — Slider

| Attribute | Type | Description |
|-----------|------|-------------|
| `value` | Integer | Current value |
| `min_value` / `max_value` | Integer | Value range |
| `left_value` | Integer | Left value (range mode) |
| `mode` | Enum | `"normal"`, `"symmetrical"`, `"range"` |

**Style parts:** `main`, `indicator`, `knob`

---

#### `<lv_bar>` — Progress Bar

| Attribute | Type | Description |
|-----------|------|-------------|
| `value` | Integer | Current value |
| `min_value` / `max_value` | Integer | Value range |
| `start_value` | Integer | Start value (range mode) |
| `mode` | Enum | `"normal"`, `"symmetrical"`, `"range"` |

**Style parts:** `main`, `indicator`

---

#### `<lv_switch>` — Toggle Switch

| Attribute | Type | Description |
|-----------|------|-------------|
| `checked` | Boolean | Initial state |

**Style parts:** `main`, `indicator`, `knob`

---

#### `<lv_checkbox>` — Checkbox

| Attribute | Type | Description |
|-----------|------|-------------|
| `text` | String | Label text |
| `checked` | Boolean | Initial state |

**Style parts:** `main`, `indicator`

---

#### `<lv_dropdown>` — Dropdown List

| Attribute | Type | Description |
|-----------|------|-------------|
| `options` | String | Options separated by `&#10;` in XML (e.g., `"Apple&#10;Banana&#10;Orange"`) |
| `selected` | Integer | Selected index |
| `dir` | Enum | Drop direction: `"bottom"` (default), `"top"`, `"left"`, `"right"` |
| `text` | String | Fixed button label (overrides showing selected option) |

**Style parts:** `main`, `indicator`, list: `main`, `selected`, `scrollbar`

> [!NOTE]
> Options use XML entity `&#10;` for newlines, not `\n`. The `text` attribute pins the
> button label regardless of selection — useful for icon-style or "Menu" dropdowns.

---

#### `<lv_roller>` — Roller

| Attribute | Type | Description |
|-----------|------|-------------|
| `options` | String | Options separated by `&#10;` (e.g., `"Mon&#10;Tue&#10;Wed"`) |
| `selected` | Integer | Selected index |
| `options-mode` | Enum | `"normal"` (stops at ends) or `"infinite"` (wraps around) |
| `visible_row_count` | Integer | Number of visible rows |

**Style parts:** `main`, `selected`

---

#### `<lv_textarea>` — Text Area

| Attribute | Type | Description |
|-----------|------|-------------|
| `text` | String | Text content |
| `placeholder` | String | Placeholder text |
| `max_length` | Integer | Maximum character count |
| `one_line` | Boolean | Single line mode |
| `password_mode` | Boolean | Password masking |
| `accepted_chars` | String | Character whitelist |

**Style parts:** `main`, `cursor`, `selected`

---

#### `<lv_keyboard>` — On-Screen Keyboard

| Attribute | Type | Description |
|-----------|------|-------------|
| `mode` | Enum | `"text_lower"`, `"text_upper"`, `"special"`, `"number"` |
| `textarea` | String | Name/ID of linked textarea widget |

**Style parts:** `main`, `items`

---

#### `<lv_spinner>` — Loading Spinner

No widget-specific attributes.

**Style parts:** `main`, `indicator`

---

#### `<lv_chart>` — Chart

| Attribute | Type | Description |
|-----------|------|-------------|
| `type` | Enum | `"line"`, `"bar"`, `"scatter"` |
| `point_count` | Integer | Number of data points |
| `min_value` / `max_value` | Integer | Y-axis range |

**Style parts:** `main`, `indicator`, `items`, `scrollbar`, `ticks`

---

#### `<lv_tabview>` — Tab View

| Attribute | Type | Description |
|-----------|------|-------------|
| `tab_bar_position` | Enum | `"top"`, `"bottom"`, `"left"`, `"right"`, `"none"` |
| `tab_bar_size` | Integer | Tab bar height/width in px |

**Child element:** `<lv_tabview-tab text="Tab Name"> ... </lv_tabview-tab>`

```xml
<lv_tabview name="tabview" width="100%" height="100%">
    <lv_tabview-tab text="Tab 1">
        <lv_label align="center" text="First tab" />
    </lv_tabview-tab>
    <lv_tabview-tab text="Tab 2">
        <lv_label align="center" text="Second tab" />
    </lv_tabview-tab>
</lv_tabview>
```

**Style parts:** `main`, buttons: `main`, `items`

---

#### `<lv_calendar>` — Calendar

| Attribute | Type | Description |
|-----------|------|-------------|
| `today_year`, `today_month`, `today_day` | Integer | Today's date |
| `showed_year`, `showed_month` | Integer | Currently displayed month |

**Style parts:** `main`, `items`

---

#### `<lv_scale>` — Scale / Gauge

| Attribute | Type | Description |
|-----------|------|-------------|
| `mode` | Enum | `"horizontal_top"`, `"horizontal_bottom"`, `"vertical_left"`, `"vertical_right"`, `"round_inner"`, `"round_outer"` |
| `total_tick_count` | Integer | Total ticks |
| `major_tick_every` | Integer | Major tick interval |
| `range_min`, `range_max` | Integer | Scale value range |

**Style parts:** `main`, `indicator`, `items`

---

#### `<lv_spinbox>` — Spin Box

| Attribute | Type | Description |
|-----------|------|-------------|
| `value` | Integer | Current value |
| `range_min`, `range_max` | Integer | Value range |
| `digit_count` | Integer | Total digits displayed |
| `dec_point_pos` | Integer | Decimal point position |
| `step` | Integer | Increment step |

**Style parts:** `main`, `cursor`

---

#### `<lv_led>` — LED Indicator

| Attribute | Type | Description |
|-----------|------|-------------|
| `color` | Color | LED color |
| `brightness` | Integer (0–255) | LED brightness |

**Style parts:** `main`

---

#### `<lv_line>` — Line

| Attribute | Type | Description |
|-----------|------|-------------|
| `points` | String | Point coordinates (e.g., `"0,0 50,50 100,20"`) |
| `y_invert` | Boolean | Invert Y axis |

**Style parts:** `main`

---

#### `<lv_imgbutton>` — Image Button

| Attribute | Type | Description |
|-----------|------|-------------|
| `src_released` | String | Image for released state |
| `src_pressed` | String | Image for pressed state |
| `src_disabled` | String | Image for disabled state |
| `src_checked_released` | String | Image for checked+released |
| `src_checked_pressed` | String | Image for checked+pressed |
| `src_checked_disabled` | String | Image for checked+disabled |

**Style parts:** `main`

---

#### Additional Widget Tags

| XML Tag | LVGL Widget | Description |
|---------|-------------|-------------|
| `<lv_tileview>` | `lv_tileview` | Swipeable tile container (child: `<tile column="0" row="0">`) |
| `<lv_msgbox>` | `lv_msgbox` | Modal message box (`title`, `text`, `close_button`) |
| `<lv_spangroup>` | `lv_spangroup` | Rich text with per-span styling (child: `<span>`) |
| `<lv_animimg>` | `lv_animimg` | Animated image sequence (`src_array`, `duration`, `repeat_count`) |
| `<lv_canvas>` | `lv_canvas` | Pixel drawing surface (`width`, `height`, `color_format`) |
| `<lv_menu>` | `lv_menu` | Multi-page menu system |
| `<lv_list>` | `lv_list` | Scrollable list container |
| `<lv_colorwheel>` | `lv_colorwheel` | HSV color picker (`mode`: `"hue"`, `"saturation"`, `"value"`) |
| `<lv_table>` | `lv_table` | Data table (`row_count`, `column_count`, child: `<lv_table-cell>`) |

#### `<lv_table>` Child Element Syntax

```xml
<lv_table name="table" row_count="3" column_count="2" align="center">
    <lv_table-cell row="0" column="0" value="City" />
    <lv_table-cell row="0" column="1" value="Population" />
    <lv_table-cell row="1" column="0" value="Berlin" />
    <lv_table-cell row="1" column="1" value="3.7M" />
</lv_table>
```

---

## 6. The Styling System

LVGL Pro XML supports three methods of applying styles, analogous to CSS:

### 6.1 Class-Based Styles (Reusable `<style>` Definitions)

Defined in the `<styles>` block of either `globals.xml` (global scope) or inside a
`<screen>` / `<component>` / `<widget>` (local scope).

```xml
<style
    name="style_btn"
    width="100"
    height="40"
    radius="20"
    bg_color="0x171717"
    border_width="0"
    text_font="montserrat_semibold_19"
    text_color="0xF5F5F5"
/>
```

**Applying to a widget:**
```xml
<lv_obj>
    <style name="style_btn" />
</lv_obj>
```

### 6.2 Inline Styles (The `style_` Prefix)

Apply style properties directly on a widget tag by prefixing with `style_`:

```xml
<lv_label
    text="Warning"
    style_text_color="0xFF0000"
    style_text_font="montserrat_semibold_23"
    style_pad_top="5"
    style_bg_color="0x333333"
    style_bg_opa="40%"
    style_opa="70%"
/>
```

### 6.3 Part Selectors

LVGL widgets have visual sub-parts (e.g., a slider has `main`, `indicator`, and `knob`).
Target them using the `selector` attribute:

```xml
<lv_arc mode="reverse" value="40">
    <style name="style_arc_bg" />                      <!-- applies to main -->
    <style name="style_indicator" selector="indicator" />
    <style name="style_knob" selector="knob" />
</lv_arc>
```

### 6.4 State Selectors

Combine part selectors with state qualifiers using the `|` separator:

```xml
<lv_switch width="115" height="60">
    <style name="style_off" selector="main" />
    <style name="style_on" selector="indicator|checked" />
    <style name="style_knob_base" selector="knob" />
</lv_switch>
```

```xml
<!-- Scrollbar state selectors -->
<view scroll_snap_x="center">
    <style name="style_main" />
    <style name="style_bars" selector="scrollbar" />
    <style name="style_bars" selector="scrollbar|scrolled" />
</view>
```

#### Available States

| State | Description |
|-------|-------------|
| `default` | Normal state (can usually be omitted) |
| `pressed` | While being pressed |
| `checked` | Toggled/checked state |
| `focused` | Has input focus |
| `disabled` | Disabled state |
| `user_1` .. `user_4` | Custom user-defined states |
| `scrolled` | Widget has been scrolled |

#### Widget Style Part Mapping

| Widget | Parts |
|--------|-------|
| `lv_obj` | `main`, `scrollbar` |
| `lv_button` | `main` |
| `lv_label` | `main` |
| `lv_image` | `main` |
| `lv_arc` | `main`, `indicator`, `knob` |
| `lv_slider` | `main`, `indicator`, `knob` |
| `lv_bar` | `main`, `indicator` |
| `lv_switch` | `main`, `indicator`, `knob` |
| `lv_checkbox` | `main`, `indicator` |
| `lv_dropdown` | `main`, `indicator`, list: `main`, `selected`, `scrollbar` |
| `lv_roller` | `main`, `selected` |
| `lv_textarea` | `main`, `cursor`, `selected` |
| `lv_keyboard` | `main`, `items` |
| `lv_spinner` | `main`, `indicator` |
| `lv_chart` | `main`, `indicator`, `items`, `scrollbar`, `ticks` |
| `lv_calendar` | `main`, `items` |
| `lv_tabview` | `main`, buttons: `main`, `items` |

### 6.5 Complete Style Property Reference

#### Background

| Attribute | Type | Description |
|-----------|------|-------------|
| `bg_color` | Color | Background color (`0xRRGGBB`, `0xRGB`, or `#RRGGBB`) |
| `bg_opa` | Integer/Percentage | Opacity: 0–255 or `"40%"`, `"100%"` |
| `bg_grad_color` | Color | Gradient end color |
| `bg_grad_dir` | Enum | `"none"`, `"ver"`, `"hor"` |
| `bg_main_stop`, `bg_grad_stop` | Integer | Gradient stop positions (0–255) |
| `bg_image_src` | String | Background image name |
| `bg_image_opa` | Integer | Background image opacity (0–255) |
| `bg_image_recolor` | Color | Background image tint color |
| `bg_image_tiled` | Boolean | Tile background image |

#### Border

| Attribute | Type | Description |
|-----------|------|-------------|
| `border_color` | Color | Border color |
| `border_width` | Integer | Border width in px |
| `border_side` | Enum | `"none"`, `"bottom"`, `"top"`, `"left"`, `"right"`, `"full"` |
| `border_opa` | Integer | Border opacity (0–255) |

#### Outline

| Attribute | Type | Description |
|-----------|------|-------------|
| `outline_color` | Color | Outline color |
| `outline_width` | Integer | Outline width in px |
| `outline_pad` | Integer | Gap between outline and border |
| `outline_opa` | Integer | Outline opacity (0–255) |

#### Shadow

| Attribute | Type | Description |
|-----------|------|-------------|
| `shadow_color` | Color | Shadow color |
| `shadow_width` | Integer | Shadow blur radius |
| `shadow_offset_x`, `shadow_offset_y` | Integer | Shadow offset |
| `shadow_spread` | Integer | Shadow spread |
| `shadow_opa` | Integer | Shadow opacity (0–255) |

#### Padding

| Attribute | Type | Description |
|-----------|------|-------------|
| `pad_all` | Integer | Padding on all sides |
| `pad_top`, `pad_bottom`, `pad_left`, `pad_right` | Integer | Individual padding |
| `pad_row` | Integer | Vertical gap between flex/grid children |
| `pad_column` | Integer | Horizontal gap between flex/grid children |
| `pad_gap` | Integer | Shorthand for `pad_row` + `pad_column` |

#### Text

| Attribute | Type | Description |
|-----------|------|-------------|
| `text_color` | Color | Text color |
| `text_opa` | Integer | Text opacity |
| `text_font` | String | Font name (registered in `globals.xml`) |
| `text_letter_space` | Integer | Letter spacing in px |
| `text_line_space` | Integer | Line spacing in px |
| `text_align` | Enum | `"auto"`, `"left"`, `"center"`, `"right"` |

#### Arc-Specific

| Attribute | Type | Description |
|-----------|------|-------------|
| `arc_color` | Color | Arc track color |
| `arc_width` | Integer | Arc track width in px |
| `arc_rounded` | Boolean | Rounded arc end caps |
| `arc_opa` | Integer | Arc opacity |
| `arc_image_src` | String | Arc track image |

#### Image-Specific

| Attribute | Type | Description |
|-----------|------|-------------|
| `image_opa` | Integer | Image opacity |
| `image_recolor` | Color | Image tint color |
| `image_recolor_opa` | Integer | Recolor intensity (0–255) |

#### Line-Specific

| Attribute | Type | Description |
|-----------|------|-------------|
| `line_color` | Color | Line color |
| `line_width` | Integer | Line width |
| `line_dash_width` | Integer | Dash segment length |
| `line_dash_gap` | Integer | Gap between dashes |
| `line_rounded` | Boolean | Rounded line ends |

#### Transform

| Attribute | Type | Description |
|-----------|------|-------------|
| `transform_width`, `transform_height` | Integer | Size transform |
| `transform_rotation` | Integer | Rotation in 0.1° units (e.g., `900` = 90°, `-900` = -90°) |
| `transform_scale` | Integer | Scale (256 = 100%) |
| `transform_pivot_x`, `transform_pivot_y` | Integer | Transform pivot point |
| `translate_x`, `translate_y` | Integer | Translation offset |
| `opa` | Integer/Percentage | Overall object opacity |

#### Blending

| Attribute | Type | Description |
|-----------|------|-------------|
| `blend_mode` | Enum | `"normal"`, `"additive"`, `"subtractive"`, `"multiply"` |

---

## 7. Layout System

### 7.1 Flexbox Layout

Enable by setting `layout="flex"` on a style or container:

```xml
<style
    name="flex_row"
    layout="flex"
    flex_flow="row"
    flex_main_place="center"
    flex_cross_place="center"
    flex_track_place="center"
    pad_column="12"
/>
```

#### Flex Container Properties

| Attribute | Type | Description |
|-----------|------|-------------|
| `layout` | `"flex"` | Enables flex layout |
| `flex_flow` | Enum | Direction and wrapping (see values below) |
| `flex_main_place` | Enum | Main-axis alignment |
| `flex_cross_place` | Enum | Cross-axis alignment |
| `flex_track_place` | Enum | Multi-line track alignment |

#### `flex_flow` Values

| Value | Description |
|-------|-------------|
| `row` | Horizontal left-to-right |
| `column` | Vertical top-to-bottom |
| `row_wrap` | Horizontal with wrapping |
| `column_wrap` | Vertical with wrapping |
| `row_reverse` | Horizontal right-to-left |
| `column_reverse` | Vertical bottom-to-top |

#### Placement Values (for `flex_main_place`, `flex_cross_place`, `flex_track_place`)

| Value | Description |
|-------|-------------|
| `start` | Pack items at start |
| `end` | Pack items at end |
| `center` | Center items |
| `space_evenly` | Equal space around all items |
| `space_around` | Equal space around each item |
| `space_between` | Equal space between items, none at edges |

#### Flex Child Properties

| Attribute | Type | Description |
|-----------|------|-------------|
| `flex_grow` | Integer | Flex grow factor (e.g., `1`, `2`) |

### 7.2 Grid Layout

Enable by setting `layout="grid"` on a style or container:

```xml
<style
    name="grid_2x2"
    layout="grid"
    grid_column_dsc_array="120 fr(1) fr(2)"
    grid_row_dsc_array="80 content fr(1)"
    grid_column_align="stretch"
    grid_row_align="stretch"
    pad_gap="16"
/>
```

#### Grid Container Properties

| Attribute | Description |
|-----------|-------------|
| `grid_column_dsc_array` | Space-separated column track sizes (px, `content`, `fr(n)`) |
| `grid_row_dsc_array` | Space-separated row track sizes |
| `grid_column_align` | Default column alignment |
| `grid_row_align` | Default row alignment |

#### Grid Child Properties

| Attribute | Description |
|-----------|-------------|
| `grid_cell_column_pos` | Column index (0-based) |
| `grid_cell_column_span` | Number of columns to span |
| `grid_cell_row_pos` | Row index (0-based) |
| `grid_cell_row_span` | Number of rows to span |
| `grid_cell_x_align` | Horizontal alignment: `"start"`, `"center"`, `"end"`, `"stretch"` |
| `grid_cell_y_align` | Vertical alignment: `"start"`, `"center"`, `"end"`, `"stretch"` |

---

## 8. Data Binding System

The data binding system uses a declarative observer pattern. Subjects (defined in `globals.xml`) are automatically
observed by widgets.

### 8.1 Direct Property Binding (`bind_*` Attributes)

Bind a widget property directly to a subject. The widget updates automatically when
the subject value changes from C code.

```xml
<!-- Text binding — label updates when subject changes -->
<lv_label text="10:20" bind_text="subject_time" />

<!-- Value binding — arc/slider tracks subject value -->
<lv_arc value="40" bind_value="subject_issues" />

<!-- Checked state binding -->
<lv_checkbox text="Low power mode" bind_checked="low_power_mode" />

<!-- Formatted text binding — subject value inserted into printf-style format -->
<lv_label bind_text="subject_index" bind_text-fmt="Selected option: %d" />
```

> [!IMPORTANT]
> The `text` / `value` attribute provides the **initial/fallback** display value.
> The `bind_*` attribute causes the widget to **reactively update** when the subject
> changes at runtime via C code.
>
> The `bind_text-fmt` attribute provides a `printf`-style format string. The subject
> value is inserted at the `%d` / `%s` placeholder.

### 8.1b Subject Set Event (`<subject_set_int_event>`)

Declaratively set a subject value on a widget event (e.g., on button click):

```xml
<lv_button name="button">
    <lv_label text="Jump to Wed" />
    <!-- On click, set subject_index to 2 -->
    <subject_set_int_event subject="subject_index" value="2" />
</lv_button>
```

| Attribute | Description |
|-----------|-------------|
| `subject` | Name of the subject to set |
| `value` | Integer value to write into the subject |

### 8.2 Conditional Flag Binding (`<bind_flag_if_eq>`)

Show, hide, or modify widget flags based on subject values:

```xml
<!-- Hide the wifi icon when subject_wifi equals 0 -->
<lv_image src="wifi_icon">
    <bind_flag_if_eq subject="subject_wifi" ref_value="0" flag="hidden" />
</lv_image>

<!-- Hide charging icon when charging equals 0 -->
<lv_image src="img_charging" align="left_mid" style_pad_left="45">
    <bind_flag_if_eq subject="charging" ref_value="0" flag="hidden" />
</lv_image>
```

| Attribute | Description |
|-----------|-------------|
| `subject` | Name of the subject to observe |
| `ref_value` | Value to compare against |
| `flag` | LVGL flag to set when condition is true (e.g., `"hidden"`, `"clickable"`) |

### 8.3 Conditional State Binding (`<bind_state_if_eq>`, `<bind_state_if_le>`)

Activate widget states based on subject values:

```xml
<!-- Activate user_1 state when battery_value <= 20 (low battery) -->
<lv_slider bind_value="battery_value" min_value="0" max_value="100">
    <bind_state_if_le ref_value="20" subject="battery_value" state="user_1" />
    <style name="indicator_red" selector="indicator|user_1" />
</lv_slider>

<!-- Activate user_1 state when subject equals 0 (disabled look) -->
<view extends="lv_button" style_bg_color="$enabled_color">
    <bind_state_if_eq ref_value="0" subject="$subject" state="user_1" />
    <style name="button_disabled" selector="main|user_1" />
</view>
```

| Tag | Condition |
|-----|-----------|
| `<bind_state_if_eq>` | State activates when subject **equals** `ref_value` |
| `<bind_state_if_le>` | State activates when subject **is less than or equal to** `ref_value` |

| Attribute | Description |
|-----------|-------------|
| `subject` | Name of the subject to observe |
| `ref_value` | Value to compare against |
| `state` | LVGL state to activate: `"checked"`, `"disabled"`, `"pressed"`, `"focused"`, `"user_1"` .. `"user_4"` |

---

## 9. Components (`components/<name>/<name>.xml`)

Components are **reusable UI elements** defined in pure XML. They are instantiated
as custom XML tags matching their directory name.

### 9.1 Component Structure

```xml
<component>
    <!-- Optional: Editor preview configuration -->
    <previews>
        <preview width="150" height="100" style_bg_color="0x505050" />
    </previews>

    <!-- Optional: Component parameter interface (props) -->
    <api>
        <prop name="text" type="string" />
        <prop name="preview" type="image" />
        <prop name="subject" type="subject" />
        <prop name="enabled_color" type="color" />
        <prop name="screen" type="obj" default="null" />
    </api>

    <!-- Optional: Local constants -->
    <consts>
        <bool name="low_power" value="false" />
    </consts>

    <!-- Optional: Component-scoped styles -->
    <styles>
        <style name="style_main" shadow_width="0" radius="51" />
    </styles>

    <!-- Required: Component root view -->
    <view extends="lv_button" width="300" height="90" style_bg_color="$enabled_color">
        <style name="style_main" />
        <lv_label text="$text" style_text_font="inter_28" align="center" />
    </view>
</component>
```

### 9.2 Component API Props

| Attribute | Description |
|-----------|-------------|
| `name` | Property name, becomes the XML attribute on instantiation |
| `type` | Data type: `"string"`, `"int"`, `"bool"`, `"color"`, `"image"`, `"obj"`, `"subject"` |
| `default` | Default value when not specified by the caller |
| `help` | Documentation string |

### 9.3 Template Variables (`$prop_name`)

Props are referenced inside the component using the `$` prefix:

```xml
<!-- Defined in <api>: <prop name="text" type="string" /> -->
<lv_label text="$text" />

<!-- Defined in <api>: <prop name="enabled_color" type="color" /> -->
<view style_bg_color="$enabled_color" />

<!-- Subject-type prop used in binding -->
<bind_state_if_eq ref_value="0" subject="$subject" state="user_1" />
```

### 9.4 Instantiating Components

Components are used as custom XML tags. The tag name matches the component's directory name:

```xml
<!-- In a screen file -->
<view>
    <!-- Simple component instance -->
    <top_bar />

    <!-- Component with props -->
    <button name="btn_charging" subject="charging" text="CHARGING" enabled_color="0x37c557">
        <event_cb trigger="clicked" callback="btn_charging_toggle_cb" />
    </button>

    <!-- Component with data binding -->
    <charge_slider bind_value="battery_value" align="center" x="0" y="-95" />
</view>
```

---

## 10. Widgets (`widgets/<name>/<name>.xml`)

Widgets are similar to components but use the `<widget>` root tag instead of `<component>`.
They are intended for elements that require **custom C code** alongside the XML definition
(e.g., complex rendering logic, hardware interaction).

### 10.1 Widget Structure

```xml
<widget>
    <previews>
        <preview width="100" height="100" style_bg_color="0x2f2f2f" />
    </previews>

    <styles>
        <style name="container" border_width="0" bg_opa="0" pad_all="0" />
    </styles>

    <api>
        <prop name="value" type="int" default="50" help="The value of the battery" />
        <prop name="low_power" type="bool" default="0" help="The low power state" />
        <prop name="charging" type="bool" default="0" help="The charging state" />
        <prop name="bind_value" type="subject" />
        <prop name="bind_low_power" type="subject" />
        <prop name="bind_charging" type="subject" />
    </api>

    <view extends="lv_obj" name="battery" width="79" height="36" scrollable="false">
        <style name="container" />
        <!-- Widget tree using $prop and bind_ attributes -->
    </view>
</widget>
```

> [!NOTE]
> The key difference between `<component>` and `<widget>`:
> - **Components** are pure XML — no custom C code needed.
> - **Widgets** pair XML with custom C code for behaviour the XML engine alone cannot express
>   (e.g., custom drawing, hardware drivers, complex state machines).

---

## 11. Event Callbacks

Events connect UI interactions to C callback functions:

```xml
<!-- Inline event callback on a widget -->
<lv_checkbox text="Low power mode" bind_checked="low_power_mode" align="center">
    <event_cb trigger="clicked" callback="check_low_power_click_cb" />
</lv_checkbox>

<!-- Event callback on a component instance -->
<button name="btn_charging_toggle" subject="charging" text="CHARGING" enabled_color="0x37c557">
    <event_cb trigger="clicked" callback="btn_charging_toggle_cb" />
</button>

<!-- Event with user_data passed to callback -->
<view scroll_one="true">
    <event_cb callback="view_selected_cb" trigger="clicked" user_data="$screen" />
</view>
```

### Event Callback Attributes

| Attribute | Required? | Description |
|-----------|-----------|-------------|
| `trigger` | ✅ | LVGL event type that fires the callback |
| `callback` | ✅ | Name of the C function to call |
| `user_data` | Optional | Data to pass to the callback (can use `$prop` template variables) |

### Event Trigger Types

| Trigger | Description |
|---------|-------------|
| `clicked` | Short press and release |
| `pressed` | Immediately on press |
| `released` | On release |
| `value_changed` | Widget value changed |
| `focused` | Widget gains focus |
| `defocused` | Widget loses focus |
| `gesture` | Gesture detected |

---

## 12. Color Format

Colors can be specified in several formats:

| Format | Example | Description |
|--------|---------|-------------|
| `0xRRGGBB` | `0xFF0000` | Standard 6-digit hex (preferred) |
| `0xRGB` | `0xF00` | Short 3-digit hex |
| `0xffffff` | `0xffffff` | Lowercase hex (also valid) |
| `#RRGGBB` | `#FF0000` | CSS-style hex |
| `0x000000` | `0x000000` | Black |

> [!IMPORTANT]
> The `0xRRGGBB` format (without `#`) is the dominant convention in all analysed projects.
> Use this format for consistency.

---

## 13. Value Formats

### Sizes

| Format | Example | Description |
|--------|---------|-------------|
| Integer | `"120"` | Fixed pixel value |
| Percentage | `"50%"`, `"100%"` | Percentage of parent |
| Content | `"content"` | Fit to content size |

### Opacity

| Format | Example | Description |
|--------|---------|-------------|
| Integer (0–255) | `"255"` | LVGL native opacity scale |
| Percentage | `"40%"`, `"70%"`, `"100%"` | Percentage (mapped to 0–255) |

### Rotation

Rotation values use **0.1 degree units**:

| XML Value | Actual Rotation |
|-----------|-----------------|
| `900` | 90° clockwise |
| `-900` | 90° counter-clockwise |
| `450` | 45° clockwise |
| `3600` | Full rotation (360°) |

### Scale

Scale values use **256 = 100%**:

| XML Value | Actual Scale |
|-----------|--------------|
| `256` | 100% (original size) |
| `128` | 50% |
| `512` | 200% |

---

## 14. Constants Reference System (`#const_name`)

Constants defined in `<consts>` (in `globals.xml` or screen-local) are referenced using the `#` prefix:

```xml
<!-- In globals.xml or screen-local <consts> -->
<consts>
    <int name="space_sm" value="6" />
    <int name="space_md" value="12" />
    <int name="space_lg" value="24" />
    <int name="icon_size" value="24" />
    <int name="border_width" value="1" />
    <int name="radius_default" value="8" />
    <color name="dark_blue" value="0x035391" />
    <color name="color_accent" value="0x24EAA2" />
</consts>

<!-- Referenced in styles and widget attributes -->
<style name="card" radius="#radius_default" pad_all="#space_lg" border_width="#border_width" />
<convert src="icons/wifi.svg" dest="icons/wifi.png" width="#icon_size" />
<view height="#space_md">
```

> [!IMPORTANT]
> The `#const_name` syntax allows design tokens / theme values to be defined once and
> used everywhere — similar to CSS custom properties. Constants can be `<int>`, `<color>`,
> `<bool>`, or `<px>` types. Screen-local `<consts>` override globals of the same name.

---

## 15. Inline Part+State Style Selectors (Hyphenated Syntax)

In addition to applying styles via child `<style>` elements, LVGL Pro supports **inline
part+state targeting** using a hyphenated attribute syntax:

```xml
<!-- Format: style_<property>-<part>-<state>="value" -->

<!-- Set indicator color when checked -->
<lv_checkbox style_bg_color-indicator-checked="$color" style_border_color-indicator-checked="$color" />

<!-- Set arc indicator color -->
<lv_arc style_arc_color-indicator="$color" style_bg_color-knob="$color" />

<!-- Set slider indicator color -->
<lv_slider style_bg_color-indicator="#secondary_color" />
```

> [!TIP]
> This syntax is shorthand for what would otherwise require separate `<style>` child elements
> with `selector="indicator|checked"`. Use it for one-off overrides without defining a named style.

---

## 16. Conditional Style Binding (`<bind_style>`)

The `<bind_style>` element applies a style conditionally based on a subject value — used for
runtime theme switching and conditional visual states:

```xml
<!-- Light/dark theme switching: apply dark style when subject_theme_dark == 1 -->
<view>
    <style name="style_panel_light" />
    <bind_style name="style_panel_dark" subject="subject_theme_dark" ref_value="1" />
</view>

<!-- With part selector -->
<lv_keyboard>
    <style name="style_kb_key_light" selector="items" />
    <bind_style name="style_kb_key_dark" subject="subject_theme_dark" ref_value="1" selector="items" />
</lv_keyboard>

<!-- Slider with conditional dark mode -->
<lv_slider value="20">
    <style name="style_main" />
    <bind_style name="style_main_dark" subject="subject_dark_mode" ref_value="1" />
</lv_slider>
```

| Attribute | Required? | Description |
|-----------|-----------|-------------|
| `name` | ✅ | Name of the style to apply when condition is true |
| `subject` | ✅ | Subject to observe |
| `ref_value` | ✅ | Value to compare against |
| `selector` | Optional | Widget part+state selector (e.g., `"items"`, `"indicator\|checked"`) |

> [!IMPORTANT]
> `<bind_style>` differs from `<bind_state_if_eq>` — it applies/removes an **entire style class**
> rather than activating a widget state. This is the primary mechanism for runtime theme switching.

---

## 17. Screen Navigation & Transitions

LVGL Pro supports two screen navigation patterns based on whether the target screen is **permanent** or **dynamic**.

### 17.1 Permanent vs Dynamic Screens

```xml
<!-- Permanent screen: created once, state preserved across navigations -->
<screen permanent="true">
    <view>
        <lv_slider align="center" />  <!-- value persists when navigating away and back -->
    </view>
</screen>

<!-- Dynamic screen (default): created on navigation, destroyed when left -->
<screen>
    <view>
        <lv_slider align="center" />  <!-- value is lost when navigating away -->
    </view>
</screen>
```

### 17.2 Navigation Events

```xml
<!-- Navigate to a DYNAMIC screen (creates it fresh) -->
<lv_button>
    <lv_label text="About" />
    <screen_create_event screen="screen_about" anim_type="move_top" duration="500" />
</lv_button>

<!-- Navigate to a PERMANENT screen (loads already-existing instance) -->
<lv_button>
    <lv_label text="Back" />
    <screen_load_event screen="screen_main" anim_type="move_bottom" duration="500" />
</lv_button>
```

#### `<screen_create_event>` — Navigate to Dynamic Screen

| Attribute | Required? | Description |
|-----------|-----------|-------------|
| `screen` | ✅ | Name of the target screen (matches the XML filename without `.xml`) |
| `anim_type` | Optional | Transition animation type |
| `duration` | Optional | Animation duration in milliseconds |

#### `<screen_load_event>` — Navigate to Permanent Screen

| Attribute | Required? | Description |
|-----------|-----------|-------------|
| `screen` | ✅ | Name of the target screen |
| `anim_type` | Optional | Transition animation type |
| `duration` | Optional | Animation duration in milliseconds |

#### Screen Transition Animation Types

| `anim_type` | Description |
|-------------|-------------|
| `none` | Instant switch |
| `move_left` | Slide in from right |
| `move_right` | Slide in from left |
| `move_top` | Slide in from bottom |
| `move_bottom` | Slide in from top |
| `over_left` | Overlay from right |
| `over_right` | Overlay from left |
| `over_top` | Overlay from bottom |
| `over_bottom` | Overlay from top |
| `fade_in` | Fade in |
| `fade_out` | Fade out |

---

## 18. Animation System (`<animations>` / `<timeline>`)

LVGL Pro provides a **declarative animation system** using named timelines that can be composed hierarchically.

### 18.1 Defining Timelines in a Screen

```xml
<screen>
    <animations>
        <timeline name="screen_open">
            <!-- Include timelines defined by child components -->
            <include_timeline target="show" timeline="show_up" />
            <include_timeline target="hide" timeline="show_up" />
            <include_timeline target="button_list" timeline="list_open" />
        </timeline>
    </animations>

    <view>
        <!-- Auto-play timeline on screen load -->
        <play_timeline_event target="self" timeline="screen_open" trigger="screen_loaded" />

        <list name="button_list" />

        <!-- Play timeline on click -->
        <button_normal label_text="Show" name="show">
            <play_timeline_event target="button_list" timeline="list_open" />
        </button_normal>

        <!-- Play timeline in REVERSE on click -->
        <button_normal label_text="Hide" name="hide">
            <play_timeline_event target="button_list" timeline="list_open" reverse="true" />
        </button_normal>
    </view>
</screen>
```

### 18.2 `<play_timeline_event>` Attributes

| Attribute | Required? | Description |
|-----------|-----------|-------------|
| `target` | ✅ | Widget name to play animation on, or `"self"` for current screen |
| `timeline` | ✅ | Name of the timeline to play |
| `trigger` | Optional | Event that triggers playback (e.g., `"screen_loaded"`, `"clicked"`) |
| `reverse` | Optional | `"true"` to play the timeline in reverse |

### 18.3 `<include_timeline>` Attributes

| Attribute | Required? | Description |
|-----------|-----------|-------------|
| `target` | ✅ | Widget name whose timeline to include |
| `timeline` | ✅ | Name of the timeline to include |

> [!NOTE]
> Components and widgets can define their own `<animations>` block with reusable timelines.
> Parent screens compose complex animations by including child component timelines with
> `<include_timeline>`.

---

## 19. Translation / Internationalization System

LVGL Pro includes a built-in i18n system via `translations.xml`.

### 19.1 `translations.xml`

```xml
<translations languages="en de">
    <translation tag="dog" char_count="40" en="This is a dog" de="Das ist ein Hund" />
    <translation tag="cat" char_count="40" en="A curious little cat" de="Eine neugierige kleine Katze" />
    <translation tag="house" char_count="40" en="The house is cozy and warm" de="Das Haus ist gemütlich und warm" />
    <translation
        char_count="60"
        tag="person"
        en="A kind person with a bright smile"
        de="Eine freundliche Person mit einem strahlenden Lächeln"
    />
</translations>
```

| Attribute | Description |
|-----------|-------------|
| `languages` | Space-separated list of language codes (e.g., `"en de fr"`) |
| `tag` | Unique key used to reference the translation |
| `char_count` | Maximum character count (for buffer allocation on MCU) |
| `<lang_code>` | One attribute per language with the translated string |

### 19.2 Using Translations in Widgets

```xml
<lv_label translation_tag="dog" />
<lv_label translation_tag="cat" />
```

> [!NOTE]
> When `translation_tag` is set, the label text is automatically loaded from the translation
> system. The active language can be changed at runtime from C code.
> Ensure the font used includes all characters needed for each language (use the `symbols`
> attribute on fonts to include special characters like `°äü`).

---

## 20. Component Inheritance

Components can extend other components using `extends` on the `<view>` element:

```xml
<!-- base_box: stripped-down container (removes all default styles) -->
<component>
    <view extends="lv_obj" ... />
</component>

<!-- container: extends base_box, adds flex layout -->
<component>
    <view extends="base_box" flex_flow="$flow" ... />
</component>

<!-- row: extends container, locks flow to "row" -->
<component>
    <view extends="container" flow="row" ... />
</component>

<!-- panel: extends container, adds visible card surface with theme -->
<component>
    <view extends="container" pad="$pad" gap="$gap">
        <style name="style_panel_light" />
        <bind_style name="style_panel_dark" subject="subject_theme_dark" ref_value="1" />
    </view>
</component>
```

The inheritance chain `base_box` → `container` → `row`/`column`/`panel` is the official
layout component pattern from the LVGL Pro Editor basic template.

---

## 21. Additional Widget Flags & Attributes

| Attribute | Type | Description |
|-----------|------|-------------|
| `floating` | Boolean | Widget is exempt from parent layout (positioned freely, not scrolled) |
| `ignore_layout` | Boolean | Same as `floating` — widget is positioned with absolute `x`/`y` |
| `one_line` | Boolean | Text area single-line mode |
| `password_mode` | Boolean | Text area password masking |
| `placeholder_text` | String | Text area placeholder text |
| `scrollable` | Boolean | Whether widget content is scrollable |
| `ext_click_area` | Integer | Extend click/touch area by N pixels on all sides |
| `flex_in_new_track` | Boolean | Force widget to start a new flex row/column |
| `clickable` | Boolean | Whether widget responds to pointer input |
| `remove_style_all` | Self-closing tag | Strips all default theme styles from a widget: `<remove_style_all />` |

---

## 22. Subject Event Types (Declarative Subject Mutation)

All subject event tags can be used as child elements of any widget. The `trigger` attribute controls when they fire.

### `<subject_set_int_event>` — Set Integer Subject

```xml
<subject_set_int_event subject="subject_index" value="2" trigger="clicked" />
```

### `<subject_set_string_event>` — Set String Subject

```xml
<subject_set_string_event subject="subject_text" value="Hello!" trigger="clicked" />
```

### `<subject_toggle_event>` — Toggle Subject Between 0/1

```xml
<subject_toggle_event subject="subject_dark_mode" trigger="clicked" />
```

### `<subject_increment_event>` — Increment/Decrement Subject

```xml
<subject_increment_event
    subject="subject_value"
    step="5"
    min_value="0"
    max_value="100"
    rollover="true"
    trigger="long_pressed_repeat"
/>
```

| Attribute | Description |
|-----------|-------------|
| `subject` | Target subject name |
| `step` | Increment amount (negative for decrement) |
| `min_value` | Minimum allowed value (clamp) |
| `max_value` | Maximum allowed value (clamp) |
| `rollover` | `"true"` wraps around at min/max boundaries |
| `trigger` | Event trigger (see below) |

### Event Trigger Values

| Trigger | Description |
|---------|-------------|
| `clicked` | Widget is clicked/tapped |
| `pressed` | Widget is pressed down |
| `long_pressed_repeat` | Long press with auto-repeat |
| `focused` | Widget gains focus |
| `defocused` | Widget loses focus |
| `cancel` | Cancelled input |
| `ready` | Widget ready/completed |
| `screen_loaded` | Screen has been loaded |

---

## 23. Animation Property Definitions

Within a `<timeline>`, the `<animation>` tag defines individual property transitions:

```xml
<timeline name="show_up">
    <animation target="self" prop="opa" start="0" end="255" duration="200" early_apply="true" />
    <animation target="self" prop="translate_y" start="20" end="0" duration="200" early_apply="true" />
</timeline>
```

| Attribute | Required? | Description |
|-----------|-----------|-------------|
| `target` | ✅ | Widget name or `"self"` |
| `prop` | ✅ | Style property to animate (e.g., `opa`, `translate_x`, `translate_y`) |
| `start` | ✅ | Start value |
| `end` | ✅ | End value |
| `duration` | ✅ | Duration in milliseconds |
| `early_apply` | Optional | `"true"` to apply the start value immediately |

`<include_timeline>` can also include a `delay` attribute:

```xml
<include_timeline target="button_0" timeline="show_up" delay="0" />
<include_timeline target="button_1" timeline="show_up" delay="100" />
```

---

## 24. Widget Sub-Elements (Hyphenated Child Tags)

Complex widgets use hyphenated child tags to define internal structure:

| Widget | Sub-element | Purpose |
|--------|-------------|---------|
| `lv_tabview` | `<lv_tabview-tab text="...">` | Tab content container |
| `lv_tabview` | `<lv_tabview-tab_button index="0">` | Tab button customization |
| `lv_table` | `<lv_table-cell row="0" column="0" value="..." ctrl="merge_right" />` | Table cell with optional merge |
| `lv_table` | `<lv_table-column column="0" width="200" />` | Column width control |
| `lv_chart` | `<lv_chart-series color="..." axis="..." values="..." />` | Data series |
| `lv_chart` | `<lv_chart-axis axis="primary_y" min_value="0" max_value="100" />` | Axis configuration |
| `lv_chart` | `<lv_chart-cursor color="..." dir="hor" pos_x="60" pos_y="70" />` | Cursor line |
| `lv_scale` | `<lv_scale-section style_main="..." bind_min_value="..." bind_max_value="..." />` | Colored section |
| `lv_spangroup` | `<lv_spangroup-span text="..." style="..." />` | Rich text span |
| `lv_calendar` | `<lv_calendar-header_arrow />` | Arrow-based header |
| `lv_dropdown` | `<lv_dropdown-list ... />` | List styling |

---

## 25. Component Slot System

Components can define **pluggable content insertion areas** using `<slot>`:

```xml
<!-- In component definition -->
<component>
    <api>
        <slot name="trailing" />
    </api>
    <view>
        <lv_label text="$text" />
        <!-- Slot content is inserted here at the position of the slot declaration -->
    </view>
</component>

<!-- Usage: insert content into the slot via hyphenated tag -->
<list_item text="Settings">
    <list_item-trailing>
        <lv_switch />
    </list_item-trailing>
</list_item>
```

---

## 26. Expression Syntax (`{...}`)

Attribute values can contain expressions inside curly braces for dynamic evaluation:

```xml
<!-- Boolean/conditional flags -->
<lv_image hidden="{!icon}" />
<lv_label hidden="{!subtitle}" />

<!-- Math expressions with constants -->
<lv_label text="{base}" />
<lv_obj hidden="{10 * (2 + base)}" />
```

---

## 27. Automated Testing Framework (`<test>`)

LVGL Pro includes an XML-based testing framework for screenshot comparison:

```xml
<test>
    <view extends="screen_layouts">
        <lv_slider bind_value="subject_volume" align="center" />
    </view>
    <steps>
        <set_language name="en" />
        <subject_set subject="subject_volume" value="30" />
        <wait ms="200" />
        <screenshot_compare path="start.png" />

        <click_at x="20" y="125" />
        <wait ms="500" />
        <screenshot_compare path="checkbox_1.png" />

        <click_on name="widget_name" />
        <move_to x="430" y="176" />
        <press />
        <release />
        <subject_compare subject="subject_volume" value="50" />
    </steps>
</test>
```

---

## 28. Conditional Asset Groups (`if_target`)

Images and fonts blocks can be conditionally included for specific hardware targets:

```xml
<images if_target="large" memory="ospi">
    <data name="logo" src_path="images/logo.png" color_format="argb8888" />
</images>

<fonts if_target="large" memory="ospi">
    <bin name="font_large" src_path="fonts/Montserrat.ttf" size="32" bpp="4" as_file="false" />
</fonts>
```
