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

    # 3. Generate screen XML files
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
        for s in (out_path / "screens").glob("*.xml"):
            print(f"  - {s}")
        return 0
    except Exception as err:
        print(f"Error generating project: {err}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
