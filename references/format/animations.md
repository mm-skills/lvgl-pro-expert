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


## Official Update
---
title: Animations
description: Guide to creating and controlling animations in LVGL Pro Editor using timeline-based animation system.
---

Create smooth, professional animations for your UI components using LVGL's timeline-based animation system, which allows you to define and control complex sequences with ease.

## Overview

XML animations are built on timeline animations that organize multiple animation steps into coordinated sequences.

Timelines are composed of simple animations. For example: *"change the `bg_opa` of `my_button_2` from 0 to 255 in 500 ms."*

Each Component can define its own timeline animations, which can then be played by the Component itself or by any parent Components.

## Defining Timelines

Timelines can be defined inside [`<screen>`](./screens)s and [`<component>`](./components)s. 

Example:

```xml
<component>
 <animations>
  <!-- Show Component and its children -->
  <timeline name="load">
   <animation prop="translate_x" target="self" start="-30" end="0" duration="500"/>
   <animation prop="opa" target="text" start="0" end="255" duration="500" delay="200"/>
   <include_timeline target="icon" timeline="show_up" delay="300"/>
  </timeline>

  <!-- Shake horizontally -->
  <timeline name="shake" repeat_count="infinite" repeat_delay="200">
   <animation prop="translate_x" target="self" start="0" end="-30" duration="150"/>
   <animation prop="translate_x" target="self" start="-30" end="30" duration="300" delay="150"/>
   <animation prop="translate_x" target="self" start="30" end="0" duration="150" delay="450"/>
  </timeline>
 </animations>

 <view>
  <lv_button width="200">
   <my_icon name="icon" src="image1"/>
   <lv_label name="text" text="Click me"/>
  </lv_button>
 </view>
</component>
```

### Timeline Properties

Inside `<animations>`, you can define `<timeline>`s with unique names that you can reference later. A `<timeline>` supports these properties:

- `name` - Unique name used to reference and play the timeline.
- `repeat_count` - How many times the whole timeline repeats. Use a number, or `infinite` to loop forever. Default is `1`.
- `repeat_delay` - Delay in milliseconds between repetitions. Default is `0`.

### Simple Animations 

Within each `timeline`, add individual `<animation>` elements to describe each step. The following properties are supported:

- `prop` - Style property to animate. All integer, percentage, and color style properties are supported.
- `selector` - Style selector, e.g. `knob|pressed`. Default: `main|default`.
- `target` - Name of the UI element to animate. `self` refers to the root element of the Component (the `view`).
- `start` - Start value (integer only).
- `end` - End value (integer only).
- `duration` - Duration of the animation in milliseconds.
- `delay` - Delay before starting in milliseconds. Default is 0.
- `early_apply` - If `true`, the start value is applied immediately, even during the delay. Default is `false`.


### Include External Timelines

The `include_timeline` element can be used in a `<timeline>` to reference animations from another timeline. For example, if `my_icon` defines a `"show_up"` timeline that fades in and enlarges the icon, you can include that timeline in other animations without duplicating the code.

To include a timeline, use the following properties:

- `target` - Name of the target UI element whose timeline should be included. `self` refers to the root element of the Component (the `view`).
- `timeline` - Name of the timeline to include. Must be defined in the `target`'s XML file.
- `delay` - Delay before starting in milliseconds. Default is 0.

## Playing Timelines

Timelines can be triggered by events (such as clicks) using the `<play_timeline_event>` element as a child of any widget.

Learn more about it in [Events](./events) section.

## Under the Hood

Understanding how timelines work internally helps you use them more effectively.

When an XML file is registered, the contents of the `animations` section are parsed, and the `timeline` data is stored as a "blueprint". The descriptors store target names as strings.

When a Component or Screen instance is created, `lv_anim_timeline`s are created and initialized from the saved blueprints. If `include_timeline`s are used, the requested timeline is included in the Component's timeline at this point. As all children are created at this point, the saved animation target names are resolved to pointers using `lv_obj_find_by_name`.

The created timeline instances and their names are saved in the Component's instance. Since each instance has its own timeline, you can have multiple Components (for example, 10 `list_item`s) and play their `load` timelines independently with different delays.

When a `play_timeline_event` is added to a UI element, the target and timeline names are saved as strings. Pointers cannot be used because the event can reference UI elements that will be created only later in the `view`.

Finally, when the play timeline event is triggered, the selected timeline is retrieved by its name from the target and started according to the other parameters (reverse, delay, and so on).