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
