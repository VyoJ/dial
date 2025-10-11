"""Utility functions for geometric calculations and color handling."""

import math
import platform
from pathlib import Path
from typing import Any, Dict, List, Tuple, Union

import numpy as np
from PIL import Image, ImageColor, ImageFont

# Color type aliases
ColorType = Union[str, Tuple[int, int, int], Tuple[int, int, int, int]]
GradientType = Dict[str, Any]


def point_on_circle(
    center: Tuple[float, float], radius: float, angle_degrees: float
) -> Tuple[float, float]:
    """Calculate a point on a circle at a given angle.

    Args:
        center: The (x, y) center of the circle.
        radius: The radius of the circle.
        angle_degrees: The angle in degrees (0 = top, clockwise).

    Returns:
        The (x, y) coordinates of the point.
    """
    # Convert to radians and adjust for clock orientation (0 = top)
    angle_rad = math.radians(angle_degrees - 90)
    x = center[0] + radius * math.cos(angle_rad)
    y = center[1] + radius * math.sin(angle_rad)
    return (x, y)


def rotate_point(
    point: Tuple[float, float], center: Tuple[float, float], angle_degrees: float
) -> Tuple[float, float]:
    """Rotate a point around a center by the given angle.

    Args:
        point: The (x, y) point to rotate.
        center: The (x, y) center of rotation.
        angle_degrees: The rotation angle in degrees (clockwise).

    Returns:
        The rotated (x, y) coordinates.
    """
    angle_rad = math.radians(angle_degrees)
    cos_a = math.cos(angle_rad)
    sin_a = math.sin(angle_rad)

    # Translate to origin
    dx = point[0] - center[0]
    dy = point[1] - center[1]

    # Rotate
    new_x = dx * cos_a - dy * sin_a
    new_y = dx * sin_a + dy * cos_a

    # Translate back
    return (new_x + center[0], new_y + center[1])


def parse_color(
    color: Union[ColorType, GradientType],
) -> Union[str, Tuple[int, int, int], GradientType]:
    """Parse and validate a color specification.

    Args:
        color: Color as string, tuple, or gradient dictionary.

    Returns:
        Normalized color specification.

    Raises:
        ValueError: If color specification is invalid.
    """
    if isinstance(color, dict):
        # Gradient specification
        if "type" not in color:
            raise ValueError("Gradient specification must include 'type' field")
        if "colors" not in color:
            raise ValueError("Gradient specification must include 'colors' field")

        gradient_type = color["type"]
        if gradient_type not in [
            "linear",
            "linear_gradient",
            "radial",
            "radial_gradient",
        ]:
            raise ValueError(f"Unsupported gradient type: {gradient_type}")

        # Validate colors in gradient
        colors = color["colors"]
        if not isinstance(colors, list) or len(colors) < 2:
            raise ValueError("Gradient must have at least 2 colors")

        for c in colors:
            try:
                ImageColor.getrgb(c)
            except ValueError as e:
                raise ValueError(f"Invalid color in gradient: {c}") from e

        return color

    elif isinstance(color, (str, tuple)):
        # Single color
        try:
            # Validate the color by trying to parse it
            ImageColor.getrgb(color)
            return color
        except ValueError as e:
            raise ValueError(f"Invalid color specification: {color}") from e

    else:
        raise ValueError(
            f"Color must be string, tuple, or gradient dict, got {type(color)}"
        )


def create_gradient_image(size: Tuple[int, int], gradient: GradientType) -> Image.Image:
    """Create an image with a gradient fill.

    Args:
        size: The (width, height) of the image.
        gradient: Gradient specification dictionary.

    Returns:
        PIL Image with gradient.
    """
    width, height = size
    gradient_type = gradient["type"]
    colors = gradient["colors"]

    if gradient_type in ["linear", "linear_gradient"]:
        angle = gradient.get("angle", 0)
        return _create_linear_gradient(width, height, colors, angle)
    elif gradient_type in ["radial", "radial_gradient"]:
        return _create_radial_gradient(width, height, colors)
    else:
        raise ValueError(f"Unsupported gradient type: {gradient_type}")


def _create_linear_gradient(
    width: int, height: int, colors: List[str], angle: float
) -> Image.Image:
    """Create a linear gradient image."""
    # Convert angle to radians
    angle_rad = math.radians(angle)

    # Calculate gradient direction
    cos_a = math.cos(angle_rad)
    sin_a = math.sin(angle_rad)

    # Create gradient using numpy for efficiency
    x = np.linspace(0, width - 1, width)
    y = np.linspace(0, height - 1, height)
    X, Y = np.meshgrid(x, y)

    # Project coordinates onto gradient direction
    # Normalize to 0-1 range
    projected = X * cos_a + Y * sin_a
    projected = (projected - projected.min()) / (projected.max() - projected.min())

    # Interpolate colors
    r_values = np.zeros_like(projected)
    g_values = np.zeros_like(projected)
    b_values = np.zeros_like(projected)

    for i in range(len(colors) - 1):
        start_color = ImageColor.getrgb(colors[i])
        end_color = ImageColor.getrgb(colors[i + 1])

        start_pos = i / (len(colors) - 1)
        end_pos = (i + 1) / (len(colors) - 1)

        mask = (projected >= start_pos) & (projected <= end_pos)
        local_t = (projected - start_pos) / (end_pos - start_pos)

        r_values[mask] = (
            start_color[0] + (end_color[0] - start_color[0]) * local_t[mask]
        )
        g_values[mask] = (
            start_color[1] + (end_color[1] - start_color[1]) * local_t[mask]
        )
        b_values[mask] = (
            start_color[2] + (end_color[2] - start_color[2]) * local_t[mask]
        )

    # Convert to image
    rgb_array = np.stack([r_values, g_values, b_values], axis=-1).astype(np.uint8)
    return Image.fromarray(rgb_array).convert("RGBA")


