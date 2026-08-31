# Ecosystems and Target Architecture

LVGL Pro divides an embedded graphical application into a strict **Two-Layer Architecture**:

1. **UI Layer (Hardware-Agnostic)**: Pure XML screens, components, styles, subjects, and animations managed by the LVGL Pro XML engine.
2. **Hardware Layer (Ecosystem-Specific)**: Board-specific display drivers, touch controllers, framebuffers, OS task runners, and peripheral interfaces.

```
┌─────────────────────────────────────────────────────────────┐
│                    UI LAYER (LVGL Pro XML)                  │
│       screens/*.xml, components/*.xml, globals.xml          │
└──────────────────────────────┬──────────────────────────────┘
                               │ LVGL v9 Core C Engine
┌──────────────────────────────┴──────────────────────────────┐
│                  HARDWARE / ECOSYSTEM LAYER                 │
│   Linux (DRM/SDL) | VSCode Sim | Zephyr RTOS | Custom Bare-metal│
└─────────────────────────────────────────────────────────────┘
```

---

## The 4 Supported Ecosystems

| Ecosystem | Environment & Backends | Target Hardware | Configuration |
|---|---|---|---|
| **Linux** | SDL2, Wayland, X11, DRM/KMS, Linux fbdev | Embedded Linux (Raspberry Pi, i.MX6/8, Toradex, BeagleBone) | Configurable arbitrary resolutions and color formats in `project.xml` |
| **VSCode** | Desktop simulator using SDL2 backend | Host PC (Windows, macOS, Linux) for rapid UI design and testing | Adjustable virtual display resolution and color depth |
| **Zephyr** | Zephyr RTOS with hardware device tree overlays | 7 officially supported MCU boards (Renesas, STM32, NXP, Espressif) | Predefined board profiles and overlay configurations |
| **UI-Only** | Standalone portable XML UI files | Any custom platform (FreeRTOS, ESP-IDF, Bare-metal) | Platform-independent XML files compiled via LVGL Pro CLI or runtime parser |

---

## `project.xml` Target Configuration

Target configurations specify display dimensions, shape, color format, and optional memory pool declarations for the hardware target.

### Example 1: Standard Embedded Target with Memory Regions
```xml
<project lvgl_version="9.5.0" theme="default">
    <targets>
        <target name="target1">
            <display width="480" height="320" color_depth="16" color_format="RGB565" />
            <memory name="int_ram" size="512KB" />
            <memory name="ext_flash" size="16MB" bandwidth="100MB/s" />
        </target>
    </targets>
</project>
```

### Example 2: Circular Smartwatch Display Target
```xml
<project lvgl_version="9.5.0">
    <targets>
        <target name="smartwatch">
            <display width="466" height="466" radius="233" color_depth="32" color_format="ARGB8888" />
        </target>
    </targets>
</project>
```

---

## Target Attributes & Tags Reference

### `<display>` Attributes
| Attribute | Type | Description |
|---|---|---|
| `width` | Integer (px) | Horizontal resolution |
| `height` | Integer (px) | Vertical resolution |
| `radius` | Integer (px) | Corner radius (`width / 2` for a complete circle) |
| `color_depth` | Integer | Pixel bit depth: `16` (RGB565), `24` (RGB888), `32` (ARGB8888) |
| `color_format` | Enum | `RGB565`, `ARGB8888`, `RGB888`, `XRGB8888` |
| `dpi` | Integer | Screen DPI for auto-scaling |

### `<memory>` Attributes
| Attribute | Type | Description |
|---|---|---|
| `name` | String | Region identifier (e.g. `int_ram`, `ospi_flash`) |
| `size` | String | Region capacity (e.g. `512KB`, `8MB`) |
| `bandwidth` | String | Bus bandwidth rating (e.g. `80MB/s`) |


## Official Update
---
title: Targets
description: Learn how to use `<target>`s to preview your UI on different screen sizes with different assets.
---

<Callout type="info">
This feature requires [LVGL Pro Editor v2.0](https://github.com/lvgl/lvgl_pro/releases) or higher.
</Callout>

If multiple `<target>`s are declared in [`project.xml`](./project), the Editor will allow you to conditionally
include/exclude assets, styles, and even views based on the selected target. 

## Example configuration

We will use the following `project.xml` as an example:
```xml
<project name="my_ui" lvgl_version="9.5.0">
    <targets>
        <target name="large">
            <display width="800" height="480"/>
            <memory name="int_flash" size="1MB"/>
            <memory name="ospi" size="16MB" bandwidth="4MB/s"/>
        </target>
        <target name="small">
            <display width="480" height="320"/>
            <memory name="int_flash" size="512kB"/>
        </target>
    </targets>
</project>
```

## `if_target`

Several XML elements support an `if_target` property where one or more targets can be added to 
enable the content of that block. 
For example:

```xml
<globals>
    <!-- Images for the `large` target -->
    <images if_target="large">
        <data name="logo.png" src_path="images/logo_large.png" />
        <data name="sunny.png" src_path="images/sunny_large.png" />
    </images>

    <!-- Images for all the other cases -->
    <images>
        <data name="logo.png" src_path="images/logo_normal.png" />
        <data name="sunny.png" src_path="images/sunny_normal.png" />
    </images>
</globals>
```

The same works for 
- `<fonts>`
- `<styles>`
- `<consts>`
- and most importantly `<view>`

Multiple targets can be specified as `if_target="large|medium"`. 
The block will be included if the current target is either `large` or `medium`.


## Memory Usage

When a target is set for an `<images>` or `<fonts>` block a `memory` attribute can be added to specify the memory 
region to be used from the given target. 

If the memory region is set and `globals.xml` is opened, the editor will show an overview of the memory usage 
for the selected target. It also shows the access time estimation based on the set `bandwidth` for the given memory region.

![Memory usage summary in LVGL Pro](../_static/images/memory_usage_summary.png)

## Precedence

Always the first match has priority, so if a `<view>` has an `if_target` 
that matches the current target, all the other `<view>`s will be ignored. 
This allows you to have a default `<view>` as the last block, and then override it for specific targets before that.

## Selecting a target

When C code is exported all the blocks with `if_target` are wrapped to `if` and `#if`. That
is, it's possible to select the target at runtime or at compile time. 

### Runtime selection

It's useful when you need to support multiple targets with the same binary. For example, if you have a product that comes in two different screen sizes, you can use the same firmware for both, and select the target at runtime based on the detected hardware.

Its disadvantage is that all the assets and styles for all targets will be included in the binary, which increases the size of the firmware.

Also, the firmware needs to support all the features of all targets, which can be a problem if the targets have very different capabilities. For example if a widget uses OpenGL and 3D, it can't run on an MCU. In this case compile time selection is the only option.

To select the target at runtime, you can call `<project_name>_set_target(<PROJECT_NAME>_<TARGET_NAME>)`. For example:
```c
my_ui_set_target(MY_UI_LARGE);
```

### Compile time selection

To save memory and binary size, you can select the target at compile time. This way only the assets and styles for the selected target will be included in the binary.

Just set a `<PROJECT_NAME>_TARGET` `define` to `<PROJECT_NAME>_<TARGET_NAME>`. For example:
```c
#define MY_UI_TARGET MY_UI_LARGE
```
In CMake you can add a definition like this:
```cmake
add_definitions(-DMY_UI_TARGET=MY_UI_LARGE)
```
