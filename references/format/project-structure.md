# LVGL Pro XML: Project Structure

Covers `project.xml`, `globals.xml`, `translations.xml`, and the overall directory layout of an LVGL Pro project.

> [!NOTE]
> Unlike SquareLine Studio's single JSON file, LVGL Pro uses a modular, multi-file XML architecture where each screen, component, and custom widget gets its own file.

## 1. Directory Structure

A standard LVGL Pro project directory looks like this:

```text
my_project/
├── project.xml           # Target display config, theme, LVGL version
├── globals.xml           # Registry for subjects, images, fonts, global styles
├── translations.xml      # Multi-language strings (optional)
├── screens/              # Screen definitions (1 file per screen)
│   ├── main.xml
│   └── settings.xml
├── components/           # Reusable pure-XML components (optional)
│   └── custom_button/
│       └── custom_button.xml
├── widgets/              # XML+C custom widgets (optional)
│   └── custom_gauge/
│       └── custom_gauge.xml
├── images/               # Image assets (PNG, JPG, SVG)
└── fonts/                # Font assets (TTF, OTF, BIN)
```

> [!IMPORTANT]
> Components and widgets must live in their own subdirectories matching their tag name. For example, the XML tag `<my_component />` requires a file at `components/my_component/my_component.xml`.

---

## 2. `project.xml` Schema

Defines hardware targets, screen dimensions, theme, and memory regions.

### Complete Example
```xml
<project name="my_ui" lvgl_version="9.5.0" theme="default">
    <targets>
        <target name="target1">
            <!-- Rectangular display -->
            <display width="480" height="320" color_format="RGB565" />
            
            <!-- Declare memory regions for assets to use -->
            <memory name="int_ram" size="1MB" />
            <memory name="int_flash" size="2MB" bandwidth="100MB/s" />
        </target>
        <target name="target_round">
            <!-- Round display (radius = width/2) -->
            <display width="466" height="466" radius="233" />
        </target>
    </targets>
</project>
```

### Display Attributes
| Attribute | Description |
|-----------|-------------|
| `width` / `height` | Display resolution in pixels |
| `radius` | Corner radius; set to `width/2` for fully circular displays |
| `color_format` | Default pixel format (e.g. `"RGB565"`, `"ARGB8888"`) |

---

## 3. `globals.xml` Schema

The central registry. Everything used across multiple screens must be declared here.

### Complete Example
```xml
<globals>
    <!-- Constants referenced with #const_name -->
    <consts>
        <color name="primary_color" value="0x24EAA2" />
        <int name="spacing_md" value="16" />
        <bool name="low_power_mode" value="false" />
    </consts>

    <!-- Global Styles -->
    <styles>
        <style name="card_bg" bg_color="0x2A2A2A" radius="8" pad_all="#spacing_md" />
    </styles>

    <!-- Reactive Data Subjects -->
    <subjects>
        <int name="battery_level" value="100" min_value="0" max_value="100" />
        <string name="wifi_status_text" value="Disconnected" />
    </subjects>

    <!-- Image Assets -->
    <images memory="int_flash">
        <data name="img_logo" src_path="images/logo.png" color_format="argb8888" />
        <convert src="images/icon.svg" dest="images/icon.png" width="32" color_format="argb8888" />
        <data name="img_icon" src_path="images/icon.png" color_format="argb8888" />
    </images>

    <!-- Font Assets -->
    <fonts memory="int_flash">
        <bin name="font_primary" src_path="fonts/Inter.ttf" size="16" bpp="4" as_file="false" range="0x20-0x7f" />
    </fonts>
</globals>
```

> [!TIP]
> The `<convert>` tag inside `<images>` is a powerful build-time tool to rasterize SVGs into PNGs before they are embedded with `<data>`.
