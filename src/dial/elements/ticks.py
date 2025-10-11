"""Ticks element for hour and minute markers."""

from typing import Any, Dict, List, Tuple

from PIL import Image, ImageDraw

from dial.element import Element
from dial.utils import parse_color, point_on_circle


class Ticks(Element):
    """Hour and minute tick marks around the clock face."""

    @property
    def z_order(self) -> int:
        """Ticks are drawn after the face but before numerals."""
        return 1

    def _validate_properties(self) -> None:
        """Validate Ticks element properties."""
        # Validate hour_spec
        hour_spec = self.get_property("hour_spec", {})
        if hour_spec:
            self._validate_tick_spec(hour_spec, "hour_spec")

        # Validate minute_spec
        minute_spec = self.get_property("minute_spec", {})
        if minute_spec:
            self._validate_tick_spec(minute_spec, "minute_spec")

        # Validate visible hours
        visible_hours = self.get_property("visible_hours")
        if visible_hours is not None:
            if not isinstance(visible_hours, list):
                raise ValueError("visible_hours must be a list")
            for hour in visible_hours:
                if not isinstance(hour, int) or hour < 1 or hour > 12:
                    raise ValueError("visible_hours must contain integers from 1 to 12")

        # Validate visible minutes
        visible_minutes = self.get_property("visible_minutes")
        if visible_minutes is not None:
            if not isinstance(visible_minutes, list):
                raise ValueError("visible_minutes must be a list")
            for minute in visible_minutes:
                if not isinstance(minute, int) or minute < 0 or minute > 59:
                    raise ValueError(
                        "visible_minutes must contain integers from 0 to 59"
                    )

        # Validate rotation
        rotation = self.get_property("rotation", 0)
        if not isinstance(rotation, (int, float)):
            raise ValueError("rotation must be a number")

    def _validate_tick_spec(self, spec: Dict[str, Any], spec_name: str) -> None:
        """Validate a tick specification dictionary."""
        # Validate shape
        shape = spec.get("shape", "line")
        if shape not in ["line", "circle"]:
            raise ValueError(f"{spec_name} shape must be 'line' or 'circle'")

        # Validate color
        color = spec.get("color")
        if color is not None:
            parse_color(color)

        # Validate length
        length = spec.get("length")
        if length is not None:
            if not isinstance(length, (int, float)) or length <= 0:
                raise ValueError(f"{spec_name} length must be a positive number")

        # Validate width
        width = spec.get("width")
        if width is not None:
            if not isinstance(width, (int, float)) or width <= 0:
                raise ValueError(f"{spec_name} width must be a positive number")

    def draw(
        self,
        image: Image.Image,
        draw: ImageDraw.ImageDraw,
        center: Tuple[float, float],
        radius: float,
    ) -> None:
        """Draw the tick marks.

        Args:
            image: The PIL Image to draw on.
            draw: The PIL ImageDraw object for drawing operations.
            center: The (x, y) center point of the clock face.
            radius: The radius of the clock face.
        """
        rotation = self.get_property("rotation", 0)

        # Draw hour ticks
        hour_spec = self.get_property("hour_spec")
        if hour_spec:
            visible_hours = self.get_property("visible_hours", list(range(1, 13)))
            self._draw_hour_ticks(
                draw, center, radius, hour_spec, visible_hours, rotation
            )

        # Draw minute ticks
        minute_spec = self.get_property("minute_spec")
        if minute_spec:
            visible_minutes = self.get_property("visible_minutes", list(range(0, 60)))
            self._draw_minute_ticks(
                draw, center, radius, minute_spec, visible_minutes, rotation
            )

    def _draw_hour_ticks(
        self,
        draw: ImageDraw.ImageDraw,
        center: Tuple[float, float],
        radius: float,
        spec: Dict[str, Any],
        visible_hours: List[int],
        rotation: float,
    ) -> None:
        """Draw hour tick marks."""
        shape = spec.get("shape", "line")
        color = parse_color(spec.get("color", "black"))
        length = spec.get("length", 0.1) * radius
        width = spec.get("width", 2)

        for hour in visible_hours:
            # Convert hour to angle (12 = 0°, 1 = 30°, 2 = 60°, etc.)
            angle = ((hour % 12) * 30) + rotation  # 360/12 = 30 degrees per hour

            if shape == "line":
                self._draw_line_tick(draw, center, radius, angle, length, width, color)
            elif shape == "circle":
                self._draw_circle_tick(
                    draw, center, radius, angle, length, width, color
                )

    def _draw_minute_ticks(
        self,
        draw: ImageDraw.ImageDraw,
        center: Tuple[float, float],
        radius: float,
        spec: Dict[str, Any],
        visible_minutes: List[int],
        rotation: float,
    ) -> None:
        """Draw minute tick marks."""
        shape = spec.get("shape", "line")
        color = parse_color(spec.get("color", "black"))
        length = spec.get("length", 0.05) * radius
        width = spec.get("width", 1)

        for minute in visible_minutes:
            # Convert minute to angle (0 = 0°, 15 = 90°, etc.)
            angle = minute * 6 + rotation  # 360/60 = 6 degrees per minute

            if shape == "line":
                self._draw_line_tick(draw, center, radius, angle, length, width, color)
            elif shape == "circle":
                self._draw_circle_tick(
                    draw, center, radius, angle, length, width, color
                )

    def _draw_line_tick(
        self,
        draw: ImageDraw.ImageDraw,
        center: Tuple[float, float],
        radius: float,
        angle: float,
        length: float,
        width: float,
        color: Any,
    ) -> None:
        """Draw a line tick mark."""
        # Calculate outer point (at the edge of clock face)
        outer_point = point_on_circle(center, radius * 0.95, angle)

        # Calculate inner point (shortened by tick length)
        inner_point = point_on_circle(center, radius * 0.95 - length, angle)

        # Draw line
        draw.line([inner_point, outer_point], fill=color, width=int(width))

    def _draw_circle_tick(
        self,
        draw: ImageDraw.ImageDraw,
        center: Tuple[float, float],
        radius: float,
        angle: float,
        size: float,
        width: float,
        color: Any,
    ) -> None:
        """Draw a circular tick mark."""
        # Calculate position for circle
        tick_center = point_on_circle(center, radius * 0.9, angle)

        # Calculate circle bounds
        half_size = size / 2
        bbox = [
            tick_center[0] - half_size,
            tick_center[1] - half_size,
            tick_center[0] + half_size,
            tick_center[1] + half_size,
        ]

        # Draw circle (filled if width >= size, outline otherwise)
        if width >= size:
            draw.ellipse(bbox, fill=color)
        else:
            draw.ellipse(bbox, outline=color, width=int(width))
