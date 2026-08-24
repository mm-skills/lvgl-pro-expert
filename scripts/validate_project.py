#!/usr/bin/env python3
"""
Validation script for LVGL Pro project directories.

Validates:
  - project.xml exists and has <targets> with at least one <target> containing <display>
  - globals.xml exists and parses as valid XML
  - At least one .xml file exists in screens/
  - Every widget element (lv_*) has a name attribute
  - Widget names are unique within each screen file
  - All widget types are in the known set (30+ types) or recognized sub-elements
  - Dropdown/roller options don't contain literal \\n (must use &#10;)
  - Subject references in bind_* attributes and events match declarations in globals.xml <subjects>
  - Constant references (#name) match declarations in globals.xml <consts>

Usage:
  python3 validate_project.py /path/to/project/
"""

import argparse
import os
import sys
import xml.etree.ElementTree as ET
import xml.parsers.expat
from pathlib import Path
from typing import Dict, List, Optional, Set, Tuple


KNOWN_WIDGETS = {
    "lv_obj",
    "lv_label",
    "lv_button",
    "lv_image",
    "lv_slider",
    "lv_arc",
    "lv_bar",
    "lv_switch",
    "lv_checkbox",
    "lv_dropdown",
    "lv_roller",
    "lv_textarea",
    "lv_keyboard",
    "lv_spinner",
    "lv_spinbox",
    "lv_scale",
    "lv_table",
    "lv_tabview",
    "lv_chart",
    "lv_calendar",
    "lv_led",
    "lv_line",
    "lv_canvas",
    "lv_spangroup",
    "lv_buttonmatrix",
    "lv_imagebutton",
    "lv_animimg",
    "lv_gif",
    "lv_qrcode",
}

ALLOWED_NON_WIDGET_TAGS = {
    # Structural & container tags
    "screen",
    "view",
    "component",
    "globals",
    "project",
    "targets",
    "target",
    "display",
    "memory",
    "api",
    "consts",
    "subjects",
    "images",
    "fonts",
    "styles",
    "style",
    # Global / API child types
    "int",
    "string",
    "color",
    "bool",
    "float",
    "dim",
    "pointer",
    "group",
    "data",
    "bin",
    "prop",
    "param",
    "slot",
    "element",
    "part",
    "parts",
    "arg",
    # Event and bind tags
    "subject_set_int_event",
    "subject_set_string_event",
    "subject_toggle_event",
    "subject_increment_event",
    "screen_create_event",
    "screen_load_event",
    "play_timeline_event",
    "event_cb",
    "bind_flag_if_eq",
    "bind_flag_if_gt",
    "bind_state_if_gt",
    "bind_style",
    # Animations
    "animations",
    "timeline",
    "animation",
}

SUBJECT_EVENT_TAGS = {
    "subject_set_int_event",
    "subject_set_string_event",
    "subject_toggle_event",
    "subject_increment_event",
    "bind_style",
    "bind_flag_if_eq",
    "bind_flag_if_gt",
    "bind_state_if_gt",
}


class LineTreeBuilder(ET.TreeBuilder):
    """Custom TreeBuilder that records line numbers for XML elements."""

    def __init__(self):
        super().__init__()
        self.parser = None
        self.elem_lines: Dict[ET.Element, int] = {}

    def start(self, tag, attrs):
        elem = super().start(tag, attrs)
        if self.parser:
            self.elem_lines[elem] = self.parser.CurrentLineNumber
        return elem


