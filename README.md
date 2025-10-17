# Dial - Analog Clock Face Generator

A Python library for procedural and declarative generation of analog clock faces, designed to be both human-friendly and AI/LLM-friendly.

## Quick Start

### Command Line Interface

```bash
# Install the library
uv add dial

# Create a simple clock
dial create "3:15:30" my_clock.png --style classic

# Generate example clocks
dial example examples/

# List available styles
dial styles

# Use JSON configuration
dial config config.json output.png
```

### Python Interface (Simple)

```python
import dial

# Create a classic clock in one line
clock = dial.Clock.create("3:15:30", "classic")
clock.save("my_clock.png")
```

### Python Interface (Full Control)

```python
import dial

config = {
    "width": 400,
    "height": 400,
    "elements": [
        {"type": "Face", "properties": {"shape": "circle", "color": "white"}},
        {"type": "Hands", "properties": {"time": "3:15:30"}}
    ]
}

clock = dial.Clock.from_config(config)
clock.save("custom_clock.png")
```

## Features

- **Command Line Tool**: Easy-to-use CLI with typer for quick clock generation
- **Dual Interface**: Simple presets for humans, full configuration for AI agents
- **High Quality**: Built-in antialiasing and supersampling
- **Compositional**: Layer-based architecture with customizable elements
- **Accurate**: Precise hand positioning with smooth movement
- **Flexible**: Support for gradients, custom fonts, multiple numeral systems
- **Complex Designs**: Multi-dial chronographs, 24-hour displays, date windows, sub-dials
- **Advanced Positioning**: Custom center/radius for any element, perfect for multi-dial layouts
- **Image Operations**: Post-processing support (flip, rotate, transpose)

## Available Preset Styles

- `classic` - Traditional black-on-white design with Arabic numerals
- `modern` - Dark theme with contemporary styling and selective numerals
- `minimal` - Clean, simplified appearance with corner numerals only

## Installation

```bash
# Using uv (recommended)
uv add dial

# Using pip
pip install dial
```

## CLI Commands

```bash
# Create a single clock
dial create "3:15:30" output.png --style classic --quality 4

# Generate all example clocks
dial example examples/

# List available preset styles
dial styles

# Create from JSON configuration
dial config config.json output.png
```

## Advanced Features

### Sub-Dials & Chronographs

Create complex multi-dial designs by positioning elements with custom `center` and `radius`:

```python
config = {
    "width": 600,
    "height": 600,
    "elements": [
        # Main clock
        {"type": "Face", "properties": {"shape": "circle", "color": "white"}},
        {"type": "Numerals", "properties": {"system": "arabic"}},
        {"type": "Hands", "properties": {"time": "10:10:30"}},
        
        # Sub-dial at custom position
        {"type": "Face", "properties": {
            "center": [200, 200],  # Custom position
            "radius": 60,           # Custom size
            "color": "#e6f3ff"
        }},
        {"type": "Hands", "properties": {
            "center": [200, 200],
            "radius": 60,
            "time": "3:00:00"
        }}
    ]
}
```

### 24-Hour Clocks

```python
{
    "type": "Numerals",
    "properties": {
        "values": [13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24],
        "system": "arabic"
    }
},
{
    "type": "Ticks",
    "properties": {
        "divisions": 24  # 24-hour divisions
    }
},
{
    "type": "Hands",
    "properties": {
        "time": "18:30:00",
        "mode": "24h"  # 24-hour mode
    }
}
```

### Date Windows & Overlays

```python
{
    "type": "Overlay",
    "properties": {
        "type": "date_window",
        "position": [300, 420],  # Custom position
        "date": "2025-10-18",
        "font_size": 20,
        "text_color": "darkred",
        "background_color": "white",
        "border_color": "darkred",
        "padding": 8
    }
}
```

### Gradient Backgrounds

```python
{
    "type": "Face",
    "properties": {
        "shape": "circle",
        "color": {
            "type": "radial",
            "colors": ["#FF69B4", "#9370DB", "#1E3A8A"],
            "center": [0.5, 0.5]
        }
    }
}
```

### Image Post-Processing

Apply transformations to the final rendered image:

```python
config = {
    "width": 500,
    "height": 500,
    "post_processing": {
        "flip_horizontal": True,  # Mirror the image
        "rotate": 45,             # Rotate degrees
        "transpose": False        # Diagonal flip
    },
    "elements": [...]
}
```

### Custom Numeral Positioning

```python
{
    "type": "Numerals",
    "properties": {
        "system": "arabic",
        "values": [5, 10, 15, 20, 25, 30, 35, 40, 45, 50, 55, 60],  # Custom values
        "radius_offset": -0.2,  # Move inward/outward
        "visible": [12, 3, 6, 9],  # Show only specific numerals
        "custom_map": {3: "III", 6: "VI"}  # Override specific numerals
    }
}
```

## Example Gallery

The library can create a wide variety of clock designs:

- **Classic Designs**: Traditional analog clocks with Arabic or Roman numerals
- **Modern Styles**: Contemporary dark themes with selective numbering
- **Chronographs**: Multi-dial watches with sub-complications
- **Specialty Clocks**: 24-hour displays, gradient faces, date windows
- **Custom Elements**: Positioned overlays, custom hands, artistic gradients
- **Complex Layouts**: Multiple independent sub-dials with custom positioning

See the `examples/` folder for sample outputs and complete working examples.

## Documentation

- [API Reference](docs/api.md) - Complete API documentation
- [Usage Guide](docs/usage.md) - Detailed usage examples
- [Architecture](docs/architecture.md) - Design philosophy and LLM integration
- [Examples](docs/examples.md) - Gallery of example configurations

## Requirements

- Python 3.12+
- Pillow (PIL)
- NumPy  
- Typer (for CLI)

## Technical Notes

### Scale-Aware Positioning

All custom positioning (center, radius, position) is automatically scaled during high-resolution rendering for antialiasing. User-specified coordinates always refer to the target canvas size, ensuring intuitive and predictable positioning.

### Element Layering

Elements are rendered in z-order:
- 0: Face (background)
- 1: Ticks
- 2: Numerals  
- 3: Overlays
- 4: Hands

## License

MIT License - see LICENSE file for details.