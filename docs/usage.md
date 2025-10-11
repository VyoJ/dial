# Dial Library Usage Guide

## Overview

The `dial` library provides two interfaces for creating analog clock faces:

1. **Human-friendly interface**: Simple preset-based clock creation
2. **Agent-friendly interface**: Full configuration control via dictionaries/JSON

## Human-Friendly Interface

Perfect for quick clock creation with sensible defaults.

### Basic Usage

```python
import dial

# Create a classic clock showing 3:15:30
clock = dial.Clock.create("3:15:30", "classic")
clock.save("my_clock.png")
```

### Available Preset Styles

- **`classic`**: Traditional black-on-white design
- **`modern`**: Dark theme with contemporary styling  
- **`minimal`**: Clean, simplified appearance

### Customization Options

```python
# Custom size and quality
clock = dial.Clock.create(
    time="6:30:00",
    style="modern", 
    width=600,
    height=600,
    scale_factor=3  # Higher quality
)
```

### Mixed Approach

Start with a preset, then add custom elements:

```python
# Start with preset
clock = dial.Clock.create("12:00:00", "classic")

# Add custom date window
from dial.elements.overlay import Overlay
date_window = Overlay(
    type="date_window",
    date="2025-01-08",
    position=(200, 300)
)
clock.add_element(date_window)
clock.save("custom_clock.png")
```

## Agent-Friendly Interface

Perfect for LLMs and complex, fully customized designs.

### Full Configuration

```python
import dial

config = {
    "width": 400,
    "height": 400,
    "elements": [
        {
            "type": "Face",
            "properties": {
                "shape": "circle",
                "color": "white",
                "border_color": "black",
                "border_width": 2
            }
        },
        {
            "type": "Hands", 
            "properties": {
                "time": "3:15:30",
                "hour_spec": {"shape": "line", "color": "black", "length": 0.5, "width": 6},
                "minute_spec": {"shape": "line", "color": "black", "length": 0.8, "width": 4}
            }
        }
    ]
}

clock = dial.Clock.from_config(config)
clock.save("agent_clock.png")
```

### Advanced Features

The agent interface supports:
- Gradients (linear and radial)
- Custom fonts and colors
- Roman numerals and custom symbols
- Date windows and overlays
- Precise positioning control

## When to Use Each Interface

### Use Human Interface When:
- You want quick results with good defaults
- You're prototyping or learning
- You need standard clock designs
- You want to start simple and customize later

### Use Agent Interface When:
- You need pixel-perfect control
- You're building complex, unique designs
- You're integrating with AI/LLM systems
- You need to programmatically generate many variations

## Hand Positioning Accuracy

The library automatically handles accurate hand positioning:
- At 3:15, the hour hand moves 1/4 of the way toward 4
- At 6:30, the hour hand points halfway between 6 and 7
- Second hand moves continuously (not in discrete steps)

## Quality Settings

Both interfaces support quality control:
- `antialias=True` (default): Smooth, high-quality output
- `scale_factor=2` (default): Balance of quality and performance
- `scale_factor=1`: Pixelated, retro aesthetic
- `scale_factor=4+`: Maximum quality for print use