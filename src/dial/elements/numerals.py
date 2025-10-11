"""Numerals element for hour numbers and symbols."""

from typing import Any, List, Tuple

from PIL import Image, ImageDraw

from dial.element import Element
from dial.utils import load_font, parse_color, point_on_circle


class Numerals(Element):
    """Hour numerals around the clock face."""

    @property
    def z_order(self) -> int:
        """Numerals are drawn after ticks but before overlays."""
        return 2

    def _validate_properties(self) -> None:
        """Validate Numerals element properties."""
        # Validate system
        system = self.get_property("system", "arabic")
        if system not in ["arabic", "roman", "custom"]:
            raise ValueError("system must be 'arabic', 'roman', or 'custom'")

        # Validate custom_list if system is custom
        if system == "custom":
            custom_list = self.get_property("custom_list")
            if custom_list is None:
                raise ValueError("custom_list is required when system is 'custom'")
            if not isinstance(custom_list, list) or len(custom_list) != 12:
                raise ValueError("custom_list must be a list of 12 strings")

        # Validate visible
        visible = self.get_property("visible")
        if visible is not None:
            if not isinstance(visible, list):
                raise ValueError("visible must be a list")
            for num in visible:
                if not isinstance(num, int) or num < 1 or num > 12:
                    raise ValueError("visible must contain integers from 1 to 12")

        # Validate font_size
        font_size = self.get_property("font_size", 12)
        if not isinstance(font_size, (int, float)) or font_size <= 0:
            raise ValueError("font_size must be a positive number")

        # Validate color
        color = self.get_property("color")
        if color is not None:
            parse_color(color)

        # Validate orientation
        orientation = self.get_property("orientation", "upright")
        if orientation not in ["upright", "radial"]:
            raise ValueError("orientation must be 'upright' or 'radial'")

        # Validate flip
        flip = self.get_property("flip", "none")
        if flip not in ["none", "horizontal", "vertical"]:
            raise ValueError("flip must be 'none', 'horizontal', or 'vertical'")

        # Validate rotation
        rotation = self.get_property("rotation", 0)
        if not isinstance(rotation, (int, float)):
            raise ValueError("rotation must be a number")

        # Validate font_path if provided
        font_path = self.get_property("font_path")
        if font_path is not None and not isinstance(font_path, str):
            raise ValueError("font_path must be a string")

    def draw(
        self,
        image: Image.Image,
        draw: ImageDraw.ImageDraw,
        center: Tuple[float, float],
        radius: float,
    ) -> None:
        """Draw the numerals.

        Args:
            image: The PIL Image to draw on.
            draw: The PIL ImageDraw object for drawing operations.
            center: The (x, y) center point of the clock face.
            radius: The radius of the clock face.
        """
        system = self.get_property("system", "arabic")
        visible = self.get_property("visible", list(range(1, 13)))
        font_path = self.get_property("font_path")
        font_size = self.get_property("font_size", 12)
        color = parse_color(self.get_property("color", "black"))
        orientation = self.get_property("orientation", "upright")
        flip = self.get_property("flip", "none")
        rotation = self.get_property("rotation", 0)

        # Load font
        try:
            font = load_font(font_path, int(font_size))
        except Exception as e:
            print(f"Warning: Failed to load font, using default: {e}")
            try:
                font = load_font(None, int(font_size))
            except Exception:
                # Final fallback - use PIL default font
                from PIL import ImageFont

                font = ImageFont.load_default()

        # Get numeral strings
        numeral_strings = self._get_numeral_strings(system)

        # Draw each visible numeral
        for hour in visible:
            if 1 <= hour <= 12:
                text = numeral_strings[hour - 1]  # Convert to 0-based index
                self._draw_numeral(
                    draw,
                    center,
                    radius,
                    hour,
                    text,
                    font,
                    color,
                    orientation,
                    flip,
                    rotation,
                    image,
                )

    def _get_numeral_strings(self, system: str) -> List[str]:
        """Get the list of numeral strings for the given system."""
        if system == "arabic":
            return ["1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11", "12"]
        elif system == "roman":
            return [
                "I",
                "II",
                "III",
                "IV",
                "V",
                "VI",
                "VII",
                "VIII",
                "IX",
                "X",
                "XI",
                "XII",
            ]
        elif system == "custom":
            return self.get_property("custom_list", [])
        else:
            raise ValueError(f"Unknown numeral system: {system}")

    def _draw_numeral(
        self,
        draw: ImageDraw.ImageDraw,
        center: Tuple[float, float],
        radius: float,
        hour: int,
        text: str,
        font: Any,
        color: Any,
        orientation: str,
        flip: str,
        rotation: float,
        image: Image.Image = None,
    ) -> None:
        """Draw a single numeral."""
        # Calculate position angle - 12 should be at top (0°)
        # Hour 12 -> 0°, Hour 1 -> 30°, Hour 2 -> 60°, etc.
        angle = ((hour % 12) * 30) + rotation

        # Position at about 80% of radius from center
        text_radius = radius * 0.8
        text_center = point_on_circle(center, text_radius, angle)

        # Apply text flipping
        display_text = self._apply_flip(text, flip)

        # Get text dimensions
        bbox = draw.textbbox((0, 0), display_text, font=font)
        text_width = bbox[2] - bbox[0]
        text_height = bbox[3] - bbox[1]

        # Calculate text position (centered on the calculated point)
        text_x = text_center[0] - text_width / 2
        text_y = text_center[1] - text_height / 2

        if orientation == "upright":
            # Draw text upright
            draw.text((text_x, text_y), display_text, fill=color, font=font)

        elif orientation == "radial":
            # Draw text rotated to match radial position
            # Create a temporary image for the rotated text
            temp_size = max(text_width, text_height) * 2
            temp_image = Image.new(
                "RGBA", (int(temp_size), int(temp_size)), (0, 0, 0, 0)
            )
            temp_draw = ImageDraw.Draw(temp_image)

            # Draw text in center of temp image
            temp_x = temp_size / 2 - text_width / 2
            temp_y = temp_size / 2 - text_height / 2
            temp_draw.text((temp_x, temp_y), display_text, fill=color, font=font)

            # Rotate the temp image
            rotated = temp_image.rotate(angle, expand=True)

            # Calculate position to paste rotated text
            paste_x = int(text_center[0] - rotated.width / 2)
            paste_y = int(text_center[1] - rotated.height / 2)

            # Paste onto main image using alpha compositing
            if rotated.mode == "RGBA":
                # Use alpha channel for transparency
                image.paste(rotated, (paste_x, paste_y), rotated)
            else:
                image.paste(rotated, (paste_x, paste_y))

    def _apply_flip(self, text: str, flip: str) -> str:
        """Apply text flipping transformation."""
        if flip == "none":
            return text
        elif flip == "horizontal":
            # Reverse the string for horizontal flip
            return text[::-1]
        elif flip == "vertical":
            # For vertical flip, we could use Unicode characters if available
            # This is a simple implementation - more sophisticated flipping
            # would require font manipulation or custom character mapping
            flip_map = {
                "0": "0",
                "1": "1",
                "2": "2",
                "3": "3",
                "4": "4",
                "5": "5",
                "6": "9",
                "7": "7",
                "8": "8",
                "9": "6",
                "I": "I",
                "V": "V",
                "X": "X",
            }
            return "".join(flip_map.get(c, c) for c in text[::-1])
        else:
            return text
