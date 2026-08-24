# LVGL Pro XML: Styles & Parts

Covers how to apply styles, use part/state selectors, define class-based vs inline styles, and the flex/grid layout system.

> [!NOTE]
> LVGL styles behave similarly to CSS. You can define reusable classes in `<styles>` blocks or apply them inline using the `style_` prefix.

## 1. Named Styles (Classes)

Defined in `globals.xml` or locally inside a `<screen>`.

```xml
<styles>
    <!-- Reusable style definitions -->
    <style name="card_bg" bg_color="0x2A2A2A" radius="8" pad_all="12" />
    <style name="text_white" text_color="0xFFFFFF" text_font="font_primary" />
</styles>
```

Applying named styles to a widget using the `<style>` child tag:
```xml
<lv_obj>
    <style name="card_bg" />
</lv_obj>
```

## 2. Inline Styles (`style_` prefix)

You can apply properties directly on the widget tag using the `style_` prefix. This is equivalent to an inline `style="..."` attribute in HTML.

```xml
<lv_label text="Warning" style_text_color="0xFF0000" style_pad_top="5" />
```

## 3. Part and State Selectors

Widgets are composed of **parts** (e.g., `main`, `indicator`, `knob`). They can also be in different **states** (e.g., `checked`, `pressed`, `disabled`, `focused`).

### Selector Syntax on Named Styles
Use the `selector` attribute on the `<style>` child tag, combining part and state with `|`.

```xml
<lv_slider value="50">
    <style name="slider_bg" selector="main" />
    <style name="slider_indic" selector="indicator|disabled" />
</lv_slider>
```

### Inline Part+State Selectors (Hyphenated)
For inline styles, append `-<part>-<state>` to the property name.

```xml
<!-- Sets the indicator background color when checked -->
<lv_checkbox style_bg_color-indicator-checked="0x00FF00" />

<!-- Sets the arc knob color in the default state -->
<lv_arc style_bg_color-knob="0xFF0000" />
```

## 4. Conditional Styles (`<bind_style>`)

Applies a style class only when a data subject matches a specific value (ideal for Light/Dark themes).

```xml
<lv_obj>
    <!-- Default style always applied -->
    <style name="panel_light" />
    
    <!-- Applies panel_dark only if subject_theme_dark == 1 -->
    <bind_style name="panel_dark" subject="subject_theme_dark" ref_value="1" />
</lv_obj>
```

## 5. Flexbox Layout System

Flexbox can be enabled via styles.

```xml
<style 
    name="row_layout"
    layout="flex"
    flex_flow="row"
    flex_main_place="space_between"
    flex_cross_place="center"
    pad_gap="10"
/>
```

| Property | Values |
|----------|--------|
| `flex_flow` | `row`, `column`, `row_wrap`, `column_wrap`, `row_reverse`, `column_reverse` |
| `flex_main_place` | `start`, `center`, `end`, `space_evenly`, `space_around`, `space_between` |
| `flex_cross_place` | `start`, `center`, `end` |
| `flex_grow` | (On child elements) Int ratio of remaining space to consume |

## 6. Common Style Properties

| Category | Properties |
|----------|------------|
| Background | `bg_color`, `bg_opa`, `bg_grad_color`, `bg_grad_dir` |
| Border | `border_color`, `border_width`, `border_side`, `border_opa` |
| Padding | `pad_all`, `pad_top`, `pad_bottom`, `pad_left`, `pad_right`, `pad_row`, `pad_column`, `pad_gap` |
| Text | `text_color`, `text_font`, `text_align`, `text_letter_space`, `text_line_space` |
| Shadow | `shadow_color`, `shadow_width`, `shadow_offset_x`, `shadow_offset_y` |
| Transform | `transform_scale`, `transform_rotation` (0.1° units), `translate_x`, `translate_y` |
