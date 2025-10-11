# AGENTS.md: A Guide to the `dial` Library Architecture

## 1. Introduction

`dial` is a Python library designed for the procedural and declarative generation of analog clock faces. Its primary goal is to provide a highly customizable and flexible interface that allows developers and Large Language Models (LLMs) to create a vast array of clock designs with ease.

This document outlines the core design, architecture, and feature set of the library. It is intended to be the primary reference for both human developers and AI agents seeking to understand and utilize `dial`.

## 2. Core Design Philosophy

The `dial` library is built on a **Compositional and Layer-Based Architecture**.

Instead of a single, monolithic `Clock` class with hundreds of parameters, a clock face is constructed by combining and layering independent, configurable **Elements**. Each element represents a distinct visual component of the clock (like the face, the hands, or the numerals).

This approach provides several key advantages:

- **Modularity:** Each component is self-contained and can be configured independently.
- **Extensibility:** New, custom elements can be easily created and integrated without modifying the core library.
- **Flexibility:** Elements can be combined in countless ways to achieve complex and unique designs.
- **Agent & LLM Friendliness:** This compositional model maps perfectly to declarative data structures like JSON or Python dictionaries, which are easy for LLMs to generate. An agent can create a clock by simply describing its constituent elements and their properties.

## 3. Key Concepts

- **Clock:** The main canvas object that holds, manages, and renders all the visual elements.
- **Element:** A drawable component of the clock. Every visual piece, from the background to the second hand, is an `Element`. Each element has a set of configurable properties.
- **`z_order`:** An integer property on every `Element` that determines its rendering order (stacking layer). Lower numbers are drawn first, appearing "behind" elements with higher numbers.
- **Configuration Dictionary:** A declarative Python `dict` (or JSON) that describes the entire clock face. This is the primary, agent-friendly interface for creating clocks without writing procedural Python code.

## 4. Library Architecture

The library is structured around a main `Clock` class and a collection of `Element` classes.

### 4.1. The Main `dial.Clock` Class

This class acts as the canvas and renderer.

**Initialization:**
`__init__(self, width: int, height: int)`

- Creates a blank image canvas of the specified size.

**Methods:**

- `add_element(self, element: Element)`: Adds a configured `Element` instance to the clock's rendering queue.
- `render(self) -> Image`: Renders all added elements onto the canvas in ascending order of their `z_order` and returns a Pillow `Image` object.
- `save(self, path: str)`: A convenience method that calls `render()` and saves the resulting image to the specified file path.
- `from_config(cls, config: dict)`: A class method that constructs a complete `Clock` object, including all its elements, from a single configuration dictionary. **This is the primary entry point for LLMs.**

### 4.2. Core Element Classes (`dial.elements`)

All elements inherit from a base `Element` class and have a `z_order` property and a `draw(...)` method.

#### **`Face`**

The background of the clock.

- `z_order = 0`
- **Properties:**
  - `shape` (str): The shape of the clock face. e.g., `'circle'`, `'square'`.
  - `color`: The fill color. Can be a color name (`'white'`), a hex code (`'#FFFFFF'`), or a gradient dictionary (e.g., `{'type': 'linear', 'colors': ['blue', 'red'], 'angle': 90}`).
  - `border_color` (str): Color of the face's border.
  - `border_width` (int): Width of the border in pixels.
  - `image_path` (str): Optional path to an image file to be used as the clock face background.

#### **`Ticks`**

The hour and minute markers around the edge of the clock.

- `z_order = 1`
- **Properties:**
  - `hour_spec` (dict): Configuration for the 12 hour ticks.
    - Keys: `shape` ('line', 'circle'), `color`, `length`, `width`.
  - `minute_spec` (dict): Configuration for the 60 minute ticks.
    - Keys: `shape`, `color`, `length`, `width`.
  - `visible_hours` (list[int]): A list of which hour ticks to draw. e.g., `[3, 6, 9, 12]`. Defaults to all 12.
  - `visible_minutes` (list[int]): A list of which minute ticks to draw.
  - `rotation` (float): An overall rotation in degrees for the entire set of ticks.

#### **`Numerals`**

The numbers or symbols representing the hours.

