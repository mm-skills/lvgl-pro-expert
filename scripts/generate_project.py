#!/usr/bin/env python3
"""
Scaffold generator for LVGL Pro projects.

Creates a minimal, valid LVGL Pro project directory structure:
  project.xml          - Display targets and LVGL version configuration
  globals.xml          - Global subjects, constants, styles, images, fonts, api
  screens/screen_*.xml - One or more initial screen definitions

Usage:
  python3 generate_project.py --name NAME --width W --height H [--radius R] [--screens 'name1 name2'] [--output DIR]
"""

import argparse
import os
import sys
from pathlib import Path
from typing import List, Optional


PROJECT_XML_TEMPLATE = """<project lvgl_version="9.5.0">
    <targets>
        <target name="default">
            {display_tag}
        </target>
    </targets>
</project>
"""

GLOBALS_XML_TEMPLATE = """<globals>
    <!-- Component API definitions and properties -->
    <api></api>

    <!-- Global constants (colors, dimensions, strings) -->
    <!-- Example: <color name="accent" value="0x6366f1" /> -->
    <consts></consts>

    <!-- Reactive data subjects for dynamic data binding -->
    <!-- Example: <int name="subject_count" default="0" /> -->
    <subjects></subjects>

    <!-- Global image assets -->
    <!-- Example: <data name="logo" src_path="assets/logo.png" /> -->
    <images></images>

    <!-- Global font assets -->
    <!-- Example: <bin name="font_roboto_16" src_path="assets/roboto_16.bin" /> -->
    <fonts></fonts>

    <!-- Global reusable styles -->
    <!-- Example: <style name="style_btn" bg_color="0x2196F3" radius="8" /> -->
    <styles></styles>
</globals>
"""

SCREEN_XML_TEMPLATE = """<screen>
    <view flex_flow="column"
          style_flex_main_place="center"
          style_flex_cross_place="center">
        <lv_label name="title" text="{screen_title}" />
    </view>
</screen>
"""

AGENTS_MD_TEMPLATE = """# LVGL Pro — Agent Ground Rules

This project uses [LVGL Pro](https://lvgl.io/docs/pro) XML format.
Before editing any XML, read these rules.

## Three Sigils

| Sigil | Meaning | Example |
|-------|---------|---------|
| `$`   | Component API prop | `text="$title"` |
| `#`   | Named constant (from `<consts>`) | `style_text_color="#accent"` |
| `{{}}`  | One-time expression (evaluated once) | `width="{{parent.width / 2}}"` |

## File Kinds

| Root tag | Purpose | Needs C code? |
|----------|---------|---------------|
| `<component>` | Reusable XML-only UI block | No |
| `<screen>` | Top-level screen | No |
| `<widget>` | Custom widget with C behaviour | Yes |

## Key Rules

1. **Never invent attributes.** Check the widget schema at
   `lvgl_widgets_xml/v9.5.0/lv_<widget>.xml` or use the MCP server.
2. **Styles initialise once.** `$api_prop` cannot go inside a `<style>` block —
   use it directly on the `<view>` element instead.
3. **Every widget needs a `name` attribute** (becomes the C variable name).
4. **Dropdown/roller options** use `&#10;` for line separators, not `\\n`.
5. **Style selectors** use hyphens: `style_bg_color-indicator-checked="0x4CAF50"`.
6. **Never edit generated C files** — they are overwritten on every Export Code.
7. **`<bin>` fonts require `as_file="false"` or `as_file="true"`**.
8. **`color_format` values must be lowercase** (`rgb565` not `RGB565`).

## Validation

```bash
lvglpro validate .          # Pro/Platform license
python3 scripts/validate_project.py .  # Free fallback
```

## MCP Server

The LVGL MCP server provides grounded documentation answers:
- Endpoint: `https://lvgl.mcp.kapa.ai/` (read-only)
- Config is in `.claude/.mcp.json` if present
"""


