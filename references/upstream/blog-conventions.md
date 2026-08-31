# LVGL Pro Conventions and Best Practices

**Source Attribution:**
- *LVGL Pro Project Structure and Naming Guide* by Felix Biego (March 2026) - https://lvgl.io/blog/lvgl-pro-project-structure-guide
- *Building a Custom Widget with Scroll Effects in LVGL Pro* by Felix Biego (April 2026) - https://lvgl.io/blog/tutorial-lvgl-pro-custom-widgets

---

## 1. Naming Conventions

Consistency is key when a project grows to dozens of screens and hundreds of assets.

*   **Images:** Always use descriptive prefixes like `icon_home` or `img_background`.
*   **Fonts:** Use the format `font_size_weight` (e.g., `font_16_bold`).
*   **Project Name:** NEVER name the project `lvgl` due to namespace conflicts with the LVGL library itself.
*   **Styles:** Use the `style_` prefix. For multi-theme apps, include the theme name: `style_dark_button` or `style_light_button`.
*   **Subjects:** Use the `subject_` prefix (e.g., `subject_settings`).
*   **Custom Widgets:** Use the `wd_` prefix to distinguish widgets from standard components (e.g., `wd_menu`, `wd_statusbar`, `wd_clock`).

## 2. Resource Management

Mixing raw source files with generated code leads to accidental deletions.

*   **Raw Assets:** Keep raw `.png` source files in an `images/raw/` subfolder.
*   **Generated Assets:** Generated `.c` files go in the `images/` root.
*   **Icons:** Always include the size suffix in icon filenames (e.g., `icon_home_20dp.png`).

## 3. Architecture Rules

*   Use the "Add New Component / Widget / Screen" workflow. It automatically organizes files into subfolders, keeping the tree navigable.
*   **THE GOLDEN RULE:** NEVER edit generated C files. Any manual changes made to generated C files will be overwritten and lost the next time you hit "Export Code" in the editor.
    *   *Need a UI change?* Modify the source XML.
    *   *Need custom behavior?* Use the API, external logic hooks, or custom widgets.

## 4. XML Best Practices

### Avoid Inline Styles
Inline styles make XML bloated and hard to update. Define reusable named styles instead.

**DON'T: Inline Styles**
```xml
<lv_obj style_bg_color="0x000000" style_bg_opa="255" />
```

**DO: Named Styles**
```xml
<styles>
   <style name="style_main_bg" bg_color="0x000000" bg_opa="255" />
</styles>
<lv_obj>
   <style name="style_main_bg" />
</lv_obj>
```

### Component Sizing
Prefer using `width="content"` / `height="content"` or `100%` instead of hardcoded pixel values when possible.

## 5. Component API & State Safety

API properties (`$api_prop`) CANNOT be used directly inside `<style>` definitions. Styles are initialized once before properties bind.

*   **DO:** Use API properties on the `<view>` directly or via `{ }` expressions.

```xml
<api name="text" type="string" help="Sets the label text of the header" />
```

## 6. Custom Widget Workflow

### Terminology
*   **Built-in widgets:** `lv_arc`, `lv_button`, `lv_label` (No C required).
*   **Components (`<component>`):** Pure XML, no C, layout/styling only.
*   **Widgets (`<widget>`):** XML definition + C implementation. Use only when behavior cannot be expressed in XML alone.

### The Pattern
1.  **Define XML:** Name widgets with `wd_` prefix (e.g. `wd_list`). Start with `<widget>` root in XML, define `<api>` props for C access.
2.  **Export Code:** Export from the editor to get generated C stubs.
3.  **Implement Logic:** Add custom scroll or layout logic in C, attach via event callbacks (e.g. `LV_EVENT_SCROLL`).
4.  **Parse Props:** Implement `_xml_parser` in C to read `<api>` props defined in the XML.

### Example: Custom Scroll List Widget XML

```xml
<!-- button.xml (Supporting Component) -->
<component>
	<previews>
		<preview width="320" height="240" style_bg_color="0xeee" />
	</previews>
	<api>
		<prop name="label" type="string" default="Label 1" />
	</api>
	<styles>
		<style name="style_base" width="100%" pad_ver="20" radius="40" />
	</styles>
	<view extends="lv_button">
		<style name="style_base" />
		<lv_label text="$label" align="center" />
	</view>
</component>
```

```xml
<!-- wd_list.xml (Widget Definition) -->
<widget>
	<previews>
		<preview width="320" height="240" style_bg_color="0xeee" />
	</previews>
	<api>
		<prop name="translate_scroll" type="bool" default="false" />
	</api>
	<styles>
		<style
			name="style_base"
			width="100%"
			height="100%"
			pad_all="10"
			pad_row="10"
			layout="flex"
			flex_flow="column"
		/>
	</styles>
	<view extends="lv_obj" scrollbar_mode="off">
		<style name="style_base" />
	</view>
</widget>
```

### Example: Widget C Implementation Snippets

**Event Callback:**
```c
static void scroll_event_cb(lv_event_t * e)
{
    lv_obj_t * cont = lv_event_get_target_obj(e);
    wd_list_t * widget = (wd_list_t *)lv_event_get_user_data(e);
 
    lv_area_t cont_a;
    lv_obj_get_coords(cont, &cont_a);
    int32_t cont_y_center = cont_a.y1 + lv_area_get_height(&cont_a) / 2;
 
    int32_t r = lv_obj_get_height(cont) * 7 / 10;
    int32_t child_cnt = (int32_t)lv_obj_get_child_count(cont);
 
    for(int32_t i = 0; i < child_cnt; i++) {
        lv_obj_t * child = lv_obj_get_child(cont, i);
 
        lv_area_t child_a;
        lv_obj_get_coords(child, &child_a);
 
        int32_t child_y_center = child_a.y1 + lv_area_get_height(&child_a) / 2;
        int32_t diff_y = LV_ABS(child_y_center - cont_y_center);
 
        int32_t x;
        if(diff_y >= r) {
            x = r;
        } else {
            uint32_t x_sqr = r * r - diff_y * diff_y;
            lv_sqrt_res_t res;
            lv_sqrt(x_sqr, &res, 0x8000);
            x = r - res.i;
        }
 
        // Apply effect if enabled via XML api property
        lv_obj_set_style_translate_x(child, widget->translate_scroll ? x : 0, 0);
    }
}
```

**Constructor Hook:**
```c
void wd_list_constructor_hook(lv_obj_t *obj)
{
    wd_list_t * widget = (wd_list_t *)obj;
    lv_obj_add_event_cb(obj, scroll_event_cb, LV_EVENT_SCROLL, widget);
    lv_obj_add_event_cb(obj, scroll_event_cb, LV_EVENT_CHILD_CHANGED, widget);
    lv_obj_set_scroll_dir(obj, LV_DIR_VER);
}
```

**XML Parser and API Updater:**
```c
void wd_list_xml_apply(lv_xml_parser_state_t * state, const char ** attrs)
{
    void * item = lv_xml_state_get_item(state);
 
    lv_xml_obj_apply(state, attrs);
 
    for(int i = 0; attrs[i]; i += 2) {
        const char * name = attrs[i];
        const char * value = attrs[i + 1];
            if(lv_streq("translate_scroll", name)) {
                wd_list_set_translate_scroll(item, lv_xml_to_bool(value));
            }
    }
}

void wd_list_set_translate_scroll(lv_obj_t * wd_list, bool translate_scroll)
{
    wd_list_t * widget = (wd_list_t *)wd_list;
    widget->translate_scroll = translate_scroll;
    lv_obj_send_event(wd_list, LV_EVENT_SCROLL, widget);
}
```
