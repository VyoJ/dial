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
- **Complex Designs**: Multi-dial chronographs, 24-hour displays, date windows

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

## Example Gallery

The library can create a wide variety of clock designs:

- **Classic Designs**: Traditional analog clocks with Arabic or Roman numerals
- **Modern Styles**: Contemporary dark themes with selective numbering
- **Chronographs**: Multi-dial watches with sub-complications
- **Specialty Clocks**: 24-hour displays, gradient faces, date windows
- **Custom Elements**: Overlay text, custom hands, artistic gradients

See the `examples/` folder for sample outputs and the `docs/` folder for complete usage documentation.

## Documentation

- [Complete Usage Guide](docs/) - Detailed examples and API reference
- [Architecture Guide](AGENTS.md) - Design philosophy and LLM integration

## Requirements

- Python 3.12+
- Pillow (PIL)
- NumPy  
- Typer (for CLI)

## License

MIT License - see LICENSE file for details.