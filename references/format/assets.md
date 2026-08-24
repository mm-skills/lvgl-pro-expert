# LVGL Pro XML: Assets (Images & Fonts)

Covers how to declare, convert, and use images and fonts within an LVGL Pro project. All assets must be declared in the `<images>` and `<fonts>` blocks in `globals.xml`.

## 1. Memory Regions

In `project.xml`, hardware targets define memory regions:
```xml
<memory name="int_flash" size="2MB" />
```
In `globals.xml`, asset groups are mapped to these regions:
```xml
<images memory="int_flash"> ... </images>
```

## 2. Images

Images can be embedded as C arrays, loaded from the filesystem, or generated from SVG at build time.

```xml
<images memory="int_flash">
    <!-- Embedded as C array (Fastest, no filesystem needed) -->
    <data name="img_bg" src_path="images/bg.png" color_format="rgb565" />
    
    <!-- Loaded from filesystem at runtime -->
    <file name="img_photo" src_path="images/photo.png" />
    
    <!-- SVG to PNG Build-Time Conversion Pipeline -->
    <convert src="images/icons/wifi.svg" dest="images/icons/wifi.png" width="32" color_format="argb8888" />
    <data name="icon_wifi" src_path="images/icons/wifi.png" color_format="argb8888" />
</images>
```

### Color Formats
- `rgb565`: 16-bit, no transparency (Best for solid backgrounds).
- `rgb565a8`: 16-bit + 8-bit alpha (Best balance for transparent UI elements).
- `argb8888`: 32-bit true color with full alpha (Highest quality).
- `a8`: Alpha-only mask (Useful for monochrome icons tinted with `image_recolor`).

## 3. Fonts

LVGL supports three font rendering backends.

```xml
<fonts memory="int_flash">
    <!-- Binary Bitmap (Pre-compiled, lowest RAM usage) -->
    <bin 
        name="font_sm" 
        src_path="fonts/Roboto.ttf" 
        size="14" 
        bpp="4" 
        as_file="false" 
        range="0x20-0x7F" 
    />
    
    <!-- Tiny TTF (Vector rendered at runtime, low footprint) -->
    <tiny_ttf 
        name="font_md" 
        src_path="fonts/Roboto.ttf" 
        size="24" 
        as_file="false" 
    />
    
    <!-- FreeType (Full vector engine, requires high RAM/PSRAM) -->
    <freetype 
        name="font_lg" 
        src_path="fonts/Noto.ttf" 
        size="48" 
    />
</fonts>
```

### Attributes for `<bin>` fonts:
- `size`: Pixel height.
- `bpp`: Bits per pixel for anti-aliasing (1, 2, 4, 8). Higher = smoother but larger size.
- `as_file`: `false` = embed as C array; `true` = generate `.bin` file to load at runtime.
- `range`: Unicode range to generate (e.g. `0x20-0x7F` for ASCII).
- `symbols`: Specific extra characters to include (e.g. `"°äü"`).
