# Examples

This page showcases various clock designs created with the dial library.

## Preset Styles

### Classic Style

A traditional black-on-white design with clear readability.

```python
import dial

clock = dial.Clock.create("3:15:30", "classic")
clock.save("classic_clock.png")
```

![Classic Clock](final_test_classic_31530.png)

### Modern Style

A dark theme with contemporary styling and selective numerals.

```python
import dial

clock = dial.Clock.create("6:30:45", "modern")
clock.save("modern_clock.png")
```

![Modern Clock](final_test_modern_63045.png)

### Minimal Style

A clean, simplified appearance with only essential elements.

```python
import dial

clock = dial.Clock.create("9:45:15", "minimal")
clock.save("minimal_clock.png")
```

![Minimal Clock](final_test_minimal_94515.png)

## Hand Positioning Accuracy

The library ensures accurate hand positioning at all times:

### 3:15 - Quarter Past

At 3:15, the hour hand moves 1/4 of the way between 3 and 4.

![Hand Position 3:15](hand_test_031500.png)

### 6:30 - Half Past

At 6:30, the hour hand points halfway between 6 and 7.

![Hand Position 6:30](hand_test_063000.png)

### 9:45 - Quarter To

At 9:45, the hour hand moves 3/4 of the way between 9 and 10.

![Hand Position 9:45](hand_test_094500.png)

## Quality Settings

### High Resolution

Using `scale_factor=4` for maximum quality:

```python
clock = dial.Clock.create("3:15:30", "classic", scale_factor=4)
```

![High Quality](final_test_hq.png)

### Retro Pixelated

Using `antialias=False` for a retro aesthetic:

```python
clock = dial.Clock.create("3:15:30", "classic", antialias=False)
```

![Retro Style](final_test_retro.png)

## Mixed Interface Approach

Starting with a preset and adding custom elements:

```python
import dial
from dial.elements.overlay import Overlay

# Start with preset
clock = dial.Clock.create("6:30:00", "modern")

# Add custom date window
date_window = Overlay(
    type="date_window",
    date="2025-01-08",
    position=(200, 300),
    font_size=14,
    text_color="#ecf0f1",
    background_color="#34495e"
)
clock.add_element(date_window)
clock.save("mixed_clock.png")
```

![Mixed Approach](final_test_mixed.png)

## Complex Agent Configuration

For advanced users and AI agents, here's a complex configuration example:

```python
import dial

config = {
    "width": 500,
    "height": 500,
    "antialias": True,
    "scale_factor": 3,
    "elements": [
        {
            "type": "Face",
            "properties": {
                "shape": "circle",
                "color": {
                    "type": "radial_gradient",
                    "colors": ["#87CEEB", "#4169E1", "#191970"],
                    "center": [0.5, 0.3]
                },
                "border_color": "#000080",
                "border_width": 5
            }
        },
        {
            "type": "Ticks",
            "properties": {
                "hour_spec": {"shape": "line", "color": "white", "length": 0.1, "width": 4},
                "minute_spec": {"shape": "line", "color": "#E0E0E0", "length": 0.05, "width": 2}
            }
        },
        {
            "type": "Numerals",
            "properties": {
                "system": "roman",
                "color": "white",
                "font_size": 36,
                "orientation": "upright"
            }
        },
        {
            "type": "Overlay",
            "properties": {
                "type": "date_window",
                "date": "2025-01-08",
                "position": [250, 350],
                "font_size": 18,
                "text_color": "#000080",
                "background_color": "white",
                "border_color": "#000080",
                "padding": 8
            }
        },
        {
            "type": "Hands",
            "properties": {
                "time": "3:15:30",
                "hour_spec": {"shape": "line", "color": "white", "length": 0.5, "width": 8},
                "minute_spec": {"shape": "line", "color": "white", "length": 0.8, "width": 6},
                "second_spec": {"shape": "line", "color": "#FFD700", "length": 0.9, "width": 3},
                "pivot_spec": {"shape": "circle", "color": "white", "radius": 12}
            }
        }
    ]
}

clock = dial.Clock.from_config(config)
clock.save("complex_clock.png")
```

![Complex Configuration](agent_complex.png)