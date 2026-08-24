# Embedded UX & Layout Design Guidelines

Embedded touchscreens differ significantly from desktop and mobile web screens. Resource constraints, variable lighting, and finger touch accuracy require deliberate layout design.

---

## 1. Touch Target Sizing & Hit Areas

- **Minimum Touch Target**: 48 × 48 px (never smaller than 40 × 40 px on high-DPI screens).
- **Extended Click Area**: For compact icons, expand the touch perimeter without changing visual dimensions:
```xml
<!-- Extends touch bounding box by 10px on all sides -->
<lv_image name="btn_close" src="icon_close" ext_click_area="10" clickable="true" />
```

---

## 2. Spacing & Padding Tokens

Establish consistent 4px/8px-based spacing tokens in `<consts>` in `globals.xml`:

| Token Name | Value | Purpose |
|---|---|---|
| `space_xs` | 4 px | Micro spacing inside badges and tags |
| `space_sm` | 8 px | Gap between icon and label in buttons |
| `space_md` | 16 px | Standard padding inside cards and containers |
| `space_lg` | 24 px | Screen margins and inter-card section gaps |
| `space_xl` | 32 px | Major structural separation |

---

## 3. Responsive Flex Layout Patterns

Always prefer flex layout (`layout="flex"`) over absolute coordinates for maintainability.

### Pattern A: Centered Vertical Form Column
```xml
<view layout="flex" flex_flow="column" style_flex_main_place="center" style_flex_cross_place="center" style_pad_gap="16">
    <lv_label text="Welcome" />
    <lv_button width="200" height="48" />
</view>
```

### Pattern B: Horizontal Navigation Header / Top Bar
```xml
<lv_obj width="100%" height="48" layout="flex" flex_flow="row"
        style_flex_main_place="space_between" style_flex_cross_place="center" style_pad_hor="16">
    <lv_label text="Dashboard" />
    <lv_image src="icon_battery" />
</lv_obj>
```

### Pattern C: Multi-Card Responsive Grid Wrap
```xml
<lv_obj width="100%" layout="flex" flex_flow="row_wrap" style_pad_gap="12">
    <lv_obj width="48%" height="100" />
    <lv_obj width="48%" height="100" />
</lv_obj>
```

---

## 4. Circular & Round Display Considerations

When targeting circular smartwatch displays (e.g. 466 × 466 px with `radius="233"`):

1. **Avoid Corner Placement**: Top-left, top-right, bottom-left, and bottom-right corners are clipped off screen.
2. **Center-Focused Hierarchy**: Place critical text, readings, and focal controls strictly in the center 60% of the display.
3. **Radial Indicators**: Use `<lv_arc>` tracking the circumference rather than linear horizontal bars.
4. **Padding Margins**: Apply at least 24–32 px padding on top and bottom edges.

---

## 5. Typography Scales by Display Size

| Display Class | Resolution | Heading (h1/h2) | Body Text | Micro / Captions |
|---|---|---|---|---|
| **Small (Wearables/IoT)** | 240×240 – 320×240 | 18–22 px | 14 px | 10–12 px |
| **Medium (Handheld/HMI)** | 480×320 – 800×480 | 24–32 px | 16–18 px | 12–14 px |
| **Large (Automotive/Panel)** | 1024×600 – 1280×800 | 36–48 px | 20–24 px | 16–18 px |

---

## 6. Sunlight-Readable Color Contrast

For outdoor and industrial readability:

- **Minimum Contrast Ratio**: Maintain at least 4.5:1 (WCAG AA) between foreground text and backgrounds.
- **High-Contrast Dark Theme**: Dark slate `0x0f172a` with clean white text `0xf8fafc` and vivid emerald `0x10b981` or amber `0xf59e0b` accents.
- **Avoid Subtle Pastels**: Pale grays wash out completely under direct sunlight or poor viewing angles.
