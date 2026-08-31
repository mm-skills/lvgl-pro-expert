# Official Examples

### round_button.xml
```xml
<!-- A small round button that increments a subject on press and long-press repeat. -->
<component>
	<api>
		<prop name="text" type="string" default="?" />
		<prop name="subject" type="subject" default="" />
		<prop name="step" type="int" default="1" />
	</api>

	<consts>
		<int name="size" value="36" />
	</consts>

	<view extends="lv_button" width="#size" height="#size" style_radius="#size" ext_click_area="8">
		<lv_label text="$text" align="center" />

		<subject_increment_event subject="$subject" step="$step" trigger="pressed" />
		<subject_increment_event subject="$subject" step="$step" trigger="long_pressed_repeat" />
	</view>
</component>

```

### sliderbox.xml
```xml
<!-- A title + and - buttons + a slider, all bound to one subject. Shows light/dark previews. -->
<component>
	<previews>
		<preview name="light" style_pad_all="20" />
		<preview name="dark" style_pad_all="20" style_bg_color="0x888">
			<set_subject name="subject_dark_mode" value="1" />
		</preview>
	</previews>

	<api>
		<prop name="title" type="string" default="Title" />
		<prop name="subject" type="subject" default="volume" />
		<prop name="unit" type="string" default="%d" />
	</api>

	<consts>
		<int name="width" value="200" help="Width of the whole slider box" />
	</consts>

	<styles>
		<style name="style_dark" bg_color="0x333" text_color="0xfff" border_color="0x111" />
	</styles>

	<view width="#width" height="content" flex_flow="row" style_flex_cross_place="center">
		<bind_style name="style_dark" subject="subject_dark_mode" ref_value="1" />

		<!-- Just show the title from the API property -->
		<lv_label text="$title" width="100%" style_text_align="center" />

		<!-- The round button just needs a subject and a text and it will increment
        that subject accordingly. Check out its implementation too.  -->
		<round_button text="-" flex_in_new_track="true" subject="$subject" step="-1" />

		<!-- Bind the label's text to the subject. As format string use the unit -->
		<lv_label flex_grow="1" bind_text="$subject" bind_text-fmt="$unit" style_text_align="center" />

		<!-- Same as the previous button, but with positive step. -->
		<round_button text="+" subject="$subject" step="1" />

		<!-- Bind the subject to the slider too -->
		<lv_slider bind_value="$subject" flex_in_new_track="true" width="100%" />
	</view>
</component>

```

### section.xml
```xml
<!-- A simple label like component that acts as an lv_label but has some custom styles
     For the sake of simplicity inline styles were used instead of a <style> tag -->
<component>
	<view
		extends="lv_label"
		style_width="100%"
		style_text_align="center"
		style_border_side="bottom"
		style_border_width="1"
		style_margin_top="12"
	/>
</component>

```

### globals.xml
```xml
<!-- Project-wide definitions: shared constants, styles, subjects, images and fonts.
     Anything defined here can be referenced from any screen or component. -->
<globals>
	<api>
		<!-- Add <enumdefs> here -->
	</api>

	<consts>
		<!-- Add <px>, <int>, <color> etc here -->
		<int name="unit_small" value="6" />
		<int name="unit_medium" value="12" />
		<int name="unit_large" value="24" />
		<color name="dark_blue" value="0x035391" />
		<color name="yellow" value="0xda9d19" />
	</consts>
	<subjects>
		<!-- Add <int>, <string>, or <float> subjects here -->
		<int name="subject_dark_mode" value="0" />
		<int name="subject_max_current" value="0" />
		<int name="subject_timeout" value="0" />
		<int name="subject_volume" value="0" />
		<int name="subject_segment" value="0" />
	</subjects>

	<images memory="int_flash">
		<!-- Add <file> or <data> tags here -->

		<data src_path="images/orange-flower.png" name="flower_data" color_format="argb8888" />
		<file src_path="images/orange-flower.png" name="flower_file" />
	</images>

	<fonts memory="int_flash">
		<!-- Add <bin> , <tiny_ttf>, <freetype> tags here -->

		<!-- <bin as_file="false"> means convert the font to C array -->
		<bin
			name="montserrat_14_c_array"
			as_file="false"
			bpp="2"
			src_path="fonts/Montserrat_Medium.ttf"
			size="14"
			range="0x20-0x7f"
			symbols="°äü"
		/>

		<!-- <bin as_file="true"> means to create bin file they can be loaded at runtime-->
		<bin
			name="montserrat_16_bin_file"
			as_file="false"
			bpp="2"
			src_path="fonts/Montserrat_Medium.ttf"
			size="16"
			range="0x20-0x7f"
			symbols="°"
		/>
		<!-- <tiny_ttf as_file="false" means convert the TTF files raw data to a C array and load it runtime with TinyTTF.
		     Characters will be rendered at runtime from the TTF file./> -->
		<tiny_ttf name="montserrat_18_tiny_ttf_data" as_file="false" size="18" src_path="fonts/Montserrat_Medium.ttf" />

		<!-- <tiny_ttf as_file="true" means load the TTF files at runtime with TinyTTF.
		     Characters will be rendered at runtime from the TTF file./> -->
		<tiny_ttf name="montserrat_20_tiny_ttf_file" as_file="true" size="20" src_path="fonts/Montserrat_Medium.ttf" />
	</fonts>

	<styles>
		<!-- Add <style> tags here -->
	</styles>

</globals>

```

### project.xml
```xml
<project name="tutorials" lvgl_version="9.5.0" theme="default">
	<targets>
		<target name="target1">
			<display width="480" height="320" />
			<memory name="int_ram" size="1MB" />
			<memory name="int_flash" size="2MB" bandwidth="100MB/s" />
		</target>
	</targets>
</project>

```

### hello_world.xml
```xml
404: Not Found
```

### data_bindings.xml
```xml
404: Not Found
```

### layout.xml
```xml
404: Not Found
```

### animations.xml
```xml
404: Not Found
```