- `z_order = 2`
- **Properties:**
  - `system` (str): The numeral system to use. e.g., `'arabic'` (1, 2), `'roman'` (I, II), `'custom'`.
  - `custom_list` (list[str]): A list of 12 strings to use when `system` is `'custom'`. This allows for any symbol, including the mirrored numbers seen in the examples (`['SI', 'II', 'OI', ...]`).
  - `visible` (list[int]): A list of which numerals to draw. e.g., `[12, 3, 6, 9]`.
  - `font_path` (str): Path to a `.ttf` or `.otf` font file.
  - `font_size` (int): The font size in points.
  - `color` (str): The color of the text.
  - `orientation` (str): How numerals are oriented. `'upright'` (all text is vertical) or `'radial'` (text is rotated to match its position on the clock face).
  - `flip` (str): Flips the numeral text. e.g., `'none'`, `'horizontal'`, `'vertical'`.
  - `rotation` (float): An overall rotation in degrees for the entire set of numerals.

#### **`Hands`**

The hour, minute, and second hands of the clock.

- `z_order = 4`
- **Properties:**
  - `time` (str): The time to display, in `"HH:MM:SS"` format.
  - `hour_spec` (dict): Configuration for the hour hand.
    - Keys: `shape` ('line', 'triangle', 'custom_polygon'), `color`, `length` (as a fraction of radius), `width`.
    - `custom_polygon` (list[tuple]): A list of (x, y) points defining a custom hand shape.
  - `minute_spec` (dict): Same configuration as `hour_spec`.
  - `second_spec` (dict): Same configuration as `hour_spec`. Can be omitted for no second hand.
  - `pivot_spec` (dict): Configuration for the central pivot point.
    - Keys: `shape` ('circle'), `color`, `radius`.

#### **`Complication`**

Additional elements on the clock face, like a date window.

- `z_order = 3`
- **Properties:**
  - `type` (str): The type of complication. e.g., `'date_window'`.
  - `date` (str): The date to display, in `"YYYY-MM-DD"` format.
  - `position` (tuple[float, float]): The (x, y) center coordinate of the complication.
  - `font_path`, `font_size`, `text_color`.
  - `background_color`, `border_color`, `padding`.

## 5. Agent-Friendly Configuration (`from_config`)

The most powerful way to use `dial` is through the `Clock.from_config()` method. An LLM's primary task is to generate a dictionary that conforms to this structure.

The top-level dictionary contains the canvas dimensions and a list of element configurations.

**Example `config` dictionary:**

```python
rainbow_clock_config = {
    "width": 500,
    "height": 500,
    "elements": [
        {
            "type": "Face",
            "properties": {
                "shape": "circle",
                "color": {
                    "type": "linear_gradient",
                    "colors": ["#4f86f7", "#a04f77", "#ec6c4f"],
                    "angle": 45
                },
                "border_color": "#333333",
                "border_width": 8
            }
        },
        {
            "type": "Ticks",
            "properties": {
                "minute_spec": {"shape": "line", "color": "white", "length": 0.05, "width": 1}
            }
        },
        {
            "type": "Numerals",
            "properties": {
                "system": "arabic",
                "visible": [3, 6, 9, 12],
                "font_path": "path/to/your/bold_font.ttf",
                "font_size": 60,
                "color": "white"
            }
        },
        {
            "type": "Complication",
            "properties": {
                "type": "date_window",
                "date": "2025-12-08",
                "position": [250, 350],
                "font_path": "path/to/your/regular_font.ttf",
                "font_size": 20,
                "text_color": "#333333",
                "background_color": "white"
            }
        },
        {
            "type": "Hands",
            "properties": {
                "time": "10:10:37",
                "hour_spec": {"shape": "line", "color": "white", "length": 0.5, "width": 8},
                "minute_spec": {"shape": "line", "color": "white", "length": 0.8, "width": 8},
                "second_spec": {"shape": "line", "color": "#ec6c4f", "length": 0.9, "width": 3},
                "pivot_spec": {"shape": "circle", "color": "white", "radius": 10}
            }
        }
    ]
}

# Usage:
# my_clock = dial.Clock.from_config(rainbow_clock_config)
# my_clock.save("rainbow_clock.png")
```

## 6. Dependencies

- **Primary:** `Pillow` - Used for all core 2D drawing operations, including shapes, text, and image manipulation.
- **Optional:** `numpy` - Can be used internally for more efficient and readable geometric calculations (rotations, point-on-circle, etc.), but will not be exposed in the public API.

## 7. Future Directions

The compositional architecture allows for significant future expansion:

- **New Elements:** Add elements for `MoonPhase`, `WeatherIcon`, or `DigitalDisplay`.
- **Vector Output:** Add a new renderer backend that outputs SVG for resolution-independent graphics.
- **Animation:** Extend the `render` method to output a sequence of frames for creating animated GIFs of a running clock.
- **Advanced Gradients:** Implement radial and conical gradients for more complex face designs.

## 8. Code Instructions

Do not over-complicate or obfuscate code with additional features I have not asked for yet. Make the code as elegant and logical as possible without adding complexity.