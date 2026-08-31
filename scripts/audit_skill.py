#!/usr/bin/env python3
"""
audit_skill.py — Deep compliance audit of lvgl-pro-expert skill references
against the upstream lvgl_pro widget XML schemas.

Usage:
    python3 scripts/audit_skill.py

Exit codes: 0 = no FAILs, 1 = FAILs found
"""

import re
import sys
import xml.etree.ElementTree as ET
from pathlib import Path

SKILL_ROOT   = Path(__file__).parent.parent
UPSTREAM_XML = SKILL_ROOT / "tmp" / "lvgl_pro" / "lvgl_widgets_xml" / "v9.5.0"
WIDGET_CAT   = SKILL_ROOT / "references" / "format" / "widget-catalog.md"
REPORT_OUT   = SKILL_ROOT / "audit_report.md"
LVGL_VERSION = "v9.5.0"

# Props that matter most — missing from skill = real gap (WARN-CORE).
# Anything else missing = expected extended detail (INFO).
CORE_PROP_PATTERNS = re.compile(
    r"^(value|min_value|max_value|start_value|bind_value|bind_src|bind_text|"
    r"mode|type|orientation|options|selected|text|src|data|"
    r"start_angle|end_angle|bg_start_angle|bg_end_angle|rotation|"
    r"digit_count|decimal_point_position|range_min|range_max|step|"
    r"range_min_value|range_max_value|total_tick_count|major_tick_every|"
    r"label_show|angle_range|"
    r"today_year|today_month|today_day|shown_year|shown_month|"
    r"tab_bar_position|active|col_count|row_count|"
    r"anim_duration|arc_sweep|duration|repeat_count|"
    r"one_line|placeholder_text|password_mode|"
    r"color|brightness|points|"
    r"map|ctrl_map|one_checked|"
    r"update_mode|point_count|hor_div_line_count|ver_div_line_count|"
    r"overflow|max_lines|indent)$"
)

def parse_widget_xml(xml_path):
    try:
        tree = ET.parse(xml_path)
        root = tree.getroot()
    except ET.ParseError:
        return None

    widget_name = xml_path.stem
    props = {}
    enums = {}
    elements = []  # sub-elements

    api = root.find("api")
    if api is None:
        return {"name": widget_name, "props": props, "enums": enums, "elements": elements}

    for enumdef in api.findall("enumdef"):
        ename = enumdef.get("name", "")
        values = [e.get("name", "") for e in enumdef.findall("enum")]
        enums[ename] = values

    for prop in api.findall("prop"):
        pname = prop.get("name", "")
        ptype = prop.get("type", "")
        if not ptype:
            params = prop.findall("param")
            if params:
                ptype = params[0].get("type", "multi-param")
            # Also capture hyphenated param names (e.g. options-mode, bind_text-fmt)
            for param in params:
                param_name = param.get("name", "")
                if param_name and param_name != pname:
                    props[f"{pname}-{param_name}"] = param.get("type", "string")
        props[pname] = ptype

    for element in api.findall("element"):
        elements.append(element.get("name", ""))

    return {"name": widget_name, "props": props, "enums": enums, "elements": elements}


def parse_skill_catalog(md_path):
    """Extract widget names and prop tokens per widget section.

    Picks up tokens from:
      1. Backtick-quoted identifiers:  `bind_value`
      2. XML attribute names in code:  value="50"  bind_value="subj"
    """
    text = md_path.read_text(encoding="utf-8")
    catalog = {}
    backtick_pat = re.compile(r"`([\w][\w_\-]*)`")
    xml_attr_pat  = re.compile(r"\b([a-z][a-z0-9_\-]+)=[\"\']")
    current_widget = None

    for line in text.splitlines():
        heading_match = re.match(r"^#+", line)
        if heading_match:
            wm = re.search(r"(lv_\w+)", line)
            if wm:
                current_widget = wm.group(1)
                catalog.setdefault(current_widget, set())
                continue
        if current_widget:
            for m in backtick_pat.finditer(line):
                token = m.group(1)
                if "_" in token or "-" in token:
                    catalog[current_widget].add(token)
            for m in xml_attr_pat.finditer(line):
                token = m.group(1)
                if "_" in token or "-" in token:
                    catalog[current_widget].add(token)

    return catalog


def is_core_prop(pname):
    return bool(CORE_PROP_PATTERNS.match(pname))


def audit_widget(spec, skill_props):
    findings = []
    wname = spec["name"]

    for pname, ptype in spec["props"].items():
        in_skill = pname in skill_props or f"{pname}-anim" in skill_props

        if in_skill:
            findings.append(("PASS", wname, f"Prop `{pname}` ✓"))
        elif is_core_prop(pname):
            findings.append(("WARN-CORE", wname,
                f"Core prop `{pname}` ({ptype}) in upstream but MISSING from skill catalog"))
        else:
            findings.append(("INFO", wname,
                f"Extended prop `{pname}` ({ptype}) — expected, MCP pointer covers this"))

    # Sub-elements
    for ename in spec["elements"]:
        hyphen_name = f"{wname}-{ename}"
        if hyphen_name not in skill_props and ename not in skill_props:
            findings.append(("WARN-CORE", wname,
                f"Sub-element `<{hyphen_name}>` not documented in skill catalog"))
        else:
            findings.append(("PASS", wname, f"Sub-element `<{hyphen_name}>` ✓"))

    # Hallucination check — skill mentions something not in upstream
    # Build a broad set including sub-element props and known part names
    upstream_names = set(spec["props"].keys())
    upstream_names.update(v for vals in spec["enums"].values() for v in vals)
    upstream_names.update(spec["elements"])
    # Common part names and param suffixes are not hallucinations
    KNOWN_SAFE = {"textarea_placeholder", "scrollbar", "selected", "cursor", "indicator",
                  "knob", "items", "main", "anim", "animated", "fmt"}
    for sprop in skill_props:
        base = sprop.split("-")[0]
        if base.startswith("lv_") or base.startswith("style_") or base.startswith("bind_"):
            continue
        if base in KNOWN_SAFE or sprop in KNOWN_SAFE:
            continue
        if base and base not in upstream_names and sprop not in upstream_names:
            if re.match(r"^(mode|value|text|dir|sel|opt|min|max|start|type|src)$", base):
                findings.append(("FAIL", wname,
                    f"Skill mentions `{sprop}` but NOT in upstream XML — possible hallucination"))

    return findings


