"""Overlay element for additional features like date windows."""

from datetime import datetime
from typing import Tuple

from PIL import Image, ImageDraw

from dial.element import Element
from dial.utils import load_font, parse_color


class Overlay(Element):
    """Overlay element for additional clock features like date windows."""

    @property
    def z_order(self) -> int:
        """Overlays are drawn after numerals but before hands."""
        return 3

    def _validate_properties(self) -> None:
        """Validate Overlay element properties."""
        # Validate type
        overlay_type = self.get_property("type")
        if overlay_type is None:
            raise ValueError("Overlay element requires 'type' property")

        if overlay_type not in ["date_window"]:
            raise ValueError(f"Unsupported overlay type: {overlay_type}")

        # Validate position
        position = self.get_property("position")
        if position is not None:
            if not isinstance(position, (list, tuple)) or len(position) != 2:
                raise ValueError("position must be a (x, y) tuple or list")
            if not all(isinstance(coord, (int, float)) for coord in position):
                raise ValueError("position coordinates must be numbers")

        # Validate date format if provided
        if overlay_type == "date_window":
            date = self.get_property("date")
            if date is not None:
                try:
                    datetime.strptime(date, "%Y-%m-%d")
                except ValueError:
                    raise ValueError("date must be in YYYY-MM-DD format")

        # Validate font properties
        font_size = self.get_property("font_size")
        if font_size is not None:
            if not isinstance(font_size, (int, float)) or font_size <= 0:
                raise ValueError("font_size must be a positive number")

        font_path = self.get_property("font_path")
        if font_path is not None and not isinstance(font_path, str):
            raise ValueError("font_path must be a string")

        # Validate colors
        text_color = self.get_property("text_color")
        if text_color is not None:
            parse_color(text_color)

        background_color = self.get_property("background_color")
        if background_color is not None:
            parse_color(background_color)

        border_color = self.get_property("border_color")
        if border_color is not None:
            parse_color(border_color)

        # Validate padding
        padding = self.get_property("padding")
        if padding is not None:
            if not isinstance(padding, (int, float)) or padding < 0:
                raise ValueError("padding must be a non-negative number")

    def draw(
        self,
        image: Image.Image,
        draw: ImageDraw.ImageDraw,
        center: Tuple[float, float],
        radius: float,
    ) -> None:
        """Draw the overlay element.

        Args:
            image: The PIL Image to draw on.
            draw: The PIL ImageDraw object for drawing operations.
            center: The (x, y) center point of the clock face.
            radius: The radius of the clock face.
        """
        overlay_type = self.get_property("type")

        if overlay_type == "date_window":
            self._draw_date_window(draw, center, radius)
        else:
            print(f"Warning: Unknown overlay type: {overlay_type}")

    def _draw_date_window(
        self, draw: ImageDraw.ImageDraw, center: Tuple[float, float], radius: float
    ) -> None:
        """Draw a date window overlay."""
        # Get properties with defaults
        date_str = self.get_property("date")
        position = self.get_property("position", (center[0], center[1] + radius * 0.3))
        font_path = self.get_property("font_path")
        font_size = self.get_property("font_size", 14)
        text_color = parse_color(self.get_property("text_color", "black"))
        background_color = self.get_property("background_color")
        border_color = self.get_property("border_color")
        padding = self.get_property("padding", 4)

        # Determine date text
        if date_str:
            try:
                date_obj = datetime.strptime(date_str, "%Y-%m-%d")
                date_text = str(date_obj.day)  # Just the day number
            except ValueError:
                date_text = date_str  # Use as-is if parsing fails
        else:
            # Use current date
            date_text = str(datetime.now().day)

        # Load font
        try:
            font = load_font(font_path, int(font_size))
        except Exception as e:
            print(f"Warning: Failed to load font for overlay, using default: {e}")
            try:
                font = load_font(None, int(font_size))
            except Exception:
                from PIL import ImageFont

                font = ImageFont.load_default()

        # Get text dimensions
        bbox = draw.textbbox((0, 0), date_text, font=font)
        text_width = bbox[2] - bbox[0]
        text_height = bbox[3] - bbox[1]

        # Calculate window size with padding
        window_width = text_width + 2 * padding
        window_height = text_height + 2 * padding

        # Calculate window position (centered on given position)
        window_x = position[0] - window_width / 2
        window_y = position[1] - window_height / 2

        # Window bounds
        window_bbox = [
            window_x,
            window_y,
            window_x + window_width,
            window_y + window_height,
        ]

        # Draw background if specified
        if background_color:
            bg_color = parse_color(background_color)
            draw.rectangle(window_bbox, fill=bg_color)

        # Draw border if specified
        if border_color:
            border_col = parse_color(border_color)
            draw.rectangle(window_bbox, outline=border_col, width=1)

        # Draw text
        text_x = window_x + padding
        text_y = window_y + padding
        draw.text((text_x, text_y), date_text, fill=text_color, font=font)
