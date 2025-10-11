"""Main Clock class for creating and rendering clock faces."""

from typing import Any, Dict, List

from PIL import Image, ImageDraw

from dial.element import Element
from dial.utils import create_gradient_image, parse_color


class Clock:
    """Main clock canvas that manages and renders elements.

    The Clock class acts as a canvas for composing multiple elements
    to create a complete clock face. Elements are rendered in order
    of their z_order property.
    """

    # Preset styles for human-friendly interface
    PRESET_STYLES = {
        "classic": {
            "face": {
                "shape": "circle",
                "color": "white",
                "border_color": "black",
                "border_width": 3,
            },
            "ticks": {
                "hour_spec": {
                    "shape": "line",
                    "color": "black",
                    "length": 0.08,
                    "width": 3,
                },
                "minute_spec": {
                    "shape": "line",
                    "color": "black",
                    "length": 0.04,
                    "width": 1,
                },
            },
            "numerals": {"system": "arabic", "color": "black", "font_size": 28},
            "hands": {
                "hour_spec": {
                    "shape": "line",
                    "color": "black",
                    "length": 0.5,
                    "width": 6,
                },
                "minute_spec": {
                    "shape": "line",
                    "color": "black",
                    "length": 0.8,
                    "width": 4,
                },
                "second_spec": {
                    "shape": "line",
                    "color": "red",
                    "length": 0.9,
                    "width": 2,
                },
                "pivot_spec": {"shape": "circle", "color": "black", "radius": 5},
            },
        },
        "modern": {
            "face": {
                "shape": "circle",
                "color": "#2c3e50",
                "border_color": "#34495e",
                "border_width": 2,
            },
            "ticks": {
                "hour_spec": {
                    "shape": "line",
                    "color": "#ecf0f1",
                    "length": 0.06,
                    "width": 4,
                },
                "minute_spec": {
                    "shape": "line",
                    "color": "#bdc3c7",
                    "length": 0.03,
                    "width": 1,
                },
            },
            "numerals": {
                "system": "arabic",
                "visible": [12, 3, 6, 9],
                "color": "#ecf0f1",
                "font_size": 32,
            },
            "hands": {
                "hour_spec": {
                    "shape": "line",
                    "color": "#ecf0f1",
                    "length": 0.45,
                    "width": 8,
                },
                "minute_spec": {
                    "shape": "line",
                    "color": "#ecf0f1",
                    "length": 0.75,
                    "width": 6,
                },
                "second_spec": {
                    "shape": "line",
                    "color": "#e74c3c",
                    "length": 0.85,
                    "width": 2,
                },
                "pivot_spec": {"shape": "circle", "color": "#ecf0f1", "radius": 8},
            },
        },
        "minimal": {
            "face": {
                "shape": "circle",
                "color": "white",
                "border_color": "#bdc3c7",
                "border_width": 1,
            },
            "ticks": {
                "hour_spec": {
                    "shape": "line",
                    "color": "#34495e",
                    "length": 0.05,
                    "width": 2,
                }
            },
            "numerals": {
                "system": "arabic",
                "visible": [12, 3, 6, 9],
                "color": "#34495e",
                "font_size": 24,
            },
            "hands": {
                "hour_spec": {
                    "shape": "line",
                    "color": "#34495e",
                    "length": 0.4,
                    "width": 4,
                },
                "minute_spec": {
                    "shape": "line",
                    "color": "#34495e",
                    "length": 0.7,
                    "width": 3,
                },
                "pivot_spec": {"shape": "circle", "color": "#34495e", "radius": 4},
            },
        },
    }

    def __init__(
        self,
        width: int = 400,
        height: int = 400,
        background_color: str = "white",
        antialias: bool = True,
        scale_factor: int = 2,
    ) -> None:
        """Initialize a new clock canvas.

        Args:
            width: Canvas width in pixels.
            height: Canvas height in pixels.
            background_color: Background color for the canvas.
            antialias: Whether to use antialiasing for better image quality.
            scale_factor: Supersampling scale factor for antialiasing (higher = better quality).

        Raises:
            ValueError: If width or height are not positive integers.
        """
        if not isinstance(width, int) or width <= 0:
            raise ValueError("Width must be a positive integer")
        if not isinstance(height, int) or height <= 0:
            raise ValueError("Height must be a positive integer")
        if not isinstance(scale_factor, int) or scale_factor < 1:
            raise ValueError("Scale factor must be a positive integer")

        self.width = width
        self.height = height
        self.background_color = parse_color(background_color)
        self.elements: List[Element] = []
        self.antialias = antialias
        self.scale_factor = scale_factor if antialias else 1

        # Calculate clock center and radius (using actual output dimensions)
        self.center = (width / 2, height / 2)
        self.radius = min(width, height) / 2 * 0.9  # Leave some margin

    @classmethod
    def create(
        cls,
        time: str,
        style: str = "classic",
        width: int = 400,
        height: int = 400,
        antialias: bool = True,
        scale_factor: int = 2,
    ) -> "Clock":
        """Create a complete clock with preset styling (human-friendly interface).

        Args:
            time: Time to display in "HH:MM:SS" format.
            style: Preset style name ('classic', 'modern', 'minimal').
            width: Canvas width in pixels.
            height: Canvas height in pixels.
            antialias: Whether to use antialiasing.
            scale_factor: Supersampling scale factor for antialiasing.

        Returns:
            A Clock instance with all elements configured.

        Raises:
            ValueError: If style is not recognized.
        """
        if style not in cls.PRESET_STYLES:
            available_styles = ", ".join(cls.PRESET_STYLES.keys())
            raise ValueError(
                f"Style '{style}' not recognized. Available styles: {available_styles}"
            )

        # Create clock instance
        clock = cls(
            width=width, height=height, antialias=antialias, scale_factor=scale_factor
        )

        # Get preset configuration
        preset = cls.PRESET_STYLES[style]

        # Import element classes here to avoid circular imports
        from dial.elements.face import Face
        from dial.elements.hands import Hands
        from dial.elements.numerals import Numerals
        from dial.elements.ticks import Ticks

        # Add elements based on preset
        if "face" in preset:
            face = Face(**preset["face"])
            clock.add_element(face)

        if "ticks" in preset:
            ticks = Ticks(**preset["ticks"])
            clock.add_element(ticks)

        if "numerals" in preset:
            numerals = Numerals(**preset["numerals"])
            clock.add_element(numerals)

        if "hands" in preset:
            hands = Hands(time=time, **preset["hands"])
            clock.add_element(hands)

        return clock

    def add_element(self, element: Element) -> None:
        """Add an element to the clock.

        Args:
            element: The element to add.

        Raises:
            TypeError: If element is not an Element instance.
        """
        if not isinstance(element, Element):
            raise TypeError("element must be an instance of Element")

        self.elements.append(element)

    def clear_elements(self) -> None:
        """Remove all elements from the clock."""
        self.elements.clear()

    def render(self, format: str = "RGBA") -> Image.Image:
        """Render the clock face with all elements.

        Args:
            format: Image format ('RGBA', 'RGB', etc.).

        Returns:
            Rendered PIL Image.

        Raises:
            ValueError: If format is not supported.
        """
        valid_formats = ["RGBA", "RGB", "L", "1"]
        if format not in valid_formats:
            raise ValueError(f"Format must be one of {valid_formats}")

        # Calculate rendering dimensions (use supersampling for antialiasing)
        render_width = self.width * self.scale_factor
        render_height = self.height * self.scale_factor
        render_center = (render_width / 2, render_height / 2)
        render_radius = self.radius * self.scale_factor

        # Create base image at higher resolution
        if isinstance(self.background_color, dict):
            # Gradient background
            image = create_gradient_image(
                (render_width, render_height), self.background_color
            )
        else:
            # Solid color background
            image = Image.new(
                "RGBA", (render_width, render_height), self.background_color
            )

        # Create drawing context
        draw = ImageDraw.Draw(image)

        # Sort elements by z_order and render
        sorted_elements = sorted(self.elements, key=lambda e: e.z_order)

        for element in sorted_elements:
            try:
                element.draw(image, draw, render_center, render_radius)
            except Exception as e:
                # Continue rendering other elements if one fails
                print(
                    f"Warning: Failed to render element {type(element).__name__}: {e}"
                )

        # Downsample for antialiasing (if scale_factor > 1)
        if self.scale_factor > 1:
            image = image.resize((self.width, self.height), Image.Resampling.LANCZOS)

        # Convert to requested format
        if format != "RGBA":
            image = image.convert(format)

        return image

    def save(self, path: str, format: str = None, **kwargs: Any) -> None:
        """Render and save the clock face to a file.

        Args:
            path: Output file path.
            format: Image format (auto-detected from path if None).
            **kwargs: Additional arguments passed to PIL Image.save().
        """
        image = self.render()

        # Convert path to string if it's a Path object
        path_str = str(path)

        # Auto-detect format from file extension if not specified
        if format is None:
            path_lower = path_str.lower()
            if path_lower.endswith(".png"):
                format = "PNG"
            elif path_lower.endswith((".jpg", ".jpeg")):
                format = "JPEG"
            elif path_lower.endswith(".gif"):
                format = "GIF"
            elif path_lower.endswith(".bmp"):
                format = "BMP"
            elif path_lower.endswith(".tiff"):
                format = "TIFF"
            elif path_lower.endswith(".webp"):
                format = "WEBP"
            else:
                format = "PNG"  # Default fallback

        # Convert image if needed for format
        if format == "JPEG":
            # JPEG doesn't support transparency
            if image.mode in ["RGBA", "LA"]:
                # Create white background
                bg = Image.new("RGB", image.size, "white")
                bg.paste(image, mask=image.split()[-1])  # Use alpha channel as mask
                image = bg

        image.save(path_str, format=format, **kwargs)

    @classmethod
    def from_config(cls, config: Dict[str, Any]) -> "Clock":
        """Create a Clock instance from a configuration dictionary.

        Args:
            config: Configuration dictionary with 'width', 'height', and 'elements'.

        Returns:
            Configured Clock instance.

        Raises:
            ValueError: If configuration is invalid.
            KeyError: If required keys are missing.
        """
        # Validate required keys
        if "width" not in config:
            raise KeyError("Configuration must include 'width'")
        if "height" not in config:
            raise KeyError("Configuration must include 'height'")
        if "elements" not in config:
            raise KeyError("Configuration must include 'elements'")

        # Validate types
        width = config["width"]
        height = config["height"]
        elements_config = config["elements"]

        if not isinstance(width, int) or width <= 0:
            raise ValueError("Width must be a positive integer")
        if not isinstance(height, int) or height <= 0:
            raise ValueError("Height must be a positive integer")
        if not isinstance(elements_config, list):
            raise ValueError("Elements must be a list")

        # Create clock instance with optional antialiasing settings
        background_color = config.get("background_color", "white")
        antialias = config.get("antialias", True)
        scale_factor = config.get("scale_factor", 2)
        clock = cls(width, height, background_color, antialias, scale_factor)

        # Create and add elements
        for element_config in elements_config:
            element = _create_element_from_config(element_config)
            clock.add_element(element)

        return clock


def _create_element_from_config(config: Dict[str, Any]) -> Element:
    """Create an element instance from configuration.

    Args:
        config: Element configuration dictionary.

    Returns:
        Configured element instance.

    Raises:
        ValueError: If configuration is invalid.
        KeyError: If required keys are missing.
    """
    if "type" not in config:
        raise KeyError("Element configuration must include 'type'")

    element_type = config["type"]
    properties = config.get("properties", {})

    # Import element classes dynamically to avoid circular imports
    if element_type == "Face":
        from dial.elements.face import Face

        return Face(**properties)
    elif element_type == "Ticks":
        from dial.elements.ticks import Ticks

        return Ticks(**properties)
    elif element_type == "Numerals":
        from dial.elements.numerals import Numerals

        return Numerals(**properties)
    elif element_type == "Hands":
        from dial.elements.hands import Hands

        return Hands(**properties)
    elif element_type == "Overlay":
        from dial.elements.overlay import Overlay

        return Overlay(**properties)
    else:
        raise ValueError(f"Unknown element type: {element_type}")