def write_report(all_findings, widgets_audited):
    passes     = [f for f in all_findings if f[0] == "PASS"]
    core_warns = [f for f in all_findings if f[0] == "WARN-CORE"]
    infos      = [f for f in all_findings if f[0] == "INFO"]
    fails      = [f for f in all_findings if f[0] == "FAIL"]

    lines = [
        "# LVGL Pro Expert — Skill Compliance Audit",
        "",
        f"**Upstream:** `lvgl_pro` {LVGL_VERSION} (shallow clone in `tmp/lvgl_pro`)",
        f"**Skill:** `references/format/widget-catalog.md`",
        f"**Widgets audited:** {len(widgets_audited)}",
        "",
        "## Summary",
        "",
        "| Level | Count | Meaning |",
        "|-------|-------|---------|",
        f"| ✅ PASS | {len(passes)} | In upstream and documented in skill |",
        f"| ❌ FAIL | {len(fails)} | In skill but NOT in upstream (hallucination) |",
        f"| ⚠️ WARN-CORE | {len(core_warns)} | Core prop in upstream, missing from skill |",
        f"| ℹ️ INFO | {len(infos)} | Extended prop — expected, MCP pointer covers |",
        "",
    ]

    if fails:
        lines += ["## ❌ Failures — Hallucinations / Wrong Attributes", ""]
        for _, w, msg in fails:
            lines.append(f"- **{w}**: {msg}")
        lines.append("")

    if core_warns:
        lines += ["## ⚠️ Core Warnings — Real Gaps to Fix", ""]
        by_widget = {}
        for _, w, msg in core_warns:
            by_widget.setdefault(w, []).append(msg)
        for widget, msgs in sorted(by_widget.items()):
            lines.append(f"### `{widget}`")
            for m in msgs:
                lines.append(f"- {m}")
            lines.append("")

    lines += ["## Per-Widget Status", ""]
    widget_status = {}
    for level, w, _ in all_findings:
        if w not in widget_status:
            widget_status[w] = "PASS"
        if level == "FAIL":
            widget_status[w] = "FAIL"
        elif level == "WARN-CORE" and widget_status[w] not in ("FAIL",):
            widget_status[w] = "WARN"

    for w in sorted(widgets_audited):
        status = widget_status.get(w, "PASS")
        icon = {"PASS": "✅", "WARN": "⚠️", "FAIL": "❌"}.get(status, "?")
        core_w = sum(1 for f in all_findings if f[0] == "WARN-CORE" and f[1] == w)
        info_c = sum(1 for f in all_findings if f[0] == "INFO" and f[1] == w)
        lines.append(f"- {icon} `{w}` — core gaps: {core_w}, extended (MCP): {info_c}")

    REPORT_OUT.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"\nReport written to: {REPORT_OUT}")


def main():
    if not UPSTREAM_XML.exists():
        print(f"ERROR: Upstream XML not found at {UPSTREAM_XML}")
        sys.exit(1)

    if not WIDGET_CAT.exists():
        print(f"ERROR: widget-catalog.md not found at {WIDGET_CAT}")
        sys.exit(1)

    print(f"Parsing skill catalog: {WIDGET_CAT}")
    skill_catalog = parse_skill_catalog(WIDGET_CAT)

    xml_files = sorted(UPSTREAM_XML.glob("lv_*.xml"))
    print(f"Found {len(xml_files)} upstream widget XML files\n")

    all_findings = []
    widgets_audited = []

    for xml_file in xml_files:
        spec = parse_widget_xml(xml_file)
        if spec is None:
            print(f"  SKIP  {xml_file.name}")
            continue

        skill_props = skill_catalog.get(spec["name"], set())
        findings = audit_widget(spec, skill_props)
        all_findings.extend(findings)
        widgets_audited.append(spec["name"])

        core_w = sum(1 for f in findings if f[0] == "WARN-CORE")
        fails  = sum(1 for f in findings if f[0] == "FAIL")
        status = "❌ FAIL" if fails else ("⚠️ WARN" if core_w else "✅ PASS")
        print(f"  {status:12s}  {spec['name']:28s}  core_gaps={core_w}  fails={fails}")

    write_report(all_findings, widgets_audited)

    total_fails = sum(1 for f in all_findings if f[0] == "FAIL")
    total_core  = sum(1 for f in all_findings if f[0] == "WARN-CORE")
    total_info  = sum(1 for f in all_findings if f[0] == "INFO")
    print(f"\nTotal: {len(widgets_audited)} widgets | {total_core} core gaps | {total_info} extended (MCP) | {total_fails} failures")
    sys.exit(1 if total_fails else 0)

if __name__ == "__main__":
    main()