class ProjectValidator:
    def __init__(self, project_path: Path):
        self.project_path = project_path.resolve()
        self.errors: List[str] = []
        self.warnings: List[str] = []
        self.declared_subjects: Set[str] = set()
        self.declared_consts: Set[str] = set()
        self.declared_styles: Set[str] = set()
        self.custom_components: Set[str] = set()

    def add_error(self, file_path: Path, line: Optional[int], message: str):
        rel_path = self._rel(file_path)
        loc = f"{rel_path}:{line}" if line else rel_path
        self.errors.append(f"[ERROR] {loc}: {message}")

    def add_warning(self, file_path: Path, line: Optional[int], message: str):
        rel_path = self._rel(file_path)
        loc = f"{rel_path}:{line}" if line else rel_path
        self.warnings.append(f"[WARNING] {loc}: {message}")

    def _rel(self, path: Path) -> str:
        try:
            return str(path.relative_to(self.project_path))
        except ValueError:
            return str(path)

    def parse_xml_file(self, file_path: Path) -> Tuple[Optional[ET.Element], Dict[ET.Element, int]]:
        if not file_path.exists():
            self.add_error(file_path, None, "File does not exist")
            return None, {}

        tb = LineTreeBuilder()
        parser = xml.parsers.expat.ParserCreate()
        tb.parser = parser
        parser.StartElementHandler = tb.start
        parser.EndElementHandler = tb.end
        parser.CharacterDataHandler = tb.data

        try:
            with open(file_path, "rb") as f:
                parser.ParseFile(f)
            root = tb.close()
            return root, tb.elem_lines
        except Exception as e:
            self.add_error(file_path, getattr(parser, "CurrentLineNumber", None), f"XML parse error: {e}")
            return None, {}

    def discover_components(self):
        """Find any custom component definitions in components/."""
        components_dir = self.project_path / "components"
        if components_dir.is_dir():
            for comp_file in components_dir.rglob("*.xml"):
                self.custom_components.add(comp_file.stem)

    def validate_project_xml(self) -> bool:
        project_file = self.project_path / "project.xml"
        if not project_file.is_file():
            self.add_error(project_file, None, "Missing required configuration file 'project.xml'")
            return False

        root, lines = self.parse_xml_file(project_file)
        if root is None:
            return False

        if root.tag != "project":
            self.add_error(project_file, lines.get(root, 1), f"Root tag must be <project>, found <{root.tag}>")

        targets = root.find("targets")
        if targets is None:
            self.add_error(project_file, lines.get(root, 1), "Missing <targets> block in project.xml")
            return False

        target_elems = targets.findall("target")
        if not target_elems:
            self.add_error(project_file, lines.get(targets, 1), "<targets> must contain at least one <target>")
            return False

        has_display = False
        for target in target_elems:
            display = target.find("display")
            if display is not None:
                has_display = True
                width = display.get("width")
                height = display.get("height")
                if not width or not height:
                    self.add_error(project_file, lines.get(display, 1), "<display> must specify both 'width' and 'height'")
                else:
                    try:
                        int(width)
                        int(height)
                    except ValueError:
                        self.add_error(project_file, lines.get(display, 1), "'width' and 'height' in <display> must be integers")

        if not has_display:
            self.add_error(project_file, lines.get(targets, 1), "At least one <target> must contain a <display> element")
            return False

        return True

    def validate_globals_xml(self) -> bool:
        globals_file = self.project_path / "globals.xml"
        if not globals_file.is_file():
            self.add_error(globals_file, None, "Missing required declarations file 'globals.xml'")
            return False

        root, lines = self.parse_xml_file(globals_file)
        if root is None:
            return False

        if root.tag != "globals":
            self.add_error(globals_file, lines.get(root, 1), f"Root tag must be <globals>, found <{root.tag}>")

        # Collect declared subjects
        subjects_elem = root.find("subjects")
        if subjects_elem is not None:
            for child in subjects_elem:
                name = child.get("name")
                if name:
                    self.declared_subjects.add(name)
                else:
                    self.add_warning(globals_file, lines.get(child, 1), f"Subject declaration <{child.tag}> is missing 'name' attribute")

        # Collect declared constants
        consts_elem = root.find("consts")
        if consts_elem is not None:
            for child in consts_elem:
                name = child.get("name")
                if name:
                    self.declared_consts.add(name)
                else:
                    self.add_warning(globals_file, lines.get(child, 1), f"Constant declaration <{child.tag}> is missing 'name' attribute")

        # Collect declared styles
        styles_elem = root.find("styles")
        if styles_elem is not None:
            for child in styles_elem:
                name = child.get("name")
                if name:
                    self.declared_styles.add(name)

        return True

    def validate_screens_directory(self) -> List[Path]:
        screens_dir = self.project_path / "screens"
        if not screens_dir.is_dir():
            self.add_error(screens_dir, None, "Missing required 'screens/' directory")
            return []

        screen_files = sorted(screens_dir.glob("*.xml"))
        if not screen_files:
            self.add_error(screens_dir, None, "No XML screen files found in 'screens/' directory")
            return []

        return screen_files

    def validate_screen_element(
        self,
        elem: ET.Element,
        file_path: Path,
        lines: Dict[ET.Element, int],
        seen_widget_names: Set[str],
        screens_dir: Path,
    ):
        line = lines.get(elem, 1)
        tag = elem.tag

        # 1. Check tag type validity
        is_known_widget = tag in KNOWN_WIDGETS
        is_sub_element = "-" in tag and tag.startswith("lv_")
        is_allowed_non_widget = tag in ALLOWED_NON_WIDGET_TAGS or tag in self.custom_components

        if not (is_known_widget or is_sub_element or is_allowed_non_widget):
            if tag.startswith("lv_"):
                self.add_error(file_path, line, f"Unknown widget type '<{tag}>'")
            else:
                self.add_error(file_path, line, f"Unknown XML tag '<{tag}>'")

        if is_sub_element:
            base_widget = tag.split("-")[0]
            if base_widget not in KNOWN_WIDGETS:
                self.add_error(file_path, line, f"Sub-element '<{tag}>' references unknown base widget '{base_widget}'")

        # 2. Check widget name requirement & uniqueness
        if is_known_widget:
            name = elem.get("name")
            if not name:
                self.add_error(file_path, line, f"Widget <{tag}> is missing required 'name' attribute")
            else:
                if name in seen_widget_names:
                    self.add_error(file_path, line, f"Duplicate widget name '{name}' within screen")
                else:
                    seen_widget_names.add(name)

        # 3. Check dropdown/roller options for literal \n
        if "options" in elem.attrib:
            options_val = elem.attrib["options"]
            if "\\n" in options_val:
                self.add_error(
                    file_path,
                    line,
                    f"<{tag}> 'options' contains literal '\\n'. Use '&#10;' entity for line separators instead.",
                )

        # 4. Check subject references in bind_* attributes
        for attr_name, attr_val in elem.attrib.items():
            if attr_name.startswith("bind_"):
                # Attributes ending in -fmt are format strings (e.g. bind_text-fmt="%d°C")
                if attr_name.endswith("-fmt") or "-fmt" in attr_name:
                    continue
                # For actual subject binding
                subject_name = attr_val.strip()
                if subject_name not in self.declared_subjects:
                    self.add_error(
                        file_path,
                        line,
                        f"Subject '{subject_name}' referenced in '{attr_name}' is not declared in globals.xml <subjects>",
                    )

        # 5. Check subject references in event/binding tags
        if tag in SUBJECT_EVENT_TAGS or "subject" in elem.attrib:
            subject_attr = elem.get("subject")
            if subject_attr:
                if subject_attr not in self.declared_subjects:
                    self.add_error(
                        file_path,
                        line,
                        f"Subject '{subject_attr}' referenced in <{tag}> is not declared in globals.xml <subjects>",
                    )

        # 6. Check constant references (#name)
        for attr_name, attr_val in elem.attrib.items():
            if isinstance(attr_val, str) and attr_val.startswith("#"):
                const_name = attr_val[1:].strip()
                if const_name not in self.declared_consts:
                    self.add_error(
                        file_path,
                        line,
                        f"Constant '{attr_val}' referenced in '{attr_name}' is not declared in globals.xml <consts>",
                    )

        # 7. Check screen navigation targets
        if tag in {"screen_create_event", "screen_load_event"} and "screen" in elem.attrib:
            target_screen = elem.attrib["screen"].strip()
            # Normalize target screen search
            possible_names = [
                f"{target_screen}.xml",
                f"screen_{target_screen}.xml",
            ]
            if target_screen.startswith("screen_"):
                possible_names.append(f"{target_screen[len('screen_'):]}.xml")
            
            exists = any((screens_dir / p).is_file() for p in possible_names)
            if not exists:
                self.add_warning(
                    file_path,
                    line,
                    f"Navigation target screen '{target_screen}' does not match any file in screens/",
                )

        # Recursively validate children
        for child in elem:
            self.validate_screen_element(child, file_path, lines, seen_widget_names, screens_dir)

    def validate_screen_file(self, file_path: Path, screens_dir: Path):
        root, lines = self.parse_xml_file(file_path)
        if root is None:
            return

        if root.tag != "screen":
            self.add_warning(file_path, lines.get(root, 1), f"Screen root tag is typically <screen>, found <{root.tag}>")

        # Also collect local styles if defined in screen
        styles_block = root.find("styles")
        if styles_block is not None:
            for s in styles_block.findall("style"):
                s_name = s.get("name")
                if s_name:
                    self.declared_styles.add(s_name)

        seen_widget_names: Set[str] = set()
        for child in root:
            self.validate_screen_element(child, file_path, lines, seen_widget_names, screens_dir)

    def validate(self) -> bool:
        self.discover_components()
        self.validate_project_xml()
        self.validate_globals_xml()
        screen_files = self.validate_screens_directory()

        screens_dir = self.project_path / "screens"
        for screen_file in screen_files:
            self.validate_screen_file(screen_file, screens_dir)

        return len(self.errors) == 0


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Validate an LVGL Pro project directory for syntax and structure errors."
    )
    parser.add_argument(
        "project_dir",
        type=str,
        nargs="?",
        default=".",
        help="Path to the LVGL Pro project directory (default: current directory)",
    )

    args = parser.parse_args()
    project_path = Path(args.project_dir)

    if not project_path.is_dir():
        print(f"Error: Directory '{project_path}' does not exist.", file=sys.stderr)
        return 1

    validator = ProjectValidator(project_path)
    is_valid = validator.validate()

    # Output warnings and errors
    for warning in validator.warnings:
        print(warning)

    for error in validator.errors:
        print(error, file=sys.stderr)

    error_count = len(validator.errors)
    warning_count = len(validator.warnings)

    if is_valid:
        print(f"\nProject at '{project_path.resolve()}' is valid! ({warning_count} warnings, 0 errors)")
        return 0
    else:
        print(
            f"\nValidation failed with {error_count} error(s) and {warning_count} warning(s).",
            file=sys.stderr,
        )
        return 1


if __name__ == "__main__":
    sys.exit(main())
