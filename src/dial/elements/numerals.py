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
        if system not in ["arabic", "roman", "custom", "none"]:
            raise ValueError("system must be 'arabic', 'roman', 'custom', or 'none'")

        # Validate custom_list if system is custom
        if system == "custom":
            custom_list = self.get_property("custom_list")
            if custom_list is None:
                raise ValueError("custom_list is required when system is 'custom'")
            if not isinstance(custom_list, list):
                raise ValueError("custom_list must be a list")

        # Validate values (for custom hour positions)
        values = self.get_property("values")
        if values is not None:
            if not isinstance(values, list):
                raise ValueError("values must be a list")
            for val in values:
                if not isinstance(val, int):
                    raise ValueError("values must contain integers")

        # Validate visible - now accepts any integers
        visible = self.get_property("visible")
        if visible is not None:
            if not isinstance(visible, list):
                raise ValueError("visible must be a list")
            for num in visible:
                if not isinstance(num, int):
                    raise ValueError("visible must contain integers")

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
        if orientation not in ["upright", "radial", "tangent"]:
            raise ValueError("orientation must be 'upright', 'radial', or 'tangent'")

        # Validate flip
        flip = self.get_property("flip", "none")
        if flip not in ["none", "horizontal", "vertical", "both"]:
            raise ValueError("flip must be 'none', 'horizontal', 'vertical', or 'both'")

        # Validate rotation
        rotation = self.get_property("rotation", 0)
        if not isinstance(rotation, (int, float)):
            raise ValueError("rotation must be a number")

        # Validate radius_offset
        radius_offset = self.get_property("radius_offset", 0.0)
        if not isinstance(radius_offset, (int, float)):
            raise ValueError("radius_offset must be a number")

        # Validate font_path if provided
        font_path = self.get_property("font_path")
        if font_path is not None and not isinstance(font_path, str):
            raise ValueError("font_path must be a string")

        # Validate positions (custom angles)
        positions = self.get_property("positions")
        if positions is not None:
            if not isinstance(positions, list):
                raise ValueError("positions must be a list")
            for pos in positions:
                if not isinstance(pos, (int, float)):
                    raise ValueError(
                        "positions must contain numbers (angles in degrees)"
                    )

        # Validate custom_map
        custom_map = self.get_property("custom_map")
        if custom_map is not None:
            if not isinstance(custom_map, dict):
                raise ValueError("custom_map must be a dictionary")

    def draw(
        self,
        image: Image.Image,
        draw: ImageDraw.ImageDraw,
        center: Tuple[float, float],
        radius: float,
        scale_factor: float = 1.0,
    ) -> None:
        """Draw the numerals.

        Args:
            image: The PIL Image to draw on.
            draw: The PIL ImageDraw object for drawing operations.
            center: The (x, y) center point of the clock face (already scaled).
            radius: The radius of the clock face (already scaled).
            scale_factor: Scale factor for custom element positioning.
        """
        # Use element's own center and radius if specified
        element_center = self.get_center(center, scale_factor)
        element_radius = self.get_radius(radius, scale_factor)

        system = self.get_property("system", "arabic")
        values = self.get_property("values")
        visible = self.get_property("visible")
        font_path = self.get_property("font_path")
        font_size = self.get_property("font_size", 12)
        color = parse_color(self.get_property("color", "black"))
        orientation = self.get_property("orientation", "upright")
        flip = self.get_property("flip", "none")
        rotation = self.get_property("rotation", 0)
        radius_offset = self.get_property("radius_offset", 0.0)
        positions = self.get_property("positions")
        custom_map = self.get_property("custom_map")

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

        # Determine what to draw
        if values:
            # Use custom values
            nums_to_draw = values
        elif visible:
            # Use visible list
            nums_to_draw = visible
        else:
            # Default to 1-12
            nums_to_draw = list(range(1, 13))

        # Get numeral strings
        numeral_strings = self._get_numeral_strings(system, len(nums_to_draw))

        # Draw each numeral
        for idx, num in enumerate(nums_to_draw):
            # Get text from custom_map, or use numeral_strings
            if custom_map and num in custom_map:
                text = custom_map[num]
            elif idx < len(numeral_strings):
                text = numeral_strings[idx]
            else:
                text = str(num)

            # Determine angle
            if positions and idx < len(positions):
                angle = positions[idx]
            else:
                # Default: evenly distribute around circle
                angle = (
                    (num % 12) * 30
                    if len(nums_to_draw) <= 12
                    else (360 / len(nums_to_draw)) * idx
                )

            self._draw_numeral(
                draw,
                element_center,
                element_radius,
                angle,
                text,
                font,
                color,
                orientation,
                flip,
                rotation,
                radius_offset,
                image,
            )

    def _get_numeral_strings(self, system: str, count: int = 12) -> List[str]:
        """Get the list of numeral strings for the given system.

        Args:
            system: The numeral system to use.
            count: Number of numerals needed.

        Returns:
            List of numeral strings.
        """
        if system == "arabic":
            return [str(i) for i in range(1, count + 1)]
        elif system == "roman":
            # Roman numerals up to 24
            roman_map = {
                1: "I",
                2: "II",
                3: "III",
                4: "IV",
                5: "V",
                6: "VI",
                7: "VII",
                8: "VIII",
                9: "IX",
                10: "X",
                11: "XI",
                12: "XII",
                13: "XIII",
                14: "XIV",
                15: "XV",
                16: "XVI",
                17: "XVII",
                18: "XVIII",
                19: "XIX",
                20: "XX",
                21: "XXI",
                22: "XXII",
                23: "XXIII",
                24: "XXIV",
            }
            return [roman_map.get(i, str(i)) for i in range(1, min(count + 1, 25))]
        elif system == "custom":
            return self.get_property("custom_list", [])
        elif system == "none":
            return []
        else:
            raise ValueError(f"Unknown numeral system: {system}")

    def _draw_numeral(
        self,
        draw: ImageDraw.ImageDraw,
        center: Tuple[float, float],
        radius: float,
        angle: float,
        text: str,
        font: Any,
        color: Any,
        orientation: str,
        flip: str,
        rotation: float,
        radius_offset: float,
        image: Image.Image = None,
    ) -> None:
        """Draw a single numeral.

        Args:
            angle: The angle in degrees (0 = top, clockwise).
        """
        # Apply rotation
        final_angle = angle + rotation

        # Position at adjustable radius from center (default 80%)
        text_radius = radius * (0.8 + radius_offset)
        text_center = point_on_circle(center, text_radius, final_angle)

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

        elif orientation in ["radial", "tangent"]:
            # Draw text rotated to match radial position
            # Create a temporary image for the rotated text
            temp_size = max(text_width, text_height) * 3
            temp_image = Image.new(
                "RGBA", (int(temp_size), int(temp_size)), (0, 0, 0, 0)
            )
            temp_draw = ImageDraw.Draw(temp_image)

            # Draw text in center of temp image
            temp_x = temp_size / 2 - text_width / 2
            temp_y = temp_size / 2 - text_height / 2
            temp_draw.text((temp_x, temp_y), display_text, fill=color, font=font)

            # Rotate the temp image
            # For tangent, add 90 degrees
            rotation_angle = (
                final_angle if orientation == "radial" else final_angle + 90
            )
            rotated = temp_image.rotate(-rotation_angle, expand=True)

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
                "3": "Ɛ",
                "4": "4",
                "5": "S",
                "6": "9",
                "7": "L",
                "8": "8",
                "9": "6",
                "I": "I",
                "V": "Ʌ",
                "X": "X",
            }
            return "".join(flip_map.get(c, c) for c in text[::-1])
        elif flip == "both":
            # Apply both horizontal and vertical
            text = self._apply_flip(text, "horizontal")
            text = self._apply_flip(text, "vertical")
            return text
        else:
            return text