def parse_screen_names(screens_arg: Optional[List[str]]) -> List[str]:
    """Parse screen names from CLI arguments, handling strings and lists."""
    if not screens_arg:
        return ["home"]
    
    names = []
    for item in screens_arg:
        for part in item.split():
            clean = part.strip()
            if clean:
                names.append(clean)
    return names if names else ["home"]


def format_screen_title(screen_name: str) -> str:
    """Format screen name into a clean user-facing title."""
    clean = screen_name
    if clean.startswith("screen_"):
        clean = clean[len("screen_"):]
    return clean.replace("_", " ").replace("-", " ").title()


def format_screen_filename(screen_name: str) -> str:
    """Ensure screen filename starts with screen_ and ends with .xml."""
    clean = screen_name
    if clean.endswith(".xml"):
        clean = clean[:-4]
    if not clean.startswith("screen_"):
        clean = f"screen_{clean}"
    return f"{clean}.xml"


def generate_project(
    name: str,
    width: int,
    height: int,
    radius: Optional[int] = None,
    screens: Optional[List[str]] = None,
    output_dir: Optional[str] = None,
) -> Path:
    """Generate an LVGL Pro project structure."""
    target_dir = Path(output_dir) if output_dir else Path(name)
    screens_dir = target_dir / "screens"
    
    target_dir.mkdir(parents=True, exist_ok=True)
    screens_dir.mkdir(parents=True, exist_ok=True)

    # 1. Generate project.xml
    if radius is not None:
        display_tag = f'<display width="{width}" height="{height}" radius="{radius}" />'
    else:
        display_tag = f'<display width="{width}" height="{height}" />'

    project_content = PROJECT_XML_TEMPLATE.format(display_tag=display_tag)
    (target_dir / "project.xml").write_text(project_content, encoding="utf-8")

    # 2. Generate globals.xml
    (target_dir / "globals.xml").write_text(GLOBALS_XML_TEMPLATE, encoding="utf-8")

    # 3. Generate AGENTS.md (agent ground rules for subsequent AI editing)
    (target_dir / "AGENTS.md").write_text(AGENTS_MD_TEMPLATE, encoding="utf-8")

    # 4. Generate screen XML files
    screen_list = parse_screen_names(screens)
    for screen_raw_name in screen_list:
        filename = format_screen_filename(screen_raw_name)
        title = format_screen_title(screen_raw_name)
        screen_content = SCREEN_XML_TEMPLATE.format(screen_title=title)
        (screens_dir / filename).write_text(screen_content, encoding="utf-8")

    return target_dir


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Scaffold a minimal, valid LVGL Pro project."
    )
    parser.add_argument(
        "--name",
        type=str,
        required=True,
        help="Project name",
    )
    parser.add_argument(
        "--width",
        type=int,
        required=True,
        help="Display width in pixels (e.g. 480)",
    )
    parser.add_argument(
        "--height",
        type=int,
        required=True,
        help="Display height in pixels (e.g. 320)",
    )
    parser.add_argument(
        "--radius",
        type=int,
        default=None,
        help="Display radius for round displays (optional)",
    )
    parser.add_argument(
        "--screens",
        nargs="+",
        default=["home"],
        help="Screen names (space-separated or list, default: 'home')",
    )
    parser.add_argument(
        "--output",
        type=str,
        default=None,
        help="Target output directory (default: ./<NAME>)",
    )

    args = parser.parse_args()

    try:
        out_path = generate_project(
            name=args.name,
            width=args.width,
            height=args.height,
            radius=args.radius,
            screens=args.screens,
            output_dir=args.output,
        )
        print(f"LVGL Pro project '{args.name}' successfully created at: {out_path.resolve()}")
        print(f"  - {out_path / 'project.xml'}")
        print(f"  - {out_path / 'globals.xml'}")
        print(f"  - {out_path / 'AGENTS.md'}")
        for s in (out_path / "screens").glob("*.xml"):
            print(f"  - {s}")
        return 0
    except Exception as err:
        print(f"Error generating project: {err}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
