# Dial - Analog Clock Face Generator

A Python library for procedural and declarative generation of analog clock faces, designed to be both human-friendly and AI/LLM-friendly.

## Quick Start

### Human-Friendly Interface (Simple)

```python
import dial

# Create a classic clock in one line
clock = dial.Clock.create("3:15:30", "classic")
clock.save("my_clock.png")
```

### Agent-Friendly Interface (Full Control)

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

- **Dual Interface**: Simple presets for humans, full configuration for AI agents
- **High Quality**: Built-in antialiasing and supersampling
- **Compositional**: Layer-based architecture with customizable elements
- **Accurate**: Precise hand positioning with smooth movement
- **Flexible**: Support for gradients, custom fonts, multiple numeral systems

## Available Preset Styles

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

## Documentation

- [Complete Usage Guide](USAGE.md) - Detailed examples and API reference
- [Architecture Guide](AGENTS.md) - Design philosophy and LLM integration

## Requirements

- Python 3.8+
- Pillow (PIL)
- NumPy

## License

MIT License - see LICENSE file for details.