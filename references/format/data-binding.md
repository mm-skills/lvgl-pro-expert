# LVGL Pro XML: Data Binding

Covers the reactive subject system used to bind UI elements to backend variables without writing C code.

> [!NOTE]
> LVGL Pro completely removes SquareLine's event-driven update model in favor of a declarative Observer pattern using "Subjects".

## 1. Defining Subjects

Subjects are defined in `globals.xml`. They act as global state variables.

```xml
<subjects>
    <int name="battery_level" value="50" min_value="0" max_value="100" />
    <int name="is_charging" value="0" />
    <string name="user_name" value="Guest" />
</subjects>
```

## 2. Direct Property Binding (`bind_*`)

Bind a widget's property directly to a subject. When the subject changes, the widget updates automatically.

```xml
<!-- Label text updates dynamically -->
<lv_label text="Loading..." bind_text="user_name" />

<!-- Arc value updates dynamically -->
<lv_arc value="0" bind_value="battery_level" />

<!-- Formatted text binding (replaces %d / %s) -->
<lv_label bind_text="battery_level" bind_text-fmt="Battery: %d%%" />

<!-- Checkbox state binding -->
<lv_checkbox bind_checked="is_charging" />
```

## 3. Conditional Flags (`<bind_flag_if_eq>`)

Toggle LVGL flags (like `hidden`, `clickable`, `disabled`) based on subject values.

```xml
<lv_image src="img_charging_icon">
    <!-- Hide the charging icon if is_charging == 0 -->
    <bind_flag_if_eq subject="is_charging" ref_value="0" flag="hidden" />
</lv_image>
```
Variants: `<bind_flag_if_not_eq>`, `<bind_flag_if_gt>`, `<bind_flag_if_ge>`, `<bind_flag_if_lt>`, `<bind_flag_if_le>`.

## 4. Conditional States (`<bind_state_if_le>`)

Activate widget states based on subject values (e.g., triggering a warning state).

```xml
<lv_bar bind_value="battery_level">
    <!-- Activate "user_1" state if battery <= 20 -->
    <bind_state_if_le subject="battery_level" ref_value="20" state="user_1" />
    
    <!-- Style applied only when user_1 state is active -->
    <style name="red_indicator" selector="indicator|user_1" />
</lv_bar>
```
Variants: `<bind_state_if_eq>`, `<bind_state_if_not_eq>`, `<bind_state_if_gt>`, `<bind_state_if_ge>`, `<bind_state_if_lt>`.

## 5. Subject Interaction Events

UI interactions can declaratively modify subjects.

```xml
<lv_button>
    <lv_label text="Toggle Charge Mode" />
    <!-- Toggle the integer subject between 0 and 1 on click -->
    <subject_toggle_event trigger="clicked" subject="is_charging" />
</lv_button>

<lv_button>
    <lv_label text="Volume Up" />
    <!-- Increment subject by 5 -->
    <subject_increment_event trigger="clicked" subject="volume" step="5" min_value="0" max_value="100" />
</lv_button>

<lv_button>
    <lv_label text="Reset" />
    <!-- Set subject to absolute value -->
    <subject_set_int_event trigger="clicked" subject="volume" value="50" />
</lv_button>
```

## 6. C Callbacks (`<event_cb>`)

When declarative binding isn't enough, fire a custom C callback.

```xml
<lv_button>
    <event_cb trigger="clicked" callback="my_custom_c_function" user_data="optional_string" />
</lv_button>
```

### Common Trigger Events
- `clicked`: Short press and release
- `pressed`: Immediately on touch
- `released`: On touch release
- `value_changed`: When a slider, arc, or checkbox value changes
- `focused` / `defocused`: Focus state changes
