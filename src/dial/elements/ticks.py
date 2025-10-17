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
        # Validate divisions
        divisions = self.get_property("divisions", 12)
        if not isinstance(divisions, int) or divisions <= 0:
            raise ValueError("divisions must be a positive integer")

        # Validate hour_spec
        hour_spec = self.get_property("hour_spec", {})
        if hour_spec:
            self._validate_tick_spec(hour_spec, "hour_spec")

        # Validate minute_spec
        minute_spec = self.get_property("minute_spec", {})
        if minute_spec:
            self._validate_tick_spec(minute_spec, "minute_spec")

        # Validate tick_spec array (new flexible format)
        tick_spec = self.get_property("tick_spec")
        if tick_spec is not None:
            if not isinstance(tick_spec, list):
                raise ValueError("tick_spec must be a list")
            for spec in tick_spec:
                self._validate_tick_spec(spec, "tick_spec")

        # Validate visible hours - now accepts any integers
        visible_hours = self.get_property("visible_hours")
        if visible_hours is not None:
            if not isinstance(visible_hours, list):
                raise ValueError("visible_hours must be a list")
            for hour in visible_hours:
                if not isinstance(hour, int):
                    raise ValueError("visible_hours must contain integers")

        # Validate visible minutes
        visible_minutes = self.get_property("visible_minutes")
        if visible_minutes is not None:
            if not isinstance(visible_minutes, list):
                raise ValueError("visible_minutes must be a list")
            for minute in visible_minutes:
                if not isinstance(minute, int):
                    raise ValueError("visible_minutes must contain integers")

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
        scale_factor: float = 1.0,
    ) -> None:
        """Draw the tick marks.

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

        rotation = self.get_property("rotation", 0)
        divisions = self.get_property("divisions", 12)

        # Check for new flexible tick_spec format
        tick_spec = self.get_property("tick_spec")
        if tick_spec:
            self._draw_flexible_ticks(
                draw, element_center, element_radius, tick_spec, divisions, rotation
            )
        else:
            # Legacy format: hour_spec and minute_spec
            # Draw hour ticks
            hour_spec = self.get_property("hour_spec")
            if hour_spec:
                visible_hours = self.get_property(
                    "visible_hours", list(range(1, divisions + 1))
                )
                self._draw_hour_ticks(
                    draw,
                    element_center,
                    element_radius,
                    hour_spec,
                    visible_hours,
                    rotation,
                    divisions,
                )

            # Draw minute ticks
            minute_spec = self.get_property("minute_spec")
            if minute_spec:
                visible_minutes = self.get_property(
                    "visible_minutes", list(range(0, 60))
                )
                self._draw_minute_ticks(
                    draw,
                    element_center,
                    element_radius,
                    minute_spec,
                    visible_minutes,
                    rotation,
                )

    def _draw_flexible_ticks(
        self,
        draw: ImageDraw.ImageDraw,
        center: Tuple[float, float],
        radius: float,
        tick_specs: List[Dict[str, Any]],
        divisions: int,
        rotation: float,
    ) -> None:
        """Draw ticks using flexible tick_spec format."""
        for spec in tick_specs:
            indices = spec.get("indices", [])
            if indices == "all":
                indices = list(range(divisions))
            elif indices == "all_others":
                # Will be handled after other specs
                continue

            shape = spec.get("shape", "line")
            color = parse_color(spec.get("color", "black"))
            length = spec.get("length", 0.1) * radius
            width = spec.get("width", 2)

            for idx in indices:
                angle = (360 / divisions) * idx + rotation

                if shape == "line":
                    self._draw_line_tick(
                        draw, center, radius, angle, length, width, color
                    )
                elif shape == "circle":
                    self._draw_circle_tick(
                        draw, center, radius, angle, length, width, color
                    )

    def _draw_hour_ticks(
        self,
        draw: ImageDraw.ImageDraw,
        center: Tuple[float, float],
        radius: float,
        spec: Dict[str, Any],
        visible_hours: List[int],
        rotation: float,
        divisions: int = 12,
    ) -> None:
        """Draw hour tick marks."""
        shape = spec.get("shape", "line")
        color = parse_color(spec.get("color", "black"))
        length = spec.get("length", 0.1) * radius
        width = spec.get("width", 2)

        for hour in visible_hours:
            # Convert hour to angle based on divisions
            angle = ((hour % divisions) * (360 / divisions)) + rotation

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
