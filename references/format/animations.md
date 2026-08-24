# LVGL Pro XML: Animations & Screen Transitions

Covers animation timelines, triggering animations, and screen navigation events.

## 1. Screen Navigation

LVGL Pro uses two events for navigation depending on the screen lifecycle:
- **Dynamic Screens:** `<screen_create_event>` — The target screen is created on entry and destroyed on exit to save memory.
- **Permanent Screens:** `<screen_load_event>` — The target screen is preserved in memory. The screen tag must have `permanent="true"`.

```xml
<!-- Button that navigates to a new dynamic screen -->
<lv_button>
    <lv_label text="Open Settings" />
    <screen_create_event 
        screen="screen_settings" 
        trigger="clicked"
        anim_type="move_left" 
        duration="300" 
    />
</lv_button>
```

### Animation Types
| `anim_type` | Description |
|-------------|-------------|
| `none` | Instant switch |
| `move_left`, `move_right` | Slide in horizontally |
| `move_top`, `move_bottom` | Slide in vertically |
| `fade_on` | Fade in new screen over old |

## 2. Animation Timelines

Animations in LVGL Pro are defined using `<animations>` and `<timeline>`. They animate specific properties of targeted widgets over time.

```xml
<animations>
    <!-- Define a timeline that groups multiple animations -->
    <timeline name="bounce_anim">
        <!-- Target widget by name, property to animate, values, and duration -->
        <animation 
            target="my_logo" 
            prop="y" 
            start="0" 
            end="-50" 
            duration="500" 
            early_apply="true" 
        />
        <animation 
            target="my_logo" 
            prop="y" 
            start="-50" 
            end="0" 
            duration="500" 
            delay="500" 
        />
    </timeline>
</animations>
```

### Attributes
- `target`: The `name` attribute of the widget to animate.
- `prop`: Property to animate (`x`, `y`, `width`, `height`, `opa`, `transform_scale`, `transform_rotation`, etc.).
- `start` / `end`: Starting and ending values.
- `duration`: Length of animation in ms.
- `delay`: Offset from timeline start in ms.
- `early_apply`: If true, applies the `start` value immediately when the timeline begins, even before the `delay` has finished.

## 3. Triggering Timelines

Timelines are triggered using the `<play_timeline_event>` tag attached to a widget.

```xml
<lv_button>
    <lv_label text="Play Animation" />
    <play_timeline_event 
        trigger="clicked" 
        timeline="bounce_anim" 
        target="self" 
        reverse="false" 
    />
</lv_button>
```

Alternatively, timelines can be embedded directly using `<include_timeline>` inside a timeline to compose complex sequences.
