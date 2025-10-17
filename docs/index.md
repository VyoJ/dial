# Dial - Documentation

Welcome to the Dial library documentation!

## Overview

Dial is a Python library for procedural and declarative generation of analog clock faces. It provides both a simple preset-based interface for quick clock creation and a powerful configuration-based interface for complex, custom designs.

## Documentation Sections

### [Usage Guide](usage.md)
Complete usage guide covering both human-friendly and agent-friendly interfaces, with examples of basic and advanced features.

### [API Reference](api.md)
Detailed API documentation for all classes, methods, and configuration options.

### [Architecture](architecture.md)
Design philosophy, compositional architecture, and guidance for LLM/AI agent integration.

### [Examples](examples.md)
Gallery of example configurations demonstrating various clock designs and features.

## Quick Start

### Simple Clock Creation

```python
import dial

# Create a classic clock in one line
clock = dial.Clock.create("3:15:30", "classic")
clock.save("my_clock.png")
```

### Complex Configuration

```python
import dial

config = {
    "width": 600,
    "height": 600,
    "elements": [
        {"type": "Face", "properties": {"shape": "circle", "color": "white"}},
        {"type": "Numerals", "properties": {"system": "roman"}},
        {"type": "Hands", "properties": {"time": "10:10:30"}}
    ]
}

clock = dial.Clock.from_config(config)
clock.save("custom_clock.png")
```

## Key Features

- **Dual Interface**: Simple presets and full configuration control
- **High Quality**: Built-in antialiasing and supersampling
- **Compositional**: Layer-based architecture with independent elements
- **Advanced Positioning**: Custom center/radius for sub-dials and chronographs
- **24-Hour Support**: Full 24-hour time display capabilities
- **Image Operations**: Post-processing transformations (flip, rotate)
- **Date Windows**: Overlay text and date displays
- **Gradients**: Radial and linear gradient backgrounds

## Available Styles

- `classic` - Traditional black-on-white design
- `modern` - Dark theme with contemporary styling
- `minimal` - Clean, simplified appearance

## Installation

```bash
# Using uv (recommended)
uv add dial

# Using pip
pip install dial
```

## Requirements

- Python 3.8+
- Pillow (PIL)
- NumPy

## License

MIT License - see LICENSE file for details.