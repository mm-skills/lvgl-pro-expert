# Component System Reference

Components are reusable, parameterized UI blocks defined in pure XML. They require no C coding and can be nested, extended, and styled.

---

## 1. Component Anatomy & Structure

Every component lives in its own subdirectory: `components/<component_name>/<component_name>.xml`.

```xml
<component>
    <!-- 1. Editor visual preview configuration -->
    <previews>
        <preview name="light" width="200" height="80" />
        <preview name="dark" width="200" height="80" style_bg_color="0x1e293b" />
    </previews>

    <!-- 2. Parameter interface (props & slots) -->
    <api>
        <prop name="title" type="string" default="Card Title" help="Header text" />
        <prop name="accent_color" type="color" default="0x3b82f6" />
        <prop name="is_active" type="bool" default="true" />
        <slot name="content" help="Body content slot" />
    </api>

    <!-- 3. Local constants scoped to this component -->
    <consts>
        <int name="card_radius" value="12" />
    </consts>

    <!-- 4. Component-scoped styles -->
    <styles>
        <style name="style_card" radius="#card_radius" pad_all="16" bg_color="0xffffff" />
    </styles>

    <!-- 5. Root view tree (extends base widget or parent component) -->
    <view extends="lv_obj">
        <style name="style_card" />
        <lv_label text="$title" style_text_color="$accent_color" />
    </view>
</component>
```

---

## 2. Parameter Properties (`<prop>`)

Props define configurable parameters passed into the component upon instantiation.

### Supported Prop Types
| Type | Description | Example Default |
|---|---|---|
| `string` | Text string | `default="Submit"` |
| `int` | Integer value or px | `default="16"` |
| `bool` | Boolean flag | `default="false"` |
| `color` | Color hex or token | `default="0x2563eb"` or `default="#color_accent"` |
| `image` | Registered image asset name | `default="icon_arrow"` |
| `font` | Registered font asset name | `default="montserrat_14"` |
| `subject` / `subject_int` | Dynamic reactive subject binding | `default=""` |
| `enum:<type>` | Enum choice (e.g. `enum:lv_flex_flow`) | `default="row"` |

### Template Variable Syntax (`$prop_name`)
Inside the `<view>` tree, reference prop values using the `$` prefix:
```xml
<!-- ✅ Correct: Prop reference with $ prefix -->
<lv_label text="$title" style_text_color="$accent_color" />

<!-- ❌ Incorrect: Missing $ prefix or using # (reserved for constants) -->
<lv_label text="title" style_text_color="#accent_color" />
```

---

## 3. Slot System (`<slot>`)

Slots allow callers to inject arbitrary child widgets into specific regions inside the component.

### Declaration and Insertion Pattern
1. Declare the slot in the component's `<api>`: `<slot name="trailing" />`
2. Target a container inside the `<view>` with matching name: `<container name="trailing" />`
3. Callers inject content using the hyphenated tag `<component_name-slot_name>`:

```xml
<!-- Usage in a screen -->
<list_item title="Wi-Fi Network" subtitle="Connected">
    <list_item-trailing>
        <lv_switch name="wifi_sw" checked="true" />
    </list_item-trailing>
</list_item>
```

---

## 4. Component Inheritance (`extends="..."`)

Components can extend other components or base LVGL widgets. The official layout inheritance chain is:
`base_box` → `container` → `panel` / `row` / `column`.

```xml
<!-- panel extends container, inheriting flex layout and passing through props -->
<component>
    <api>
        <prop name="pad" type="int" default="#space_lg" />
        <prop name="gap" type="int" default="#space_md" />
    </api>
    <view extends="container" pad="$pad" gap="$gap">
        <style name="style_panel_bg" />
    </view>
</component>
```

---

## 5. Real-World Component Examples

### Example A: Button Component (`components/button/button.xml`)
```xml
<component>
    <previews><preview width="180" height="48" /></previews>
    <api>
        <prop name="text" type="string" default="Click Me" />
        <prop name="icon" type="image" default="" />
        <prop name="bg_color" type="color" default="#color_primary" />
    </api>
    <view extends="lv_button" style_bg_color="$bg_color" flex_flow="row" style_flex_cross_place="center" style_pad_gap="8">
        <lv_image src="$icon" hidden="{!icon}" />
        <lv_label text="$text" align="center" />
    </view>
</component>
```

### Example B: Card Panel Component (`components/panel/panel.xml`)
```xml
<component>
    <api>
        <prop name="pad" type="int" default="16" />
        <prop name="flow" type="enum:lv_flex_flow" default="column" />
    </api>
    <view extends="container" pad="$pad" flow="$flow">
        <style name="style_panel_light" />
        <bind_style name="style_panel_dark" subject="subject_dark_mode" ref_value="1" />
    </view>
</component>
```

### Example C: List Item Component with Slot (`components/list_item/list_item.xml`)
```xml
<component>
    <api>
        <prop name="title" type="string" default="Option" />
        <prop name="subtitle" type="string" default="" />
        <slot name="trailing" />
    </api>
    <view extends="container" flow="row" style_flex_cross_place="center" pad="12" gap="12">
        <container grow="1" flow="column" gap="4">
            <lv_label text="$title" style_text_font="font_bold" />
            <lv_label text="$subtitle" hidden="{!subtitle}" style_text_color="0x64748b" />
        </container>
        <container name="trailing" flow="row" gap="8" />
    </view>
</component>
```