def _create_radial_gradient(width: int, height: int, colors: List[str]) -> Image.Image:
    """Create a radial gradient image."""
    center_x, center_y = width // 2, height // 2
    max_radius = max(width, height) // 2

    # Create gradient using numpy
    x = np.linspace(0, width - 1, width)
    y = np.linspace(0, height - 1, height)
    X, Y = np.meshgrid(x, y)

    # Calculate distance from center, normalized
    distances = np.sqrt((X - center_x) ** 2 + (Y - center_y) ** 2)
    distances = np.clip(distances / max_radius, 0, 1)

    # Interpolate colors
    r_values = np.zeros_like(distances)
    g_values = np.zeros_like(distances)
    b_values = np.zeros_like(distances)

    for i in range(len(colors) - 1):
        start_color = ImageColor.getrgb(colors[i])
        end_color = ImageColor.getrgb(colors[i + 1])

        start_pos = i / (len(colors) - 1)
        end_pos = (i + 1) / (len(colors) - 1)

        mask = (distances >= start_pos) & (distances <= end_pos)
        local_t = (distances - start_pos) / (end_pos - start_pos)

        r_values[mask] = (
            start_color[0] + (end_color[0] - start_color[0]) * local_t[mask]
        )
        g_values[mask] = (
            start_color[1] + (end_color[1] - start_color[1]) * local_t[mask]
        )
        b_values[mask] = (
            start_color[2] + (end_color[2] - start_color[2]) * local_t[mask]
        )

    # Convert to image
    rgb_array = np.stack([r_values, g_values, b_values], axis=-1).astype(np.uint8)
    return Image.fromarray(rgb_array).convert("RGBA")


def get_default_font_path() -> str:
    """Get a default system font path.

    Returns:
        Path to a default font file.

    Raises:
        FileNotFoundError: If no suitable font is found.
    """
    system = platform.system()

    if system == "Windows":
        # Try common Windows fonts
        candidates = [
            "C:/Windows/Fonts/arial.ttf",
            "C:/Windows/Fonts/calibri.ttf",
            "C:/Windows/Fonts/segoeui.ttf",
        ]
    elif system == "Darwin":  # macOS
        candidates = [
            "/System/Library/Fonts/Helvetica.ttc",
            "/System/Library/Fonts/Arial.ttf",
            "/Library/Fonts/Arial.ttf",
        ]
    else:  # Linux and others
        candidates = [
            "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
            "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf",
            "/usr/share/fonts/TTF/DejaVuSans.ttf",
        ]

    for font_path in candidates:
        if Path(font_path).exists():
            return font_path

    raise FileNotFoundError("No suitable default font found on system")


def load_font(font_path: str = None, font_size: int = 12) -> ImageFont.FreeTypeFont:
    """Load a font with the given size.

    Args:
        font_path: Path to font file. If None, uses system default.
        font_size: Font size in points.

    Returns:
        PIL ImageFont object.

    Raises:
        FileNotFoundError: If font file is not found.
    """
    if font_path is None:
        font_path = get_default_font_path()

    if not Path(font_path).exists():
        raise FileNotFoundError(f"Font file not found: {font_path}")

    try:
        return ImageFont.truetype(font_path, font_size)
    except OSError as e:
        raise ValueError(f"Failed to load font {font_path}: {e}") from e


def validate_time_format(time_str: str) -> Tuple[int, int, int]:
    """Validate and parse time string.

    Args:
        time_str: Time in "HH:MM:SS" format.

    Returns:
        Tuple of (hours, minutes, seconds).

    Raises:
        ValueError: If time format is invalid.
    """
    try:
        parts = time_str.split(":")
        if len(parts) != 3:
            raise ValueError("Time must be in HH:MM:SS format")

        hours = int(parts[0])
        minutes = int(parts[1])
        seconds = int(parts[2])

        if not (0 <= hours <= 23):
            raise ValueError("Hours must be 0-23")
        if not (0 <= minutes <= 59):
            raise ValueError("Minutes must be 0-59")
        if not (0 <= seconds <= 59):
            raise ValueError("Seconds must be 0-59")

        return (hours, minutes, seconds)

    except (ValueError, IndexError) as e:
        raise ValueError(f"Invalid time format '{time_str}': {e}") from e


def time_to_angles(
    hours: int, minutes: int, seconds: int
) -> Tuple[float, float, float]:
    """Convert time to clock hand angles.

    Args:
        hours: Hours (0-23).
        minutes: Minutes (0-59).
        seconds: Seconds (0-59).

    Returns:
        Tuple of (hour_angle, minute_angle, second_angle) in degrees.
    """
    # Convert 24-hour to 12-hour
    hours = hours % 12

    # Calculate angles (0 degrees = 12 o'clock, clockwise)
    second_angle = seconds * 6  # 360 / 60
    minute_angle = minutes * 6 + seconds * 0.1  # Include seconds for smooth movement
    hour_angle = hours * 30 + minutes * 0.5  # 360 / 12, include minutes

    return (hour_angle, minute_angle, second_angle)
