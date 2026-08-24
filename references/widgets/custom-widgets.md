# Custom Widgets with C Code

Custom widgets combine a declarative XML interface with hand-written C code. Use them when you need custom rendering, direct hardware access, or algorithms that pure XML composition cannot express.

---

## When to Use `<widget>` vs `<component>`

| Criteria | `<component>` (Pure XML) | `<widget>` (XML + C Code) |
|---|---|---|
| **Implementation** | Pure XML layout and styles | Hand-written C logic and draw callbacks |
| **C Code Required** | ❌ No C code needed | ✅ C constructor, parser, and logic files |
| **Use Cases** | Cards, buttons, toolbars, list rows | Custom canvas draw algorithms, physics engines, custom DSP graphs |
| **Portability** | Portable across all targets | Requires compiling C files into firmware |

> [!TIP]
> Always prefer `<component>` by default. Only create a `<widget>` when XML composition is insufficient.

---

## File Structure for a Custom Widget

Every custom widget lives in its own subdirectory under `widgets/<widget_name>/`:

```text
widgets/wd_meter/
├── wd_meter.xml              # Widget API, preview, and initial view definition
├── wd_meter.h                # Public C header and API function declarations
├── wd_meter.c                # C implementation (drawing, event handling, logic)
└── wd_meter_xml_parser.c     # XML parser bridge connecting XML attributes to C functions
```

---

## 1. Widget XML Definition (`widgets/wd_meter/wd_meter.xml`)

```xml
<widget>
    <previews>
        <preview width="240" height="240" style_bg_color="0x1e293b" />
    </previews>

    <api>
        <prop name="value" type="int" default="0" help="Current meter readout" />
        <prop name="max_val" type="int" default="100" help="Maximum scale limit" />
        <prop name="bind_value" type="subject" help="Subject to observe for value" />
        <!-- Custom child elements can be declared in <api> -->
        <element name="needle" access="add" type="lv_obj" help="Add needle pointer">
            <arg name="color" type="color" />
        </element>
    </api>

    <styles>
        <style name="style_meter_base" width="200" height="200" radius="100" bg_color="0x0f172a" />
    </styles>

    <view extends="lv_obj">
        <style name="style_meter_base" />
    </view>
</widget>
```

---

## 2. XML Parser Bridge (`wd_meter_xml_parser.c`)

The parser file implements three functions: creation, attribute application, and XML system registration.

```c
#include "wd_meter.h"
#include "lvgl/lvgl.h"
#include "lv_xml_private/lv_xml_private.h"

// 1. Create widget instance from XML state
void * wd_meter_xml_create(lv_xml_parser_state_t * state, const char ** attrs) {
    LV_UNUSED(attrs);
    lv_obj_t * parent = lv_xml_state_get_parent(state);
    return wd_meter_create(parent);
}

// 2. Parse XML attributes and forward to C functions
void wd_meter_xml_apply(lv_xml_parser_state_t * state, const char ** attrs) {
    void * item = lv_xml_state_get_item(state);
    lv_xml_obj_apply(state, attrs); // Apply standard base object attributes

    for (int i = 0; attrs[i]; i += 2) {
        const char * name = attrs[i];
        const char * value = attrs[i + 1];

        if (lv_streq("value", name)) {
            wd_meter_set_value(item, lv_xml_atoi(value));
        } else if (lv_streq("max_val", name)) {
            wd_meter_set_max(item, lv_xml_atoi(value));
        } else if (lv_streq("bind_value", name)) {
            lv_subject_t * subject = lv_xml_get_subject(&state->scope, value);
            if (subject) {
                wd_meter_bind_value(item, subject);
            }
        }
    }
}

// 3. Register widget tag with LVGL XML engine
void wd_meter_register(void) {
    lv_xml_register_widget("wd_meter", wd_meter_xml_create, wd_meter_xml_apply);
}
```

---

## 3. Using the Custom Widget in Screens

Once registered, instantiate the widget using its folder name as the XML tag:

```xml
<!-- ✅ Correct: Instantiating the custom widget in a screen -->
<view>
    <wd_meter name="temp_meter"
              align="center"
              value="42"
              max_val="120"
              bind_value="subject_engine_temp" />
</view>
```
