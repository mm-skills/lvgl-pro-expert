# Zephyr Board Targets Reference

LVGL Pro provides turnkey integration with Zephyr RTOS for 7 officially supported hardware development kits.

---

## Supported Boards Specification Table

| Board Identifier | SoC / Vendor | Display Resolution | Interface Bus | Display Controller / Touch |
|---|---|---|---|---|
| **EK-RA8D1** | Renesas RA8D1 (Arm Cortex-M85) | 480 × 854 | MIPI DSI (2-lane) | ILI9806E / GT911 |
| **EK-RA6M3** | Renesas RA6M3 (Arm Cortex-M4F) | 480 × 272 | GLCDC RGB Parallel | RTK7EKA6M3B / FT5x06 |
| **STM32U5G9J-DK2** | STMicroelectronics STM32U5G9 (Cortex-M33) | 800 × 480 | LTDC RGB Parallel | NeoChrom GPU / GT911 |
| **EK-RA8D2** | Renesas RA8D2 (Arm Cortex-M85) | 1024 × 600 | GLCDC RGB Parallel | High-res capacitive |
| **FRDM-MCXN947** | NXP MCX N947 (Dual Cortex-M33) | 480 × 320 | 8080 8-bit MIPI DBI | ST7796S / FT6336 |
| **MIMXRT1170-EVK** | NXP i.MX RT1170 (Cortex-M7 + M4) | 720 × 1280 | MIPI DSI (2-lane) | HX8394 / FT5406 |
| **M5Stack Core2** | Espressif ESP32-D0WDQ6-V3 (Xtensa) | 320 × 240 | SPI (4-wire) | ILI9342C / FT6336U |

---

## West Build Commands

Use Zephyr's `west` meta-tool to compile and flash LVGL Pro generated applications:

### 1. Renesas EK-RA8D1
```bash
west build -b renesas_ra8d1_ek -s app/ -- -DSHIELD=display_ili9806e
west flash
```

### 2. Renesas EK-RA6M3
```bash
west build -b renesas_ra6m3_ek -s app/
west flash
```

### 3. ST STM32U5G9J-DK2 Discovery Kit
```bash
west build -b stm32u5g9j_dk2 -s app/
west flash
```

### 4. Renesas EK-RA8D2
```bash
west build -b renesas_ra8d2_ek -s app/
west flash
```

### 5. NXP FRDM-MCXN947
```bash
west build -b frdm_mcxn947/mcxn947/cpu0 -s app/ -- -DSHIELD=frdm_st7796s
west flash
```

### 6. NXP MIMXRT1170-EVK
```bash
west build -b mimxrt1170_evk/mimxrt1176/cm7 -s app/ -- -DSHIELD=rk055hdmipi4m
west flash
```

### 7. M5Stack Core2 (ESP32)
```bash
west build -b m5stack_core2 -s app/
west flash
```

---

## `project.xml` Display Matching

Ensure your `project.xml` display resolution matches the target board's native panel:

```xml
<!-- Example: Renesas EK-RA8D1 Target Configuration -->
<project lvgl_version="9.5.0">
    <targets>
        <target name="ek_ra8d1">
            <display width="480" height="854" color_depth="16" color_format="RGB565" />
            <memory name="sram" size="1MB" />
            <memory name="ospi_flash" size="64MB" bandwidth="120MB/s" />
        </target>
    </targets>
</project>
```
